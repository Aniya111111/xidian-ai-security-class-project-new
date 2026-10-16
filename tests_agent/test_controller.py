import json
from pathlib import Path

import pytest

from agent_ifc.controller import Controller, controller_lock
from agent_ifc.storage import read_text, write_json
from agent_ifc.synthesis import SynthesisWorkflow
from tests_agent.test_synthesis import library


def coordinator(config, directory=None):
    config["controller"] = {"settle_seconds": 2, "retry_base_seconds": 5, "max_attempts": 3}
    return Controller(config, directory)


def latest(controller):
    return controller.state["jobs"][-1]


def test_debounce_dedup_and_no_implicit_write(library):
    config, root, paper = library
    source = paper()
    paper("pending", status="reading")
    original = source.read_bytes()
    controller = coordinator(config)
    assert controller.tick(now=10)["status"] == "settling"
    assert not controller.state["jobs"]
    assert controller.tick(now=11)["status"] == "settling"
    assert controller.tick(now=12)["status"] == "waiting_for_approval"
    job = latest(controller)
    assert len(job["sources"]) == 1 and job["attempts"] == 1
    assert not Path(job["target"]).exists()
    assert json.loads(read_text(Path(job["run_dir"]) / "approvals.json")) == []
    for now in (20, 30, 40):
        controller.tick(now=now)
    assert len(controller.state["jobs"]) == 1
    assert source.read_bytes() == original


def test_persistent_deferred_review_and_confirmation_required(library):
    config, root, paper = library
    paper()
    controller = coordinator(config)
    controller.tick(immediate=True)
    job_id = latest(controller)["id"]
    flow = controller.open_review(job_id)
    assert latest(controller)["notified"]
    resumed = Controller(config)
    resumed.tick(immediate=True)
    assert latest(resumed)["notified"]  # Do not repeatedly pop up after close/restart.
    assert len(resumed.state["jobs"]) == 1
    with pytest.raises(ValueError, match="明确确认"):
        resumed.publish(job_id, flow.state["draft_hash"], False)
    assert not flow.target().exists()
    resumed.publish(job_id, flow.state["draft_hash"], True)
    resumed.publish(job_id, flow.state["draft_hash"], True)
    assert latest(resumed)["status"] == "published"
    assert len(json.loads(read_text(flow.run_dir / "approvals.json"))) == 1
    resumed.tick(immediate=True)
    assert resumed.state["status"] == "idle" and len(resumed.state["jobs"]) == 1
    flow.target().write_text(read_text(flow.target()) + "\n我的手写笔记\n", encoding="utf-8")
    resumed.tick(immediate=True)
    assert len(resumed.state["jobs"]) == 1  # Manual notes do not trigger a publish loop.


@pytest.mark.parametrize("change", ["added", "edited", "unreviewed", "target"])
def test_change_during_review_blocks_stale_confirmation_and_requeues(library, change):
    config, root, paper = library
    source = paper()
    controller = coordinator(config)
    controller.tick(immediate=True)
    old_id = latest(controller)["id"]
    flow = controller.open_review(old_id)
    if change == "added":
        paper("b")
    elif change == "edited":
        source.write_text(read_text(source) + "\n修改证据", encoding="utf-8")
    elif change == "unreviewed":
        paper(status="reading")
    else:
        flow.target().write_text("# 主题\n\n手写内容\n", encoding="utf-8")
    with pytest.raises(ValueError, match="审核期间来源或目标已变化"):
        controller.publish(old_id, flow.state["draft_hash"], True)
    controller.tick(immediate=True)
    assert controller.job(old_id)["status"] == "superseded"
    assert flow.draft_text()  # Never remove the user's previous draft.
    if change == "unreviewed":
        assert controller.state["status"] == "no_sources"
        assert len(controller.state["jobs"]) == 1
    else:
        new = latest(controller)
        assert new["id"] != old_id and new["status"] == "waiting_for_approval"
        if change == "target":
            assert "手写内容" in controller.flow(new).draft_text()


def test_incremental_review_and_deleted_published_target(library):
    config, root, paper = library
    paper()
    second = paper("b", status="reading")
    controller = coordinator(config)
    controller.tick(immediate=True)
    job = latest(controller)
    flow = controller.open_review(job["id"])
    controller.publish(job["id"], flow.state["draft_hash"], True)
    controller.tick(immediate=True)
    assert len(controller.state["jobs"]) == 1
    paper("b", status="reviewed")
    controller.tick(immediate=True)
    assert len(latest(controller)["sources"]) == 2
    assert len(controller.state["jobs"]) == 2
    flow = controller.open_review(latest(controller)["id"])
    controller.publish(latest(controller)["id"], flow.state["draft_hash"], True)
    flow.target().unlink()
    controller.tick(immediate=True)
    assert latest(controller)["status"] == "waiting_for_approval"
    assert not flow.target().exists()  # Repair is also subject to explicit confirmation.


def test_transient_backoff_stops_at_limit_and_manual_retry(library, monkeypatch):
    config, root, paper = library
    paper()
    controller = coordinator(config)
    original = SynthesisWorkflow.create
    def unavailable(*args, **kwargs):
        raise PermissionError("temporarily busy")
    monkeypatch.setattr(SynthesisWorkflow, "create", unavailable)
    controller.tick(now=100, immediate=True)
    job_id = latest(controller)["id"]
    assert latest(controller)["status"] == "retry_wait"
    assert latest(controller)["next_retry_at"] == 105
    controller.tick(now=104)
    assert latest(controller)["attempts"] == 1
    controller.tick(now=105)
    assert latest(controller)["attempts"] == 2 and latest(controller)["next_retry_at"] == 115
    controller.tick(now=115)
    assert latest(controller)["status"] == "failed" and latest(controller)["attempts"] == 3
    controller.tick(now=1000)
    assert latest(controller)["attempts"] == 3
    monkeypatch.setattr(SynthesisWorkflow, "create", original)
    controller.retry(job_id)
    controller.tick(now=1001)
    assert latest(controller)["status"] == "waiting_for_approval"
    assert latest(controller)["attempts"] == 1


def test_permanent_failure_keeps_attempt_run_and_requires_fix(library):
    config, root, paper = library
    paper()
    target = root / "20_Themes/幻觉防御.md"
    target.write_text("<!-- Agent-IFC:hallucination-synthesis:begin -->", encoding="utf-8")
    controller = coordinator(config)
    controller.tick(immediate=True)
    job = latest(controller)
    assert job["status"] == "blocked" and job["attempts"] == 1
    assert Path(job["run_dir"]).is_dir()
    assert Path(job["run_dir"], "errors.json").is_file()
    controller.tick(now=100000, immediate=True)
    assert latest(controller)["attempts"] == 1
    target.write_text("# 修复后的主题\n\n保留笔记\n", encoding="utf-8")
    controller.tick(immediate=True)
    assert controller.job(job["id"])["status"] == "superseded"
    assert "保留笔记" in controller.flow(latest(controller)).draft_text()


@pytest.mark.parametrize("complete", [True, False])
def test_restart_recovers_preparing_job(library, complete):
    config, root, paper = library
    paper()
    controller = coordinator(config)
    controller.tick(immediate=True)
    job = latest(controller)
    job["status"] = "preparing"
    if not complete:
        flow = controller.flow(job)
        flow.state["status"] = "preparing"
        flow.base.save()
    controller.save()
    resumed = Controller(config)
    resumed.tick(immediate=True)
    assert latest(resumed)["status"] == "waiting_for_approval"
    assert len(resumed.state["jobs"]) == 1
    assert latest(resumed)["attempts"] == (1 if complete else 2)
    assert len(latest(resumed)["runs"]) == (1 if complete else 2)
    assert not Path(job["target"]).exists()


def test_crash_after_engine_publish_reconciles_without_republication(library):
    config, root, paper = library
    paper()
    controller = coordinator(config)
    controller.tick(immediate=True)
    job = latest(controller)
    flow = controller.open_review(job["id"])
    # Simulate engine completion just before ledger update/process failure.
    flow.publish(flow.state["draft_hash"], confirmed=True)
    resumed = Controller(config)
    resumed.tick(immediate=True)
    assert latest(resumed)["status"] == "published" and resumed.state["status"] == "idle"
    assert len(resumed.state["jobs"]) == 1
    assert len(json.loads(read_text(flow.run_dir / "approvals.json"))) == 1


def test_shared_state_lock_and_boundaries(library, tmp_path):
    config, root, paper = library
    paper()
    directory = tmp_path / "controller"
    first, second = coordinator(config, directory), Controller(config, directory)
    with controller_lock(directory):
        with pytest.raises(RuntimeError, match="另一个总控"):
            second.tick(immediate=True)
    first.tick(immediate=True)
    second.tick(immediate=True)
    assert len(second.state["jobs"]) == 1
    wrong = dict(config, project_root=str(root / "another"))
    with pytest.raises(ValueError, match="路径不匹配"):
        Controller(wrong, directory)
    job = latest(second)
    job["run_dir"] = str(tmp_path / "outside")
    with pytest.raises(ValueError, match="超出当前总控"):
        second.flow(job)


def test_invalid_yaml_is_reported_and_force_preserves_old_draft(library):
    config, root, paper = library
    paper()
    (root / "10_Papers/broken.md").write_text("---\ntitle: [\n---\n正文", encoding="utf-8")
    controller = coordinator(config)
    controller.tick(immediate=True)
    assert any("YAML" in notice for notice in controller.state["notices"])
    old = latest(controller)
    controller.tick(force=True)
    assert len(controller.state["jobs"]) == 2
    assert controller.job(old["id"])["status"] == "superseded"
    assert Path(old["run_dir"], "draft.md").is_file()


def test_scan_failure_is_visible_and_recovers(library):
    config, root, paper = library
    paper()
    config["synthesis"]["target"] = "../escape.md"
    controller = coordinator(config)
    controller.tick(immediate=True)
    assert controller.state["status"] == "scan_failed"
    assert controller.state["last_error"] and not controller.state["jobs"]
    controller.config["synthesis"]["target"] = "20_Themes/幻觉防御.md"
    controller.tick(immediate=True)
    assert controller.state["last_error"] is None
    assert controller.state["status"] == "waiting_for_approval"


def test_controller_does_not_call_model(library, monkeypatch):
    config, root, paper = library
    paper()
    def forbidden(*args, **kwargs):
        raise AssertionError("unexpected model invocation")
    monkeypatch.setattr("agent_ifc.workflow.Workflow.analyze_live", forbidden)
    controller = coordinator(config)
    controller.tick(immediate=True)
    assert latest(controller)["status"] == "waiting_for_approval"
