from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import venv
from pathlib import Path

CLIENT_DIRS = {
    "codex": Path(".agents") / "skills",
    "claude": Path(".claude") / "skills",
    "opencode": Path(".config") / "opencode" / "skills",
}

RUNTIME_PATHS = (
    "SKILL.md",
    "requirements.txt",
    "scripts",
    "references",
    "agents",
    "examples",
)


def read_skill_name(root: Path) -> str:
    text = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r"^---\s*$.*?^name:\s*([A-Za-z0-9._-]+)\s*$", text, re.MULTILINE | re.DOTALL)
    if not match:
        raise RuntimeError("Could not read skill name from SKILL.md frontmatter.")
    return match.group(1)


def detect_client(home: Path) -> str:
    candidates: list[str] = []
    if shutil.which("codex") or (home / ".codex").exists() or (home / ".agents").exists():
        candidates.append("codex")
    if shutil.which("claude") or (home / ".claude").exists():
        candidates.append("claude")
    if shutil.which("opencode") or (home / ".config" / "opencode").exists():
        candidates.append("opencode")

    if not candidates:
        return "codex"
    if "codex" in candidates:
        return "codex"
    return candidates[0]


def venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def copy_runtime(root: Path, target: Path, force: bool) -> None:
    marker = target / ".skill-install.json"
    if target.exists() and not marker.exists() and any(target.iterdir()) and not force:
        raise RuntimeError(
            f"{target} already exists and was not created by this installer. "
            "Use --force only if you intend to replace it."
        )

    if force and target.exists() and not marker.exists():
        shutil.rmtree(target)

    target.mkdir(parents=True, exist_ok=True)

    for name in RUNTIME_PATHS:
        source = root / name
        destination = target / name
        if not source.exists():
            raise RuntimeError(f"Missing runtime path: {source}")
        if source.is_dir():
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)


def install_dependencies(target: Path) -> Path:
    env_dir = target / ".venv"
    python = venv_python(env_dir)
    if not python.exists():
        venv.EnvBuilder(with_pip=True, clear=False).create(env_dir)
    subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "-r",
            str(target / "requirements.txt"),
        ],
        check=True,
    )
    (target / ".skill-python").write_text(str(python.resolve()) + "\n", encoding="utf-8")
    return python


def validate_install(target: Path, python: Path) -> None:
    subprocess.run(
        [
            str(python),
            str(target / "scripts" / "validate_page_spec.py"),
            str(target / "examples" / "page-spec.example.json"),
            "--strict",
        ],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install this Agent Skill and its Python runtime."
    )
    parser.add_argument(
        "--client",
        choices=("auto", "codex", "claude", "opencode"),
        default="auto",
        help="Target agent client. Defaults to automatic detection.",
    )
    parser.add_argument(
        "--home",
        type=Path,
        default=Path.home(),
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--skip-deps",
        action="store_true",
        help="Register the skill without creating its isolated Python environment.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing unrecognized skill directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the selected client and target path without changing files.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    skill_name = read_skill_name(root)
    client = detect_client(args.home) if args.client == "auto" else args.client
    target = args.home / CLIENT_DIRS[client] / skill_name

    if args.dry_run:
        print(
            json.dumps(
                {
                    "ok": True,
                    "dry_run": True,
                    "client": client,
                    "skill": skill_name,
                    "target": str(target),
                },
                ensure_ascii=False,
            )
        )
        return

    try:
        copy_runtime(root, target, args.force)
        python = Path(sys.executable)
        if not args.skip_deps:
            python = install_dependencies(target)

        marker = {
            "installer": "image-ppt",
            "skill": skill_name,
            "client": client,
            "source": str(root),
        }
        (target / ".skill-install.json").write_text(
            json.dumps(marker, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        if not args.skip_deps:
            validate_install(target, python)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f"install: error: {exc}\n")

    print(
        json.dumps(
            {
                "ok": True,
                "client": client,
                "skill": skill_name,
                "target": str(target),
                "python": str(python),
                "verified": not args.skip_deps,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
