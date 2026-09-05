# Changelog

本项目的所有显著变更都记录在此文件中。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本遵循语义化版本。

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
