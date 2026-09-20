from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_skill_frontmatter_uses_slidemuse() -> None:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "name: slidemuse" in text


def test_installer_dry_run_targets_slidemuse(tmp_path: Path) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "install.py"),
            "--client",
            "codex",
            "--home",
            str(tmp_path),
            "--dry-run",
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    assert result["ok"] is True
    assert result["skill"] == "slidemuse"
    assert Path(result["target"]) == tmp_path / ".agents" / "skills" / "slidemuse"
