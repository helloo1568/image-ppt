import copy
import json
from pathlib import Path

import plan_deck_update
from PIL import Image


def make_spec(tmp_path):
    spec = json.loads((Path(__file__).resolve().parents[1] / "examples/page-spec.example.json").read_text(encoding="utf-8"))
    first = spec["slides"][0]
    first["image_status"] = "approved"
    second = copy.deepcopy(first)
    second.update(id="s02", page_number=2, image_file="slides/02.png", title="第二页")
    spec["slides"].append(second)
    for slide in spec["slides"]:
        image = tmp_path / slide["image_file"]
        image.parent.mkdir(exist_ok=True)
        Image.new("RGB", (160, 90), slide["title"] == "第二页" and "black" or "white").save(image)
    path = tmp_path / "page-spec.json"
    path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    return path, spec


def test_only_changed_slide_needs_regeneration(tmp_path):
    path, spec = make_spec(tmp_path)
    snapshot = plan_deck_update.snapshot(path)
    assert [item["action"] for item in plan_deck_update.plan(snapshot, spec, tmp_path)["slides"]] == ["reuse", "reuse"]
    spec["slides"][1]["elements"][0]["text"] = "新的准确标题"
    result = plan_deck_update.plan(snapshot, spec, tmp_path)
    assert [item["action"] for item in result["slides"]] == ["reuse", "regenerate"]
    assert result["slides"][1]["stale_approval"]


def test_style_change_invalidates_all_and_changed_image_needs_review(tmp_path):
    path, spec = make_spec(tmp_path)
    snapshot = plan_deck_update.snapshot(path)
    Image.new("RGB", (160, 90), "red").save(tmp_path / spec["slides"][0]["image_file"])
    result = plan_deck_update.plan(snapshot, spec, tmp_path)
    assert [item["action"] for item in result["slides"]] == ["review_existing", "reuse"]
    assert result["slides"][0]["stale_approval"]
    spec["style"]["visual_spec"] = "新配色"
    assert all(item["action"] == "regenerate" for item in plan_deck_update.plan(snapshot, spec, tmp_path)["slides"])


def test_fingerprint_does_not_mutate_spec(tmp_path):
    _, spec = make_spec(tmp_path)
    spec["slides"][0]["elements"][0]["prompt_record"] = "old prompt"
    before = copy.deepcopy(spec)
    plan_deck_update.slide_fingerprint(spec["slides"][0])
    assert spec == before


def test_reference_pixels_invalidate_style(tmp_path):
    path, spec = make_spec(tmp_path)
    reference = tmp_path / "styles/selected.png"
    reference.parent.mkdir()
    Image.new("RGB", (16, 9), "blue").save(reference)
    spec["style"]["tokens"]["reference_images"] = ["styles/selected.png"]
    path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    baseline = plan_deck_update.snapshot(path)
    Image.new("RGB", (16, 9), "green").save(reference)
    result = plan_deck_update.plan(baseline, spec, tmp_path)
    assert result["global_changes"] == ["style_or_canvas_changed"]
