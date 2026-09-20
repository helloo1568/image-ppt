# 参与贡献 · Contributing

欢迎改进提示词、文档、Page Spec / Scene 协议、导出脚本与测试，也欢迎分享获准公开的作品。

## 报告问题

通过 [GitHub Issues](https://github.com/helloo1568/slidemuse/issues) 提供：

- 使用的 Agent、操作系统、Python 和技能版本。
- 问题出现在哪个阶段，以及最短复现步骤。
- 预期结果、实际结果和相关报错。
- 脱敏后的最小 Page Spec / Scene、必要素材或截图。

请勿提交凭证、私人源材料或没有公开授权的内容。功能建议请说明具体使用场景与期望交付。

## 提交修改

1. Fork 仓库，从 `main` 创建功能分支。
2. 保持改动聚焦；面向用户的变更同步更新中英文文档和 `CHANGELOG.md`。
3. 修改脚本或协议时，添加有意义的回归测试并运行下方检查。
4. 提交 Pull Request，说明解决的问题、变更后的行为和验证结果；视觉变更附预览。

```sh
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m ruff check .
python -m pytest tests/ -q
python scripts/validate_page_spec.py examples/page-spec.example.json --strict
```

流程变更应明确说明对内容确认、风格选择、图片生成、可编辑还原及已有文件兼容性的影响。结构测试不能替代实际渲染检查。

## English

Contributions to prompts, documentation, Page Spec / Scene contracts, exporters, tests, and authorized showcase images are welcome.

- **Bugs:** open an [issue](https://github.com/helloo1568/slidemuse/issues) with your agent, OS, Python and skill versions, workflow stage, reproduction steps, expected/actual behavior, and a minimal sanitized example.
- **Changes:** fork from `main`, keep the scope focused, update both language versions and the changelog where relevant, and run the checks above for code or contract changes.
- **Pull requests:** explain the problem, resulting behavior, and validation. Include previews for visual changes and note compatibility implications for workflow changes.
- **Shared files:** exclude credentials, private documents, and content you do not have permission to publish. Structural tests do not replace rendered visual inspection.

By contributing, you agree that your contributions are provided under the repository's [MIT License](LICENSE).
