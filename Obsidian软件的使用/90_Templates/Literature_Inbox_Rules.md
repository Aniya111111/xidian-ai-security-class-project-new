---
type: workflow-rule
applies_to: literature_candidate
schema_version: 1
updated: "2026-10-12"
tags: [workflow, literature, inbox]
---

# 科研情报候选条目规则

## 1. 写入边界

- 科研情报工具只能在 Agent-IFC/00_Inbox/Literature/ 中新建或更新候选条目。
- 不得直接写入 Agent-IFC/10_Papers/、20_Themes/、30_Projects/ 或 40_Evidence/。
- 不得修改 status 为 reviewed 或 used 的正式论文卡片。
- 候选条目不是论文精读卡，不得假装完成全文阅读。

## 2. 文件名与去重

- 推荐文件名：年份_第一作者_简短标题_candidate.md。
- 去重优先级：DOI（小写）> arXiv ID（去掉版本号）> OpenAlex ID > 规范化标题、第一作者和年份。
- candidate_id 使用最强可用标识，例如 doi:10.xxxx、arxiv:2401.xxxxx 或 openalex:Wxxxx。
- 找到重复条目时更新已有候选的发现来源，不创建第二份文件。
- 如果正式论文卡片已经存在，将候选标为 imported 并填写 paper_card，不再重复推荐。

## 3. 来源范围

source_scope 只能使用：

- metadata_only：只有题录信息。
- abstract_only：已读取摘要，但没有全文。
- fulltext：实际读取了完整论文。

仅有元数据或摘要时，不得填写全文实验结果、作者局限、图表内容或精确页码。未知内容必须留空或写“未核验”。

## 4. 六维评分

| 字段 | 上限 |
| --- | ---: |
| score_topic | 35 |
| score_method | 20 |
| score_source | 15 |
| score_network | 10 |
| score_applied | 10 |
| score_archival | 10 |

- score_total 必须等于六项之和，范围为 0–100。
- 任一维度不得超过上限。
- score_topic 低于 10 时提出拒绝建议并说明理由，triage_status 保持 candidate；由总控 Agent 弹窗请求用户确认后才能改为 rejected，不因期刊知名度提高相关性分数。
- score_network 衡量与用户关注的作者、机构或合作网络的实际联系，不衡量一般知名度。
- 初次无法可靠评分时使用 score_status: unscored，并将各分值保留为 null，不填猜测分数。
- 经过人工或规则核查后使用 score_status: checked。

## 5. 分类与筛选状态

classification 可选：

- A_核心主线
- B_章节支撑
- C_工程背景
- D_方法借鉴
- E_暂存低优先

triage_status 只能使用：

- candidate：新发现，等待人工筛选。
- selected：用户确认进入全文获取和精读流程。
- rejected：重复、不相关、来源不足或价值较低。
- imported：正式论文卡片已创建且可以回读。

科研情报工具写入新条目时只能设置 candidate。selected 和 rejected 由用户确认；imported 只有在 paper_card 指向的文件真实存在时才能设置。

## 6. 进入 DeepTutor 的条件

候选条目必须同时满足以下条件才能交给 DeepTutor：

- triage_status 为 selected；
- 已完成重复检查；
- PDF 已合法获取并保存到 Agent-IFC/90_Attachments/，或者明确只能使用摘要；
- 已记录来源链接和来源范围；
- 已明确希望 DeepTutor回答的研究问题。

DeepTutor 成功创建并回读正式卡片后：

1. 在候选条目的 paper_card 中填写正式卡片的 Obsidian 链接；
2. 将 triage_status 改为 imported；
3. 正式卡片仍保持 status: reading，等待用户人工核查。
