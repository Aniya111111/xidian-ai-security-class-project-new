---
type: workflow-prompt
tool: DeepTutor
updated: "2026-10-12"
tags: [workflow, DeepTutor, paper]
---

# DeepTutor 导入论文到 Obsidian

将下面的提示词发送给已连接当前 Obsidian 库的 DeepTutor。

```text
请将当前论文整理为 Obsidian 论文卡片。

开始前必须读取：
1. Agent-IFC/90_Templates/Paper_Rules.md
2. Agent-IFC/90_Templates/Paper_Template.md

目标目录：Agent-IFC/10_Papers/
附件目录：Agent-IFC/90_Attachments/

执行要求：
1. 按 Paper_Rules 的优先级搜索 paper_id、DOI、arXiv ID 和标题，先去重。
2. 已有卡片时，只报告现有路径和建议补充内容；不要创建重复卡片，不要覆盖已有正文或用户笔记。
3. 没有卡片时，复制模板并填写；文件名为“年份_第一作者_简短标题.md”。
4. 只依据当前实际读取到的材料填写。未知信息保留空值或写“未提供”，禁止补造元数据、页码、实验设置和结论。
5. 每条核心结论使用 C01、C02……编号，记录原文页码/章节/图表号、关键数值、适用边界和待核查状态。
6. 明确区分 [Paper]、[Analysis] 与 [Hypothesis]；作者局限与 AI 分析分开。
7. 只读到摘要时，将 source_scope 设为 abstract_only、locator_mode 设为 source-limited，不填写全文实验细节。
8. status 设为 reading，不得设为 reviewed 或 used。
9. 关联笔记只链接库内已经存在且确实相关的笔记；无法确认时写“待关联”。
10. 完成后报告实际创建或更新的路径、缺失字段、需要人工核查的结论编号。若无法写入 Obsidian，请输出完整 Markdown，不要声称已写入。
```
