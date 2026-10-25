---
type: workflow-rule
applies_to: paper
schema_version: 1
updated: "2026-10-12"
tags: [workflow, paper]
---

# 论文卡片填写规则

## 1. 文件与去重

- 每篇论文只对应 `Agent-IFC/10_Papers/` 下的一份 Markdown 卡片。
- 文件名使用 `年份_第一作者_简短标题.md`；文件名不承担唯一标识功能。
- 去重优先级：DOI（统一为小写）> arXiv ID（去掉版本号）> 标题、第一作者与年份组合 > 本地 PDF 的 SHA-256。
- 创建前必须搜索 `paper_id`、`doi`、`arxiv_id` 和标题。已有卡片时只报告路径与建议补充项，不新建重复卡片，不覆盖用户笔记。

## 2. 状态规则

`status` 只能使用以下值：

- `inbox`：已收集，尚未开始阅读。
- `reading`：正在阅读，或已由 AI 整理但尚未人工核查。
- `reviewed`：用户已核查元数据和每条核心结论的原文证据。
- `used`：已将核查过的内容用于综述、论文或其他研究输出。

DeepTutor 或其他 AI 创建、补全卡片后，最多只能设为 `reading`。AI 不得自行设为 `reviewed` 或 `used`；后两种状态由用户修改。

## 3. 来源范围与定位

- `source_scope` 只能使用 `fulltext`、`abstract_only`、`excerpt` 或 `unknown`。
- `locator_mode` 只能使用 `page-grounded`、`structure-grounded`、`source-limited` 或 `unknown`。
- 完整 PDF 且页序可靠时使用 `[Paper: PDF p. N, Figure/Table/Equation/Section]`。
- 只有结构定位时不得写页码；使用章节、图、表或公式编号。
- 只有摘要或片段时不得推断未见的方法、实验、图表或局限；来源写 `[Paper: Abstract]` 或 `[Paper: User-provided excerpt]`。
- 未知内容写“未提供”或保留空值，禁止猜测作者、DOI、页码、样本量、模型版本和数值。

## 4. 证据与观点边界

- `[Paper]`：论文直接报告，必须附来源位置。
- `[External]`：论文以外来源核验，必须给出引用或链接。
- `[Analysis]`：AI 基于已标明证据进行的分析，不能写成作者结论。
- `[Hypothesis]`：需要实验验证的解释或研究方向，必须给出验证与证伪条件。
- `[User]`：用户提供的判断或关联。
- 每条核心结论使用稳定编号 `C01`、`C02`……并保持结论强度与证据一致。
- 作者明确承认的局限与 AI 的批判性分析必须分开。

## 5. 关联笔记

- `topics` 和 `projects` 属性填写不带路径的规范名称，便于查询。
- 正文“关联笔记”使用 Obsidian 双向链接，例如 `[[Agent-IFC/20_Themes/课程知识图谱|课程知识图谱]]`。
- 只链接库内实际存在且确实相关的笔记；不能确认时写“待关联”，不要创建虚假的项目或论文关联。
- 主题笔记应反向链接论文卡片，形成显式双向导航。

## 6. PDF 与附件

- PDF 存放在 `Agent-IFC/90_Attachments/`，卡片属性 `pdf` 保存相对于 Obsidian 库根目录的路径。
- 上传到 DeepTutor 的文件不会自动成为 Obsidian 附件；需要单独确认 PDF 已存在于附件目录。

## 7. 人工核查门槛

只有同时满足以下条件，用户才将 `status` 改为 `reviewed`：

- 元数据与实际 PDF 版本一致；
- 每条 `Cxx` 结论均能定位到原文；
- 关键数值与图表一致；
- 不存在未标记的 AI 推断；
- 主题链接有效，项目链接已确认或明确保留“待关联”。
