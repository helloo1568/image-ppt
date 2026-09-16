# Page Spec v1：图片生成与可编辑还原的中间契约

[机器 Schema](page-spec.schema.json) · [示例](../examples/page-spec.example.json)

`page-spec.json` 在内容大纲已确认、视觉方向已锁定后创建。它保存已经知道的准确内容和语义结构，避免 Step 3 从整页图片重新 OCR 或猜测图表数据。

它不是 PPTX 导出场景：位置只允许写 `bbox_hint`，不要求像 Scene 一样精确；最终坐标、原生样式与素材路径仍写入 `scene.json`。

## 生命周期

1. Step 1 内容确认后，把页序、标题、核心结论、准确文字/数据和来源写入 Page Spec。
2. 风格选定、锁定参考或明确跳过预览后，补齐 `style`，再运行验证器。
3. Step 2 每完成一页，记录最终 `image_file`、`image_status`、实际提示词和更新后的布局提示。
4. 交付图片版前使用 `--require-images` 再验证一次，确保所有页面图片存在且状态为 `approved`。
5. Step 3 以 Page Spec 为语义事实源、页面图片为视觉事实源。两者冲突时先记录并向用户确认，不得静默用 OCR 覆盖已确认内容。

直接还原现有页面时，将 `style.decision` 设为 `locked-reference`，`visual_spec` 写明保持原页，`authorization` 记录用户要求还原原图的指令；低置信度内容按元素标记为 `unresolved`。

## 关键字段

- `content_approved` 固定为 `true`，表示新材料任务的大纲已经确认，或直接还原任务已明确授权保留原页内容；`content_version` 与 `content_authorization` 记录对应版本和用户原话。它不代表每个模糊字符都已确认。
- `style.decision` 记录 `selected`、`locked-reference`、`skipped` 或 `delegated`，并保留相关授权原文。
- `slides[].elements` 使用稳定 ID。准确文字写 `text`，表格/图表原始值写 `data`，来源写 `source_ref`。
- `confirmation_status` 区分用户确认、来源可验证和未解决内容；直接还原中的低置信度文字必须标为 `unresolved` 并记录 `confidence`，不能伪装成已确认。
- `native_intent` 表示 Step 3 期望的输出：`native`、`raster` 或 `either`。
- `bbox_hint` 是 `[x, y, w, h]` 的整页画布坐标提示；它可以在图片页验收后更新，但不能冒充最终 Scene 坐标。
- `separate_asset: true` 表示该视觉对象在可编辑版中需要独立移动或替换。

## 验证

内容与风格锁定、尚未生成图片时：

```sh
python "<skill-dir>/scripts/validate_page_spec.py" "<work>/page-spec.json" --strict
```

图片版交付前：

```sh
python "<skill-dir>/scripts/validate_page_spec.py" "<work>/page-spec.json" --require-images --strict
```

验证器检查 Schema、有限数值、连续页码、唯一 ID、画布边界、相对图片路径，以及已批准图片是否存在并可作为 PNG/JPEG 读取。`--strict` 还会拒绝未解决元素；直接还原任务可先不加 `--strict` 以保留低置信度项，但交付前必须逐项说明。验证器不检查图片中的文字是否正确，也不替代逐页视觉验收。
