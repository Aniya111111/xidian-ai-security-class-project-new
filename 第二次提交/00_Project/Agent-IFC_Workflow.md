---
type: workflow
name: Agent-IFC
version: 1
updated: "2026-10-12"
tags: [workflow, research, literature]
---

# Agent-IFC 工作流

## 总流程

~~~text
AI 安全科研情报
  -> Agent-IFC/00_Inbox/Literature 候选条目
  -> 人工筛选 selected / rejected
  -> 获取 PDF
  -> DeepTutor 精读
  -> Agent-IFC/10_Papers 正式论文卡片
  -> 人工核查 status: reviewed
  -> Agent-IFC/20_Themes 跨论文综合
  -> Agent-IFC/30_Projects 项目论证
  -> Agent-IFC/40_Evidence 写作证据
  -> 论文写作
~~~

## 工具职责

| 工具或目录 | 负责 | 不负责 |
| --- | --- | --- |
| AI 安全科研情报 | 发现、去重、初筛、六维评分 | 不生成正式论文卡片 |
| 00_Inbox/Literature | 保存候选条目 | 不保存未经核查的正式结论 |
| DeepTutor | 阅读选中论文、按模板生成卡片 | 不把卡片设为 reviewed |
| 10_Papers | 保存一篇论文一份正式卡片 | 不保存每日推荐列表 |
| 20_Themes | 综合多篇 reviewed 论文 | 不替代原始证据 |
| 30_Projects | 组织研究问题、假设和任务 | 不直接承载原文摘录 |
| 40_Evidence | 保存论断—证据—来源映射 | 不接收无法追溯的 AI 结论 |
| 用户 | 决定 selected、reviewed 和 used | 不需要手工重复填写模板 |

## 关键状态

候选文献：

~~~text
candidate -> selected -> imported
          \-> rejected
~~~

正式论文卡片：

~~~text
inbox -> reading -> reviewed -> used
~~~

两个状态系统不可混用。triage_status 属于候选条目；status 属于正式论文卡片。

## 质量门槛

### 候选进入精读

- 唯一标识或标题去重通过。
- 来源范围明确。
- 推荐理由与研究问题直接相关。
- 六维评分可复算；主题匹配分不低于 10/35。
- 用户将 triage_status 改为 selected。

### 正式卡片进入 reviewed

- 元数据与 PDF 版本一致。
- 每条 Cxx 结论都能回到页码、章节、图或表。
- 关键数值已经人工核对。
- 作者陈述、AI 分析和研究假设明确分开。
- PDF 与主题链接有效。

### 证据进入写作

- 来源卡片状态至少为 reviewed。
- 论断强度不超过原始证据。
- 能定位到原论文，而不是只引用 AI 摘要。

## 主要入口

- [[Agent-IFC/00_Inbox/Literature|科研情报收件箱]]
- [[Agent-IFC/00_Project/Research_Profile|研究关注配置]]
- [[Agent-IFC/90_Templates/Literature_Candidate_Template|候选文献模板]]
- [[Agent-IFC/90_Templates/Literature_Inbox_Rules|候选筛选规则]]
- [[Agent-IFC/90_Templates/Research_Intelligence_Import_Prompt|科研情报写入提示词]]
- [[Agent-IFC/90_Templates/DeepTutor_Import_Prompt|DeepTutor 导入提示词]]
- [[Agent-IFC/90_Templates/Paper_Template|正式论文卡片模板]]
- [[Agent-IFC/90_Templates/Paper_Rules|正式论文卡片规则]]
