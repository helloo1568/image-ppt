# Changelog

本项目的所有显著变更都记录在此文件中。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本遵循语义化版本。

## [2.1.0] - 2026-09-16

### Changed

- 将 Step 1 拆为“内容大纲确认”和“风格方案确认”两个硬门禁；未确认内容时不得生成风格总览。
- 明确四套方案的确定性豁免：严格沿用指定参考、明确跳过预览或明确授权代选，Agent 不得自行推断。
- Step 3 改为 Page Spec 提供语义事实、页面图片提供视觉事实；已确认文字和数据不再通过 OCR 重新猜测。

### Added

- Page Spec v1、JSON Schema、示例和验证脚本，记录准确内容、来源、稳定元素 ID、原生/图片意图、位置提示与页面图片状态。
- Page Spec 的 Schema、唯一 ID、连续页码、画布边界、路径约束和交付图片测试。
- CI 增加 Page Spec 示例验证。

## [2.0.1] - 2026-09-16

### Changed

- 将入口规范为唯一三阶段流程：内容提炼与四套幻灯片浏览视图 → 图片版逐页生成 → 经明确授权后的可编辑 PPTX 还原。
- 恢复硬状态机与五项需求门禁；普通任务表达不再被解释为允许自主推断、代选或跳步。
- Scene v1、分层素材和原生对象编译固定为第三阶段能力，不再作为绕过图片版的“编辑优先”替代路线。
- 规范项目定位与平台说明：最佳推荐 Codex + GPT Image 2.5，其他 Agent 调用其自身生图/编辑能力；本地脚本不冒充图像后端。
- 同步更新制作规格、阶段提示词、中英文 README、技能元数据和模型使用说明。

### Compatibility

- 保留 2.0.0 的 Scene v1、原生编译、素材裁剪、审查脚本和文件格式，不影响已有 scene.json。
- 已有页面图片/扫描 PDF 的可编辑还原可按明确请求直接从第三阶段开始；已有可编辑 PPTX 的普通修改不进入本流程。

## [2.0.0] - 2026-09-15

### Changed

- 默认改为编辑优先：先规划原生信息，再生成独立视觉素材；图片版仍可单独使用。
- 移除普通请求强制确认四项需求及四轮风格门禁；用户要求风格选择时继续等待选型。
- 更新 GPT Image 2.5 Sunburst / Flare 指南，区分宿主工具与直接 API，不假定工具支持指定模型。
- 基于 PPT Master 等项目的公开方法补齐分层重建、背景清理、稳定坐标和逐元素验收规范。

### Added

- Scene v1 JSON Schema 与原生 PPTX 编译器，支持文字、形状、线/箭头、嵌套组合、独立图片、表格、五类图表及内嵌数据工作簿。
- 素材裁剪与可选遮罩工具，记录来源、实际 bbox、透明度与文件哈希。
- 可编辑性审查，检查原生对象、内容、数据、几何、层级、素材和原图残留。
- 三页可运行场景、PowerPoint 导出的示例与预览、重建与调研参考文档。
- 原生对象往返、编辑数据、错误场景、alpha、裁剪与兼容性测试；Windows/Linux CI。

### Compatibility

- 原有 build_image_ppt.py / overlay_text.py 命令和示例继续可用。
- 新脚本增加 jsonschema 依赖，要求 Python 3.10+。
- 本地脚本不自动识图、执行 OCR、调用生图 API 或推断隐藏信息；宿主 Agent 完成识别和生图。
- 复杂插画是独立可替换图片，不宣称所有像素或曲线均已原生化。

## [1.5.0] - 2026-09-05

### Fixed

- `build_image_ppt.py`：`--fit cover` 不再把图片以负坐标溢出画布，改为整页放置 + 居中裁剪。放映效果不变，但 PowerPoint 编辑视图里不再出现挂在画布外的图片。
- `build_image_ppt.py`：自动应用 EXIF 方向信息，带旋转元数据的照片不再出现宽高比计算错误。

### Added

- `build_image_ppt.py`：新增 `--max-width` 与 `--jpeg-quality`，嵌入前等比缩小 / 重编码 JPEG，大型图片版 PPT 的体积可降低一个数量级；透明图片会先合成到 `--background` 指定的背景色。
- 新增 `scripts/overlay_text.py`：按 JSON 规格将准确文字确定性叠加到背景图上（百分比坐标、自动换行、对齐、行距、加粗、纯色页），作为生图模型文字不可靠时的兜底，对应 SKILL.md Step 2 的混合制作方式。
- 新增 `tests/` pytest 测试套件（20 个用例）与 GitHub Actions CI（ruff lint + pytest，Python 3.10–3.13 矩阵）。
- 新增 `CHANGELOG.md`、`requirements-dev.txt` 与 `examples/overlay-spec.example.json`。

### Changed

- `build_image_ppt.py`：页面背景改用幻灯片背景填充替代整页矩形，减少编辑时可误选中的形状；图片形状以源文件名命名，便于在 PowerPoint 中识别与导航。
- 中文 README 效果展示补齐缺失图片并改用仓库内相对路径，不再依赖外部 CDN 热链。
- `manifest.yaml` 版本升至 1.5.0，文件清单与仓库实际内容同步。

## [1.4.0] 及更早

见提交历史。
