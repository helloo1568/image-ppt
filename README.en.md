<div align="center">

<img src="docs/assets/hero.svg" alt="image-ppt: from source material to polished slides and editable PPTX" width="100%">

# image-ppt · AI Competition & Cinematic Presentations

**Give good ideas a beautiful presentation—and room to keep editing.**

Turn books, PDFs, papers, and reports into a visually consistent image deck.<br>
Create **competition presentations, cinematic slides, startup pitch decks, research talks, and thesis defenses**.<br>
Reconstruct slide images as native editable PowerPoint (PPTX) when needed.

[![CI](https://github.com/helloo1568/image-ppt/actions/workflows/ci.yml/badge.svg)](https://github.com/helloo1568/image-ppt/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-2.1.0-79e9d1?labelColor=14243c)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/Python-3.10%2B-82b5ff?labelColor=14243c)](requirements.txt)
[![License: MIT](https://img.shields.io/badge/License-MIT-f2c98a?labelColor=14243c)](LICENSE)

[简体中文](README.md) · **English**

[Showcase](#showcase) · [Why image-ppt](#features) · [Quick start](#quick-start) · [Guide](docs/guide.en.md) · [Contributing](CONTRIBUTING.md)

</div>

---

<a id="showcase"></a>

## See the results

One workflow, two visual directions. These are actual pages produced with this project's workflow. Click an image to view the original.

### Snowline Watch · Glacier blue & silver

An intelligent glacier inspection and ecological early-warning concept, with a consistent visual language across the story, scenarios, and technology comparison.

| 01 / Cover | 02 / Problem |
| :---: | :---: |
| [![Snowline Watch: glacier inspection cover](showcase/snowline-watch-01.png)](showcase/snowline-watch-01.png) | [![Snowline Watch: problem statement](showcase/snowline-watch-02.png)](showcase/snowline-watch-02.png) |
| **03 / Solution** | **04 / Technology** |
| [![Snowline Watch: solution](showcase/snowline-watch-03.png)](showcase/snowline-watch-03.png) | [![Snowline Watch: technology comparison](showcase/snowline-watch-04.png)](showcase/snowline-watch-04.png) |

### Glaze Reborn · Red & gold

A competition presentation that connects the problem, solution, and craft technology through a shared red-and-gold palette.

| 02 / Problem | 03 / Solution |
| :---: | :---: |
| [![Glaze Reborn: problem statement](showcase/red-gold-competition-02.png)](showcase/red-gold-competition-02.png) | [![Glaze Reborn: solution](showcase/red-gold-competition-03.png)](showcase/red-gold-competition-03.png) |

<details>
<summary>View more: Glaze Reborn · Process technology</summary>

[![Glaze Reborn: process technology](showcase/red-gold-competition-04.png)](showcase/red-gold-competition-04.png)

</details>

<sub>Images demonstrate visual output. Editability is assessed through the delivered PPTX objects and audit report. Business and technology figures in these examples are presentation content, not benchmarks for this skill.</sub>

<a id="features"></a>

## Why image-ppt

| | What you get |
| :--- | :--- |
| **🎨 Choose a direction first** | Approve the content outline, then compare **4 slide-sorter overviews** using the same content before full production. |
| **🧩 Designed to keep editing** | Optional reconstruction into native text, shapes, tables, and **5 chart types**. Photos and complex artwork become separate, replaceable images. |
| **📝 Preserve approved content** | **Page Spec** records exact text, numbers, sources, and stable element IDs. Reconstruction reuses known content instead of recognizing it again. |
| **🔁 Resume and revise** | `deck-spec.md` tracks production state; `scene.json` stores layout. Update affected elements and assets, then export again. |
| **🔍 Inspect the deliverable** | Audit objects, text, table and chart data, stacking, and full-page background remnants; follow with rendered visual review. |
| **🔓 Open and adaptable** | **MIT licensed**, with support for agents that provide the required capabilities. Local Python tools make no network requests and need no API key. |

> **How it runs:** image-ppt is an agent skill. The host reads materials, interprets images, and generates artwork; local scripts assemble, crop, compile, and audit. End-to-end production requires those host capabilities. See [runtime and model notes](references/models.md).

## What can you make?

| Use case or style | How image-ppt helps |
| :--- | :--- |
| **Competition PPT / competition presentations** | Connect the problem, solution, technical advantages, and applications in a consistent visual story. |
| **Innovation competitions / startup pitch decks** | Turn project proposals, research material, or business plans into slides tailored to the competition brief. |
| **Cinematic PPT / cinematic slides / poster-style presentations** | Explore cinematic lighting, scene composition, and poster-style covers through four visual directions. |
| **Academic presentations / thesis defense / research slides** | Extract questions, methods, results, and conclusions from papers and PDFs while preserving data and sources. |
| **Business presentations / project updates / book presentations** | Adapt long source materials to the audience, slide count, and speaking context. |
| **AI presentation generation / PDF to PPT / image to editable PPTX** | Generate an image deck from source material, or reconstruct existing slide images and scanned PDF pages as editable objects. |

Cinematic, technology, and red-and-gold styles are visual directions you can request. Results depend on source material, the host's image capabilities, and slide-by-slide review.

### Specific competition presentation scenarios

Use project proposals, research papers, survey reports, and the current competition brief as source material. The examples below suggest ways to organize a presentation; confirm the outline against the requirements of your track.

| Competition | Search terms | Presentation focus |
| :--- | :--- | :--- |
| [中国国际大学生创新大赛](https://hudong.moe.gov.cn/srcsite/A08/s5672/202607/t20260731_1445670.html) | **大学生创新大赛 PPT / 互联网+ PPT / innovation pitch deck** | Problem, innovation, validation, team, and development plan. |
| [“挑战杯”全国大学生课外学术科技作品竞赛](https://www.tiaozhanbei.net/focus) | **挑战杯 PPT / 大挑 PPT / Challenge Cup research presentation** | Research question, methods, novelty, results, and applications. |
| [“挑战杯”中国大学生创业计划竞赛](https://www.tiaozhanbei.net/focus) | **小挑 PPT / Challenge Cup business plan presentation** | Customer needs, product, market, business model, and execution. |
| [全国大学生电子商务“创新、创意及创业”挑战赛](https://www.3chuang.net/) | **三创赛 PPT / e-commerce competition presentation** | E-commerce context, ideas, operations, project results, and value. |
| [“正大杯”全国大学生市场调查与分析大赛](https://www.china-cssc.org/show-568-1912-1.html) | **正大杯 PPT / 市调大赛 PPT / market research presentation** | Research questions, survey design, data analysis, findings, and recommendations. |

Also useful for **大创 (undergraduate innovation and entrepreneurship training projects)**: proposal defenses, progress reports, and final presentations. These are project reporting scenarios, listed separately from competitions.

## Three stages, from source to delivery

| 01 · Content & style | 02 · Image deck | 03 · Editable reconstruction (optional) |
| :--- | :--- | :--- |
| Extract content and approve the outline | Save Page Spec and generate each slide | Reconstruct layers from the spec and images |
| Compare four overviews and choose a style | Review text and visuals; assemble the PPTX | Compile native objects, audit, and render |
| **Approved production plan** | **Slide images + image-only PPTX** | **Editable PPTX + Scene + assets** |

Content approval precedes style selection by default. Stage 3 requires an explicit editable-deck request. Existing slide images or scanned PDFs can enter reconstruction directly. Preview skips and delegated choices follow the [full workflow rules](docs/guide.en.md).

<a id="quick-start"></a>

## Quick start

### 1. Get the skill and dependencies

Requires **Python 3.10+** and an agent with skill-file support, document reading, image generation, and local file tools.

```sh
git clone https://github.com/helloo1568/image-ppt.git
cd image-ppt
python -m pip install -r requirements.txt
python scripts/validate_page_spec.py examples/page-spec.example.json --strict
```

### 2. Connect it to your agent

Install the **complete repository** in your host's skill directory, or ask an agent supporting this format to read [SKILL.md](SKILL.md) and use its repository resources. Keep source materials and deliverables in a separate working directory.

### 3. Attach your material and ask

```text
Use $image-ppt to turn the attached report into a 10-slide project pitch.
The audience is competition judges. I have no style reference.
Show the content outline for approval, then four slide-sorter overviews for selection.
After I choose a style, create the image deck, then reconstruct an editable PPTX.
Include page-spec.json, scene.json, assets, and the editability report.
```

<details>
<summary>More examples: image-only decks / existing slide reconstruction</summary>

**Image-only classroom presentation:**

```text
Use $image-ppt to make a 12-slide classroom presentation from the attached material.
The audience is my classmates. No style reference; deliver only an image deck.
Confirm the outline first, then show four slide-sorter options for me to choose from.
```

**Make existing slide images editable:**

```text
Use $image-ppt starting at Step 3 to reconstruct all attached slide images as editable PPTX.
Preserve wording, aspect ratio, layout, and page order. Separate text, charts, and subjects.
Keep complex artwork as independent images, remove background remnants,
and deliver the Scene, assets, and editability report.
```

</details>

## What can you edit?

| Slide content | Reconstructed object | Editable properties |
| :--- | :--- | :--- |
| Headings, body text, labels, page numbers | Native text boxes | Text, font, color, position |
| Geometry, arrows, flow nodes | Native shapes, lines, groups | Size and style; ungroup to edit children |
| Tables | Native tables | Cell content and formatting |
| Column, bar, line, pie, doughnut charts | Native charts + embedded workbooks | Data and chart styling |
| Photos, people, complex illustrations | Separate image objects | Position, size, crop, replacement |

Complex artwork remains raster within each image. Recognition, segmentation, and background repair depend on host tools; the local scripts include no automatic OCR or segmentation model. Structural audits do not replace visual review or guarantee recovery of occluded information. See [capabilities and validation](docs/guide.en.md).

## Documentation & community

| Your next step | Resource |
| :--- | :--- |
| Installation, workflow, commands, and validation | [Usage & technical guide](docs/guide.en.md) |
| Agent instructions | [SKILL.md](SKILL.md) |
| Content contracts and editable objects | [Page Spec](references/page-spec.md) · [Scene v1](references/scene-format.md) · [Reconstruction](references/reconstruction.md) |
| Versions and design references | [Changelog](CHANGELOG.md) · [Research](references/research.md) |
| Bug reports, suggestions, and code contributions | [Issues](https://github.com/helloo1568/image-ppt/issues) · [Contributing](CONTRIBUTING.md) |

### Credits & license

Thanks to [PPT Master by Hugo He](https://github.com/hugohe3/ppt-master), [banana-slides](https://github.com/Anionex/banana-slides), and [PPTAgent](https://github.com/icip-cas/PPTAgent) for methodological inspiration, and to Xiaoheihe author 玩家22186848 and Bilibili creator 一往无前河井 for their tutorials. The scene compiler is independently implemented; see [research notes](references/research.md) for attribution and tradeoffs.

Local scripts need no API key. Host image and vision services may receive supplied materials; their own pricing and privacy terms apply.

<div align="center">

**Start your next presentation with a good idea.**

If image-ppt helps you, give it a Star or share your work and improvements.

[MIT License](LICENSE) © 2026 风清云影（[helloo1568](https://github.com/helloo1568)）

</div>
