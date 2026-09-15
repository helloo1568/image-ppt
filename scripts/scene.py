"""Load the portable scene contract and validate geometry and local assets."""

from __future__ import annotations

import json
import math
from pathlib import Path

from jsonschema import Draft202012Validator
from PIL import Image

SCHEMA = Path(__file__).resolve().parents[1] / "references" / "scene.schema.json"


def walk(elements):
    for element in elements:
        yield element
        if element["type"] == "group":
            yield from walk(element["children"])


def asset_path(base: Path, value: str) -> Path:
    """Scene assets are portable, relative, and confined to the scene directory."""
    path = Path(value)
    root = base.resolve()
    resolved = (root / path).resolve()
    if path.is_absolute() or not resolved.is_relative_to(root):
        raise ValueError(f"Asset must stay inside scene directory: {value}")
    if not resolved.is_file():
        raise ValueError(f"Missing asset: {value}")
    return resolved


def _finite(value):
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Scene numbers must be finite")
    if isinstance(value, dict):
        for item in value.values():
            _finite(item)
    if isinstance(value, list):
        for item in value:
            _finite(item)


def validate_scene(scene: dict, base: Path) -> list[str]:
    _finite(scene)
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema).iter_errors(scene))
    if errors:
        error = errors[0]
        location = "/".join(str(p) for p in error.absolute_path) or "root"
        raise ValueError(f"Scene schema at {location}: {error.message}")
    width, height = scene["canvas"]["width"], scene["canvas"]["height"]
    if not 1 <= scene["canvas"].get("width_inches", 13.333333) * height / width <= 56:
        raise ValueError("Calculated slide height must be between 1 and 56 inches")
    slide_ids, warnings = set(), []
    for slide in scene["slides"]:
        if slide["id"] in slide_ids:
            raise ValueError(f"Duplicate slide id: {slide['id']}")
        slide_ids.add(slide["id"])
        if slide.get("source_image"):
            asset_path(base, slide["source_image"])
        ids = set()
        for e in walk(slide["elements"]):
            label = f"{slide['id']}/{e['id']}"
            if e["id"] in ids:
                raise ValueError(f"Duplicate element id: {label}")
            ids.add(e["id"])
            kind = e["type"]
            if kind == "group":
                continue
            if kind == "line":
                if max(e["x1"], e["x2"]) > width or max(e["y1"], e["y2"]) > height:
                    raise ValueError(f"Line outside canvas: {label}")
                if (e["x1"], e["y1"]) == (e["x2"], e["y2"]):
                    raise ValueError(f"Zero-length line: {label}")
            elif e["x"] + e["w"] > width + 1e-6 or e["y"] + e["h"] > height + 1e-6:
                raise ValueError(f"Element outside canvas: {label}")
            if e.get("confidence", 1) < 0.85:
                warnings.append(
                    f"{label}: low-confidence reconstruction; verify source"
                )
            if e.get("rotation", 0):
                warnings.append(f"{label}: rotated extents require rendered review")
            if kind == "image":
                path = asset_path(base, e["path"])
                with Image.open(path) as im:
                    if im.format not in ("PNG", "JPEG"):
                        raise ValueError(f"Use PNG or JPEG assets: {label}")
                    im.verify()
                if (
                    e.get("role") in ("background", "reference")
                    or e["w"] * e["h"] > 0.8 * width * height
                ):
                    warnings.append(
                        f"{label}: large/background raster; check for baked-in elements"
                    )
            if kind == "table":
                cols = len(e["rows"][0])
                if any(len(row) != cols for row in e["rows"]):
                    raise ValueError(f"Ragged table: {label}")
                if "column_widths" in e and len(e["column_widths"]) != cols:
                    raise ValueError(f"Table column widths mismatch: {label}")
            if kind == "chart":
                if any(len(s["values"]) != len(e["categories"]) for s in e["series"]):
                    raise ValueError(f"Chart categories/values mismatch: {label}")
                if e["chart_type"] in ("pie", "doughnut") and (
                    len(e["series"]) != 1
                    or any(v < 0 for v in e["series"][0]["values"])
                    or sum(e["series"][0]["values"]) <= 0
                ):
                    raise ValueError(
                        f"Pie/doughnut requires one nonnegative, nonzero series: {label}"
                    )
    return warnings


def load_scene(path: Path):
    scene = json.loads(path.read_text(encoding="utf-8-sig"))
    warnings = validate_scene(scene, path.resolve().parent)
    return scene, warnings
