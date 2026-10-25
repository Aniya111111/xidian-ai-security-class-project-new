---
schema_version: 1
type: literature_candidate
candidate_id: ""
title: ""
authors: []
year: null
venue: ""
doi: ""
arxiv_id: ""
openalex_id: ""
source_url: ""
discovered_from: ""
discovered_at: ""
source_scope: metadata_only
topics: []
projects: []
classification: ""
triage_status: candidate
score_status: unscored
score_topic: null
score_method: null
score_source: null
score_network: null
score_applied: null
score_archival: null
score_total: null
pdf: ""
paper_card: ""
tags: [literature-candidate]
---

# {{title}}

## 一句话判断

待填写。说明为什么值得或不值得进入精读，不使用“重要”“前沿”等空泛表述。

## 摘要与来源边界

- 当前可用材料：metadata_only / abstract_only / fulltext
- 摘要或内容概述：待填写。
- 尚未核验的信息：待填写。

## 推荐理由

- 与研究问题的联系：待填写。
- 可借鉴的方法：待填写。
- 可能补充的证据：待填写。

## 六维评分

| 维度 | 得分上限 | 得分 | 理由 |
| --- | ---: | ---: | --- |
| 主题匹配 | 35 | 待评分 | 与核心研究问题的直接程度 |
| 方法价值 | 20 | 待评分 | 方法质量、可复用性与实验设计价值 |
| 来源质量 | 15 | 待评分 | 出版渠道、可信度与可核验性 |
| 研究网络相关性 | 10 | 待评分 | 与关注作者、机构或合作网络的联系 |
| 应用价值 | 10 | 待评分 | 数据、基准、工具或工程启示 |
| 归档价值 | 10 | 待评分 | 长期参考、综述或教学价值 |
| 总分 | 100 | 待评分 | 必须等于六项之和 |

## 与现有知识库的关系

- 相关主题：待关联
- 相关项目：待关联
- 相关论文：待关联
- 重复检查：待执行

## 风险与不确定性

- [ ] 预印本或未经同行评审。
- [ ] 只有摘要或元数据。
- [ ] DOI、作者或年份尚未核验。
- [ ] 可能与已有论文重复。
- [ ] 推荐理由依赖未经验证的外部信息。

## 下一步

- [ ] 人工选择：selected / rejected
- [ ] 获取合法全文并放入 Agent-IFC/90_Attachments/
- [ ] selected 后交给 DeepTutor 精读
- [ ] 正式卡片生成后填写 paper_card
- [ ] 确认正式卡片存在后改为 imported
