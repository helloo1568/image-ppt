<p align="center">
  <b>简体中文</b> | <a href="./README.en.md">English</a>
</p>

# image-ppt

[![GitHub stars](https://img.shields.io/github/stars/helloo1568/image-ppt?style=flat-square)](https://github.com/helloo1568/image-ppt)
[![License](https://img.shields.io/github/license/helloo1568/image-ppt?style=flat-square)](./LICENSE)
![Agent Skill](https://img.shields.io/badge/Agent-Skill-111111?style=flat-square)
![PowerPoint](https://img.shields.io/badge/Output-PPTX-B7472A?style=flat-square)

将书籍、PDF、论文、报告和 Markdown 等材料转化为图片版或可编辑 PowerPoint 的 Agent Skill。

它采用分阶段工作流：先理解内容并提供四套风格缩略图供用户选择，再逐页生成图片版 PPT；只有用户明确要求时，才继续还原为可编辑 PPTX。

![image-ppt preview](./social-preview.png)

## 功能

- 从长文档中提炼适合演示的结构、观点、案例和结论
- 生成四套不同视觉方向的风格缩略图供用户选型
- 按选定风格逐页生成统一的 PPT 页面图片
- 将页面图片确定性合并为 16:9 图片版 PPTX
- 可选地将主要文字、简单形状和图表还原为可编辑元素
- 使用制作规格记录需求、页序、准确数据和逐页状态，支持中断后继续

## 效果展示

以下为使用本技能实际生成的 PPT 页面效果：

**耕云 — AI 惠农产品创新赛道参赛 PPT**（新中式水墨风）

<img src="./examples/gengyun-cover.jpg" width="560">

**晚晴心语公众号运营周报**（同内容、两种风格对比）

| B 套：深蓝金商务风 | C 套：新中式青绿金风 |
|:---:|:---:|
| <img src="./examples/wanqing-weekly-b-cover.jpg" width="380"> | <img src="./examples/wanqing-weekly-c-p1.jpg" width="380"> |

**中老年情感公众号运营方案**（复古暖橙风）

<img src="./examples/silver-emotion-p1.jpg" width="560">

> 更多效果图见 `examples/` 目录。

## 工作流

```text
源材料
  ↓
需求确认
  ↓
内容提炼与四套风格缩略图
  ↓ 用户选择一种风格
图片版 PPT 逐页生成与合并
  ↓ 用户明确要求可编辑化
可编辑 PPTX 还原（可选）
```

默认有两个不可自动跳过的确认节点：

1. 确认源材料、参考风格、使用场景和页数预期
2. 展示四套风格缩略图后等待用户选择

用户可以明确说“跳过缩略图”“你替我选择风格”或“只制作图片版”，让流程按授权范围快进。普通的“帮我生成 PPT”不构成跳过授权。

## 风格缩略图是什么

本项目中的“缩略图”不是单张 PPT 页面缩小后的图片，也不是把四种风格拼成一个 2×2 对比图。

每套风格缩略图都是一张类似 PowerPoint“幻灯片浏览视图”的横向总览图：

- 一张图只展示一种完整设计风格
- 图中以 3×2、4×2 或相近网格排列 6–8 张迷你 16:9 幻灯片
- 页面通常覆盖封面、核心数据、正文、图表、案例和总结/行动页
- 四套缩略图使用相同的页面顺序和内容，只改变配色、字体、版式、图形语言和素材风格
- 四张风格缩略图分别展示并编号为 1–4，等待用户选型

这种方式能在正式生成整套页面前，同时检查单页设计和跨页一致性。

## 安装

将仓库克隆到 Agent 的技能目录。不同产品的技能目录可能不同，请以当前产品文档为准。

### Codex

```bash
git clone https://github.com/helloo1568/image-ppt.git ~/.codex/skills/image-ppt
```

### Claude Code

```bash
git clone https://github.com/helloo1568/image-ppt.git ~/.claude/skills/image-ppt
```

安装后确认以下文件存在：

```text
image-ppt/SKILL.md
image-ppt/references/prompts.md
```

需要运行图片合并脚本时安装依赖：

```bash
python -m pip install -r requirements.txt
```

## 快速开始

向 Agent 提供材料，并说明使用场景和页数：

```text
使用 image-ppt，把这份 PDF 做成 12 页课堂汇报 PPT。
没有参考模板。先生成四套幻灯片浏览视图式风格缩略图，我选定后再继续。
```

其他示例：

```text
把这本书做成读书分享 PPT，约 15 页，没有参考风格。
把这份周报做成周例会图片版 PPT，不需要可编辑还原。
从这份图片版 PPT 开始，只执行可编辑化还原。
跳过风格缩略图，你替我选择适合管理层汇报的风格。
```

## 输出

根据用户授权范围，技能可以生成：

- 四张独立的幻灯片浏览视图式风格缩略图
- 按页码排序的 PNG/JPEG 页面图片
- 每页为整张图片的图片版 `.pptx`
- 主要信息可编辑的混合式 `.pptx`（可选）
- 临时制作规格 `deck-spec.md`，用于记录状态和恢复任务

## 确定性合并脚本

`scripts/build_image_ppt.py` 按文件名自然排序，将 PNG/JPEG 页面图片合并成 PPTX：

```bash
python scripts/build_image_ppt.py ./slides ./output/deck.pptx
```

推荐使用零填充文件名：

```text
01-cover.png
02-dashboard.png
03-analysis.png
```

常用选项：

```bash
python scripts/build_image_ppt.py ./slides ./deck.pptx --fit cover
python scripts/build_image_ppt.py ./slides ./deck.pptx --fit contain --background FFFFFF
```

脚本默认创建 16:9 幻灯片，保存后会重新打开文件并核对页数。运行脚本需要 Python、Pillow 和 python-pptx。

## 项目结构

```text
image-ppt/
├── SKILL.md
├── README.md
├── README.en.md
├── LICENSE
├── manifest.yaml
├── requirements.txt
├── .gitignore
├── agents/
│   └── openai.yaml
├── references/
│   ├── prompts.md
│   └── deck-spec-template.md
├── scripts/
│   └── build_image_ppt.py
├── examples/
│   ├── gengyun-cover.jpg         ← 耕云参赛PPT（水墨风）
│   ├── wanqing-weekly-b-cover.jpg ← 晚晴心语周报B套（商务风）
│   ├── wanqing-weekly-c-p1.jpg    ← 晚晴心语周报C套（新中式风）
│   ├── wanqing-weekly-c-p2.jpg
│   ├── wanqing-weekly-c-p4.jpg
│   ├── silver-emotion-p1.jpg      ← 中老年情感方案（复古风）
│   └── silver-emotion-p2.jpg
├── social-preview.jpg
└── social-preview.png
```

## 平台与工具

技能本身不绑定具体图像模型。推荐在具备以下能力的 Agent 环境中使用：

- 读取 PDF、Markdown 和长文本
- 调用图像生成模型
- 运行本地脚本并输出文件
- 检查生成图片和 PPTX

Codex 可以负责材料读取、流程编排和 PPTX 拼装。图像页面可由 GPT Image、Agnes、Midjourney 或其他可用模型生成。若外部工具不支持图生图，应把选定缩略图提炼为稳定的文字视觉规范，再逐页复用。

## 限制

- 图像模型可能生成错字、错误数字或不一致的跨页样式，必须逐页验收
- 图片版 PPT 的页面内容不可直接编辑
- 可编辑还原采用“复杂视觉保真 + 主要信息可编辑”的混合策略，不能保证所有元素完全原生化
- 高密度表格和需要精确计算的图表更适合程序化制作，不适合完全依赖生图
- 不同 Agent 和图像服务的文件能力、尺寸限制、费用和内容政策不同

## 安全与隐私

- 仓库不包含 API Key 或账号凭证
- `build_image_ppt.py` 只读取本地图片并写入本地 PPTX，不发起网络请求
- 实际使用的外部图像或文档服务可能上传提示词、材料或页面内容，请遵守对应服务的隐私政策
- 不要把含密钥的 `config.json`、环境变量文件或私有材料提交到仓库

## 参与贡献

欢迎提交 Issue 和 Pull Request。建议在提交前：

1. 保持 `SKILL.md` 简洁，并把长提示词或模板放入 `references/`
2. 不在仓库中加入 API Key、生成缓存或用户材料
3. 运行 `python -m py_compile scripts/build_image_ppt.py`
4. 使用至少一组真实材料检查需求门禁、四套缩略图选型和 PPTX 合并流程
5. 同步更新中文与英文 README

## 来源与致谢

本技能的早期工作流参考了：

- 小黑盒社区教程《青年大学习AI版：零基础用GPT5.6做精美可编辑PPT》，作者“玩家22186848”
- B 站 UP 主“一往无前河井”的学术 PPT 制作思路

感谢原作者和社区贡献者分享方法与实践经验。

## 许可证

[MIT License](./LICENSE) © 2026 风清云影（helloo1568）
