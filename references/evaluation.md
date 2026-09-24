# 交付评测：绑定实际产物的可复跑评分卡

在质量回归、版本发布或用户要求可审查的验收记录时使用。本流程评估**当前 PPTX 文件**，不是对提示词或模型能力打分。普通交付仍按 SKILL.md 逐页检查；不必为每个任务制作完整评分卡。

## 证据与门槛

| 维度 | 证据 | 通过条件 |
|---|---|---|
| 内容 | Page Spec、批准图片、逐页看图或 OCR 后人工校对的 `observations*.json` | 每页记录为 `complete`，已确认文字及 `required_visible_values` 均可见；图表/表格数据另行目视核对 |
| 视觉 | 实际 PPTX 渲染的逐页 PNG、`review.png`、`visual-review.json` | 每页人工检查布局、画幅、裁切、字体、数字、主视觉和来源图差异，记录 `pass` 或 `fail` |
| 可编辑性 | 当前 PPTX、`scene.json` | 可编辑版传 `--scene`，结构审查没有错误，仍须按技能流程抽查实际编辑行为 |

`pass` 表示上述**已提供**证据均通过；没有 Scene 的图片版可通过且报告显示 `editability.checked: false`。可编辑版只有传入 `--scene` 才能称可编辑性已纳入评分。`fail` 表示发现内容、视觉或结构错误；`incomplete` 表示缺少逐页内容观察或视觉复核。像素差异均值只帮助定位变化，不设自动通过阈值。若 PowerPoint 与 LibreOffice 渲染结果不同，记录所用后端并目视复查；不能混用不同后端的旧复核记录。

## 操作

先按 [Page Spec 内容核对](page-spec.md)为**每页**建立观察记录。`--init` 只生成模板，必须看图后填写 `observed_text` 并将 `status` 设为 `complete`。图表数据、单位和小字要在视觉复核中明确检查，不能因文字匹配而略过。

```sh
python scripts/render_deck.py output/editable.pptx output/review --page-spec work/page-spec.json
python scripts/evaluate_delivery.py work/page-spec.json output/review/render-report.json work/visual-review.json --init-review
```

打开 `output/review/review.png` 和每页渲染 PNG，对照批准图片逐页复核。填写 `visual-review.json` 中每页的 `status`（`pass`、`fail`、`pending`）及简短 `notes`。只有真正看过本次渲染结果，才能标为 `pass`。然后汇总；`--observations` 可重复传入，覆盖所有页面：

```sh
python scripts/evaluate_delivery.py work/page-spec.json output/review/render-report.json work/visual-review.json \
  --observations work/observations-s01.json --observations work/observations-s02.json \
  --scene work/scene.json --output output/scorecard.json
```

图片版省略 `--scene`。输出报告保存 PPTX、Page Spec、渲染报告、视觉复核、观察记录和可选 Scene 的 SHA-256，方便回溯本次评分依据。命令仅在 `pass` 时返回 0；`fail` 或 `incomplete` 返回 1。PPTX、Page Spec、渲染 PNG 或批准图片变更后，重新渲染并重新复核；哈希不匹配会被拒绝。不要把旧评分卡沿用到新文件。
