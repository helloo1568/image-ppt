# image-ppt 2.0

**AI-generated visuals with editable PowerPoint text, shapes, tables, charts, and separate image assets.**

[中文](README.md) · [Skill](SKILL.md) · [Changelog](CHANGELOG.md) · [Research](references/research.md)

An open-source skill for agent environments such as Codex. The host agent reads documents, interprets images and generates visual assets. Local Python scripts compile and inspect the result.

## What's new

- Editable-first authoring: plan native information layers before generating visual assets.
- Image reconstruction: preserve visible content and layout while separating semantic elements.
- A versioned JSON scene with stable IDs, geometry, stacking, groups and provenance.
- Native text, shapes, arrows, nested groups, tables and charts with embedded workbooks.
- Deterministic asset extraction from supplied bounding boxes and optional masks.
- An editability audit that checks exported objects against the scene.
- GPT Image 2.5 guidance for Flare exploration and Sunburst reference editing.
- Existing image-only export and raster text overlay commands remain available.

See the [official image guide](https://developers.openai.com/api/docs/guides/image-generation).
The host may not expose an image model selector. These recommendations are not a measured model benchmark.

## Editability contract

| Content | Export | Editing |
|---|---|---|
| Headings, body copy, labels | Native text boxes | Text, font, position, color |
| Geometry and diagrams | Native shapes, lines, groups | Geometry and style; ungroup to edit children |
| Tables | Native tables | Cells and formatting |
| Bar, column, line, pie, doughnut | Native charts with workbooks | Data and chart formatting |
| Photos and complex illustrations | Separate image objects | Move, crop, resize, replace |

Raster artwork does not become editable vector paths. Missing or occluded details cannot be recovered with guaranteed accuracy.
**The local scripts do not perform OCR, automatic segmentation or image understanding.** Those steps belong to the host agent and its available vision/image tools.

## Quick start

Python 3.10+:

```sh
git clone https://github.com/helloo1568/image-ppt.git
cd image-ppt
python -m pip install -r requirements.txt
python scripts/build_editable_ppt.py examples/editable-scene.example.json output/editable-demo.pptx
python scripts/audit_editability.py output/editable-demo.pptx --scene examples/editable-scene.example.json --output output/editability.json --strict
```

[Download editable demo](examples/editable-demo.pptx) · [Scene source](examples/editable-scene.example.json)

The three-slide demo tests compilation of an authored scene, not automatic reconstruction accuracy. All chart values are illustrative.

![Native data slide](examples/editable-preview-02.png)

Install the complete repository as image-ppt in your host's skill directory, or provide SKILL.md to an agent supporting this format.
Keep task materials and outputs in a separate working directory.

## Example requests

```text
Use $image-ppt to turn this report into a 10-slide editable deck.
Use native text, diagrams, tables, and charts with verifiable data.
Generate independent visual assets with GPT Image 2.5 where available.
Choose an appropriate style, validate a representative slide, then finish the deck.
```

```text
Use $image-ppt to reconstruct these slide images into editable PPTX.
Preserve wording, layout and page order. Separate every element I need to edit.
Remove duplicated content from the background and include the scene and assets.
```

## Workflows

- **Editable-first:** content → layout → separate visual assets → scene → native PPTX → review.
- **Image-first:** content → slide images → image-only PPTX.
- **Reconstruction:** normalized source pages → agent recognition → layer preparation → scene → native PPTX → comparison.

Read available material before asking unnecessary questions. Infer ordinary style/page-count preferences when reasonable.
If the user requests four design options, generate four comparable contact sheets and wait for selection.

## Commands and contract

- build_editable_ppt.py: validate a scene and compile native objects.
- audit_editability.py: inspect PPTX and optionally compare it with a scene; --strict fails on warnings.
- extract_assets.py: crop known regions, apply supplied masks, record coordinates and hashes.
- build_image_ppt.py: existing image-only assembler with natural sorting and fit controls.
- overlay_text.py: existing deterministic raster text overlay.

[Scene format](references/scene-format.md) · [Layer reconstruction](references/reconstruction.md) · [Models](references/models.md)

Scene coordinates are canvas pixels; fonts and strokes are points. Asset paths are relative to and confined to the scene directory.
Group children use full-slide coordinates. Array order determines stacking.
This version does not implement a generic SVG importer, merged table cells, automatic connector attachment, or inline rich text.

## Validation

```sh
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m pytest tests/ -q
```

CI covers Windows/Linux and Python 3.10/3.12/3.13.
Audit checks declared objects, not source-image completeness or visual similarity.
Render and inspect every slide before delivery. The checked-in previews were exported with PowerPoint; automated tests do not require it.

## Credits

Research includes [PPT Master by Hugo He](https://github.com/hugohe3/ppt-master),
[banana-slides](https://github.com/Anionex/banana-slides) and [PPTAgent](https://github.com/icip-cas/PPTAgent).
The scene compiler is independently implemented; their code and dependencies are not bundled.
See [research notes](references/research.md) for specific references and tradeoffs.

Early workflow inspiration: Xiaoheihe author 玩家22186848 and Bilibili creator 一往无前河井.
Historical visual samples remain under examples/ and do not demonstrate element-level reconstruction.

Local scripts perform no network requests and need no API key. Host AI services may receive supplied content.
Exclude private source documents and credentials from shared outputs.

[MIT](LICENSE) © 2026 风清云影（helloo1568）
