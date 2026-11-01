---
type: inbox-index
scope: literature
updated: "2026-10-12"
tags: [workflow, literature, inbox]
---

# 科研情报收件箱

这里保存尚未进入正式精读流程的候选论文。科研情报工具只能写入候选目录，不得直接修改正式论文卡片。

## 入口与规则

- 候选目录：[[Agent-IFC/00_Inbox/Literature]]
- 候选模板：[[Agent-IFC/90_Templates/Literature_Candidate_Template]]
- 筛选规则：[[Agent-IFC/90_Templates/Literature_Inbox_Rules]]
- 研究关注：[[Agent-IFC/00_Project/Research_Profile]]
- 情报写入提示词：[[Agent-IFC/90_Templates/Research_Intelligence_Import_Prompt]]
- 总工作流：[[Agent-IFC/00_Project/Agent-IFC_Workflow]]
- 正式论文目录：[[Agent-IFC/10_Papers]]

## 状态流转

~~~text
candidate
  ├─ selected -> 获取 PDF -> DeepTutor 精读 -> imported
  └─ rejected
~~~

- candidate：科研情报工具刚发现，尚未人工判断。
- selected：用户确认值得获取全文和精读。
- rejected：重复、不相关、来源不可靠或价值不足。
- imported：已生成正式论文卡片，且 paper_card 指向真实文件。

## 当前操作

1. 科研情报工具将候选 Markdown 写入 Agent-IFC/00_Inbox/Literature/。
2. 按 DOI、arXiv ID、OpenAlex ID 和标题去重。
3. 核对六维评分及推荐理由。
4. 用户把 triage_status 改为 selected 或 rejected。
5. 对 selected 条目获取 PDF，放入 Agent-IFC/90_Attachments/。
6. 使用 DeepTutor 生成 Agent-IFC/10_Papers/ 下的正式论文卡片。
7. 卡片创建并回读成功后，将候选改为 imported，并填写 paper_card。

## 人工筛选清单

- [ ] 主题匹配分不低于 10/35。
- [ ] 总分等于六个维度之和。
- [ ] DOI、arXiv ID 或标题未与已有条目重复。
- [ ] 推荐理由具体说明与研究问题的联系。
- [ ] 来源范围标记准确，没有把摘要当成全文。
- [ ] selected 条目已经明确下一步动作。
