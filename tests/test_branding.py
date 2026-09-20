from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".py", ".json", ".svg"}


def test_no_legacy_repository_url_remains() -> None:
    legacy = "github.com/helloo1568/image-ppt"
    hits: list[str] = []

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        if legacy in text:
            hits.append(str(path.relative_to(ROOT)))

    assert not hits, f"Legacy repository URL remains in: {hits}"


def test_slidemuse_identity_is_consistent() -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "name: slidemuse" in skill
    assert "name: slidemuse" in manifest
    assert "display_name: SlideMuse" in manifest
    assert "github.com/helloo1568/slidemuse" in readme
    assert "$slidemuse" in readme
