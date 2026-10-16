from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent_ifc.deeptutor import parse_events
from agent_ifc.storage import digest, file_hash, read_text, render_card, split_card, within, write_json
from agent_ifc.workflow import CHECKS, Workflow, extract_card


def events(response="中文 • 分析", status="completed"):
    return [
        {"type": "session", "metadata": {}, "turn_id": "t1", "session_id": "s1", "seq": 1},
        {"type": "result", "metadata": {"response": response}, "turn_id": "t1", "session_id": "s1", "seq": 2},
        {"type": "done", "metadata": {"status": status}, "turn_id": "t1", "session_id": "s1", "seq": 3},
    ]


def write_events(path, payload):
    path.write_text("".join(json.dumps(event, ensure_ascii=False) + "\n" for event in payload), encoding="utf-8")


@pytest.fixture
def setup_paper(tmp_path):
    root = tmp_path / "vault" / "Agent-IFC"
    for directory in ("90_Templates", "00_Project", "10_Papers", "90_Attachments"):
        (root / directory).mkdir(parents=True)
    pdf = tmp_path / "论文.pdf"
    pdf.write_bytes(b"%PDF-1.7\noriginal test source")
    base_metadata = {
        "schema_version": 1, "type": "paper", "paper_id": "", "title": "测试幻觉防御",
        "authors": ["测试作者"], "year": 2024, "venue": "", "doi": "", "arxiv_id": "",
        "source_hash": "", "pdf": "", "status": "reading", "source_scope": "fulltext",
        "locator_mode": "page-grounded", "tags": ["paper"], "topics": [], "projects": [],
    }
    body = "# 测试幻觉防御\n\n" + "\n\n".join(f"## {i:02} 章节\n\n正文。" for i in range(1, 17))
    body += "\n\n| C01 | 实验 | 结论 | 比较 | 结果 | 边界 | 不支持 | [Paper: PDF p. 1, Table 1] | 已核查 |\n"
    body += "\n## 关联笔记\n\n- 主题：待关联\n- 项目：待关联\n"
    card = tmp_path / "source-card.md"
    card.write_text(render_card(base_metadata, body), encoding="utf-8")
    (root / "90_Templates/Paper_Template.md").write_text(render_card(base_metadata, body), encoding="utf-8")
    (root / "90_Templates/Paper_Rules.md").write_text("不能自动 reviewed", encoding="utf-8")
    (root / "00_Project/Research_Profile.md").write_text("研究主题：幻觉防御", encoding="utf-8")
    event_path = tmp_path / "events.ndjson"
    write_events(event_path, events())
    config = {
        "project_root": str(root), "vault_root": str(root.parent),
        "paper": {"pdf_source": str(pdf), "metadata": {key: base_metadata[key] for key in ("title", "authors", "year", "doi", "arxiv_id")}},
        "source": {"mode": "events", "events_path": str(event_path), "card_path": str(card)},
        "deeptutor": {},
    }
    return config, tmp_path / "runs"


def prepared(setup_paper):
    config, runs = setup_paper
    flow = Workflow.create(config, runs)
    flow.prepare()
    assert not flow.state["validation"]["fatal"]
    return flow


def pass_precheck(flow):
    report = {"schema_version": 1, "draft_hash": flow.state["draft_hash"], "status": "ready",
              "summary": "独立预审确认当前 Cxx 有原文支持。",
              "claims": [{"claim_id": "C01", "verdict": "supported", "evidence": "source",
                          "locator": "PDF p. 1, Table 1", "reason": "matches"}],
              "issues": [], "unresolved": [], "blockers": [], "decisions": {}}
    path = flow.run_dir / "precheck.json"
    write_json(path, report)
    flow.state["precheck"] = {"status": "ready", "draft_hash": report["draft_hash"],
                              "path": str(path), "blockers": 0}
    flow.save()
    return report


def test_full_cycle_utf8_review_and_idempotency(setup_paper):
    flow = prepared(setup_paper)
    root = flow.root
    assert not list((root / "10_Papers").iterdir())  # Preparing never publishes.
    assert not list((root / "90_Attachments").iterdir())
    snapshot = flow.state["draft_hash"]
    flow.publish(snapshot)
    target = Path(flow.state["target"])
    assert split_card(read_text(target))[0]["status"] == "reading"
    assert file_hash(Path(flow.state["attachment"])) == flow.state["source_hash"]
    flow.publish(snapshot)
    assert len(list((root / "10_Papers").glob("*.md"))) == 1
    pass_precheck(flow)
    flow.approve(snapshot, dict.fromkeys(CHECKS, True))
    assert split_card(read_text(target))[0]["status"] == "reviewed"
    flow.approve(snapshot, dict.fromkeys(CHECKS, True))
    audit = json.loads(read_text(flow.run_dir / "approvals.json"))
    assert [entry["action"] for entry in audit] == ["publish_reading", "reviewed"]
    assert audit[-1]["content_hash"] == snapshot
    assert "中文 •" in read_text(flow.run_dir / "analysis.md")


def test_duplicate_requires_popup_consent_and_preserves_user_notes(setup_paper):
    original = prepared(setup_paper)
    original.publish(original.state["draft_hash"])
    target = Path(original.state["target"])
    target.write_text(read_text(target) + "\n用户原有笔记。\n", encoding="utf-8")
    before = target.read_bytes()
    repeat = prepared(setup_paper)
    assert Path(repeat.state["target"]) == target
    with pytest.raises(ValueError, match="明确确认"):
        repeat.publish(repeat.state["draft_hash"])
    assert target.read_bytes() == before
    repeat.publish(repeat.state["draft_hash"], allow_existing=True)
    backup = repeat.run_dir / ("original_" + digest(before) + ".md")
    assert backup.read_bytes() == before
    assert len(list((repeat.root / "10_Papers").glob("*.md"))) == 1


def test_late_user_edit_blocks_overwrite(setup_paper):
    flow = prepared(setup_paper)
    flow.publish(flow.state["draft_hash"])
    pass_precheck(flow)
    target = Path(flow.state["target"])
    target.write_text(read_text(target) + "\n刚编辑的笔记。\n", encoding="utf-8")
    before = target.read_bytes()
    with pytest.raises(ValueError, match="其他操作修改"):
        flow.publish(flow.state["draft_hash"], allow_existing=True)
    with pytest.raises(ValueError, match="未被其他操作修改"):
        flow.approve(flow.state["draft_hash"], dict.fromkeys(CHECKS, True))
    assert target.read_bytes() == before


def test_changed_draft_invalidates_previous_approval(setup_paper):
    flow = prepared(setup_paper)
    old_hash = flow.state["draft_hash"]
    flow.save_draft(flow.draft_text() + "\n[Analysis] 新观察。\n")
    assert flow.state["draft_hash"] != old_hash
    with pytest.raises(ValueError, match="原确认失效"):
        flow.publish(old_hash)


@pytest.mark.parametrize("status", ["reviewed", "used"])
def test_existing_reviewed_or_used_never_downgraded(setup_paper, status):
    first = prepared(setup_paper)
    first.publish(first.state["draft_hash"])
    target = Path(first.state["target"])
    metadata, body = split_card(read_text(target))
    metadata["status"] = status
    target.write_text(render_card(metadata, body), encoding="utf-8")
    before = target.read_bytes()
    flow = prepared(setup_paper)
    with pytest.raises(ValueError, match="reviewed/used"):
        flow.publish(flow.state["draft_hash"], allow_existing=True)
    assert target.read_bytes() == before


def test_cannot_approve_without_all_explicit_checks(setup_paper):
    flow = prepared(setup_paper)
    flow.publish(flow.state["draft_hash"])
    pass_precheck(flow)
    with pytest.raises(ValueError, match="必须由用户确认"):
        flow.approve(flow.state["draft_hash"], {"metadata": True})
    assert split_card(read_text(Path(flow.state["target"])))[0]["status"] == "reading"


def test_review_blockers_cannot_be_bypassed_by_checkboxes(setup_paper):
    flow = prepared(setup_paper)
    flow.save_draft(flow.draft_text().replace("已核查", "待核查"))
    flow.publish(flow.state["draft_hash"])
    with pytest.raises(ValueError, match="审核阻碍"):
        flow.approve(flow.state["draft_hash"], dict.fromkeys(CHECKS, True))


def test_resume_and_close_never_approve(setup_paper):
    flow = prepared(setup_paper)
    flow.publish(flow.state["draft_hash"])
    flow.defer()
    resumed = Workflow.resume(flow.run_dir)
    assert resumed.state["status"] == "waiting_for_approval"
    assert resumed.draft_text() == flow.draft_text()
    assert split_card(read_text(Path(flow.state["target"])))[0]["status"] == "reading"


def test_changed_pdf_blocks_publication(setup_paper):
    flow = prepared(setup_paper)
    Path(flow.config["paper"]["pdf_source"]).write_bytes(b"%PDF-changed")
    with pytest.raises(ValueError, match="PDF 已发生变化"):
        flow.publish(flow.state["draft_hash"])


def test_body_links_and_missing_claims_block_review(setup_paper):
    flow = prepared(setup_paper)
    text = flow.draft_text().replace("[Paper: PDF p. 1, Table 1]", "无来源") + "\n[[Agent-IFC/20_Themes/不存在]]\n"
    report = flow.validate(text)
    assert any("C01 缺少" in item for item in report["review_blockers"])
    assert any("关联链接未找到" in item for item in report["review_blockers"])


def test_editing_yaml_reviewed_cannot_grant_approval(setup_paper):
    flow = prepared(setup_paper)
    flow.save_draft(flow.draft_text().replace("status: reading", "status: reviewed"))
    assert split_card(flow.draft_text())[0]["status"] == "reading"


def test_plain_analysis_preserved_but_not_misrepresented_as_complete_card(setup_paper):
    config, runs = setup_paper
    config["source"].pop("card_path")
    flow = Workflow.create(config, runs)
    flow.prepare()
    assert "中文 • 分析" in flow.draft_text()
    assert any("未整理" in item for item in flow.state["validation"]["review_blockers"])


def test_completed_model_card_quote_repair_preserves_raw_response(setup_paper, monkeypatch):
    config, runs = setup_paper
    original = read_text(Path(config["source"].pop("card_path")))
    response = original.replace("\n---\n", '\ncomparison:\n  trust_boundary: "维持"信任边界"。"\n---\n', 1)
    write_events(Path(config["source"]["events_path"]), events(response))
    flow = Workflow.create(config, runs)
    flow.prepare()
    metadata, body = split_card(flow.draft_text())
    assert metadata["comparison"]["trust_boundary"] == '维持"信任边界"。'
    assert metadata["status"] == "reading"
    assert body == split_card(original)[1].rstrip() + "\n"
    assert not flow.state["validation"]["fatal"]
    assert read_text(flow.run_dir / "analysis.md") == response.strip() + "\n"
    assert json.loads(read_text(flow.run_dir / "yaml-repairs.json"))["changes"][0]["field"] == "comparison.trust_boundary"
    flow.state.update(status="failed", error="旧版 YAML 解析错误")
    flow.save()
    monkeypatch.setattr("agent_ifc.workflow.run_cli", lambda *args: pytest.fail("恢复不能请求模型"))
    recovered = Workflow.recover_completed(flow.run_dir)
    assert recovered.state["status"] == "waiting_for_approval"
    assert recovered.draft_text() == flow.draft_text()
    assert not list((flow.root / "10_Papers").iterdir())


def test_multiple_duplicates_stop_before_publish(setup_paper):
    config, runs = setup_paper
    root = Path(config["project_root"])
    card = Path(config["source"]["card_path"]).read_bytes()
    for name in ("one.md", "two.md"):
        (root / "10_Papers" / name).write_bytes(card)
    flow = Workflow.create(config, runs)
    with pytest.raises(ValueError, match="多张重复"):
        flow.prepare()
    assert flow.state["status"] == "failed"


@pytest.mark.parametrize("change,error", [
    (lambda payload: payload.pop(1), "序列"),
    (lambda payload: payload[-1]["metadata"].update(status="failed"), "成功完成"),
    (lambda payload: payload[1]["metadata"].update(response=""), "结果为空"),
    (lambda payload: payload[1].update(turn_id="another"), "不能混合"),
    (lambda payload: payload[1]["metadata"].update(response="乱码\ufffd"), "替换字符"),
])
def test_invalid_event_logs_fail(tmp_path, change, error):
    path = tmp_path / "log.ndjson"
    payload = events()
    change(payload)
    write_events(path, payload)
    with pytest.raises(ValueError, match=error):
        parse_events(path)


def test_malformed_or_wrong_encoding_logs_rejected(tmp_path):
    path = tmp_path / "log.ndjson"
    path.write_text("not-json\n", encoding="utf-8")
    with pytest.raises(ValueError, match="不是完整 JSON"):
        parse_events(path)
    path.write_text("中文", encoding="utf-16")
    with pytest.raises(UnicodeError):
        parse_events(path)


def test_path_traversal_rejected(tmp_path):
    with pytest.raises(ValueError, match="超出"):
        within(tmp_path / "vault", "../outside.md")


def test_supplement_passes_question_session_and_new_approval_snapshot(setup_paper, monkeypatch):
    flow = prepared(setup_paper)
    calls = []
    metadata, body = split_card(flow.draft_text())
    response = render_card(metadata, body + "\n[Analysis] 补充核验。\n")
    def fake_analyze(self, question="", session=None):
        calls.append((question, session))
        assert self.cancel is flow.cancel
        return response, {"session_id": "s2", "turn_id": "t2", "event_count": 3}
    monkeypatch.setattr(Workflow, "analyze_live", fake_analyze)
    child = flow.supplement("请补充 Table 2 的数值")
    assert calls == [("请补充 Table 2 的数值", "s1")]
    assert child.run_dir != flow.run_dir
    assert child.state["draft_hash"] != flow.state["draft_hash"]
    assert json.loads(read_text(child.run_dir / "approvals.json")) == []
    assert not list((flow.root / "10_Papers").glob("*.md"))


def test_second_prepared_run_cannot_replace_newly_published_card(setup_paper):
    first = prepared(setup_paper)
    second = prepared(setup_paper)
    first.publish(first.state["draft_hash"])
    before = Path(first.state["target"]).read_bytes()
    with pytest.raises(ValueError, match="其他操作修改"):
        second.publish(second.state["draft_hash"], allow_existing=True)
    assert Path(first.state["target"]).read_bytes() == before


def test_completed_run_cannot_be_edited_back_to_reading(setup_paper):
    flow = prepared(setup_paper)
    flow.publish(flow.state["draft_hash"])
    pass_precheck(flow)
    flow.approve(flow.state["draft_hash"], dict.fromkeys(CHECKS, True))
    with pytest.raises(ValueError, match="审核已完成"):
        flow.save_draft(flow.draft_text() + "\n新编辑")
    assert flow.state["status"] == "reviewed"


def test_recover_completed_warning_log_and_fenced_card_without_model_or_publish(setup_paper, monkeypatch):
    config, runs = setup_paper
    original = prepared(setup_paper)
    original.publish(original.state["draft_hash"])
    target = Path(original.state["target"])
    unchanged = target.read_bytes()
    response = "说明：\n\n````markdown\n" + original.draft_text() + "\n```text\n内层代码块\n```\n````\n后记"
    original_log = original.run_dir / "deeptutor-events.ndjson"
    write_events(original_log, events(response))
    original_log.write_text(
        "Warning: No prompt file found for chat/context_summary_agent\n" + read_text(original_log),
        encoding="utf-8",
    )
    original.state.update(status="failed", error="old parse failure")
    original.save()
    before = {path.name: path.read_bytes() for path in original.run_dir.iterdir()}
    def forbidden_model(*args, **kwargs):
        raise AssertionError("recovery must not call a model")
    monkeypatch.setattr(Workflow, "analyze_live", forbidden_model)
    child = Workflow.recover_completed(original.run_dir)
    assert child.run_dir != original.run_dir
    assert child.state["status"] == "waiting_for_approval"
    assert not child.state["validation"]["fatal"]
    assert "内层代码块" in child.draft_text()
    assert "后记" not in child.draft_text()
    assert "原始分析（待整理）" not in child.draft_text()
    assert len(child.state["stdout_warnings"]) == 1
    assert child.state["recovered_from"] == str(original.run_dir)
    assert json.loads(read_text(child.run_dir / "approvals.json")) == []
    assert target.read_bytes() == unchanged
    assert {path.name: path.read_bytes() for path in original.run_dir.iterdir()} == before


def test_recovery_refuses_incomplete_turn_or_changed_pdf(setup_paper):
    original = prepared(setup_paper)
    original.state["status"] = "failed"
    original.save()
    write_events(original.run_dir / "deeptutor-events.ndjson", events(status="failed"))
    with pytest.raises(ValueError, match="成功完成"):
        Workflow.recover_completed(original.run_dir)
    write_events(original.run_dir / "deeptutor-events.ndjson", events())
    Path(original.config["paper"]["pdf_source"]).write_bytes(b"%PDF-another")
    with pytest.raises(ValueError, match="PDF 已变化"):
        Workflow.recover_completed(original.run_dir)


def test_supplement_failure_reports_child_and_sends_current_draft(setup_paper, monkeypatch):
    original = prepared(setup_paper)
    created = []
    def failing_model(self, *args):
        assert self.config["supplement_draft"] == original.draft_text()
        raise ValueError("provider failed")
    monkeypatch.setattr(Workflow, "analyze_live", failing_model)
    with pytest.raises(ValueError, match="provider failed"):
        original.supplement("check", on_created=created.append)
    assert len(created) == 1
    assert created[0].state["status"] == "failed"
    assert original.state["status"] == "waiting_for_approval"


def test_multiple_or_unterminated_card_fences_are_not_silently_selected():
    with pytest.raises(ValueError, match="多张"):
        extract_card("```md\n---\na: b\n---\none\n```\n```md\n---\na: b\n---\ntwo\n```")
    with pytest.raises(ValueError, match="没有结束"):
        extract_card("````markdown\n---\na: b\n---\ntruncated")


@pytest.mark.parametrize("styled", ["**C01**", "`C01`", "__C01__"])
def test_formatted_claim_id_still_requires_human_verification(setup_paper, styled):
    flow = prepared(setup_paper)
    report = flow.validate(flow.draft_text().replace("| C01 |", "| " + styled + " |")
                           .replace("已核查", "待核查"))
    assert report["claim_ids"] == ["C01"]
    assert any("C01 仍标记" in item for item in report["review_blockers"])
