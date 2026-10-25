---
type: workflow-prompt
tool: research-intelligence
updated: "2026-10-12"
tags: [workflow, literature, intelligence]
---

# 科研情报写入 Obsidian

将下面的提示词交给能够访问当前 Obsidian 库的科研情报工具。

~~~text
请把本次发现的候选论文写入 Obsidian 科研情报收件箱。

开始前必须读取：
1. Agent-IFC/00_Project/Research_Profile.md
2. Agent-IFC/90_Templates/Literature_Inbox_Rules.md
3. Agent-IFC/90_Templates/Literature_Candidate_Template.md

目标目录：
Agent-IFC/00_Inbox/Literature/

禁止写入或修改：
- Agent-IFC/10_Papers/
- Agent-IFC/20_Themes/
- Agent-IFC/30_Projects/
- Agent-IFC/40_Evidence/

执行要求：
1. 每篇候选论文对应一份 Markdown。
2. 创建前按 DOI、arXiv ID、OpenAlex ID、标题+第一作者+年份检查候选目录和正式论文目录。
3. 已有正式论文卡片时，不创建候选；报告正式卡片路径。
4. 已有候选时，补充新的 discovered_from 或来源信息，不创建重复文件。
5. 新条目的 triage_status 必须为 candidate。
6. 只有元数据时 source_scope=metadata_only；读取摘要后才能设为 abstract_only；读取完整论文后才能设为 fulltext。
7. 不得从摘要推断全文实验结果、作者局限、图表内容或页码。
8. 严格按六维上限评分，score_total 必须等于六项之和。
9. 如果 Research_Profile 的研究问题和关键词尚未填写，score_status=unscored，所有 score_* 保持 null，不得猜测相关性分数。
10. score_topic 低于 10 时提出拒绝建议，并说明与核心问题不相关的原因；triage_status 保持 candidate，由总控 Agent 弹窗请求用户确认，未经确认不得改为 rejected。
11. candidate_id 使用最强可用标识；无法确认时留空。
12. 只链接库内真实存在的主题、项目和论文；无法确认时写“待关联”。
13. 写入后重新读取文件，报告创建路径、候选标识、来源范围、评分状态、总分和仍需人工确认的字段。

如果无法使用 Obsidian 写入工具，请明确说明，不要声称已经写入。
~~~
