from dataclasses import replace
import json
from pathlib import Path
import sys

import pytest

from agent_ifc.inbox import InboxManager, PaperCandidate
from agent_ifc.storage import file_hash, read_text, render_card, write_json
from agent_ifc.workflow import Workflow


@pytest.fixture
def manager(tmp_path, monkeypatch):
    root = tmp_path / "vault" / "Agent-IFC"
    (root / "90_Attachments").mkdir(parents=True)
    (root / "10_Papers").mkdir()
    config = {"project_root": str(root), "vault_root": str(root.parent),
              "paper": {"pdf_source": "old", "metadata": {}}, "source": {"mode": "events"},
              "supplement_session": "old-session", "supplement_draft": "old-draft",
              "deeptutor": {"executable": sys.executable, "cwd": str(tmp_path), "knowledge_base": "old"}}
    monkeypatch.setattr("agent_ifc.inbox._run_text", lambda command: "")
    monkeypatch.setattr(InboxManager, "inspect", lambda self, path: PaperCandidate(
        str(path.resolve()), file_hash(path), "论文", ("作者",), 2026, "", "", "", excerpt="首页"))
    return InboxManager(config)


def add_pdf(manager, name="paper.pdf", data=b"%PDF-1.7\ncontent"):
    pdf = manager.attachments / name
    pdf.write_bytes(data)
    return manager.inspect(pdf)


def test_copy_settling_and_duplicate_bytes(manager):
    candidate = add_pdf(manager, "论文.PDF")
    assert not manager.discover(settle=True, now=0)
    assert not manager.discover(settle=True, now=4)
    assert manager.discover(settle=True, now=6)[0].sha256 == candidate.sha256
    add_pdf(manager, "other.pdf")
    assert len(manager.discover(now=6)) == 1
    Path(candidate.path).write_bytes(b"%PDF-1.7\nchanged")
    assert not manager.discover(settle=True, now=7)  # both changed/new paths are still settling
    assert len(manager.discover(settle=True, now=13)) == 2


def test_known_card_not_reimported(manager):
    candidate = add_pdf(manager)
    card = manager.project_root / "10_Papers" / "paper.md"
    card.write_text(render_card({"type": "paper", "source_hash": candidate.sha256}, "证据"), encoding="utf-8")
    assert manager.discover()[0].status == "archived"
    with pytest.raises(ValueError, match="已有卡片"):
        manager.import_paper(candidate)


def test_config_isolation_and_versions(manager):
    candidate = add_pdf(manager)
    config = manager.build_config(candidate, "new")
    assert config["source"] == {"mode": "live"}
    assert config["deeptutor"]["knowledge_base"] == "new"
    assert config["paper"]["metadata"]["title"] == "论文"
    assert "supplement_session" not in config and "supplement_draft" not in config
    assert manager.config["paper"]["pdf_source"] == "old"
    assert manager.knowledge_base_name(candidate) != manager.knowledge_base_name(replace(candidate, sha256="f" * 64))


def test_state_corruption_stops_discovery(manager):
    write_json(manager.state_path, {"schema_version": 99, "papers": {}})
    with pytest.raises(ValueError, match="记录损坏"):
        manager.discover()


def test_confirmed_identity_and_run_state_survive_restart(manager):
    candidate = add_pdf(manager)
    run = manager.project_root / "90_Runs" / "agent_test"
    write_json(run / "state.json", {"status": "reviewed"})
    manager.save_state(replace(candidate, title="确认后的标题"), run_dir=str(run), status="running")
    found = InboxManager(manager.config).discover()[0]
    assert found.title == "确认后的标题" and found.status == "reviewed"
    with pytest.raises(ValueError, match="已有运行记录"):
        manager.import_paper(found)


def mock_kb(manager, monkeypatch, candidate, *, existing=False, wrong=False, extra=False, status="ready"):
    kb = manager.project_root.parent / "kb"
    (kb / "raw").mkdir(parents=True)
    (kb / "raw" / "paper.pdf").write_bytes(b"wrong" if wrong else Path(candidate.path).read_bytes())
    if extra:
        (kb / "raw" / "another.pdf").write_bytes(b"other")
    name = manager.knowledge_base_name(candidate)
    calls = []
    def command(args, *unused):
        calls.append(args)
        if args[2] == "list":
            return json.dumps([{"name": name}] if existing else [])
        if args[2] == "info":
            return json.dumps({"name": name, "path": str(kb), "status": status})
        return "created"
    monkeypatch.setattr(manager, "_command", command)
    return name, calls


@pytest.mark.parametrize("existing", [True, False])
def test_kb_verifies_source_for_create_and_reuse(manager, monkeypatch, existing):
    candidate = add_pdf(manager)
    name, calls = mock_kb(manager, monkeypatch, candidate, existing=existing)
    result = manager.create_knowledge_base(candidate, name)
    assert result["deeptutor"]["knowledge_base"] == name
    assert sum(args[2] == "create" for args in calls) == (0 if existing else 1)


@pytest.mark.parametrize("options", [{"wrong": True}, {"extra": True}, {"status": "failed"}])
def test_kb_cannot_mix_papers_or_use_unready_index(manager, monkeypatch, options):
    candidate = add_pdf(manager)
    name, _ = mock_kb(manager, monkeypatch, candidate, existing=True, **options)
    with pytest.raises(ValueError):
        manager.create_knowledge_base(candidate, name)


def test_import_registers_run_before_analysis_and_does_not_approve(manager, monkeypatch):
    candidate = add_pdf(manager)
    name, _ = mock_kb(manager, monkeypatch, candidate)
    events = []
    def prepare(flow):
        entry = manager._state()["papers"][candidate.sha256]
        assert Path(entry["run_dir"]) == flow.run_dir
        assert json.loads(read_text(flow.run_dir / "request.json"))["deeptutor"]["knowledge_base"] == name
        flow.state.update(validation={"fatal": []}, draft_hash="abc")
        events.append("analysis")
    def publish(flow, approved_hash):
        events.append("reading")
        flow.state["status"] = "waiting_for_approval"
        flow.save()
    monkeypatch.setattr(Workflow, "prepare", prepare)
    monkeypatch.setattr(Workflow, "publish", publish)
    monkeypatch.setattr("agent_ifc.precheck.Precheck.run", lambda self, report: events.append("precheck"))
    flow = manager.import_paper(candidate, on_created=lambda flow: events.append("created"))
    assert events == ["created", "analysis", "reading", "precheck"]
    assert flow.state["status"] == "waiting_for_approval"
    assert json.loads(read_text(flow.run_dir / "approvals.json")) == []
    with pytest.raises(ValueError, match="已有运行记录"):
        manager.import_paper(candidate)


def test_analysis_failure_can_find_original_run(manager, monkeypatch):
    candidate = add_pdf(manager)
    mock_kb(manager, monkeypatch, candidate)
    def fail(flow):
        flow.state.update(status="failed", error="provider")
        flow.save()
        raise RuntimeError("provider")
    monkeypatch.setattr(Workflow, "prepare", fail)
    with pytest.raises(RuntimeError, match="provider"):
        manager.import_paper(candidate)
    found = manager.discover()[0]
    assert found.status == "failed" and Path(found.run_dir).is_dir()


def test_pdf_change_after_confirmation_blocks_model_call(manager):
    candidate = add_pdf(manager)
    Path(candidate.path).write_bytes(b"%PDF-changed")
    with pytest.raises(ValueError, match="PDF 已改变"):
        manager.import_paper(candidate)


def test_child_process_unicode_logs_timeout_and_cancel(manager):
    text = manager._command([sys.executable, "-c", "print('中文•')"], "transport", lambda msg: None)
    assert "中文•" in text
    assert "中文•" in read_text(manager.directory / "transport-stdout.log")
    with pytest.raises(TimeoutError):
        manager._command([sys.executable, "-c", "import time; time.sleep(30)"], "timeout", lambda msg: None, .1)
    manager.cancel.set()
    with pytest.raises(InterruptedError):
        manager._command([sys.executable, "-c", "import time; time.sleep(30)"], "cancel", lambda msg: None)


def test_metadata_never_takes_pdf_creation_year_or_next_line_as_author(manager, monkeypatch):
    candidate = add_pdf(manager)
    monkeypatch.undo()
    monkeypatch.setattr("agent_ifc.inbox._run_text", lambda args:
        "Title: Reliable title\nCreationDate: Tue Oct 13 2026\nAuthor: Doe, Jane; 王某\n" if args[0] == "pdfinfo"
        else "Reliable title\nDepartment of Security\narXiv:2401.12345v2\n2024\n")
    found = manager.inspect(Path(candidate.path))
    assert found.year == 2024 and found.arxiv_id == "2401.12345v2"
    assert found.authors == ("Doe, Jane", "王某")


def test_native_tool_non_utf8_falls_back_without_reader_thread_error(monkeypatch):
    import subprocess
    from agent_ifc.inbox import _run_text
    monkeypatch.setattr("agent_ifc.inbox.subprocess.run", lambda *args, **kwargs:
                        subprocess.CompletedProcess(args, 0, "中文".encode("gbk"), b""))
    assert _run_text(["pdfinfo", "paper.pdf"]) == ""
