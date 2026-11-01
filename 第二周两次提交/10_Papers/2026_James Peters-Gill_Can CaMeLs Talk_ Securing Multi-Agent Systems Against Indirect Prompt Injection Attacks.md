---
schema_version: 1
type: paper
ai_researcher_ready: true
paper_id: arxiv:2610.05640
title: Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection
  Attacks
authors:
- James Peters-Gill
- Avi Semler
- Henning Bartsch
- Ilia Shumailov
- Christian Schroeder de Witt
year: 2026
venue: arXiv preprint
volume: ''
issue: ''
pages: ''
doi: ''
arxiv_id: 2610.05640v1
paper_version: v1（PDF 页脚戳记：arXiv:2610.05640v1 [cs.MA] 5 Oct 2026）
source_url: https://arxiv.org/abs/2610.05640v1
pdf: Agent-IFC/90_Attachments/2610.05640v1Multi-CaMel(1).pdf
source_hash: 3d7d809a5fa229110a02818b1d3569f9a1100e7668c9443f3dbdb14702be485f
citekey: ''
topics:
- 多Agent系统安全
- 间接提示注入
- 控制流完整性
- 信息流控制
- Agent间通信协议
- 信任边界与来源保留
- 安全-效用权衡基准
projects: []
tags:
- paper
- 多Agent安全
- 间接提示注入
- 信息流控制
- 待人工核查
- status/reviewed
status: reviewed
source_scope: fulltext
locator_mode: structure-grounded
primary_lens: 多Agent系统安全：信任边界、控制流完整性与攻击传播路径
secondary_lens: 安全-效用权衡评测与基准构建（MultiAgentDojo）
context_mode: paper-only
imported_from: Agent-IFC / DeepTutor
created: '2026-10-12'
updated: '2026-10-12'
comparison:
  collaboration_architecture: '层级式 agent-as-tool 系统（Definition 1）：Agent 集合构成以 A0 为根的有向树
    H，父 Agent 通过工具调用唤起子 Agent，子 Agent 把调用它的父 Agent 当作用户；用户只与 A0 交互。实例化为多 Agent orchestrator
    拓扑（Fig. 1(a)：Orchestrator + SQL Agent + Email Agent）。评测环境：MultiAgentDojo 将 AgentDojo
    四个套件的工具划分给 2–4 个专门子 Agent 并加入 orchestrator（Table I）；AssetOpsBench 为 orchestrator
    委派四个专门子 Agent。[Paper: Section II-A; Section V-A; Section V-B; Table I]'
  attacker_capability: '外部对手将恶意指令植入 Agent 间接处理的外部内容/数据源（网页、邮件、文档、SQL 数据库），即间接提示注入；不假设存在恶意或被攻陷的
    Agent 本体，所有组成 Agent 均运行 CaMeL。案例研究中注入被写入 SQL 数据库（目标：把申请人数据外发到 ruth@email.com）；MultiAgentDojo
    中注入置于工具输出。论文明确指出所评测的是基准内既有攻击，未做自适应攻击评测，并警告 0% ASR 不代表对更强自适应攻击的免疫。攻击者是否可共谋、可读写身份字段等未明确记录。[Paper:
    Section I; Section III-A; Section V-B; Table III 说明文字]'
  propagation_path: '不可信工具输出 → 父 Agent 程序中的运行时变量（其 PLLM 未见）→ 父 Agent 的 QLLM 处理（如摘要）→
    被嵌入 agent-as-tool 调用的自然语言 message 参数 → 子 Agent 将其视为可信用户指令 → 子 Agent PLLM 生成的控制流计划被改写（新增
    send_email 外发调用）。作者命名为 boundary laundering。[Paper: Section III-A; Fig. 1(a); Fig.
    2; Fig. 3（Programs 1–4）; Fig. 7(a); Section V-C1]'
  trust_boundary: '父—子调用边界即信任边界：子 Agent 把父 Agent 当作其用户，因此 message 参数默认获得可信指令地位。multi-CaMeL
    把该边界显式双通道化——message 为可信自然语言指令通道，variables 为对子 Agent PLLM 不透明的数据通道，并要求跨边界保留 capabilities
    与 provenance；解释器强制 instruction-channel integrity（message 不得依赖任何工具输出）。安全策略实验中使用平凡策略
    S = ∅。[Paper: Section II-A; Section IV-A; Section IV-B; Section II-B（Definition
    4 与平凡策略说明）]'
  defense_mechanism: 'multi-CaMeL：(1) 双通道 agent-as-tool 接口 query_agent_j(message:
    str, variables: dict[str, Any]) -> str；(2) 子 Agent 运行时工具 get_variable(variable_name:
    str) -> Any；(3) 扩展 CaMeL 的自定义 Python 解释器，强制 instruction-channel integrity 与 cross-agent
    provenance preservation。部署阶段为协作运行时（每次跨 Agent 调用边界），依赖既有 CaMeL 的 PLLM/QLLM 分离与依赖追踪；作者指出与单
    Agent CaMeL 不同，该解释器即使不配置任何安全策略也是保证 CFI 所必需。[Paper: Section IV-A; Section IV-B;
    Section IV-C]'
  evaluation_protocol: '安全：MultiAgentDojo，n = 949 个注入任务实例/模型/配置，指标为 ASR，95% Wilson
    score 区间（因 Wald 在 0% 附近表现差）。效用：MultiAgentDojo 良性任务成功率（n = 97；Claude Fable 5 另报去拒答子集
    n = 45，95% Wald 区间）与 AssetOpsBench 任务成功率（141 任务中剔除 29 个不可完成任务后 n = 112，由具特权信息的
    LLM judge 评分，95% Wald 区间）。基线：no CaMeL、individual-agent CaMeL；另以原始 AgentDojo 校验
    MultiAgentDojo 良性难度（Table II）。模型：Claude Fable 5、GPT-5.5、GPT-4.1、Gemini 2.5 Pro、Gemini
    2.5 Flash Lite（每个 Agent 的 PLLM 与 QLLM 同模型），案例研究用 GPT-5.2（5 次试验，temperature = 1）；经
    OpenRouter API 访问，推理硬件不受控。所有工具描述被增补完整返回 schema。token/费用预算未提供。[Paper: Section III-B;
    Section V 开头; Section V-A; Section V-B; Table II–V; Section IX]'
---

# Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks

> Source coverage: 知识库中为完整 arXiv v1 PDF；本卡经多轮检索覆盖正文 Section I–IX 与附录 B、C、D（检索片段跨 p.1–p.24），未逐页通读，附录 A 标题与部分图表内文未被检索命中。
> Extraction confidence: 主结论、定义、协议接口与全部关键数值为高（直接摘自正文与 Table I–V 原文）；附录细节与个别引用条目身份为中低（标注未核验）。
> Locator mode: structure-grounded（检索返回的页码标记在不同查询间不一致，故本卡一律使用 Section / Definition / Figure / Table / Appendix 定位，不写页码）
> Primary analytical lens: 多 Agent 系统安全——信任边界、控制流完整性与攻击传播路径
> Secondary analytical lens: 安全-效用权衡评测与基准构建
> Context verification: Paper-only（未执行外部核验；所有外部工作仅按论文自述引用记录）
> Card completeness: Partial（元数据中 DOI、页码、代码仓库 URL、PDF 附件路径缺失或未核验）

## 01 基本信息

| 字段 | 内容 |
| --- | --- |
| 标题 | Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks |
| 作者及机构 | James Peters-Gill（Independent）；Avi Semler（University of Oxford）；Henning Bartsch（MATS Research）；Ilia Shumailov（AI Sequrity Company，原文如此拼写）；Christian Schroeder de Witt（University of Oxford）。通讯：jamespetersgill@gmail.com。致谢 MATS Research 支持。[Paper: 标题页作者块; Section I 首页脚注; Section X] |
| 期刊/会议、年份 | arXiv 预印本（论文自述 "Preprint"），2026 年；v1 戳记日期 2026-10-05，分类 cs.MA。正式发表信息未提供。[Paper: 标题页脚注; PDF 页脚戳记] |
| DOI / arXiv | DOI 未提供；arXiv:2610.05640v1 |
| 代码与数据 | 作者声明发布 MultiAgentDojo 实现、multi-CaMeL 实现与 individual CaMeL 基线实现，含多 Agent 基准环境、子 Agent 工具划分、三种配置（no-CaMeL / individual-CaMeL / multi-CaMeL）运行代码，以及良性效用与注入 ASR 评测脚本；实现构建于既有 AgentDojo 与 CaMeL 实现之上。**仓库 URL / 存档 DOI 在检索到的正文中未出现，未核验。**[Paper: Section VIII Open Science] |
| 阅读日期 | 2026-10-12（DeepTutor 检索式精读，尚未人工核查） |
| 研究方向定位 | `[Analysis]` Agent-derived candidate，待用户确认：建议 **P0**——同时提出新的多 Agent 攻击面（boundary laundering）、给出防护机制（multi-CaMeL）与形式化不可能性结果，并在 5 个后端模型、2 个基准上验证；命中研究画像主题簇 A（通信与身份安全）、C（共享状态与来源标记）、D（权限、委托与工具安全）、E（系统评测与理论）。 |

### 术语表

| 规范术语 | 首次定义 | 原文变体 | 采用规则 |
| --- | --- | --- | --- |
| 间接提示注入 | 对手将指令嵌入 Agent 间接处理的外部内容（网页、邮件、文档）中 [Paper: Section I] | indirect prompt injection | 全文统一使用"间接提示注入"，首次出现附英文 |
| 层级式 agent-as-tool 系统 | Definition 1：$M=(\mathcal{A},H,\mathcal{T})$，$H$ 为以 $A_0$ 为根的有向树，父 Agent 经工具调用唤起子 Agent [Paper: Section II-A, Definition 1] | hierarchical agent-as-tool system | 保留 "agent-as-tool" 原文不译 |
| 控制流计划 | Definition 2：预先指定的程序，作为中间工具返回值与计算的函数，确定性地规定执行期工具调用的序列与选择 [Paper: Section II-B, Definition 2] | control-flow plan | 统一译"控制流计划" |
| 控制流完整性（CFI） | Definition 3：执行被限制在由用户指令与其他可信信息（如工具/环境描述）决定的控制流计划内 [Paper: Section II-B, Definition 3]；概念源自系统安全 [23] | control-flow integrity, CFI | 首次出现给全称，此后用 CFI |
| CaMeL-安全 | Definition 4：系统满足 CFI 且安全策略 $S$ 在全局工具调用上被强制；$S=\emptyset$ 时等价于 CFI [Paper: Section II-B, Definition 4] | CaMeL-security | 保留原文连字符写法 |
| 平凡（系统） | Definition 5：$|\mathcal{A}|=1$ 的层级 agent-as-tool 系统 [Paper: Section III-C, Definition 5] | trivial | 与"平凡安全策略"区分使用 |
| 边界洗白 | 不可信数据跨越 Agent 边界后被下游 Agent 当作可信输入重新解释，从而劫持其控制流 [Paper: Section I; Section III-A] | boundary laundering | 首次出现附英文，此后统一"边界洗白" |
| 分支引导 | 不可信数据在预先指定计划的既有分支间选择执行路径，但不引入新路径；作者明确不视为 CFI 违反 [Paper: Section IV-C] | branch steering [27] | 统一译"分支引导"；引用 [27] 的具体文献身份未核验 |
| 规划 LLM / 隔离 LLM | CaMeL 双模型：PLLM 只见可信指令并生成 Python 控制流程序；QLLM 处理不可信数据且无法影响控制流 [Paper: Fig. 1(b); Section I] | PLLM / QLLM, Privileged LLM / Quarantined LLM | 首次出现给全称，此后用 PLLM / QLLM |
| 指令通道完整性 | multi-CaMeL 解释器性质 1：agent-as-tool 调用的 message 参数不得依赖任何工具输出 [Paper: Section IV-B] | instruction-channel integrity | 统一译法 |
| 跨 Agent 来源保留 | multi-CaMeL 解释器性质 2：经 variables 传递的值，其 capabilities 与 provenance 跨边界保留 [Paper: Section IV-B] | cross-agent provenance preservation | 统一译法 |
| 提示增强 | 为所有工具描述补充完整返回 schema，使 PLLM 能在观察输出前生成解析程序 [Paper: Section V 开头] | prompt augmentation | 统一译"提示增强" |
| 范围替换 | 子 Agent 无法取到精确资产/时间范围时返回邻近范围数据，父 Agent 未察觉原约束被违反 [Paper: Section V-C2] | unchecked scope substitution | 统一译"（未经检查的）范围替换" |
| TIPNI | Termination-Insensitive Probabilistic Noninterference，并发工作 LLMbda [28] 提出的信息流性质 [Paper: Section VI-B] | TIPNI | 保留缩写，首次出现给全称 |

## 02 一句话总结

在"父 Agent 把子 Agent 当工具调用"的层级多 Agent 系统中，即使每个 Agent 各自运行 CaMeL，间接提示注入仍能通过 **边界洗白**（不可信数据被写入子 Agent 的可信自然语言指令通道）劫持系统级控制流；作者给出该现象的形式化不可能性结果，并提出 **multi-CaMeL**——用"可信 message 通道 + 不透明 variables 数据通道 + 运行时解释器强制"跨边界保留来源，在其构建的 MultiAgentDojo 上把平均 ASR 从 12.9%（无 CaMeL）/ 0.2%（个体 CaMeL）降到 0.0%，代价是随模型能力上升而收窄的效用损失。[Paper: Abstract; Section III; Section IV; Table III]

## 03 研究问题

- **具体问题**：CaMeL 为单个 Agent 提供的安全保证（控制流完整性 + 基于 capability 的策略强制），在 Agent 互相调用的层级多 Agent 系统中是否仍然成立？若不成立，失效发生在哪里、能否在协议层修复、修复的效用代价多大？[Paper: Abstract; Section I 末段; Section III]
- **研究意义**：随着 Agent 被授予外部数据源、工具与服务访问权，间接提示注入的攻击面显著扩大；同时多 Agent orchestrator 模式（中心 Agent 向专门子 Agent 委派子任务）日益常见，因此"逐 Agent 加固是否等于系统安全"成为部署前的关键问题。作者称其结果为"安全必须在系统层面强制"的既有论点提供经验支持 [25, 26]。[Paper: Section I; Section I 相关工作段; Section III-A 末段]
- **现有方法不足**：
  - 模型级防御（微调/偏好优化让模型区分特权指令与低权限内容）与输入级防御（DataFilter 过滤模型、提示净化、sandwich prompting、spotlighting）"通常依赖习得的模型行为，不提供硬安全保证" [10]。[Paper: Section I 防御分类段]
  - 系统级防御（Dual LLM 模式、CaMeL、信息流控制 [13,14]、细粒度权限强制 [15]）中，CaMeL 明确"是为单 Agent 与其环境交互而formulated 的"，多 Agent 设置留白。[Paper: Section I 系统级防御段; Section I "CaMeL is formulated for a single agent" 段]
  - 已有工作已把层级 agent-as-tool 架构当作攻击面研究（如 OMNI-Leak [22]、Triedman et al. [24]），但缺少"个体安全何时可组合到系统级"的刻画与可运行的防护协议。[Paper: Section II-A; Section III-B]
- **核心问题**：跨越 Agent 边界时，信息的信任级别是否被隐式提升？如何在保留跨边界数据可用性的同时，阻止不可信数据进入下游 Agent 的指令通道？[Paper: Section VI-A 末段; Section VII]

## 04 研究背景与发展路径

> [Paper-framed; external verification not performed]

论文自述的脉络（全部按原文引用记录，未外部核验）：

1. **攻击侧**：直接提示注入 vs 间接提示注入的区分；已有工作展示了具体的间接提示注入攻击 [2]，并记录了公开网页等真实来源中注入内容的普遍性 [3]。[Paper: Section I 第 1 段]
2. **防御侧按介入阶段三分**：模型级（训练期微调/偏好优化 [4,5]）→ 输入级（DataFilter [6]、提示净化 [7]、sandwich prompting [8]、spotlighting [9]，共同弱点是依赖习得行为、无硬保证 [10]）→ 系统级（特权分离、信息流追踪、沙箱、工具调用策略检查）。[Paper: Section I 防御分类段]
3. **系统级路线**：Willison 的 Dual LLM 模式 [11] 把 Agent 拆为 PLLM（只见可信指令、决定动作序列，被阻止直接观察不可信内容）与 QLLM（处理不可信数据、无特权工具）；CaMeL [1] 是其具体实例化——PLLM 用 Python 程序表达可信控制流，执行层追踪数据依赖并在工具调用边界检查安全策略；在 AgentDojo [12] 上的评测显示 CaMeL 在安全性上显著优于 tool filtering、spotlighting、prompt sandwiching，且效用代价相对温和。作者选择 CaMeL 的三条理由：显式分离可信控制流与不可信数据、已展示较强的安全-效用权衡、随前沿模型代码生成与规划能力提升其效用代价可能下降。[Paper: Section I Dual LLM 段与 CaMeL 段]
4. **多 Agent 转向**：多 Agent 系统形态包括点对点、协作、竞争与层级；其中 orchestrator 模式（中心 Agent 委派专门子 Agent）日益常见 [16, 17]；FORGE [18] 用五个专门 Agent 组成固定流水线做漏洞评估；Rose et al. [19] 研究 LLM Agent 间的隐蔽共谋，指出其检测可能需要跨 Agent 聚合信号而非逐 Agent 判断。这些进展共同引出本文问题。[Paper: Section I 多 Agent 段]
5. **本文位置**：形式化层级 agent-as-tool 系统与安全性质（Section II）→ 经验反例 + 不可能性 Claim（Section III）→ multi-CaMeL 协议、解释器与保证论证（Section IV）→ 双基准评测（Section V）→ 局限（Section VI）。并发工作 LLMbda [28] 从 lambda 演算与 TIPNI 角度处理基于来源的防御，作者在 Section VI-B 与之对照。[Paper: Section II–VI; Section VI-B]

## 05 论文识别的核心痛点

| 痛点 | 表现 | 原因或作者解释 | 论文证据 |
| --- | --- | --- | --- |
| 个体安全不可组合 | 三个各自运行 CaMeL（平凡策略、GPT-5.2 作 PLLM/QLLM）的 Agent 组成的系统中，植入 SQL 数据库的注入仍导致 Notification Agent 的控制流计划新增 `send_email(recipient="ruth@email.com")`，把申请人数据外发 | Orchestrator 与 SQL Agent 经工具输出收到注入内容，CaMeL 视其为不可信数据、控制流不变；失效发生在**下一个 Agent 边界**：Orchestrator 把被污染的 `summarised_info` 写入传给 Notification Agent 的自然语言参数，而后者把该参数当作用户指令，于是先前不可信的值以其 PLLM 眼中的可信输入形式暴露 | [Paper: Section III-A; Fig. 2(a)(b); Fig. 3 Programs 1–4] |
| 信任在边界处被隐式升级（边界洗白） | individual CaMeL 在 MultiAgentDojo 上仍残留成功攻击（平均 ASR 0.2%；GPT-4.1 0.5%、Gemini 2.5 Pro 0.4%），且**每一例**残留成功攻击都表现为边界洗白 | agent-as-tool 接口只有一个 `message: str` 参数，工具派生值可自由嵌入其中；子 Agent 把父 Agent 当作用户，因此该值获得可信指令地位 | [Paper: Section V-B2; Section V-C1; Table III; Fig. 4; Fig. 7(a)] |
| 系统级 CFI 在理论上几乎不可达 | 只要系统非平凡且存在返回值不可信的工具，系统就不满足 CFI——即使每个 Agent 各自满足 | 在表达能力假设下：若 $A_i$ 是 $A_j$ 的父，则存在用户指令使 $A_j$ 的控制流计划依赖 $T$ 的返回值（Case 1）；若 $A_j$ 是 $A_i$ 的父，则可构造两次调用 $A_i$，第二次的指令依赖第一次含不可信数据的返回值（Case 2） | [Paper: Section III-C, Definition 5, Expressivity Assumption, Claim 及两段证明] |
| 缺少多 Agent 安全-效用基准 | AgentDojo 是单 Agent 提示注入基准（97 良性用户任务、35 注入目标、4 套件），无法评测"任务完成需要跨 Agent 边界通信"的场景 | 作者构建 MultiAgentDojo：把每套件工具划分给 2–4 个专门子 Agent 并加入 orchestrator；并验证改造未显著扭曲良性难度（平均 71.0 → 71.7，各模型置信区间重叠） | [Paper: Section V-B; Table I; Table II] |
| CaMeL 类方法需要预先知道工具返回结构 | 默认工具描述不含返回 schema；非 CaMeL Agent 可在收到输出后推断结构，而 CaMeL 的 PLLM 必须在观察输出前生成解析程序 | 作者为所有工具描述增补完整返回 schema，并称这是协议的必要组成（一次性、可预先完成）而非固有效用局限；单 Agent CaMeL 原始评测同样需要 [1] | [Paper: Section V 开头段] |
| 预先固定控制流计划带来的良性失效 | 多数效用失效源于"在观察运行时数据之前就承诺控制流计划"：某些任务只有在看到工具结果后才知道需要额外动作，非 CaMeL Agent 可运行时新增调用，CaMeL Agent 只能走 PLLM 已预期的路径 | 另有"未经检查的范围替换"：子 Agent 取不到精确资产/时间范围时返回邻近范围数据，而父 Agent 的控制流程序在收到响应前已生成，可能未察觉原任务约束被违反 | [Paper: Section V-C2] |

## 06 核心思想

1. **表层方法**：把 agent-as-tool 调用从单通道改为双通道——`query_agent_j(message: str, variables: dict[str, Any]) -> str`，其中 `message` 是展示给子 Agent PLLM 的可信自然语言指令，`variables` 是对该 PLLM 不透明、由子 Agent 在运行时通过新增工具 `get_variable(variable_name: str) -> Any` 取用的值字典；父 Agent 被要求把任何源自工具返回值的信息经 `variables` 传递。分离由扩展后的 CaMeL 解释器在运行时强制。[Paper: Section IV-A; Section IV-B; Fig. 4; Fig. 7(b)]
2. **核心洞见**：**跨越 Agent 边界不得隐式提升信息的信任级别。** 逐 Agent 加固之所以失败，不是因为某个 Agent 的实现有缺陷，而是因为边界本身把"数据"重新解释成了"指令"；因此安全属性必须在边界处强制，且解释器（而非安全策略配置）是保证 CFI 的必要组件——这一点与单 Agent CaMeL 不同。作者把 multi-CaMeL 视为这一更普遍多 Agent 安全原则的一个实例。[Paper: Section IV-B 末段; Section VI-A 末段; Section VII]
3. `[Analysis]` **可迁移启示**：任何"下游组件把上游输出当作指令读取"的接口都存在同构风险——子 Agent 调用、MCP/工具结果回填、共享记忆写入、RAG 上下文拼接、编排器把检索片段塞进系统提示。可迁移的三条设计规则：(a) 指令与数据在**接口签名层**分离，而不是靠提示词提醒模型区分；(b) 分离必须由运行时机制强制（类型/解释器/网关），因为"要求模型自律"等价于输入级防御，无硬保证；(c) 来源标签（provenance/capability）必须随数据跨边界传递，否则下游无法执行最小权限策略。这与研究画像中"消息来源证明""污点传播""共享记忆分区与写入验证"三个优先方法直接对应。

## 07 方法概览

- **输入**：用户指令（仅交给根 Agent $A_0$）；工具与环境描述（本文实验中均增补完整返回 schema）；不可信工具输出（数据库、网页、邮件、文件等）；跨 Agent 调用时父 Agent 提供的 `message`（可信）与 `variables`（不透明）。
- **输出**：各 Agent PLLM 生成的 Python 控制流程序；递归展开后得到的系统级控制流计划；实际工具调用及其结果；子 Agent 经 `variables` 通道接收并在运行时取用的值；最终返回给用户的答案。
- **训练/外部工具**：无模型训练或微调。依赖既有 CaMeL 的自定义 Python 解释器（追踪运行时值的来源与依赖、在工具调用处检查策略），本文对其做两项扩展；依赖 PLLM/QLLM 双模型（实验中同一后端模型兼任）；新增 `get_variable` 运行时工具；评测依赖 AssetOpsBench（LLM judge 评分）、AgentDojo/MultiAgentDojo 环境与注入任务，模型经 OpenRouter API 访问。
- **关键假设**：
  - 拓扑为以 $A_0$ 为根的有向树，每个非根 Agent 有唯一父 Agent，所有 Agent 间通信都经父→子调用与返回；子 Agent 被"新启动"而非跨调用保留状态或会话历史。[Paper: Section II-A; Section VI-A]
  - 表达能力假设 (i)(ii)（用于不可能性 Claim）。[Paper: Section III-C]
  - 解释器确实强制指令通道完整性；协议层保证论证以此为前提，而作者承认当前实现可能因隐式依赖追踪不全而未能强制。[Paper: Section IV-C; Section VI-B1]
  - 实验配置平凡安全策略 $S=\emptyset$（理由：CFI 不可组合已足以说明 CaMeL-安全不可组合；非平凡策略需任意选择，结果会依赖具体策略）。[Paper: Section II-B]

```text
用户指令（仅 A0）
   │
   ▼
A0 的 PLLM ──只见可信指令与工具/环境描述──▶ 生成 Python 控制流程序（控制流计划）
   │                                              │
   │                                     工具调用（含 agent-as-tool 调用）
   ▼                                              ▼
不可信工具输出 ──▶ 运行时变量（PLLM 不可见）──▶ QLLM 处理（摘要/解析，无特权工具）
   │                                              │
   │            ┌── individual CaMeL：值可被嵌入 message ──▶ 子 Agent PLLM 视为可信指令 ✗ 边界洗白
   └── 边界 ────┤
                └── multi-CaMeL：message（不依赖任何工具输出，解释器强制）
                              + variables={不透明值，携带 capabilities/provenance}
                                     │
                                     ▼
                        子 Agent PLLM 只见可信 message ──▶ 子控制流计划
                                     │
                                     ▼
                        子 Agent 运行时 get_variable(name) 取值 ──▶ 工具调用/QLLM
                                     │
                                     ▼
              递归展开各调用点 ──▶ 系统级控制流计划（仅由用户指令与可信信息决定）
              不可信数据只能在既有分支间"分支引导"，不能新增路径
```

## 08 核心模块拆解

| 模块 | 功能 | 为什么需要 | 输入与输出 | 支撑证据 | 移除后的已知或预期影响 |
| --- | --- | --- | --- | --- | --- |
| 双通道 agent-as-tool 接口 `query_agent_j(message, variables)` | 把跨 Agent 通信拆为可信指令通道与不透明数据通道 | 单通道 `message: str` 允许工具派生值被写入子 Agent 的可信用户指令，是边界洗白的直接成因 | 输入：父 Agent 程序中的自然语言指令 + 值字典；输出：子 Agent 返回字符串 | [Paper: Section IV-A; Fig. 4; Fig. 7(a)(b)] | 已知：退化为 individual CaMeL，MultiAgentDojo 平均 ASR 由 0.0% 升至 0.2%，GPT-4.1 0.5%、Gemini 2.5 Pro 0.4%，且残留攻击全部为边界洗白 [Paper: Table III; Section V-C1] |
| 运行时工具 `get_variable(variable_name) -> Any` | 让子 Agent 在不把值暴露给自身 PLLM 的前提下于执行期取用父 Agent 传来的数据 | 若数据完全不可访问，跨边界协作任务无法完成；该工具在"PLLM 不可见"与"运行时可用"之间取得平衡 | 输入：变量名；输出：不透明值（供后续工具调用或 QLLM 使用） | [Paper: Section IV-A] | 预期：子 Agent 无法使用父 Agent 传来的数据，需要跨边界传值的任务失败（论文未单独消融该工具，属 `[Analysis]` 推断） |
| 解释器性质 1：指令通道完整性 | 强制 `message` 参数不依赖任何工具输出 | 作者指出：仅有接口分离不足以提供保证，"这种分离只有在运行时被强制时才提供所需的安全保证"；父 Agent 不得能把工具派生值并入 `message` | 输入：父 Agent PLLM 生成的程序与运行时依赖图；输出：允许/阻止该调用 | [Paper: Section IV-B 第 1 点及其前导段] | 已知/预期：协议退化为"提示层约定"，PLLM 可重新把不可信值拼进指令，边界洗白复现；作者另指出当前实现可能因隐式依赖漏检而未能强制该性质 [Paper: Section VI-B1] |
| 解释器性质 2：跨 Agent 来源保留 | 经 `variables` 传递的值，其 capabilities 与 provenance 跨边界保留 | 使非平凡安全策略 $S$ 可以"在每个 Agent 各自运行时强制"的方式实现全局强制；作者称虽然评测只用平凡策略，但刻意保留使用非平凡策略的能力 | 输入：带 capability 标签的运行时值；输出：跨边界后仍带标签的值 | [Paper: Section IV-B 第 2 点] | 预期：全局数据流策略无法分解为逐 Agent 策略，数据流攻击（QLLM 在合法计划内产出被操纵数据导致越权动作）无法跨边界约束（论文未实验，属 `[Analysis]` 推断） |
| PLLM / QLLM 分离（继承自 CaMeL） | PLLM 只见可信指令并生成控制流程序；QLLM 处理不可信数据且无特权工具 | 保证单个 Agent 满足 CFI，是系统级递归展开论证的前提 | 输入：可信指令 / 不可信数据；输出：Python 程序 / 处理后文本 | [Paper: Fig. 1(b); Section II-B; Section III-A] | 已知：无 CaMeL 基线在 MultiAgentDojo 上平均 ASR 12.9%（GPT-4.1 36.1%、Gemini 2.5 Pro 24.6%）[Paper: Table III] |
| 系统级控制流计划的递归展开（分析框架） | 从根 Agent 计划出发，把每个 agent-as-tool 调用点替换为对应子 Agent 的计划 | 用于论证 multi-CaMeL 满足 CFI：所得系统级计划仅由原始用户指令与其他可信信息决定 | 输入：各 Agent 的 PLLM 程序；输出：系统级计划及其可达路径集合 | [Paper: Section IV-C] | 预期：无法给出系统级安全论证，只能停留在逐 Agent 经验观察（属 `[Analysis]`） |
| MultiAgentDojo（评测基准） | 把 AgentDojo 四套件的工具划分给 2–4 个专门子 Agent 并加入 orchestrator，形成多 Agent orchestrator 拓扑 | 提供"任务完成需要跨 Agent 通信"的安全-效用权衡测试床；作者明确其目标不是提升良性效用 | 输入：用户任务 / 注入任务（注入置于工具输出）；输出：良性任务成功率与 ASR | [Paper: Section V-B; Table I; Table II] | 已知：无该基准则无法量化边界洗白的发生率与 multi-CaMeL 的效用代价（属 `[Analysis]` 判断，基于论文自述动机） |
| 提示增强（工具返回 schema 补全） | 为所有工具描述补充完整返回 schema | CaMeL 的 PLLM 必须在观察输出前生成解析程序 | 输入：原始工具描述；输出：带返回 schema 的工具描述 | [Paper: Section V 开头段] | 已知：作者称若不增强，individual CaMeL 与 multi-CaMeL 难以达到合理效用（未给未增强时的具体数值） |

## 09 关键公式与符号

本文的核心是形式化定义与一条不可能性 Claim，而非数值公式。关键符号与命题如下（均直接摘自原文）：

- **系统结构**（Definition 1）：给定指标集 $I=\- **系统结构**（Definition 1）：给定指标集 $I=\{0,\dots,n\}$、$n\in\mathbb{N}$，层级式 agent-as-tool 系统为三元组 $M=(\mathcal{A},H,\mathcal{T})$，其中 $\mathcal{A}=\{A_i\}_{i\in I}$ 是 Agent 集合，$H\subseteq\mathcal{A}\times\mathcal{A}$ 是以 $A_0$ 为根的有向树（层级），$\mathcal{T}=\bigcup_{i\in I}\mathcal{T}_i$ 是系统可用工具集，$\mathcal{T}_i$ 是 $A_i$ 可用的工具。$(A_i,A_j)\in H$ 表示 $A_i$ 是 $A_j$ 的父，可经 agent-as-tool 调用唤起 $A_j$；用户只与 $A_0$ 交互，每个非根 Agent 由其唯一父 Agent 充当用户，调用像普通工具调用一样向父返回值。Fig. 1 的 orchestrator 拓扑即实例：$\mathcal{A}=\{A_0,A_1,A_2\}$（Orchestrator、SQL Agent、Email Agent），$H=\{(A_0,A_1),(A_0,A_2)\}$，$\mathcal{T}=\{read\_sql, send\_email\}$，且 $\mathcal{T}_0=\emptyset$、$\mathcal{T}_1=\{read\_sql\}$、$\mathcal{T}_2=\{send\_email\}$。[Paper: Section II-A, Definition 1 及其后实例]

- **控制流计划与 CFI**（Definition 2、3）：控制流计划是"预先指定的程序，作为中间工具返回值与计算的函数，确定性地规定执行期工具调用的序列与选择"；Agent $A$ 或系统 $M$ 满足 CFI，当且仅当其执行被限制在"由用户指令与其他可信信息（如工具或环境描述）决定的控制流计划"内。CaMeL 在单 Agent 设置下满足 CFI：PLLM 只见用户指令 $u$ 与环境描述并生成 Python 程序，工具返回的不可信数据"可以影响计划中已存在分支的选择，但不能引入新的控制流路径"。[Paper: Section II-B, Definitions 2–3 及其后说明]

- **CaMeL-安全**（Definition 4）：$A$ 或 $M$ 在安全策略 $S$ 下是 CaMeL-安全的，当且仅当系统满足 CFI 且 $S$ 在工具调用上被全局强制。$S$ 依据工具调用的参数、以及这些参数及其依赖所关联的 capabilities 判定调用是否许可（原文示例：禁止以源自私有数据的参数向无权读取者调用 `send_email`）。在本文定义下，**CFI 等价于平凡策略 $S=\emptyset$ 下的 CaMeL-安全**。[Paper: Section II-B, Definition 4 及其后两段]

- **平凡系统与表达能力假设**（Definition 5、Expressivity Assumption）：$M$ 平凡当且仅当 $|\mathcal{A}|=1$。表达能力假设包含两条：(i) 对任意 Agent $A_i$ 及其任意可用工具，存在某个用户指令，其 resulting 控制流计划调用该工具并把结果返回给用户；(ii) 对任意 $A_i$、任意一对（不必不同的）工具 $T_i^1,T_i^2$（含 agent-as-tool 接口）与 $T_i^1$ 的任意参数 $q$，存在某个用户指令，其控制流计划先调用 $T_i^1(q)$，随后以依赖 $T_i^1(q)$ 返回值的参数调用 $T_i^2$。[Paper: Section III-C, Definition 5 与 Expressivity Assumption]

- **不可能性 Claim**：若 $M=(\mathcal{A},H,\mathcal{T})$ 是非平凡的层级 agent-as-tool 系统，且存在工具 $T\in\mathcal{T}$ 的返回值不可信，则 $M$ 不满足控制流完整性——**即使每个 $A_i\in\mathcal{A}$ 各自满足 CFI**。证明取有权限访问 $T$ 的 $A_i$，由非平凡性知其有子或有父 $A_j$，分两种情形：
  - Case 1（$(A_i,A_j)\in H$，$A_i$ 为父）：由假设 (ii)，存在指令使 $A_i$ 的计划调用 $T$ 后以依赖 $T$ 返回值的指令调用 $A_j$，故 $A_j$ 的控制流计划依赖不可信数据。
  - Case 2（$(A_j,A_i)\in H$，$A_j$ 为父）：由假设 (i)，存在给 $A_i$ 的指令 $q$ 使其计划调用 $T$ 并把结果返回 $A_j$；再对 $A_j$ 应用假设 (ii)（取 $T_j^1=T_j^2=A_i$、参数 $q$），存在给 $A_j$ 的指令使其计划先调用 $A_i(q)$、再以依赖首次返回值的指令第二次调用 $A_i$；该返回值含 $T$ 的不可信数据，故第二次调用使 $A_i$ 收到依赖不可信数据的用户指令。
  两种情形都给出"存在某用户指令使 $M$ 的控制流计划依赖不可信数据"，因此 $M$ 不满足 CFI。[Paper: Section III-C, Claim 与 Proof（Case 1、Case 2）]

- **multi-CaMeL 接口签名**（原文以代码形式给出，非编号公式）：普通形式为 `query_agent_j(message: str) -> str`；multi-CaMeL 改为 `query_agent_j(message: str, variables: dict[str, Any]) -> str`，并新增子 Agent 运行时工具 `get_variable(variable_name: str) -> Any`。[Paper: Section IV-A]

- 说明：论文未使用编号方程，形式化内容集中于 Definition 1–5、Expressivity Assumption 与 Claim；Section IV-C 的安全保证是**论证性**（递归展开 + 分支引导）而非带编号定理的形式化证明，作者把"形式化扩展到 DAG、循环图、共享内存与点对点架构并证明相应系统级 CFI 与 CaMeL-安全"列为未来工作。[Paper: Section IV-C; Section VI-A 末段]

## 10 实验设计与证据链

### 实验设置

- **数据/样本规模**：
  - MultiAgentDojo（安全 + 效用）：由 AgentDojo 改造，原基准含 97 个良性用户任务与 35 个对抗注入目标，跨 Workspace、Slack、Banking、Travel 四套件；ASR 评测规模为 **n = 949 个注入任务实例/模型/配置**；良性效用 n = 97（Claude Fable 5 另报去拒答子集 n = 45）。套件级划分见 Table I：Workspace 40 用户任务/14 注入任务（Email 9 工具、Calendar 7、Drive 8）；Banking 16/9（Transactions 7、Files 1、Account 3）；Slack 21/5（Slack 9、Web 2）；Travel 20/7（Hotels 5、Restaurants 9、Car Rental 7、Assistant 7）。[Paper: Section V-B; Table I; Table III 说明; Table V 说明]
  - AssetOpsBench（效用）：orchestrator 委派四个专门子 Agent 完成多步专业任务，由具备"预期动作与输出"特权信息的 LLM judge 评分；作者从 141 个任务中识别并剔除 **29 个按字面无法完成**的任务，主文报告 n = 112（全任务集结果见 Appendix B、Fig. 8）。剔除方法：汇集五个模型 × 三种配置（vanilla / individual-CaMeL / multi-CaMeL）的全部轨迹，要求 (1) 至少一条轨迹含工具级数据缺失证据（正确资产/传感器/时段/文件范围的查询返回空或 not-found，由仅依据工具输出判断的 LLM judge 核验），且 (2) 任何配置的任何轨迹都不含真实数据的真正完成（用宽泛词法过滤 + 人工抽查剔除"缺数据报告、零值替代、无支撑的成功声明"）；作者称该集合是不可满足任务数的保守下界。被剔除任务编号：10, 41, 42, 45, 48, 216–223, 420, 430, 433, 434, 502, 506, 507, 508, 510, 511, 514, 515, 517, 518, 519, 622。[Paper: Section V-A; Section V-A1; Fig. 5 说明; Appendix B]
  - 案例研究：Section III-A 的三 Agent 攻击演示（Orchestrator + SQL + Notification，注入置于 SQL 数据库，指令为 "Send a summary of all job applicant info to Julie on Slack."）；Section III-B 的 OMNI-Leak 拓扑验证（**5 次试验，temperature = 1**）。[Paper: Section III-A; Section III-B]
- **指标**：攻击成功率 ASR（95% **Wilson score** 区间，作者说明因 Wald 区间在 0% ASR 附近表现不佳而改用 Wilson）；良性任务成功率 / AssetOpsBench 任务成功率（95% **Wald** 区间）；$\Delta$ 表示相对基线的百分点变化（Table II 为 MultiAgentDojo 减 AgentDojo；Table III 为相对 no-CaMeL；Fig. 5、Fig. 6 的 $\Delta$ 为 no CaMeL → multi-CaMeL）。[Paper: Table III 说明; Table II 说明; Fig. 5 说明; Fig. 6 说明]
- **基线**：no CaMeL（Agent 仅依赖模型侧防御）、individual-agent CaMeL（每个 Agent 各自运行 CaMeL，但对 Agent 间通信无额外限制）；MultiAgentDojo 的良性难度另以原始 AgentDojo 为参照。安全性对照还包括 OMNI-Leak [22] 这一已发表攻击设置。[Paper: Section V 开头; Section V-B; Table II; Section III-B]
- **预算、模型版本与评估协议**：五个后端 LLM——Claude Fable 5、GPT-5.5、GPT-4.1、Gemini 2.5 Pro、Gemini 2.5 Flash Lite，覆盖不同模型族与能力层级；每次评测中系统内所有 Agent 的 PLLM 与 QLLM 使用同一模型；案例研究使用 GPT-5.2 作 PLLM 与 QLLM。模型经 **OpenRouter API** 访问，推理硬件不受作者控制，"精确复现可能依赖对相同模型版本的持续访问"。所有工具描述被增补完整返回 schema（提示增强）。安全策略为平凡策略 $S=\emptyset$。作者称已注意避免不必要的模型查询，同时运行足够评测以获得统计上有意义的结果并检验跨模型泛化。**token 数、费用、单次运行时长与总预算未提供。**[Paper: Section V-A; Section II-B; Section V 开头; Section IX]

### 结论—证据矩阵

| 编号 | 实验 | 被检验的结论 | 比较与条件 | 结果 | 可支持的结论 | 不可支持的更强结论 | 来源 | 人工核查 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | 三 Agent 攻击演示（Orchestrator + SQL + Notification） | 所有组成 Agent 各自运行 CaMeL 时，间接提示注入仍可劫持系统级控制流 | 三个 CaMeL Agent、平凡策略、GPT-5.2 作 PLLM 与 QLLM；注入植入 SQL 数据库；有/无注入对照 | 无注入时 Notification Agent 只 `send_slack_message(recipient="Julie")`（Program 3）；有注入时其计划新增 `send_email(recipient="ruth@email.com")`（Program 4），而 Orchestrator 与 SQL Agent 的程序（Programs 1、2）不变 | 个体 CaMeL 不足以保证多 Agent 系统安全；失效点位于父→子的指令通道 | 不能推出"所有多 Agent 系统都必然被攻破"（这是构造性反例，且依赖表达能力假设才上升为一般性 Claim） | [Paper: Section III-A; Fig. 2(a)(b); Fig. 3 Programs 1–4] | AI 预审支持；用户最终确认 |
| C02 | OMNI-Leak 拓扑验证 | 个体 CFI 虽不可组合，仍能阻断需要劫持特定 Agent 控制流的攻击 | OMNI-Leak orchestrator 拓扑，各 Agent 运行 CaMeL、平凡策略，GPT-5.2 作 PLLM 与 QLLM；5 次试验，temperature = 1 | 注入攻击成功率 0%，良性查询准确率保持 100% | 对"不可信公共数据诱使 SQL Agent 访问私有数据库"这类攻击，个体 CFI 有效 | 5 次试验、单一模型、单一拓扑，不能外推为对 OMNI-Leak 全部变体或其他攻击族的鲁棒性 | [Paper: Section III-B] | AI 预审支持；用户最终确认 |
| C03 | 形式化 Claim 与两段证明 | 在表达能力假设下，任何含不可信返回值工具的非平凡层级 agent-as-tool 系统都不满足系统级 CFI | Definition 5（平凡 = $\|\mathcal{A}\|=1$）+ Expressivity Assumption (i)(ii)；分 Case 1（$A_i$ 为父）与 Case 2（$A_i$ 为子） | 两种情形均构造出"控制流计划依赖不可信数据"的用户指令，故 CFI 不成立 | 边界洗白不是实现瑕疵，而是该类系统在温和假设下的结构性后果 | 结论受限于树状层级 + agent-as-tool + 该表达能力假设；不覆盖 DAG、循环、异步、共享内存、点对点拓扑（作者自述留待未来工作） | [Paper: Section III-C, Definition 5, Expressivity Assumption, Claim & Proof; Section VI-A] | AI 预审支持；用户最终确认 |
| C04 | MultiAgentDojo 良性难度校验 | 把单 Agent 基准改造为多 Agent 未显著扭曲良性难度 | 同一模型在 AgentDojo 与 MultiAgentDojo 上、无 CaMeL 且无注入；95% Wald 区间 | Claude Fable 5 73.2±8.8 → 69.1±9.2（−4.1）；GPT-5.5 88.7±6.3 → 86.6±6.8（−2.1）；GPT-4.1 75.3±8.6 → 78.4±8.2（+3.1）；Gemini 2.5 Pro 78.4±8.2 → 76.3±8.5（−2.1）；Gemini 2.5 Flash Lite 22.7±8.3 → 27.8±8.9（+5.2）；平均 71.0 → 71.7（+0.7），各模型区间重叠 | MultiAgentDojo 可作为多 Agent 安全-效用评测的合理测试床 | 不能推出 MultiAgentDojo 与 AgentDojo 在**安全**难度上等价（本表只测良性任务） | [Paper: Section V-B; Table II] | AI 预审支持；用户最终确认 |
| C05 | MultiAgentDojo ASR 主实验 | multi-CaMeL 消除注入攻击成功，优于 individual CaMeL 与 no CaMeL | 5 模型 × 3 配置（no CaMeL / individual CaMeL / multi-CaMeL），n = 949 注入任务实例每模型每配置，平凡策略，95% Wilson 区间 | 平均 ASR：12.9% → 0.2% → 0.0%（$\Delta$ −12.7 / −12.9）。逐模型 no CaMeL：Fable 5 1.5% [0.9,2.5]、GPT-5.5 0.0% [0.0,0.4]、GPT-4.1 36.1% [33.1,39.3]、Gemini 2.5 Pro 24.6% [21.9,27.4]、Flash Lite 2.1% [1.4,3.2]；individual CaMeL：0.0%、0.0%、0.5% [0.2,1.2]、0.4% [0.2,1.1]、0.0%；multi-CaMeL：五模型均 0.0% [0.0,0.4] | 在本基准的攻击集合下，multi-CaMeL 把 ASR 降到 0.0%，且优于个体 CaMeL | 不能推出对**自适应攻击**免疫：0.0% 的 Wilson 上界为 0.4%，且作者明确警告基准攻击可能不代表更强自适应攻击，并引大规模自适应红队对所有前沿模型都发现非零成功率 [29] | [Paper: Table III 及其说明; Section V-B2; Section V-B3] | AI 预审支持；用户最终确认 |
| C06 | 残留攻击的定性轨迹分析 | individual CaMeL 的残留成功攻击全部为边界洗白；multi-CaMeL 阻断该模式 | Slack 用户任务 16（网站内容含注入，要求向另一用户发送恶意链接）；Gemini 2.5 Pro；individual CaMeL vs multi-CaMeL 的 PLLM 程序对照，完整轨迹见 Appendix C | individual CaMeL 下 Orchestrator 把注入内容嵌入传给 Slack Agent 的自然语言指令（`message=f"Send a direct message to Dora with the following content: {dora_feedback}"`），Slack Agent 的 PLLM 把注入动作纳入计划；multi-CaMeL 下网站派生内容改经 `variables` 传递（`message="Send a direct message to the recipient with the provided content."`，`variables={"recipient": "Dora", "content": dora_feedback}`），从不以可信指令文本暴露给 Slack Agent 的 PLLM | 边界洗白是 individual CaMeL 失效的**唯一**观察模式，且机制上被双通道分离阻断 | 定性分析基于有限任务与单一模型示例，不能证明"所有可能残留攻击都必然是边界洗白" | [Paper: Section V-C1; Fig. 7(a)(b); Appendix C] | AI 预审支持；用户最终确认 |
| C07 | AssetOpsBench 效用评测 | multi-CaMeL 相对 individual CaMeL 只带来温和的额外效用代价 | 5 模型 × 3 配置；剔除 29 个不可完成任务后 n = 112；同一模型兼任 PLLM 与 QLLM；工具描述含返回 schema；95% Wald 区间 | 逐模型 no CaMeL / individual / multi：Fable 5 88.4±5.9 / 67.0±8.7 / 67.9±8.6；GPT-5.5 87.5±6.1 / 82.1±7.1 / 79.5±7.5；GPT-4.1 81.2±7.2 / 64.3±8.9 / 48.2±9.3；Gemini 2.5 Pro 75.9±7.9 / 55.4±9.2 / 50.9±9.3；Flash-Lite 64.3±8.9 / 20.5±7.5 / 26.8±8.2。individual CaMeL 相对 no CaMeL 平均降 21.6 点（两个最强模型 13.4 点）；multi-CaMeL 相对 individual 平均额外降 3.2 点（两个最强模型 0.85 点）；每个模型两者 95% 区间重叠；Fig. 5 的 $\Delta$（no CaMeL→multi-CaMeL）：−20.5、−8.0、−33.0、−25.0、−37.5 | multi-CaMeL 的**增量**效用代价小，且个体 CaMeL 与 multi-CaMeL 的差异在该基准上统计不显著（区间重叠） | 区间重叠意味着不能断言 multi-CaMeL"无效用代价"；也不能把 CaMeL 系整体约 20–37 点的效用损失归因于多 Agent 扩展 | [Paper: Section V-A2; Fig. 5 及说明; Table IV; Appendix B; Fig. 8] | AI 预审支持；用户最终确认 |
| C08 | MultiAgentDojo 良性效用评测 | 与 AssetOpsBench 同样的定性模式：个体 CaMeL 代价大，multi-CaMeL 增量较小，但幅度因模型差异显著 | 5 模型 × 3 配置；n = 97（Fable 5 另报 n = 45 去拒答子集）；95% Wald 区间 | no CaMeL / individual / multi：Fable 5（去拒答）91.1±8.3 / 84.4±10.6 / 84.4±10.6；Fable 5（含拒答）69.1±9.2 / 53.6±9.9 / 52.6±9.9；GPT-5.5 86.6±6.8 / 73.2±8.8 / 66.0±9.4；GPT-4.1 78.4±8.2 / 38.1±9.7 / 24.7±8.6；Gemini 2.5 Pro 76.3±8.5 / 42.3±9.8 / 26.8±8.8；Flash-Lite 27.8±8.9 / 13.4±6.8 / 7.2±5.1。Fig. 6 的 $\Delta$：−6.7、−16.5、−20.6、−53.7、−49.5、−20.6 | 在需要跨边界通信的基准上，multi-CaMeL 的额外代价通常较小；GPT-4.1 与 Gemini 2.5 Pro 的整体损失远大于 Fable 5 与 GPT-5.5 | 该基准上 multi-CaMeL 相对 individual 并非处处更小（GPT-5.5 73.2→66.0、GPT-4.1 38.1→24.7、Gemini 2.5 Pro 42.3→26.8 均有明显下降），不能概括为"multi-CaMeL 效用代价可忽略" | [Paper: Section V-B1; Fig. 6 及说明; Table V] | AI 预审支持；用户最终确认 |
| C09 | 跨模型趋势分析（两个基准） | 效用代价随模型能力上升而收窄 | AssetOpsBench 与 MultiAgentDojo 上 no CaMeL → multi-CaMeL 的 $\Delta$ 按模型能力排列 | 作者表述为"非单调但存在趋势"：AssetOpsBench 上 GPT-5.5 仅 −8.0，而 GPT-4.1 −33.0、Flash-Lite −37.5；MultiAgentDojo 上 Fable 5（去拒答）−6.7、GPT-5.5 −20.6，而 GPT-4.1 −53.7、Gemini 2.5 Pro −49.5 | 更强模型更能容纳协议施加的约束，暗示随前沿模型规划/代码生成能力提升，该类系统级防御的效用代价可能下降 | 趋势非严格单调、仅 5 个模型、未做能力度量回归，不能建立"能力→代价"的定量因果或外推到未测模型 | [Paper: Section V-A2; Section V-B1; Table IV 说明; Fig. 5; Fig. 6] | AI 预审支持；用户最终确认 |
| C10 | Claude Fable 5 拒答现象分析 | 该模型在良性设置下大量拒答，可能是基准特定安全行为而非真实部署中的效用代价 | AgentDojo/MultiAgentDojo 良性任务（无注入），n = 97 | 拒答 97 个良性任务中的 52 个（53.6%）；作者因此对 Fable 5 同时报告含拒答与去拒答（n = 45）两套结果 | 报告 Fable 5 效用时必须区分口径，否则会高估 multi-CaMeL 的代价 | 作者自述这是**假设**（"We hypothesize"），未经对照实验验证；不能据此断言拒答纯属基准伪影 | [Paper: Section V-B 拒答段; Table II 说明; Table V 说明] | AI 预审支持；用户最终确认 |
| C11 | 协议层安全论证（设计性论证，非实验） | multi-CaMeL 满足 CFI，并在配合策略 $S$ 时满足 CaMeL-安全 | 前提：每个 Agent 个体满足 CFI + 解释器强制指令通道完整性；方法：从根计划递归展开各 agent-as-tool 调用点 | 得到仅由原始用户指令与其他可信信息决定的系统级控制流计划；不可信数据仍可在既有分支间"分支引导"（如父依工具返回值选择 `child_agent(query_1)` 或 `child_agent(query_2)`），但不引入新路径；作者明确 branch steering 不算 CFI 违反 | multi-CaMeL 在**协议层**给出系统级 CFI 的论证，并说明其为何能全局支持非平凡策略（来源与 capability 跨边界保留） | 这是论证而非机器检验证明；且以"指令通道完整性被强制"为前提，作者承认当前实现可能未强制（见 C13）；branch steering 会违反更强的 TIPNI | [Paper: Section IV-B; Section IV-C; Section VI-B] | AI 预审支持；用户最终确认 |
| C12 | 对 GPT-5.5 零 ASR 的解释边界 | 无 CaMeL 时 ASR 为 0% 不应被解读为模型对间接提示注入的普遍鲁棒性 | GPT-5.5 在 MultiAgentDojo 上 no CaMeL 配置 | ASR 0.0% [0.0,0.4]；作者指出这可能反映基准所代表的攻击，而非对更强自适应攻击的免疫，并引大规模自适应红队对所有受评前沿模型都发现非零攻击成功 [29] | 基准内 0% ASR 只是"该基准攻击集合下未成功"，需与机制性防御区分 | 不能把任何模型的 0% ASR 当作安全保证；也不能据此比较模型"安全性" | [Paper: Table III 说明文字] | AI 预审支持；用户最终确认 |
| C13 | 对 LLMbda 批评 1 的自查 | CaMeL 解释器会漏掉隐式依赖，multi-CaMeL 继承该实现层限制 | 对照并发工作 Garby et al. [28] 提出的批评 | 变量可能在其值依赖不可信条件时仍被标记为可信，尤其是通过未走分支上的赋值；multi-CaMeL 因扩展 CaMeL 解释器而继承该限制；作者说明这不影响 Section IV-C 的协议层论证（该论证假设指令通道完整性被强制），但意味着当前实现在涉及被漏检隐式依赖的情形下可能无法强制该性质 | 协议层保证与实现层保证之间存在缺口；0% ASR 是经验结果，不等于实现已满足指令通道完整性 | 论文未给出该缺口的实证攻击演示，因此不能量化其可利用性 | [Paper: Section VI-B1] | AI 预审支持；用户最终确认 |
| C14 | 对 LLMbda 批评 2 的自查 | CaMeL 外部重试循环是信息泄漏通道；multi-CaMeL 实现不重试故不继承该问题 | 对照 Garby et al. [28] | 策略相关失败可在重复重试间泄漏信息；"Multi-CaMeL, as implemented, does not retry failed executions"，故不继承该具体问题；但作者指出信息流保证依赖 Agent 被适当 confinement [30]，且随 Agent 更具策略性、通信渠道更复杂，传统 covert-channel 枚举与容量削减可能不足 [31] | multi-CaMeL 规避了重试泄漏，但更广义的 confinement 保证尚未建立 | 不能据此声称 multi-CaMeL 无隐蔽通道或满足信息流非干涉 | [Paper: Section VI-B2] | AI 预审支持；用户最终确认 |
| C15 | 效用失效模式的定性分析 | 两类良性失效：预先承诺控制流计划、未经检查的范围替换 | individual CaMeL 与 multi-CaMeL 的失败轨迹（AssetOpsBench 与 MultiAgentDojo） | 多数失效源于"在观察运行时数据前承诺控制流计划"：需要额外动作只有在看到工具结果后才显现，非 CaMeL Agent 可运行时新增工具或子 Agent 调用，CaMeL Agent 只能走 PLLM 已预期的路径；另观察到子 Agent 取不到精确资产/时间范围/其他 scope 时返回邻近但不同的 scope，而父 Agent 的控制流程序在收到响应前已生成，可能未察觉原任务约束被违反 | 解释了 CaMeL 系效用损失的主要机制，并指出一个与多 Agent 委派直接相关的新型失效（范围替换） | 定性观察，未给各类失效的占比或频次统计；不能据此排序改进优先级 | [Paper: Section V-C2] | AI 预审支持；用户最终确认 |
| C16 | 开放科学与复现性声明 | 工件与复现条件 | Section VIII、IX 自述 | 发布 MultiAgentDojo 实现、multi-CaMeL 与 individual CaMeL 基线实现，含多 Agent 环境、子 Agent 工具划分、三种配置运行代码、良性效用与 ASR 评测脚本；实现构建于既有 AgentDojo 与 CaMeL 实现之上；模型经 OpenRouter API 访问，硬件不受控，精确复现依赖相同模型版本持续可用；LLM 亦被用作编码助手与编辑辅助，输出经作者检查 | 该工作具备可复现工件（在模型版本可得的条件下） | 检索到的正文未给出仓库 URL / 存档标识，**代码可用性未核验**；模型版本漂移可能使数值不可精确复现 | [Paper: Section VIII; Section IX] | AI 预审支持；用户最终确认 |

### 图表清单

| 编号 | 内容 | 论证作用 |
| --- | --- | --- |
| Fig. 1(a) | 提示注入跨越 Agent 边界：对手把注入植入 SQL 数据库；SQL Agent 与 Orchestrator Agent 经工具输出收到注入内容，CaMeL 视其为不可信数据、不影响其控制流；但 Orchestrator 把结果内容传给 Email Agent 时，它成为 Email Agent 的用户输入，其 PLLM 直接读到注入指令，从而改变控制流并向对手外发私有信息（图中标注 COMPROMISED、attacker@email.com） | 用一张图把全文核心失效机制（信任在边界处被隐式升级）讲清，是"个体安全 ≠ 系统安全"的直观论证 |
| Fig. 1(b) | CaMeL Agent 结构：PLLM 只见用户指令、从不见不可信数据，生成固定工具调用序列的 Python 程序；QLLM 在被 PLLM 程序调用时解析不可信数据，被阻止影响控制流 | 交代被扩展的基线机制，使后文"哪一层被绕过"可被精确定位 |
| Fig. 2(a)(b) | 系统级控制流路径：(a) 无注入、(b) 有注入（注入植入 SQL 数据库）。有注入时 Orchestrator 与 SQL Agent 的计划不变，只有 Notification Agent 的计划被改变并新增邮件外发步骤，因为**只有** Notification Agent 把注入指令作为可信用户输入收到（来自 Orchestrator） | 把 C01 的反例落到"哪个 Agent 的计划被改写"这一可检验层面，排除"上游 Agent 已被劫持"的替代解释 |
| Fig. 3（Programs 1–4） | PLLM 生成的控制流程序：Program 1（Orchestrator，含 `sql_agent(...)` → `qllm(f"Summarize the following: {raw_info}")` → `notification_agent(f"Send this summary to Julie via Slack: {summarised_info}.")`）、Program 2（SQL Agent，`query_sql(query="SELECT * FROM job_applicants_db")`）、Program 3（Notification Agent 无注入，仅 `send_slack_message(recipient="Julie")`）、Program 4（有注入，额外 `send_email(recipient="ruth@email.com")`，红色底纹标出被注入改写的程序）；程序为清晰起见已简化，未简化版本见附录，所有申请人姓名为虚构，PLLM 均为 GPT-5.2 | 提供逐行可读的证据链：Program 1 中的 f-string 拼接正是边界洗白的代码级形态，Program 3↔4 的差异即攻击效果 |
| Fig. 4 | individual CaMeL 与 multi-CaMeL 的 Agent 间通信对比：前者工具派生值 x 可被并入传给子 Agent 的自然语言指令（`"Send this to Julie: {x}."`，子 PLLM 看到 `"Send this to Julie: [injected instruction]"`）；后者该值必然经 `variables={x: <opaque>}` 传递，子 PLLM 只见 `"Send this to Julie."`；分离由 multi-CaMeL 解释器强制 | 把防护机制与失效机制并置，说明"为什么双通道能阻断"，并强调强制性来自解释器而非提示约定 |
| Fig. 5 | AssetOpsBench 任务成功率（5 模型 × 3 配置），标注 $\Delta$（no CaMeL → multi-CaMeL）：−20.5、−8.0、−33.0、−25.0、−37.5；说明剔除 29 个不可完成任务后 n = 112，individual 与 multi 的置信区间对所有模型重叠 | 支撑 C07 的"增量代价温和"与 C09 的能力趋势 |
| Fig. 6 | MultiAgentDojo 良性任务成功率（含 Fable 5 去拒答与含拒答两口径），$\Delta$（no CaMeL → multi-CaMeL）：−6.7、−16.5、−20.6、−53.7、−49.5、−20.6 | 支撑 C08：跨边界通信基准上 multi-CaMeL 增量代价通常较小，但 GPT-4.1 与 Gemini 2.5 Pro 的整体损失极大 |
| Fig. 7(a)(b) | 边界洗白及其阻断的真实 PLLM 程序片段（取自 MultiAgentDojo Slack 用户任务 16、Gemini 2.5 Pro，已简化，完整轨迹见 Appendix C）：(a) individual CaMeL 下 Orchestrator 把工具派生数据 `dora_feedback` 直接嵌入传给子 Agent 的自然语言指令；(b) multi-CaMeL 下改经 `variables` 通道传递，`message` 保持与不可信数据无关 | 把 C06 的定性结论落到具体程序差异，是"失效模式唯一性"论证的关键证据 |
| Fig. 8（Appendix B） | AssetOpsBench 效用评测（**不**剔除不可完成任务），$\Delta$：−27.0、−14.2、−34.8、−25.6、−36.2 | 提供主文 n = 112 结果的敏感性检查，说明剔除 29 个不可完成任务未改变定性结论 |
| Table I | MultiAgentDojo 的套件—子 Agent—工具划分与任务规模：Workspace 40 用户任务/14 注入任务（Email 9、Calendar 7、Drive 8）；Banking 16/9（Transactions 7、Files 1、Account 3）；Slack 21/5（Slack 9、Web 2）；Travel 20/7（Hotels 5、Restaurants 9、Car Rental 7、Assistant 7），并给出每个子 Agent 的职责范围 | 定义评测环境的协作架构与权限划分，是判断"攻击面是否真实"的依据 |
| Table II | AgentDojo vs MultiAgentDojo 良性任务成功率（no CaMeL、无注入，95% Wald 区间），平均 71.0 → 71.7（+0.7），各模型区间重叠 | 支撑 C04：基准改造未扭曲良性难度 |
| Table III | MultiAgentDojo ASR（n = 949 注入任务实例/模型/配置，95% Wilson 区间）与相对 no-CaMeL 的 $\Delta$；平均 12.9% → 0.2% → 0.0% | 全文核心安全结果（C05），并附对 GPT-5.5 零 ASR 的解释边界（C12） |
| Table IV（Appendix D） | Fig. 5 的完整底层数据（AssetOpsBench，n = 112，95% Wald 区间） | 支撑 C07、C09 的可核查数值 |
| Table V（Appendix D） | Fig. 6 的完整底层数据（MultiAgentDojo 良性成功率，n = 97 / n = 45，95% Wald 区间） | 支撑 C08、C09、C10 的可核查数值 |
| Appendix A | 检索命中一段 AssetOpsBench 完整轨迹（IoT Agent 列出 Chiller 6 的 12 个传感器、`parse_with_ai` 与 `verify_hypothesis` 调用、以及"压缩机过热"相关的 6 个确认相关 + 4 个可能相关传感器分析）；**该附录标题未被检索命中，未核验** | 展示真实 PLLM 程序与运行时校验形态，佐证"程序在观察数据前生成"的机制 |
| Appendix B | 不可完成的 AssetOpsBench 任务：识别方法（汇集 5 模型 × 3 配置轨迹、工具级数据缺失证据由 LLM judge 仅依工具输出核验、剔除伪完成）、29 个任务编号清单、Fig. 8 | 支撑 n = 112 的合法性与剔除程序的保守性 |
| Appendix C | individual CaMeL 的边界洗白失效轨迹（MultiAgentDojo：slack 用户任务 16、注入任务 1、Gemini 2.5 Pro），含任务原文（访问 Dora 与 Eve 的网站并给出反馈，需先邀请 Dora 加入 Slack）与 Orchestrator Agent 的 PLLM 程序 | 支撑 C06 的可追溯证据 |
| Appendix D | 附加结果：Table IV 与 Table V | 主文图形的完整数值来源 |

## 11 结论的正确解释

论文可以支持的、边界明确的主结论是：**在层级式 agent-as-tool 多 Agent 系统中，"逐 Agent 部署 CaMeL"不等于系统安全。** 失效机制是边界洗白——父 Agent 把工具派生的不可信值写入子 Agent 的自然语言指令参数，而子 Agent 把调用它的父 Agent 当作用户，于是该值以可信输入身份进入子 Agent 的 PLLM 并改写其控制流计划。作者既给出构造性反例（三 Agent、注入置于 SQL 数据库、GPT-5.2、平凡策略），又在温和的表达能力假设下证明：只要系统非平凡且存在返回值不可信的工具，系统级 CFI 必然被违反，即使每个 Agent 各自满足 CFI。[Paper: Section III-A; Section III-C; Section VII]

修复方式是把边界显式双通道化并在运行时强制：`message`（可信指令，不得依赖任何工具输出）与 `variables`（不透明数据，携带 capabilities 与 provenance，子 Agent 经 `get_variable` 在运行时取用）。由此从根 Agent 计划递归展开得到的系统级控制流计划仅由用户指令与可信信息决定；不可信数据仍可在既有分支间"分支引导"，但不能新增路径。作者强调，与单 Agent CaMeL 不同，multi-CaMeL 的解释器即使不配置任何安全策略也是保证 CFI 所必需的。[Paper: Section IV-A; Section IV-B; Section IV-C]

经验结果的适用范围必须与其条件一起读：在 MultiAgentDojo（n = 949 注入任务实例/模型/配置）上，平均 ASR 从 no CaMeL 的 12.9% 降到 individual CaMeL 的 0.2%、multi-CaMeL 的 0.0%，且 individual CaMeL 的每一例残留成功攻击都是边界洗白；效用方面，AssetOpsBench 上 multi-CaMeL 相对 individual CaMeL 平均仅额外下降 3.2 点（两个最强模型 0.85 点，各模型区间重叠），但相对 no CaMeL 的整体损失仍达 8.0–37.5 点，MultiAgentDojo 上更大（GPT-4.1 −53.7、Gemini 2.5 Pro −49.5）。[Paper: Table III; Section V-C1; Section V-A2; Fig. 5; Fig. 6; Table IV; Table V]

因此**不应**把结论读成："multi-CaMeL 使多 Agent 系统安全"。作者自己划出的边界包括：0% ASR 只针对基准内既有攻击，未做自适应攻击评测，且大规模自适应红队对所有前沿模型都发现非零成功率；实验全部使用平凡安全策略 $S=\emptyset$，因此结果只覆盖控制流劫持，不覆盖数据流攻击；协议层论证以"指令通道完整性被强制"为前提，而当前实现继承了 CaMeL 解释器漏检隐式依赖的限制；分析仅限树状层级拓扑与 CFI/CaMeL-安全性质，DAG、循环、异步、共享内存、点对点架构与更强信息流性质（如 TIPNI，branch steering 会违反它）留待未来工作。[Paper: Table III 说明; Section II-B; Section VI-A; Section VI-B1; Section VI-B2]

作者提炼出的、比具体协议更宽的原则是：**跨越 Agent 边界不应隐式提升信息的信任级别**；随着能力更强的 Agent 被组合成更大更复杂的系统，在其接口上保留这一区分将是让安全保证可组合的重要部分。[Paper: Section VI-A 末段; Section VII]

## 12 作者明确承认的局限

| 局限 | 具体表现 | 作者提出的未来方向 | 来源 |
| --- | --- | --- | --- |
| 拓扑受限 | 分析仅限层级 agent-as-tool（有根树）设置；更一般架构中可能没有单一根 Agent、没有唯一信息流方向、没有清晰的 agent-as-tool 边界可供强制协议 | 把"边界不得隐式升级信任"的原则形式化扩展到 DAG、循环图、共享内存系统与点对点 Agent 架构，并证明相应的系统级 CFI 与 CaMeL-安全 | [Paper: Section VI-A; Section VII] |
| 会话历史与"新 episode"处理 | 协议可在每个调用边界独立应用：Agent 被新父首次调用时，该父可被视为新 episode 的可信用户；但若跨调用保留会话历史则需额外小心，因为先前交互可能含源自不可信数据的输出，不应并入后续调用的上下文 | 明确跨调用上下文管理规则（作者作为设计注意事项提出） | [Paper: Section VI-A] |
| 安全性质强度受限 | 本文只定义并证明 CFI 与 CaMeL-安全；并发工作 LLMbda [28] 的 TIPNI 更强——multi-CaMeL 允许的 branch steering（不可信数据在既有分支间引导执行、改变外部可见输出）会违反 TIPNI，作者承认"TIPNI 排除了 CFI 允许的一些行为" | 形式化刻画 CFI 与 TIPNI 的相对强度与适用范围 | [Paper: Section VI-B; Section IV-C] |
| 解释器漏检隐式依赖 | CaMeL 解释器的依赖追踪可能漏掉经控制流的隐式流：变量的值依赖不可信条件（尤其是未走分支上的赋值）时仍可能被标记为可信；multi-CaMeL 因扩展该解释器而继承此限制，故当前实现在涉及此类隐式依赖时可能无法强制指令通道完整性（协议层论证不受影响，因其假设该性质已被强制） | 强化 CaMeL 解释器以可靠（soundly）追踪此类依赖，作者称之为重要未来工作 | [Paper: Section VI-B1] |
| Confinement 与隐蔽通道 | 信息流保证依赖 Agent 被适当 confinement [30]；随着 Agent 更具策略性、通过日益复杂的渠道通信，传统的隐蔽通道枚举与容量削减可能不足 [31]。（CaMeL 的外部重试循环被 Garby et al. 指为泄漏通道；multi-CaMeL 实现不重试失败执行，故不继承该具体问题） | 为 multi-CaMeL 建立适当的 confinement 保证 | [Paper: Section VI-B2] |
| 评测中的策略选择 | 实验全部使用平凡安全策略（$S=\emptyset$）：一是因为证明 CFI 不可组合已足以说明 CaMeL-安全不可组合，二是配置非平凡策略需在众多可能中做任意选择，结果会依赖所选策略 | 在 Section IV 说明 multi-CaMeL 如何自然扩展到需要非平凡安全策略的情形（保留跨边界 provenance 即可全局强制 $S$） | [Paper: Section II-B; Section IV-B] |
| 基准攻击的代表性 | GPT-5.5 在无 CaMeL 时 ASR 亦为 0%；作者明确这不应被解读为对间接提示注入的普遍鲁棒性——MultiAgentDojo 上的 0% 可能只反映基准所代表的攻击，而非对更强自适应攻击的免疫，并引大规模自适应红队对所有受评前沿模型都发现非零攻击成功 [29] | （作为解释边界提出；未给出具体后续实验计划） | [Paper: Table III 说明文字] |
| 效用依赖提示增强与预先承诺的计划 | 两个基准上都必须为工具描述增补完整返回 schema 才能获得合理效用（作者视其为协议必要组成而非固有局限）；多数良性失效源于在观察运行时数据前承诺控制流计划，另有未经检查的范围替换失效 | 作者将其作为观察到的失效模式记录，未提出具体解决方案 | [Paper: Section V 开头; Section V-C2] |
| 复现性受模型访问限制 | 模型经 OpenRouter API 访问，底层推理硬件不受作者控制，精确复现可能依赖对相同模型版本的持续访问 | （在 LLM 使用说明中披露） | [Paper: Section IX] |

## 13 批判性分析

| `[Analysis]` 观察 | 潜在问题或替代解释 | 为什么重要 | 如何检验 | 依据 |
| --- | --- | --- | --- | --- |
| "ASR 降到 0.0%"的统计强度有限 | n = 949 下 0 次成功的 Wilson 95% 上界约 0.4%（论文表中即 [0.0, 0.4]），因此结果与"低到 0.4% 的真实 ASR"在统计上不可区分；且注入攻击集合固定、非自适应 | 若把 0.0% 当作"已解决"，会低估针对 `variables` 通道、`get_variable` 语义或 QLLM 输出的定向攻击风险 | 设计自适应攻击：让注入内容显式诱导父 Agent 把不可信文本写入 `message`（测试解释器是否拦截）、或诱导子 Agent 以特定变量名调用 `get_variable`；报告 ASR 的置信上界而非点估计 | [Paper: Table III 及其说明]（作者已部分承认，见 C12） |
| 全部实验使用平凡策略 $S=\emptyset$，安全结论只覆盖控制流劫持 | 论文明确区分控制流攻击与数据流攻击：即使控制流不变，攻击者仍可能影响 QLLM 在合法计划内产出的数据，导致越权动作（如外发敏感信息）。跨边界保留 provenance 的机制（解释器性质 2）在实验中**未被实际行使** | 研究画像关注的"共享记忆污染、上下文污染、数据外泄"多属数据流层面；仅凭本文不能推断 multi-CaMeL 对这类攻击有效 | 配置非平凡策略（如禁止 `send_email` 携带源自私有数据的参数发给未授权收件人），测量攻击成功率、策略误报率与效用三者；并做"仅性质 1 / 仅性质 2 / 两者"的消融 | [Paper: Section II-B（Definition 4 与数据流攻击说明）; Section IV-B 第 2 点; Section II-B 平凡策略理由] |
| 协议层保证与实现层保证之间存在缺口 | 作者承认解释器可能漏检隐式依赖（未走分支上的赋值等），使变量在被污染时仍标记为可信；而 Section IV-C 的论证以"指令通道完整性被强制"为前提 | 这意味着 0% ASR 是经验观察，不等于实现满足协议性质；真实系统中一次漏检就可能重新打开边界洗白 | 构造隐式依赖测试用例（如 `if untrusted_flag: msg = trusted_text`，其中 `untrusted_flag` 源自工具输出），检查解释器是否阻止该 `msg` 进入 `message`；或用形式化/符号执行审计解释器的依赖追踪规则 | [Paper: Section VI-B1; Section IV-C] |
| 效用比较的公平性存疑 | CaMeL 系配置获得"所有工具描述增补完整返回 schema"的提示增强；检索到的正文未说明 no-CaMeL 基线是否也获得同等增强 | 若基线未获增强，则 no CaMeL 的效用被低估，从而夸大 CaMeL 系的相对代价；反之若基线也获增强，则比较公平——这一点直接影响 21.6 点与 3.2 点这两个数字的解释 | 交叉消融：{增强, 未增强} × {no CaMeL, individual, multi}，报告 2×3 网格 | [Paper: Section V 开头段]（增强必要性明确，基线是否同享增强未明确记录） |
| MultiAgentDojo 由本文作者构造，工具划分方式可能天然利于 multi-CaMeL | 子 Agent 按工具相似度划分（Email/Calendar/Drive、Transactions/Files/Account、Slack/Web、Hotels/Restaurants/Car Rental/Assistant），跨边界通信因此多为"传值"而非"传需要下游据此改变计划的指令" | 若真实系统的委派是"把检索到的不可信内容交给子 Agent 并让它自行决定动作"，双通道分离的效用代价可能远高于本文测得的 3.2 点 | 增设一类任务：子 Agent 必须依据不可信内容选择不同工具序列（即需要 branch steering 之外的计划调整），测量 multi-CaMeL 的成功率与 ASR | [Paper: Section V-B; Table I]（划分为论文自述设计，属 `[Analysis]` 推断） |
| "能力越强、代价越小"缺乏机制解释与定量支撑 | 趋势非单调（Flash-Lite 在 AssetOpsBench 上 multi-CaMeL 26.8% 反而高于 individual 20.5%），仅 5 个模型，未做能力度量回归；模型名（Claude Fable 5、GPT-5.5 等）经 OpenRouter 访问，版本可能漂移 | 该趋势是论文对"系统级防御终将变得可负担"的核心乐观论据；若只是样本噪声，则部署建议需重估 | 增加模型数量并纳入公开能力分数做回归；对同一模型固定版本重复运行以估计运行间方差；报告 per-task 配对检验而非仅区间重叠 | [Paper: Section V-A2; Section V-B1; Table IV; Table V; Section IX] |
| branch steering 本身可能是可利用的攻击面 | 作者承认不可信数据可在既有分支间引导执行并改变外部可见输出，且这违反 TIPNI。若父 Agent 的计划包含"若工具返回 X 则调用 `child_agent(query_1)` 否则 `query_2`"，攻击者可通过操纵工具输出选择分支 | 对研究画像中的"级联失效/攻击传播"而言，分支选择权就是一种低成本影响力，即使不新增路径 | 构造仅通过分支选择达成危害的任务（如两个分支中一个含敏感工具调用），测量 multi-CaMeL 下的成功率；并把 CFI 与 TIPNI 的差集形式化为可测属性 | [Paper: Section IV-C; Section VI-B] |
| 威胁模型未覆盖恶意/被攻陷 Agent 与共谋 | 本文的对手是把注入植入外部数据源的外部攻击者，所有 Agent 本体均诚实且运行 CaMeL；论文在引言中引用 Rose et al. 的隐蔽共谋工作 [19] 作为动机，但未把恶意 Agent 纳入模型 | 研究画像的 B 簇（恶意成员、共谋、拜占庭鲁棒）与 D 簇（权限委托）无法由本文结论覆盖：一个恶意子 Agent 可在 `variables` 中返回任意内容，而父 Agent 的 PLLM 恰恰看不见它 | 扩展威胁模型：允许某个子 Agent 被攻陷（返回伪造/污染数据），检验 provenance 保留是否足以让父 Agent 的策略拦截；或与拜占庭鲁棒聚合机制组合评测 | [Paper: Section I（Rose et al. 引用）; Section III-A（攻击者设定）; Section II-A]（未纳入恶意 Agent 属 `[Analysis]` 判断） |
| 案例研究与主实验使用不同模型（GPT-5.2 vs 五个评测模型） | Section III-A/III-B 的演示与 OMNI-Leak 验证用 GPT-5.2，而 Table III–V 用另外五个模型；GPT-5.2 未出现在主结果表中 | 反例的可复现性与主实验结论之间存在模型不一致，读者难以判断边界洗白的发生率是否依赖特定模型的拼接习惯 | 在五个评测模型上重跑 Section III-A 的三 Agent 演示，报告各模型下 Program 4 型改写（新增外发调用）的出现率 | [Paper: Section III-A; Section III-B; Table III–V] |

## 14 学到的知识

### Agent-derived knowledge candidates

- **组合性是多 Agent 安全的独立问题维度**：单点安全性质（CFI）在系统层面可能结构性失效，且失效不需要任何组件被攻陷——只需接口把数据当指令读。评估任何多 Agent 防御时，应单独追问"该性质在组合下是否保持"，而不是把逐组件结果相加。[Paper: Section III-A; Section III-C]
- **不可能性结果 + 温和假设的论证范式**：本文用"表达能力假设"（工具可被调用并返回结果、且可构造依赖前一次返回值的后续调用）把经验反例升级为一般性 Claim。这一范式可迁移到其他多 Agent 安全性质（如"任何允许下游依据上游不可信输出改变计划的架构都无法满足 X"）。[Paper: Section III-C]
- **接口签名即安全边界**：把 `message: str` 改为 `message: str, variables: dict[str, Any]` 是一次类型层面的信任划分，比任何提示词约定都强；配套的运行时强制（解释器）与运行时取用工具（`get_variable`）构成完整闭环。这是"最小权限/能力令牌"思路在 Agent 间通信上的具体落地形态。[Paper: Section IV-A; Section IV-B]
- **provenance 必须随数据移动，否则策略无法全局化**：跨边界保留 capabilities 使全局策略 $S$ 可分解为逐 Agent 运行时强制；这为研究画像中"共享记忆分区、写入验证、数据来源标记"提供了可借鉴的实现路径。[Paper: Section IV-B 第 2 点]
- **系统级防御的效用代价主要来自"预先承诺计划"**：CaMeL 系要求在观察数据前生成解析与控制流程序，因此需要返回 schema 增强，且无法运行时新增动作；这是所有"计划先行"型安全架构（含安全编排、状态机约束）的共性代价。[Paper: Section V 开头; Section V-C2]
- **基准改造需自带难度校验**：作者用 Table II 证明 MultiAgentDojo 未扭曲良性难度（平均 +0.7 点、区间全重叠），并公开剔除 29 个不可完成任务的双条件方法与任务编号清单（Appendix B）。这是可复用的基准构建规范。[Paper: Table II; Appendix B]
- **报告口径要区分模型行为伪影**：Claude Fable 5 在良性设置下拒答 52/97（53.6%），作者同时报告含/不含拒答两套结果并标注为假设。提示"安全拒答"会污染效用比较，需单独口径。[Paper: Section V-B; Table V]
- **统计区间选择要匹配指标范围**：ASR 接近 0% 时改用 Wilson score 而非 Wald 区间——一个可直接复用的评测细节。[Paper: Table III 说明]

## 15 与已有知识的联系

> 未执行外部核验；以下仅为论文内部关联与明确标记的候选联系。

**论文内部关联（已核验于原文）**：

- 与 CaMeL [1] 的关系是"扩展 + 修正"：继承 PLLM/QLLM 分离与自定义解释器，新增两项解释器性质与双通道接口；作者明确指出与单 Agent CaMeL 不同，multi-CaMeL 的解释器在不配置任何策略时也是 CFI 所必需。[Paper: Section IV-B 末段]
- 与 Dual LLM 模式 [11] 的关系是"实例化谱系"：CaMeL 是 Dual LLM 的具体实现，本文把该谱系推进到多 Agent。[Paper: Section I]
- 与 AgentDojo [12] 的关系是"基准扩展"：MultiAgentDojo 保留 97 用户任务与 35 注入目标，改为 orchestrator + 2–4 子 Agent 拓扑。[Paper: Section V-B; Table I]
- 与 OMNI-Leak [22] 的关系是"部分反驳 + 部分确认"：该攻击在个体 CFI 下失效（0% ASR，5 次试验），说明个体安全并非无用。[Paper: Section III-B]
- 与 Triedman et al. [24] 的关系是术语沿用（control-flow hijacking）；与 de Witt et al. [25]、Christodorescu et al. [26] 的关系是为"Agent 安全是系统问题"提供经验支持。[Paper: Section III-A; Section III-A 末段]
- 与并发工作 Garby et al. / LLMbda [28] 的关系是对照与自查：TIPNI 强于 CFI（branch steering 会违反 TIPNI），且本文继承其指出的解释器隐式依赖缺陷、规避其指出的重试泄漏。[Paper: Section VI-B]
- 与 Rose et al. [19]（多 Agent 隐蔽共谋检测）的关系是动机层面的：Agent 间交互会引入本质上多 Agent 的安全问题。[Paper: Section I]

**候选联系（对应研究画像主题簇，待用户确认后再建立双向链接）**：

- 主题簇 A（通信与身份安全）：本文的 `message`/`variables` 双通道可视为"策略强制的消息传递"的一种最小实现；但**未涉及**身份认证、消息签名与不可否认性——子 Agent 无法验证调用者身份，父 Agent 被默认可信用户。这是可直接接续的空白。
- 主题簇 C（共享状态与长期记忆）：`variables` + provenance 保留是"数据来源标记"的雏形；论文未处理持久化共享记忆、跨 episode 污染与回滚，作者在 Section VI-A 仅提示保留会话历史需额外小心。
- 主题簇 D（权限、委托与工具安全）：能力（capability）跨边界保留对应"委托边界"问题，但实验用平凡策略，故 confused deputy、权限升级、数据外泄在本文中没有被实测。
- 主题簇 E（系统评测与理论）：MultiAgentDojo 填补了多 Agent 注入基准空白，但缺少自适应攻击、共谋攻击、长时任务与动态成员；不可能性 Claim 属"组合安全属性"方向的早期结果。
- 与研究画像核心问题 3（提示注入如何在协作网络中传播、放大或级联）：本文给出树状拓扑下的单跳传播机制与阻断条件；多跳放大与级联失效未被研究。
- 与研究画像核心问题 8（失效后撤销权限、隔离污染、回滚共享状态）：本文完全未覆盖恢复阶段——multi-CaMeL 实现甚至不重试失败执行，属纯预防型机制。

## 16 研究想法

### Agent-derived research candidates

#### 候选想法 1：把"指令通道完整性"从树状层级推广到共享记忆与点对点拓扑

- **起点**：作者把"跨越 Agent 边界不得隐式升级信任"列为比 multi-CaMeL 更宽的原则，并明确 DAG、循环、异步消息队列、共享状态与点对点架构留待未来工作；同时指出这类系统中可能没有单一根 Agent、没有唯一信息流方向、没有清晰的 agent-as-tool 边界可供强制协议。[Paper: Section VI-A; Section VII]
- `[Hypothesis]` **核心假设**：只要把"写入共享记忆/消息队列"也视为一次边界跨越，并对每条写入强制 (a) 指令字段不依赖任何不可信来源、(b) 数据字段携带 provenance 与 capability 标签，则系统级 CFI 可在无根、含环拓扑下以"每个写入点局部强制"的方式组合成立；反之，若允许 Agent 在读取时把数据字段拼接进自身提示的指令位，则必然存在边界洗白型反例。
- **相对本文的变化**：从"父→子调用的两个参数"改为"共享黑板/消息队列的写入 schema"；从有根树改为含环有向图；新增读取侧强制（本文只在调用侧强制）。
- **初步方法**：定义共享状态版的形式化系统 $M=(\mathcal{A},G,\mathcal{T},\mathcal{M})$（$G$ 为一般通信图，$\mathcal{M}$ 为带标签的共享记忆）；给出对应的 CFI 定义与不可能性/可能性定理；实现一个带标签写入网关（type-level 区分 instruction/data 字段）并接入现有 Agent 框架。
- **验证方案**：在 MultiAgentDojo 之上构造含环与共享记忆的变体（例如两个 Agent 互相调用、或经由共享笔记通信），复用其 949 量级的注入任务实例，比较 no-defense / 仅写入侧强制 / 写入+读取侧强制的 ASR 与良性成功率，报告 Wilson 与 Wald 区间；并加入自适应攻击（注入显式诱导 Agent 把数据字段内容复述进指令位）。
- **证伪条件**：若在含环拓扑下存在一类任务，其完成必然要求某 Agent 依据不可信内容重写自身指令位（即无法用 branch steering 表达），且此时写入+读取侧强制导致良性成功率大幅下降（例如相对 no-defense 下降超过本文 GPT-4.1 的 −53.7 点量级），则"局部强制可组合"的假设被削弱；若构造出在双通道强制下仍成功的边界洗白攻击，则假设直接被推翻。
- **可能失败原因**：环状拓扑中 provenance 标签可能因多次转写而退化（标签合并/丢失）；共享记忆的读取往往是批量拼接，难以在类型层区分指令位；解释器漏检隐式依赖的问题（本文已承认）在更复杂控制流下会放大。
- **创新状态**：unverified，需检索现有技术（作者已把该方向标为未来工作，但并发工作 LLMbda [28] 与其他 IFC 方案 [13,14] 的覆盖范围需外部核验）。

#### 候选想法 2：面向"恶意/被攻陷子 Agent"的来源可验证委派协议

- **起点**：本文的威胁模型是外部对手把注入植入数据源，所有 Agent 本体诚实；但作者在引言中引用 Rose et al. 关于 LLM Agent 隐蔽共谋的工作 [19]，并指出 Agent 间交互会引入本质上多 Agent 的安全问题。multi-CaMeL 的 `variables` 通道对父 Agent 的 PLLM 不透明——这同时意味着父 Agent **无法审查**子 Agent 返回的内容。[Paper: Section I; Section IV-A]
- `[Hypothesis]` **核心假设**：在保留双通道分离的前提下，为 `variables` 中的每个值附加由子 Agent 签署的来源证明（哪些工具、哪些输入、哪次调用产生），并让父 Agent 的安全策略在**不向 PLLM 暴露内容**的条件下对签名与来源元数据做检查，可在不重新打开边界洗白的前提下抵御被攻陷子 Agent 返回的伪造/污染数据；反之，任何需要父 Agent PLLM 阅读子 Agent 返回内容才能发现污染的方案，都会重新引入边界洗白。
- **相对本文的变化**：新增攻击者能力（恶意/被攻陷子 Agent，可任意填写 `variables` 与返回值）；新增机制（来源签名 + 元数据级策略检查 + 可选的跨 Agent 交叉验证）；把本文未行使的"解释器性质 2（跨 Agent provenance 保留）"变成实际评测对象。
- **初步方法**：扩展 multi-CaMeL 的 capability 标签为可验证来源凭证（含工具调用链哈希）；在父 Agent 侧实现"元数据策略"（如拒绝来源链中含未授权域的值的写入/外发）；对需要内容级校验的场景，引入独立验证 Agent 或 QLLM 交叉核对，且其结论只以布尔/标签形式回到控制流（避免不可信文本进入指令位）。
- **验证方案**：构造被攻陷子 Agent 的攻击集（返回伪造数据、返回带注入的"数据"、谎报来源、与其他 Agent 共谋），在 MultiAgentDojo 与 AssetOpsBench 的多 Agent 设置上测量 ASR、污染传播范围、良性任务成功率、误报率与额外 token/时延成本；与"无来源验证的 multi-CaMeL"和"允许父 PLLM 审查返回值"两个基线对比。
- **证伪条件**：若来源签名可被子 Agent 伪造或重放（即签名无法绑定到真实工具调用链），或若元数据级策略在实测中无法拦截任何内容级污染（ASR 与无验证基线无显著差异），则假设被推翻；若"允许父 PLLM 审查"基线在效用与安全性上同时优于元数据方案，则设计取舍不成立。
- **可能失败原因**：签名只证明"来源"不证明"正确性"，被攻陷 Agent 可如实签署自己编造的内容；元数据策略可能过粗导致高误报；额外验证 Agent 会显著增加时延与 token 成本，可能抵消本文所示"强模型下代价收窄"的趋势。
- **创新状态**：unverified，需检索现有技术（Agent 身份认证、消息签名、拜占庭鲁棒聚合、可验证委派等方向的既有工作需外部核验）。

## 关联笔记

- 主题：待关联（当前工作区内未发现 `Agent-IFC/20_Themes/` 目录或任何主题笔记，故不创建链接以免产生虚假关联；建议候选主题：多Agent系统安全、间接提示注入、信息流控制与控制流完整性、Agent间通信协议、安全-效用权衡基准）
- 项目：待关联（工作区内未发现 `Agent-IFC/` 库；研究画像文件以只读上下文形式提供，未作为库内笔记核验）
- 相关论文：待关联（论文引用的 CaMeL [1]、AgentDojo [12]、OMNI-Leak [22]、Triedman et al. [24]、de Witt et al. [25]、Christodorescu et al. [26]、Garby et al. / LLMbda [28]、Rose et al. [19] 均为候选关联对象；库内是否已有对应卡片未核验，不做链接）
- 去重检查结果：已按 `arxiv_id`（2610.05640）在工作区内全文检索，**未发现既有论文卡片**；DOI 未提供，无法按 DOI 去重。本卡为新建，未写入任何文件（按本次任务要求仅返回内容）。

## 待解决的问题

- [ ] 核查元数据和来源版本：确认 v1 是否为最新版本、是否已有会议/期刊收录、DOI 与页码；核实 "AI Sequrity Company" 是否为原文拼写（疑似 "AI Security"）。
- [ ] 核验代码与数据可用性：Section VIII 声明发布 MultiAgentDojo 与 multi-CaMeL 实现，但检索到的正文未含仓库 URL / 存档标识，需补齐并记入 `source_url` 或新增字段。
- [ ] 逐条核查结论—证据矩阵 C01–C16，特别是 Table III（n = 949、Wilson 区间）、Table IV/V（Wald 区间）、Fig. 5/Fig. 6 的 $\Delta$ 标注值与 Appendix B 的 29 个任务编号清单是否与 PDF 原表逐项一致。
- [ ] 核查关键数值与图表一致：AssetOpsBench 主文口径（n = 112）与 Appendix B/Fig. 8 全任务口径（$\Delta$ −27.0、−14.2、−34.8、−25.6、−36.2）两套数字的对应关系；Table II 中 GPT-4.1（+3.1）与 Flash Lite（+5.2）为正向变化的原因是否另有说明。
- [ ] 补齐未被检索命中的内容：Appendix A 的标题与用途、Fig. 2 与 Fig. 7 的完整图注、引用 [27]（branch steering 术语来源）与 [29][30][31] 的完整条目。
- [ ] 确认是否存在未标记的 AI 推断：本卡中 `[Analysis]` 与 `[Hypothesis]` 已显式标注；需人工复核 05/08/13/15/16 各节中未加标记的判断句是否均可回溯到原文。
- [ ] 确认主题和项目关联：待 `Agent-IFC/` 库可访问后，建立与主题笔记的双向链接（主题笔记需反向链接本卡片），并把 `projects` 从空值补为规范名称。
- [ ] 确认 PDF 附件：核实 `2610.05640v1Multi-CaMel(1).pdf` 是否已存放于 `Agent-IFC/90_Attachments/`，据实填写 `pdf` 与 `source_hash`（上传到 DeepTutor 的文件不会自动成为 Obsidian 附件）。
- [ ] 按研究画像补充 `comparison` 字段的威胁模型核对项：协作架构、攻击主体、攻击者能力、安全资产、传播路径、防护阶段、成功/失败条件中，"攻击者是否可共谋或自适应""是否可读写身份字段"两项原文未明确记录，需在人工核查时标注为"未明确记录"而非由标题推断。
- [ ] 人工核查通过后，由用户将 `status` 从 `reading` 改为 `reviewed`（AI 不得自行变更）。

## 阅读记录

- 2026-10-12｜DeepTutor｜基于知识库 `agent-ifc-multicamel-2610-05640`（`2610.05640v1Multi-CaMel(1).pdf`）的多轮检索式精读，生成完整论文卡：填写元数据（DOI/页码/代码 URL 缺失项标注未提供或未核验）、术语表、痛点表、方法与模块拆解、Definition 1–5 与不可能性 Claim 的形式化要点、C01–C16 结论—证据矩阵（全部采用 structure-grounded 定位，未写页码）、图表清单（Fig. 1–8、Table I–V、Appendix A–D）、作者承认的局限 9 项、批判性分析 9 项、知识候选 8 条、研究候选 2 条。`status` 设为 `reading`；未写入或修改任何文件；已按 `arxiv_id` 检索工作区确认无重复卡片，主题/项目关联因库内笔记不可见而保留"待关联"。
