---
type: research-profile
schema_version: 1
updated: "2026-10-12"
research_area: "多 Agent 协作系统的安全防护"
research_scope: "面向由大语言模型驱动的多 Agent 系统，研究 Agent 间通信、任务委托、共享记忆、工具调用与编排过程中的攻击预防、检测、隔离、恢复和可验证安全评估。"
previous_focus: "大语言模型幻觉防御；保留为相关风险机制与已有文献资产，不再作为主筛选方向。"
keywords_zh:
  - 多 Agent 安全
  - 多智能体系统安全
  - Agent 协作安全
  - Agent 间通信安全
  - 恶意 Agent
  - 被攻陷 Agent
  - 提示注入传播
  - 间接提示注入
  - 共享记忆污染
  - 上下文污染
  - 工具调用安全
  - 权限委托
  - 最小权限
  - 身份认证与消息来源
  - 信任管理
  - 拜占庭鲁棒性
  - 共谋与串通
  - 攻击传播与级联失效
  - 安全编排
  - 隔离与恢复
keywords_en:
  - multi-agent system security
  - LLM multi-agent security
  - secure agent collaboration
  - inter-agent communication security
  - malicious agent
  - compromised agent
  - prompt injection propagation
  - indirect prompt injection
  - shared memory poisoning
  - context poisoning
  - tool-use security
  - privilege delegation
  - least privilege
  - agent identity and message provenance
  - trust management
  - Byzantine robustness
  - agent collusion
  - cascading failure
  - secure orchestration
  - containment and recovery
excluded_terms:
  - 仅优化多 Agent 协作效率但不讨论安全、攻击、信任或鲁棒性
  - 仅讨论传统多智能体路径规划或控制且无法迁移到 LLM Agent 安全
  - 仅讨论单 Agent 越狱且没有跨 Agent、共享状态、委托或协作传播机制
  - 人类团队协作安全且不涉及自主智能体系统
tracked_authors: []
tracked_institutions: []
priority_methods:
  - Agent 身份认证、消息签名、来源追踪与完整性验证
  - 最小权限、能力令牌、工具访问控制与委托边界
  - 消息内容过滤、提示注入检测与跨 Agent 污点传播分析
  - 共享记忆分区、写入验证、数据来源标记与污染恢复
  - 恶意或被攻陷 Agent 的异常检测、隔离、降权与撤销
  - 多 Agent 共识、交叉验证、可信仲裁与拜占庭鲁棒协议
  - 编排器策略验证、沙箱、运行时监控和安全状态机
  - 共谋、身份伪造、女巫攻击和级联攻击的红队评测
  - 失效后的回滚、证据保全、事件响应与安全恢复
  - 形式化威胁建模、可组合安全属性与系统级安全基准
priority_applications:
  - 自动科研与软件开发 Agent 团队
  - 企业工作流、知识库和共享记忆 Agent
  - 工具调用、浏览器、代码执行和外部 API 编排
  - 金融、医疗、法律和关键基础设施中的多 Agent 决策
  - 机器人群体和具身 Agent 中的语言模型协作层
  - 开放式 Agent 网络与跨组织协作
search_policy:
  recent_window_months: 24
  include_seminal_works: true
  candidates_per_run: 30
  shortlist_per_run: 5
  languages: [en, zh]
  preferred_sources: [arXiv, ACL Anthology, OpenReview, IEEE Xplore, ACM Digital Library, Semantic Scholar, OpenAlex, Crossref]
scoring_weights:
  topic: 35
  threat_model: 20
  evidence: 15
  defense: 15
  system: 10
  archival: 5
approval_policy:
  profile_changes: required
  candidate_selection: required
  paper_reviewed: required
  theme_publication: required
  evidence_to_writing: required
  automatic_rejection: disabled
---

# 多 Agent 协作的安全防护研究关注配置

这份文件是科研情报与总控 Agent 的长期配置，不是单篇论文笔记。检索、去重、评分、候选推荐、DeepTutor 精读和主题综合开始前都应读取它。DeepTutor 可以提供术语和论文证据，但不得自行更改本文件；后续配置变化必须由总控 Agent 弹窗请求用户批准。

研究对象是由 LLM 驱动、能够通信、分工、委托、共享状态或调用工具的多 Agent 系统。重点不是“使用多个 Agent 是否提高任务效果”，而是协作结构引入了哪些新的信任边界、攻击面和传播路径，以及如何预防、检测、遏制并恢复。

原“幻觉防御”方向不删除：已有论文卡和主题笔记继续保留。幻觉只有在会通过 Agent 消息、共享记忆、任务分派或工具结果传播，并影响协作系统安全时，才作为本方向的直接研究对象。

## 核心研究问题

1. 多 Agent 系统的主体、资产、信任边界、权限和攻击者能力应如何建模？
2. 恶意、被攻陷或行为异常的 Agent 如何借助消息、共享记忆、计划和工具结果影响其他 Agent？
3. 提示注入、错误信息、身份伪造、共谋和权限越界如何在协作网络中传播、放大或形成级联失效？
4. 身份认证、来源证明、最小权限、隔离、仲裁和共识机制分别能阻断哪些攻击路径？
5. 如何在不暴露敏感上下文的条件下，实现可审计的通信、委托和跨 Agent 证据验证？
6. 防护机制如何平衡攻击成功率、正常任务效用、误报率、时延、token 成本和可扩展性？
7. 当前基准是否覆盖自适应攻击、共谋攻击、长时任务、动态成员和真实工具权限？
8. 局部 Agent 失效后，系统如何撤销权限、隔离污染、回滚共享状态并安全恢复？

## 威胁模型边界

每篇论文至少核对以下内容；没有明示时标记“未明确记录”，不能由标题推断：

- 协作架构：中心编排、层级、点对点、黑板/共享内存或动态网络。
- 攻击主体：外部用户、恶意 Agent、被攻陷 Agent、恶意工具/数据源或编排器。
- 攻击者能力：可读写哪些消息、记忆、提示、工具和身份字段，是否能够共谋或自适应。
- 安全资产：任务目标、机密、工具权限、共享记忆完整性、消息来源和系统可用性。
- 传播路径：Agent 消息、任务委托、计划、共享记忆、RAG、工具返回或代码执行结果。
- 防护阶段：设计期、输入/通信前、协作运行时、工具执行前后、事后恢复。
- 成功与失败条件：攻击成功率、危害、泄漏、权限越界、污染范围和正常任务效用。

## 检索主题簇

### A. 通信与身份安全

- inter-agent prompt injection and message manipulation
- agent identity, authentication, provenance and non-repudiation
- secure communication protocols and policy-enforced messaging

### B. 信任、恶意成员与共谋

- malicious or compromised agents, Byzantine agents and trust management
- collusion, Sybil attacks, reputation manipulation and deceptive agents
- consensus, arbitration, cross-agent verification and resilient coordination

### C. 共享状态与长期记忆

- shared memory poisoning, context contamination and persistent attacks
- memory access control, provenance, taint tracking, rollback and recovery
- poisoned RAG/tool output propagation through agent teams

### D. 权限、委托与工具安全

- least privilege, capability systems and scoped delegation
- tool-use policy, confused deputy, privilege escalation and data exfiltration
- sandboxing, isolation, runtime monitors and secure orchestration

### E. 系统评测与理论

- multi-agent red teaming, adaptive attackers and security benchmarks
- attack graphs, cascading failures and compositional security guarantees
- safety–utility–latency–cost trade-offs under realistic permissions

## 纳入标准

- 同时涉及两个或以上 Agent/协作组件，以及明确的安全、攻击、信任、权限或鲁棒性问题。
- 给出可检查的威胁模型、攻击路径、防护机制、实验协议或理论安全性质中的至少一项。
- 能定位攻击者能力、系统权限和安全目标；关键实验有可追踪的数据集、指标或实现设置。
- 论文身份与版本可核验；优先正式会议/期刊和可追踪预印本。
- 单 Agent 安全研究只有在能明确解释跨 Agent 传播、委托或共享状态风险时才纳入。

## 排除标准

- 只比较 Agent 数量、角色提示或协作性能，没有安全问题和攻击/防御证据。
- 只描述一般可靠性、幻觉或错误，但没有协作传播、信任边界或安全后果。
- 只研究经典多智能体优化、博弈或控制，且未建立到 LLM Agent 安全的可验证联系。
- 只提出概念性框架，没有清晰威胁模型，也没有实验、形式化分析或可核验案例。
- 无法核验作者、标题、年份、版本或来源；或与正式论文卡重复且没有新增证据。

排除词按语义判断，不作为无条件关键词黑名单。传统分布式系统、拜占庭容错和访问控制工作若为 LLM 多 Agent 威胁提供直接机制或理论基础，可以作为奠基文献纳入，但卡片必须说明迁移边界。

Agent 只能提出排除建议；最终拒绝必须通过用户弹窗确认，不得自动删除候选论文。

## 关注输出与对比字段

- **协作与信任模型**：角色、拓扑、编排方式、身份、信任假设和权限边界。
- **攻击证据**：入口、攻击者能力、传播路径、受影响资产、成功条件和适用限制。
- **防护证据**：机制、部署位置、依赖、覆盖攻击、绕过方式和恢复能力。
- **评估证据**：攻击成功率、检测率、误报率、任务效用、时延、成本和规模。
- **系统证据**：真实工具、共享记忆、长时任务、动态成员与自适应攻击下的表现。
- **写作证据**：可定位到原文页码、章节、图表或实验设置的主张，不把作者假设写成已验证结论。

论文卡 YAML 可在人工核对后补充：

```yaml
comparison:
  collaboration_architecture: "协作架构与角色拓扑"
  attacker_capability: "攻击者身份、知识与读写能力"
  propagation_path: "攻击或错误传播路径"
  trust_boundary: "信任、权限和委托边界"
  defense_mechanism: "防护机制、部署阶段与依赖"
  evaluation_protocol: "数据、攻击设置、指标、基线与成本"
```

## 候选优先级

- **P0**：提出新的多 Agent 攻击或防护机制，并在多任务、多模型或真实工具环境中验证。
- **P1**：提供高质量威胁模型、系统基准、红队数据、综述或可组合安全分析。
- **P2**：针对单一攻击面提供可复现改进，且明确权限、边界和绕过条件。
- **P3**：概念性讨论、证据有限，或主要研究一般 Agent 性能而仅间接涉及安全。

## 自动化与人工审批

- 自动完成：读取画像、标准化、去重、来源核验、评分建议、候选卡创建、reviewed 变化检测和主题草稿生成。
- 必须弹窗：研究画像修改、候选进入 DeepTutor、正式论文卡改为 reviewed、主题笔记发布、证据进入论文写作。
- DeepTutor 创建的正式论文卡最高只能设为 reading；AI 输出不能代表用户审核。
- Agent 不得因低分直接删除候选；应展示建议、证据和不确定性。
- 总控只读取符合协作关键词且命中安全关键词组的 reviewed 卡片；不因一篇论文提及 Agent 就自动纳入。

## 评分校准记录

- 2026-10-12：用户将主方向由“幻觉防御”调整为“多 Agent 协作的安全防护”；原方向作为相关机制和已有资产保留。
- 初始权重采用主题 35、威胁模型 20、证据 15、防护 15、系统性 10、归档 5。
- tracked_authors 与 tracked_institutions 暂不预设；完成 2–3 轮候选筛选后，根据误收、漏收和高质量证据网络弹窗校准。
- 新兴方向不以引用量或是否正式发表作为自动排除条件；预印本必须核验版本与实验材料。

## 接口规范

- [[Agent-IFC/00_Project/DeepTutor_Agent_Integration|DeepTutor CLI Agent 集成规范]]
