---
type: integration-spec
component: DeepTutor CLI
status: planned
updated: "2026-10-12"
tags: [workflow, deeptutor, agent, ndjson]
---

# DeepTutor Agent 集成规范

## 接口选择与验证状态

首选 `deeptutor run <capability> "<message>" --format json`。官方支持由其他 Agent 驱动 CLI，并逐行输出 NDJSON。

- 官方接口能力已核实；当前环境中 `Get-Command deeptutor` 未找到命令，尚未完成本机端到端验证。这不意味着其他虚拟环境、容器或机器上没有安装。
- 此文件是待实现的接口规范；不是已经运行的 Agent、弹窗或 DeepTutor 连接。
- 具体能力、参数和事件字段须同时通过部署版本的帮助信息与一次实际运行确认，并记录版本。

## 部署预检

在实际运行 DeepTutor 的环境执行以下命令，指定其可执行文件的绝对路径和工作目录。

~~~powershell
deeptutor --help
deeptutor run --help
deeptutor doctor --format json
deeptutor kb list --format json
~~~

总控 Agent 检查退出码和 doctor 的 `ok` 字段；未就绪时保存错误并请求用户处理，不启动精读。

界面里的 `111` 是用户已连接 Obsidian 的入口。它不能直接视为 CLI 的论文知识库：必须查询实际 CLI 知识库，核验目标 PDF 所在位置。尚未核验前，命令中的知识库名称保持占位符。

## 一篇论文的一次运行

1. 用户在候选审核弹窗批准 selected 后，获取 PDF，记录来源、版本和 SHA-256。
2. 使用已核验的知识库导入接口加入该 PDF；首次可采用专用单论文知识库，以防不同论文证据混用。
3. 读取 Paper_Template.md、Paper_Rules.md 和 DeepTutor_Import_Prompt.md，由总控 Agent 组装任务提示词。
4. 明确指定目标标题、PDF 标识、所需证据位置和输出格式，调用 CLI。
5. 持续解析事件流，保存结果、会话和错误。
6. 自动检查结果，将论文卡写为 reading；用户通过论文卡审核弹窗确认后，才更新 reviewed。

官方文档中的知识库创建形式如下，执行前还需核对安装版本帮助：

~~~powershell
deeptutor kb create "<paper-kb-name>" --doc "<absolute-pdf-path>"
~~~

建议先用 chat 对单篇知识库做原文分析；deep_research 可在后续对比试验后用于综合。原文证据不能由联网检索结果替代。

~~~powershell
deeptutor run chat "<paper-card-prompt>" --kb "<verified-paper-kb>" --language zh --format json
~~~

这些是调用示意，尚未执行。正式适配器用 subprocess 参数数组传参，不把论文内容拼接成 shell 命令。长提示词如何传入应根据实际版本验证，避免 Windows 命令行长度限制。

## NDJSON 与运行状态

- stdout 逐行解码 JSON，不当作一个 JSON 文档；stderr 单独记录。
- 读取 `result` 事件的 `metadata.response`，从 `done` 保存 `session_id` 和完成状态；同时处理 `error`。
- 非最终事件只用于进度和审计；未知事件保存原始内容，不能直接丢弃或当成成功。
- 成功必须同时满足进程正常退出、终止事件报告成功、结果可提取且论文卡验证通过。
- 非 JSON 行、截断、超时、取消、缺少完成事件或结果缺失，均不能推进为 imported 或 reviewed。
- 保存部分结果，标记失败或中断，支持重试；不能把重试结果写成重复论文卡。
- 会话上下文不等于原文定位：若不能得到可核验的 PDF 页码、章节、图表位置，保留缺失项和 reading，不编造定位。

## 续接与恢复

每篇论文使用独立会话；每次调用保存 run_id、paper_id、PDF 哈希、session_id、工具版本和配置。

~~~powershell
deeptutor run chat "<follow-up-prompt>" --session "<session-id>" --kb "<verified-paper-kb>" --language zh --format json
~~~

续接时重新传入需要的 --kb、--tool、--language，不假定这些选择随 session 自动继承。重试前先检查现有文件和运行记录，避免重复写入。

## 弹窗审批

官方说明 headless CLI 对内部 ask_user 暂停会自动提交空回复，因此不能把 CLI 内部提问作为审批关卡。

总控 Agent 的界面负责：候选批准、补充分析选择、reviewed 确认、写作证据批准。审批时将状态持久化为 waiting_for_approval；用户未答、关闭窗口或超时，都不视为批准。批准后可在重启后恢复，不需要重新检索。

若未来必须响应 DeepTutor 内部的提问，应评估 Python SDK 的 submit_user_reply()，由总控界面提交回复；这不改变外部审批规则。

## Obsidian 写入职责

用户现有的 DeepTutor 写入路径可以保留，但自动 Agent 上线时应选定一个写入者。第一版建议由总控 Agent 负责正式目录写入：DeepTutor 只返回分析，Agent 按统一模板校验并写入 reading 卡片，再展示审核弹窗。

若继续采用 DeepTutor 写入，则只写暂存位置，完成后由总控 Agent 校验并发布；不要让两者同时编辑同一论文卡。现有直接写入设置暂不变更。

## 运行记录

存放在 Agent-IFC/90_Runs/<run_id>/，至少包括 request.json、deeptutor-events.ndjson、result.json、approvals.json 和 errors.json。记录审批对象及其内容哈希：内容修改后，旧审批不能套用到新版本。日志不保存密钥和令牌。

## 官方参考

- [Command Reference](https://docs.deeptutor.info/cli/commands/)
- [Agent Handoff](https://docs.deeptutor.info/cli/agent-handoff/)
- [Python SDK](https://docs.deeptutor.info/cli/python-sdk/)

查阅日期：2026-10-12。实现阶段优先以本机版本帮助和实际事件样本确认兼容性。
