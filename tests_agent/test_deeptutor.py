import json
from pathlib import Path
import subprocess
import sys
import threading

import pytest

from agent_ifc.deeptutor import parse_events, run_cli
from agent_ifc.storage import read_text


def child_cli(tmp_path, monkeypatch, script):
    path = tmp_path / "fake_deeptutor.py"
    path.write_text(script, encoding="utf-8")
    original_popen = subprocess.Popen
    calls = []
    def routed_popen(command, **kwargs):
        calls.append((command, kwargs))
        return original_popen([sys.executable, str(path)], **kwargs)
    monkeypatch.setattr(subprocess, "Popen", routed_popen)
    config = {"executable": sys.executable, "cwd": str(tmp_path), "knowledge_base": "paper-test", "timeout_seconds": 5}
    return config, calls


def test_real_child_pipe_utf8_argv_and_stderr(tmp_path, monkeypatch):
    script = '''import json, sys
for seq, (kind, meta) in enumerate([
    ("session", {}), ("result", {"response": "中文 • ✅"}), ("done", {"status": "completed"})
], 1):
    print(json.dumps({"type": kind, "metadata": meta, "seq": seq, "turn_id": "t", "session_id": "s"}, ensure_ascii=False), flush=True)
print("诊断 stderr", file=sys.stderr)
'''
    config, calls = child_cli(tmp_path, monkeypatch, script)
    path = run_cli(config, "中文提示词 $(不执行)", tmp_path, threading.Event(), session="old-session")
    response, info = parse_events(path)
    assert response == "中文 • ✅"
    assert info["event_count"] == 3
    assert "诊断 stderr" in read_text(tmp_path / "deeptutor-stderr.log")
    argv, options = calls[0]
    assert argv[3] == "中文提示词 $(不执行)"
    assert argv[-2:] == ["--session", "old-session"]
    assert options["shell"] is False
    assert options["env"]["PYTHONIOENCODING"] == "utf-8"


def test_long_windows_prompt_uses_request_file(tmp_path, monkeypatch):
    script = '''import json
for seq, (kind, meta) in enumerate([
    ("result", {"response": "完成"}), ("done", {"status": "completed"})
], 1):
    print(json.dumps({"type": kind, "metadata": meta, "seq": seq, "turn_id": "t"}), flush=True)
'''
    config, calls = child_cli(tmp_path, monkeypatch, script)
    monkeypatch.setattr("agent_ifc.deeptutor.needs_request_file", lambda command: True)
    prompt = "长提示" * 10000
    run_cli(config, prompt, tmp_path, threading.Event(), output_prefix="precheck-01",
            attach_knowledge_base=False)
    request = json.loads((tmp_path / "precheck-01-request.json").read_text(encoding="utf-8"))
    assert request["message"] == prompt
    assert request["knowledge_base"] == "paper-test"
    assert request["attach_knowledge_base"] is False
    argv, _ = calls[0]
    assert prompt not in argv
    assert argv[1].endswith("deeptutor_file_runner.py")


def test_precheck_style_request_omits_kb_attachment_but_keeps_rag_tool(tmp_path, monkeypatch):
    script = '''import json
for seq, (kind, meta) in enumerate([
    ("result", {"response": "完成"}), ("done", {"status": "completed"})
], 1):
    print(json.dumps({"type": kind, "metadata": meta, "seq": seq, "turn_id": "t"}), flush=True)
'''
    config, calls = child_cli(tmp_path, monkeypatch, script)
    run_cli(config, "short", tmp_path, threading.Event(), attach_knowledge_base=False)
    argv, _ = calls[0]
    assert "--kb" not in argv
    assert argv[argv.index("--tool") + 1] == "rag"


@pytest.mark.parametrize("script,exception,match", [
    ("import sys; print('diagnostic'); sys.exit(2)", RuntimeError, "退出码 2"),
    ("print('not JSON')", ValueError, "UTF-8 NDJSON"),
    ("import time; time.sleep(5)", TimeoutError, "超过"),
])
def test_failures_and_timeout_preserve_logs(tmp_path, monkeypatch, script, exception, match):
    config, _ = child_cli(tmp_path, monkeypatch, script)
    config["timeout_seconds"] = 0.3 if exception is TimeoutError else 5
    with pytest.raises(exception, match=match):
        run_cli(config, "test", tmp_path, threading.Event())
    assert (tmp_path / "deeptutor-events.ndjson").is_file()
    assert (tmp_path / "deeptutor-stderr.log").is_file()


def test_cancel_terminates_own_child(tmp_path, monkeypatch):
    config, _ = child_cli(tmp_path, monkeypatch, "import time; time.sleep(10)")
    cancel = threading.Event()
    cancel.set()
    with pytest.raises(InterruptedError, match="取消"):
        run_cli(config, "test", tmp_path, cancel)


def test_known_stdout_warnings_preserved_without_losing_completed_events(tmp_path, monkeypatch):
    script = '''import json
print("Warning: No prompt file found for chat/context_summary_agent", flush=True)
for seq, (kind, meta) in enumerate([
    ("session", {}), ("result", {"response": "补充分析完整结果"}), ("done", {"status": "completed"})
], 1):
    if seq == 2:
        print("WARNING deeptutor.agents.loop.agent_loop - agent_loop_round_complete finish_reason=length", flush=True)
    print(json.dumps({"type": kind, "metadata": meta, "seq": seq, "turn_id": "t"}, ensure_ascii=False), flush=True)
'''
    config, _ = child_cli(tmp_path, monkeypatch, script)
    messages = []
    path = run_cli(config, "test", tmp_path, threading.Event(), messages.append)
    response, info = parse_events(path)
    assert response == "补充分析完整结果"
    assert info["event_count"] == 3
    assert len(info["stdout_warnings"]) == 2
    assert "Warning:" in read_text(path)  # Keep original bytes for auditing.
    assert "finish_reason=length" in read_text(tmp_path / "deeptutor-diagnostics.log")
    assert any("诊断警告" in message for message in messages)


def test_known_deeptutor_error_traceback_is_diagnostic_but_events_stay_strict(tmp_path):
    path = tmp_path / "events.ndjson"
    lines = [
        "ERROR   deeptutor.services.embedding.client - Embedding batch failed",
        "Traceback (most recent call last):",
        '  File "deeptutor/services/embedding/client.py", line 1, in embed',
        "    raise RuntimeError('bad query')",
        "RuntimeError: bad query",
        json.dumps({"type": "result", "metadata": {"response": "完成"}, "seq": 1,
                    "turn_id": "t"}, ensure_ascii=False),
        json.dumps({"type": "done", "metadata": {"status": "completed"}, "seq": 2,
                    "turn_id": "t"}, ensure_ascii=False),
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    response, info = parse_events(path)
    assert response == "完成"
    assert info["event_count"] == 2
    assert len(info["stdout_warnings"]) == 5


def test_broken_json_after_known_error_is_not_hidden(tmp_path):
    path = tmp_path / "events.ndjson"
    path.write_text("ERROR   deeptutor.x - failed\n  {broken json}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="不是完整 JSON"):
        parse_events(path)


@pytest.mark.parametrize("bad", ["WARNING unknown - lost event", '{"type": "thinking", broken}'])
def test_unknown_text_or_broken_json_still_fails(tmp_path, monkeypatch, bad):
    config, _ = child_cli(tmp_path, monkeypatch, "print(" + repr(bad) + ")")
    with pytest.raises(ValueError, match="UTF-8 NDJSON"):
        run_cli(config, "test", tmp_path, threading.Event())


def test_progress_heartbeat_while_thinking_or_waiting(tmp_path, monkeypatch):
    script = '''import json, time
for seq, (kind, meta) in enumerate([
    ("thinking", {}), ("result", {"response": "完成"}), ("done", {"status": "completed"})
], 1):
    print(json.dumps({"type": kind, "metadata": meta, "seq": seq, "turn_id": "t"}), flush=True)
    if seq == 1:
        time.sleep(5.3)
'''
    config, _ = child_cli(tmp_path, monkeypatch, script)
    config["timeout_seconds"] = 10
    messages = []
    run_cli(config, "test", tmp_path, threading.Event(), messages.append)
    assert any("模型推理中" in message and "距最新事件" in message for message in messages)
    assert any("等待运行结束" in message for message in messages)


def test_precheck_seed_uses_file_bridge_with_kb_attached(tmp_path, monkeypatch):
    script = '''import json
for seq, (kind, meta) in enumerate([("result", {"response": "完成"}), ("done", {"status": "completed"})], 1):
    print(json.dumps({"type": kind, "metadata": meta, "seq": seq, "turn_id": "t"}), flush=True)
'''
    config, calls = child_cli(tmp_path, monkeypatch, script)
    run_cli(config, "整张论文卡", tmp_path, threading.Event(), output_prefix="precheck-01",
            seed_query="ORBIT safety evaluations")
    request = json.loads(read_text(tmp_path / "precheck-01-request.json"))
    assert request["attach_knowledge_base"] is True
    assert request["seed_query"] == "ORBIT safety evaluations"
    assert request["message"] == "整张论文卡"
    assert calls[0][0][1].endswith("deeptutor_file_runner.py")


@pytest.mark.parametrize("kind,match", [("thinking", "没有新事件"), ("result", "结束归档阶段")])
def test_inactivity_and_finalization_timeouts_are_distinct(tmp_path, monkeypatch, kind, match):
    script = 'import json,time; print(json.dumps({"type": ' + repr(kind) + ', "metadata": {"response": "完成"}, "seq": 1, "turn_id": "t"}), flush=True); time.sleep(10)'
    config, _ = child_cli(tmp_path, monkeypatch, script)
    config.update(idle_timeout_seconds=.3, completion_timeout_seconds=.3)
    with pytest.raises(TimeoutError, match=match):
        run_cli(config, "test", tmp_path, threading.Event())
    with pytest.raises(ValueError, match="没有成功完成"):
        parse_events(tmp_path / "deeptutor-events.ndjson")


def test_done_with_hanging_cli_can_finish_after_strict_validation(tmp_path, monkeypatch):
    script = '''import json,time
for seq, (kind, meta) in enumerate([("result", {"response": "完成"}), ("done", {"status": "completed"})], 1):
    print(json.dumps({"type": kind, "metadata": meta, "seq": seq, "turn_id": "t"}), flush=True)
time.sleep(10)
'''
    config, _ = child_cli(tmp_path, monkeypatch, script)
    config["exit_grace_seconds"] = .3
    path = run_cli(config, "test", tmp_path, threading.Event())
    assert parse_events(path)[0] == "完成"


@pytest.mark.parametrize("value", [0, -1, True, float("nan"), float("inf"), "1200"])
def test_invalid_timeout_rejected_before_launch(tmp_path, monkeypatch, value):
    config, calls = child_cli(tmp_path, monkeypatch, "raise AssertionError('not launched')")
    config["idle_timeout_seconds"] = value
    with pytest.raises(ValueError, match="有限正数"):
        run_cli(config, "test", tmp_path, threading.Event())
    assert not calls


def chained_traceback():
    return [
        "ERROR   deeptutor.runtime.orchestrator - Capability chat failed: connection",
        "Traceback (most recent call last):",
        '  File "httpcore.py", line 1, in connect',
        "    raise exc",
        "httpcore.ConnectError: All connection attempts failed",
        "",
        "The above exception was the direct cause of the following exception:",
        "",
        "Traceback (most recent call last):",
        '  File "client.py", line 2, in request',
        "    response = await connect()",
        "               ^^^^^^^^^^^^^^^",
        "openai.APIConnectionError: Connection error.",
        "",
        "During handling of the above exception, another exception occurred:",
        "",
        "Traceback (most recent call last):",
        '  File "loop.py", line 3, in run',
        "    return await self._forced_finish(",
        "           ^^^^^^^^^^^^^^^^^^^^^^^^^^",
        "deeptutor.services.llm.exceptions.LLMProviderTransportError: 无法连接模型服务，请重试。",
    ]


def test_chained_transport_failure_reports_cause_not_encoding(tmp_path, monkeypatch):
    lines = chained_traceback() + [
        json.dumps({"type": "error", "seq": 1, "turn_id": "t", "content": "无法连接模型服务",
                    "metadata": {"error_code": "provider_transport", "retryable": True}}, ensure_ascii=False),
        json.dumps({"type": "done", "seq": 2, "turn_id": "t", "metadata": {"status": "failed"}}),
    ]
    config, _ = child_cli(tmp_path, monkeypatch, "\n".join("print(" + repr(line) + ", flush=True)" for line in lines))
    with pytest.raises(ValueError, match="无法连接模型服务.*provider_transport"):
        run_cli(config, "test", tmp_path, threading.Event())
    with pytest.raises(ValueError, match="provider_transport"):
        parse_events(tmp_path / "deeptutor-events.ndjson")
    assert "^^^^^^^^^^^^" in read_text(tmp_path / "deeptutor-diagnostics.log")


def test_chained_diagnostics_do_not_hide_later_bad_json(tmp_path):
    path = tmp_path / "events.ndjson"
    path.write_text("\n".join(chained_traceback() + ['  {"type": "thinking", broken}']) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="不是完整 JSON"):
        parse_events(path)


def test_json_event_ends_traceback_context(tmp_path):
    path = tmp_path / "events.ndjson"
    line = json.dumps({"type": "thinking", "turn_id": "t", "seq": 1})
    path.write_text("\n".join(chained_traceback() + [line, "  unknown diagnostic"]) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="不是完整 JSON"):
        parse_events(path)
