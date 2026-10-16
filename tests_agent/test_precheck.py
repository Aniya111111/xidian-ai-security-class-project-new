import json
from pathlib import Path

import pytest

from agent_ifc.precheck import Precheck, json_object
from agent_ifc.storage import read_text, split_card, write_json
from agent_ifc.workflow import CHECKS, Workflow
from tests_agent.test_workflow import prepared, setup_paper, write_events, events, pass_precheck


def response(verdict="supported", issues=None, unresolved=None):
    return {"summary": "已逐条对照原文核查。",
            "claims": [{"claim_id": "C01", "verdict": verdict, "evidence": "原文证据",
                        "locator": "PDF p. 1, Table 1", "reason": "结论与表格一致"}],
            "issues": issues or [], "unresolved": unresolved or []}


def grounded_events(payload):
    result = events(json.dumps(payload, ensure_ascii=False))
    result[1:1] = [
        {"type": "tool_call", "turn_id": "t1", "metadata": {"tool_name": "rag", "call_id": "rag-1",
            "args": {"kb_name": "configured-single-paper-kb", "query": "证据"}}},
        {"type": "tool_result", "turn_id": "t1", "metadata": {"tool_name": "rag", "call_id": "rag-1",
            "tool_metadata": {"answer": "原论文证据", "sources": []}}},
    ]
    for seq, event in enumerate(result, 1):
        event["seq"] = seq
    return result


def install_fake_cli(monkeypatch, payloads):
    calls = []
    def fake(config, prompt, run_dir, cancel, report, session=None, output_prefix="deeptutor", **kwargs):
        calls.append((prompt, output_prefix))
        payload = payloads.pop(0)
        path = run_dir / f"{output_prefix}-events.ndjson"
        assert kwargs["attach_knowledge_base"] is True
        assert kwargs["seed_query"] == "测试幻觉防御"
        write_events(path, grounded_events(payload))
        return path
    monkeypatch.setattr("agent_ifc.precheck.run_cli", fake)
    return calls


def publish_ready(setup_paper):
    flow = prepared(setup_paper)
    flow.publish(flow.state["draft_hash"])
    return flow


def test_precheck_is_hash_bound_covers_every_claim_and_enables_exception_review(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    calls = install_fake_cli(monkeypatch, [response()])
    result = Precheck(flow).run()
    assert result["draft_hash"] == flow.state["draft_hash"]
    assert result["claims"][0]["claim_id"] == "C01"
    assert "不能自动 reviewed" not in calls[0][0]  # Uses card + KB, not rule text as authority.
    assert "不得" in calls[0][0] and calls[0][1] == "precheck-01"
    # A supported Cxx no longer asks the user to discover and mark it manually.
    assert not any("C01 仍标记" in item for item in flow.validate(flow.draft_text())["review_blockers"])
    flow.approve(flow.state["draft_hash"], dict.fromkeys(CHECKS, True))
    target = read_text(Path(flow.state["target"]))
    assert split_card(target)[0]["status"] == "reviewed"
    assert "AI 预审支持；用户最终确认" in target


@pytest.mark.parametrize("mutator,error", [
    (lambda r: r.update(claims=[]), "未覆盖全部"),
    (lambda r: r["claims"].append(dict(r["claims"][0])), "缺失、重复"),
    (lambda r: r["claims"][0].update(verdict="maybe"), "verdict"),
    (lambda r: r["claims"][0].update(locator=""), "证据摘录"),
    (lambda r: r.update(summary=""), "缺少摘要"),
])
def test_malformed_precheck_cannot_be_used(setup_paper, mutator, error):
    flow = publish_ready(setup_paper)
    value = response()
    mutator(value)
    with pytest.raises(ValueError, match=error):
        Precheck(flow).validate(value, flow.draft_text())


def test_unsupported_claim_blocks_review_even_if_user_checks_boxes(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    install_fake_cli(monkeypatch, [response(verdict="insufficient_evidence")])
    Precheck(flow).run()
    with pytest.raises(ValueError, match="审核阻碍|未解决项"):
        flow.approve(flow.state["draft_hash"], dict.fromkeys(CHECKS, True))


def test_high_risk_issue_requires_decision(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    issue = {"id": "I01", "severity": "high", "category": "boundary", "description": "边界不明确",
             "claim_id": None, "evidence": "原文", "locator": "PDF p. 2", "suggested_old": "",
             "suggested_new": "", "confidence": 0.7}
    install_fake_cli(monkeypatch, [response(issues=[issue])])
    precheck = Precheck(flow)
    precheck.run()
    with pytest.raises(ValueError, match="I01"):
        flow.approve(flow.state["draft_hash"], dict.fromkeys(CHECKS, True))
    precheck.resolve({"I01": "accept"})
    flow.approve(flow.state["draft_hash"], dict.fromkeys(CHECKS, True))


def test_edit_invalidates_precheck_and_old_approval(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    install_fake_cli(monkeypatch, [response()])
    Precheck(flow).run()
    flow.save_draft(flow.draft_text() + "\n用户编辑。\n")
    assert flow.state["precheck"]["status"] == "stale"
    with pytest.raises(ValueError, match="预审失效|原确认失效"):
        Precheck(flow).load()


def test_structure_repair_reuses_saved_precheck_without_model(setup_paper, monkeypatch):
    flow = prepared(setup_paper)
    text = flow.draft_text().replace(
        "## 01 章节",
        "## 00 本次定向核查\n\n| C01 | 摘要行 |\n\n## 01 章节",
    )
    flow.save_draft(text)
    flow.publish(flow.state["draft_hash"])
    before = flow.state["draft_hash"]
    pass_precheck(flow)
    monkeypatch.setattr("agent_ifc.precheck.run_cli",
                        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("no model")))

    result = Precheck(flow).repair_format_and_reuse()

    assert result["draft_hash"] != before
    assert "### 00 本次定向核查" in flow.draft_text()
    assert "| 核查-C01 | 摘要行 |" in flow.draft_text()
    assert not result["validation"]["fatal"]
    assert not result["validation"]["review_blockers"]
    cached = Precheck(flow).load()
    assert cached["reused_without_model"] is True
    assert cached["reuse_history"][-1]["from_hash"] == before
    assert Path(flow.state["target"]).read_text(encoding="utf-8") == flow.draft_text()
    assert list(flow.run_dir.glob("draft-before-format-repair-*.md"))
    assert list(flow.run_dir.glob("precheck-before-format-repair-*.json"))


def test_resume_recovers_structure_repair_after_stale_gui_state_save(setup_paper, monkeypatch):
    flow = prepared(setup_paper)
    flow.save_draft(flow.draft_text().replace(
        "## 01 章节", "## 00 核查\n\n| C01 | 摘要 |\n\n## 01 章节"))
    flow.publish(flow.state["draft_hash"])
    stale = json.loads(json.dumps(flow.state))
    pass_precheck(flow)
    Precheck(flow).repair_format_and_reuse()
    repaired_hash = flow.state["draft_hash"]

    # Simulate an old window closing after the external repair.
    write_json(flow.run_dir / "state.json", stale)
    resumed = Workflow.resume(flow.run_dir)

    assert resumed.state["draft_hash"] == repaired_hash
    assert resumed.state["published_hash"] == repaired_hash
    assert resumed.state["precheck"]["repair_scope"] == "structure_only"
    assert not resumed.state["validation"]["review_blockers"]


def test_repeated_precheck_uses_cache_and_preserves_decisions_until_forced(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    issue = {"id": "I01", "severity": "high", "category": "boundary", "description": "范围待确认",
             "claim_id": None, "evidence": "原文", "locator": "PDF p. 2", "suggested_old": "",
             "suggested_new": "", "confidence": 0.7}
    calls = install_fake_cli(monkeypatch, [response(issues=[issue]), response()])
    precheck = Precheck(flow)
    precheck.run()
    precheck.resolve({"I01": "accept"})
    original = precheck.path.read_bytes()
    cached = precheck.run()
    assert len(calls) == 1
    assert cached["decisions"] == {"I01": "accept"}
    assert precheck.path.read_bytes() == original
    precheck.run(force=True)
    assert len(calls) == 2


def test_cache_refuses_changed_pdf(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    calls = install_fake_cli(monkeypatch, [response()])
    precheck = Precheck(flow)
    precheck.run()
    Path(flow.config["paper"]["pdf_source"]).write_bytes(b"changed pdf")
    with pytest.raises(ValueError, match="PDF 已发生变化"):
        precheck.run()
    assert len(calls) == 1


def test_reverted_edit_can_restore_matching_saved_precheck(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    text = flow.draft_text()
    calls = install_fake_cli(monkeypatch, [response()])
    precheck = Precheck(flow)
    precheck.run()
    flow.save_draft(text + "\n实质变更。\n")
    flow.save_draft(text)
    assert flow.state["precheck"]["status"] == "stale"
    precheck.run()
    assert len(calls) == 1
    assert flow.state["precheck"]["status"] == "ready"
    assert flow.state["precheck"]["draft_hash"] == flow.state["draft_hash"]


def test_incomplete_structure_repair_preserves_all_current_files(setup_paper):
    flow = prepared(setup_paper)
    flow.save_draft(flow.draft_text().replace("## 01 章节", "## 00 补充\n\n## 01 章节")
                    .replace("## 02 章节", "## 缺失编号章节"))
    flow.publish(flow.state["draft_hash"])
    pass_precheck(flow)
    paths = [flow.run_dir / "draft.md", flow.run_dir / "state.json", flow.run_dir / "precheck.json",
             Path(flow.state["target"])]
    before = {path: path.read_bytes() for path in paths}
    with pytest.raises(ValueError, match="原草稿和预审保持不变"):
        Precheck(flow).repair_format_and_reuse()
    assert {path: path.read_bytes() for path in paths} == before


def test_reuse_does_not_resolve_unsupported_claims(setup_paper):
    flow = prepared(setup_paper)
    flow.save_draft(flow.draft_text().replace("## 01 章节", "## 00 补充\n\n## 01 章节"))
    flow.publish(flow.state["draft_hash"])
    review = pass_precheck(flow)
    review["claims"][0]["verdict"] = "insufficient_evidence"
    review["blockers"] = [{"id": "C01", "reason": "insufficient_evidence"}]
    write_json(flow.run_dir / "precheck.json", review)
    Precheck(flow).repair_format_and_reuse()
    with pytest.raises(ValueError, match="C01"):
        flow.approve(flow.state["draft_hash"], dict.fromkeys(CHECKS, True))


def test_safe_fix_applies_exact_body_text_then_rechecks(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    issue = {"id": "I01", "severity": "medium", "category": "boundary", "description": "措辞过强",
             "claim_id": None, "evidence": "原文", "locator": "PDF p. 2",
             "suggested_old": "## 03 章节\n\n正文。",
             "suggested_new": "## 03 章节\n\n正文（范围受限）。", "confidence": 0.95}
    install_fake_cli(monkeypatch, [response(issues=[issue]), response()])
    result = Precheck(flow).run()
    assert "正文（范围受限）。" in flow.draft_text()
    assert "正文（范围受限）。" in read_text(Path(flow.state["target"]))
    assert result["auto_fixes"]["issue_ids"] == ["I01"]
    assert result["draft_hash"] == flow.state["draft_hash"]
    assert (flow.run_dir / "precheck-01.json").is_file()
    assert (flow.run_dir / "precheck-02.json").is_file()
    flow.approve(flow.state["draft_hash"], dict.fromkeys(CHECKS, True))


@pytest.mark.parametrize("old,new", [("title: 测试幻觉防御", "title: 另一个"),
                                      ("正文。", "C99 新结论")])
def test_unsafe_fixes_never_auto_apply(setup_paper, monkeypatch, old, new):
    flow = publish_ready(setup_paper)
    before = flow.draft_text()
    issue = {"id": "I01", "severity": "medium", "category": "other", "description": "建议",
             "claim_id": None, "evidence": "证据", "locator": "PDF p. 2", "suggested_old": old,
             "suggested_new": new, "confidence": 0.99}
    install_fake_cli(monkeypatch, [response(issues=[issue])])
    result = Precheck(flow).run()
    assert flow.draft_text() == before and "auto_fixes" not in result


def test_failed_precheck_is_auditable_and_does_not_review(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    def fail(*args, **kwargs):
        raise RuntimeError("provider unavailable")
    monkeypatch.setattr("agent_ifc.precheck.run_cli", fail)
    with pytest.raises(RuntimeError, match="unavailable"):
        Precheck(flow).run()
    assert flow.state["precheck"]["status"] == "failed"
    assert (flow.run_dir / "precheck-01-error.json").is_file()
    with pytest.raises(ValueError, match="尚未完成"):
        flow.approve(flow.state["draft_hash"], dict.fromkeys(CHECKS, True))


def test_completed_precheck_log_can_be_recovered_without_model(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    path = flow.run_dir / "precheck-01-events.ndjson"
    write_events(path, grounded_events(response()))
    monkeypatch.setattr("agent_ifc.precheck.run_cli",
                        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("no model")))
    result = Precheck(flow).recover_completed(path)
    assert result["claims"][0]["verdict"] == "supported"
    assert flow.state["precheck"]["status"] == "ready"
    assert flow.state["precheck"]["recovered_from"] == str(path.resolve())


@pytest.mark.parametrize("raw", ["not json", "[]", "```json\n{}", "前言 {}"])
def test_only_one_complete_json_object_is_accepted(raw):
    with pytest.raises(ValueError):
        json_object(raw)


def test_missing_rag_does_not_apply_edits_or_mark_precheck_ready(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    before = flow.draft_text()
    path = flow.run_dir / "precheck-01-events.ndjson"
    write_events(path, events(json.dumps(response(), ensure_ascii=False)))
    with pytest.raises(ValueError, match="没有成功检索"):
        Precheck(flow).recover_completed(path)
    assert flow.draft_text() == before
    assert flow.state["precheck"]["status"] == "failed"


def test_recursive_failure_keeps_new_draft_hash_and_attempt(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    issue = {"id": "I01", "severity": "medium", "category": "boundary", "description": "措辞",
             "claim_id": None, "evidence": "原文", "locator": "PDF p. 2",
             "suggested_old": "## 03 章节\n\n正文。", "suggested_new": "## 03 章节\n\n限定范围。",
             "confidence": 0.95}
    def fake(config, prompt, run_dir, cancel, report, **kwargs):
        if kwargs["output_prefix"] == "precheck-02":
            raise TimeoutError("结束阶段超时")
        path = run_dir / "precheck-01-events.ndjson"
        write_events(path, grounded_events(response(issues=[issue])))
        return path
    monkeypatch.setattr("agent_ifc.precheck.run_cli", fake)
    with pytest.raises(TimeoutError):
        Precheck(flow).run()
    assert flow.state["precheck"]["draft_hash"] == flow.state["draft_hash"]
    assert flow.state["precheck"]["attempt"] == 2
    assert not (flow.run_dir / "precheck-01-error.json").exists()


def test_recovery_rejects_changed_draft_snapshot(setup_paper):
    flow = publish_ready(setup_paper)
    path = flow.run_dir / "precheck-01-events.ndjson"
    write_events(path, grounded_events(response()))
    write_json(flow.run_dir / "precheck-01-input.json", {"draft_hash": flow.state["draft_hash"]})
    flow.save_draft(flow.draft_text() + "\n新的用户编辑。")
    with pytest.raises(ValueError, match="草稿已变化"):
        Precheck(flow).recover_completed(path)


def two_claims(flow):
    row = next(line for line in flow.draft_text().splitlines() if line.startswith("| C01 |"))
    flow.save_draft(flow.draft_text().replace(row, row + "\n" + row.replace("C01", "C02")))
    flow.publish(flow.state["draft_hash"], allow_existing=True)
    payload = response()
    payload["claims"].append({**payload["claims"][0], "claim_id": "C02"})
    return payload


def test_incremental_keeps_unaffected_evidence_and_user_decisions(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    payload = two_claims(flow)
    payload["issues"] = [{"id": "I01", "claim_id": "C02", "severity": "low", "category": "claim",
                          "description": "边界提示", "evidence": "原文", "locator": "p.1",
                          "suggested_old": "", "suggested_new": "", "confidence": 0.8}]
    calls = install_fake_cli(monkeypatch, [payload, response()])
    precheck = Precheck(flow)
    first = precheck.run()
    precheck.resolve({"I01": "keep"})
    flow.save_draft(flow.draft_text().replace("| C01 | 实验 | 结论 |", "| C01 | 实验 | 修订后的结论 |"))
    result = precheck.run()
    assert len(calls) == 2
    assert result["review_scope"] == ["C01"]
    assert result["decisions"] == {"I01": "keep"}
    assert result["claims"][0] == first["claims"][1]
    assert '必须覆盖的结论编号：["C01"]' in calls[1][0]
    assert flow.state["precheck"]["draft_hash"] == flow.state["draft_hash"]


@pytest.mark.parametrize("edit", ["body", "metadata", "remove", "force", "global_issue", "unresolved"])
def test_shared_changes_and_uncertainty_require_full_review(setup_paper, monkeypatch, edit):
    flow = publish_ready(setup_paper)
    payload = two_claims(flow)
    if edit == "global_issue":
        payload["issues"] = [{"id": "I01", "claim_id": None, "severity": "low", "category": "other",
                              "description": "全局", "evidence": "", "locator": "",
                              "suggested_old": "", "suggested_new": "", "confidence": 0.5}]
    if edit == "unresolved":
        payload["unresolved"] = ["全局待核查"]
    second = json.loads(json.dumps(payload))
    calls = install_fake_cli(monkeypatch, [payload, second])
    precheck = Precheck(flow)
    precheck.run()
    text = flow.draft_text().replace("| C01 | 实验 | 结论 |", "| C01 | 实验 | 修改 |")
    if edit == "body":
        text += "\n新的方法解释。\n"
    if edit == "metadata":
        text = text.replace("venue: ''", "venue: new venue")
    if edit == "remove":
        text = "\n".join(line for line in text.splitlines() if not line.startswith("| C02 |"))
        second["claims"] = [second["claims"][0]]
    flow.save_draft(text)
    result = precheck.run(force=edit == "force")
    assert result["review_scope"] == "full"
    assert len(calls) == 2


def test_dependency_reference_expands_incremental_scope(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    payload = two_claims(flow)
    flow.save_draft(flow.draft_text().replace("| C02 | 实验 | 结论 |", "| C02 | 实验 | 基于 C01 |"))
    calls = install_fake_cli(monkeypatch, [payload, payload])
    precheck = Precheck(flow)
    precheck.run()
    flow.save_draft(flow.draft_text().replace("| C01 | 实验 | 结论 |", "| C01 | 实验 | 修改 |"))
    assert precheck.run()["review_scope"] == ["C01", "C02"]
    assert len(calls) == 2


def test_format_preflight_repairs_before_model_and_blocks_missing_sections(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    flow.save_draft(flow.draft_text().replace("## 01 章节", "## 00 补充\n\n## 01 章节"))
    calls = install_fake_cli(monkeypatch, [response()])
    Precheck(flow).run()
    assert "### 00 补充" in calls[0][0]
    assert list(flow.run_dir.glob("draft-before-preflight-*.md"))
    flow.save_draft(flow.draft_text().replace("## 02 章节", "## 缺失章节"))
    with pytest.raises(ValueError, match="格式检查未通过"):
        Precheck(flow).run()
    assert len(calls) == 1


def test_failed_incremental_can_recover_scoped_events_without_new_model(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    payload = two_claims(flow)
    install_fake_cli(monkeypatch, [payload])
    precheck = Precheck(flow)
    precheck.run()
    flow.save_draft(flow.draft_text().replace("| C01 | 实验 | 结论 |", "| C01 | 实验 | 修改 |"))
    def interrupted(config, prompt, run_dir, *args, **kwargs):
        write_events(run_dir / (kwargs["output_prefix"] + "-events.ndjson"), grounded_events(response()))
        raise TimeoutError("归档失败")
    monkeypatch.setattr("agent_ifc.precheck.run_cli", interrupted)
    with pytest.raises(TimeoutError):
        precheck.run()
    recovered = precheck.recover_completed(flow.run_dir / "precheck-02-events.ndjson")
    assert recovered["review_scope"] == ["C01"]
    assert len(recovered["claims"]) == 2


def test_incremental_does_not_reuse_changed_claim_decisions_or_hide_bad_output(setup_paper, monkeypatch):
    flow = publish_ready(setup_paper)
    payload = two_claims(flow)
    payload["issues"] = [{"id": "I01", "claim_id": "C01", "severity": "high", "category": "claim",
                          "description": "错误", "evidence": "原文", "locator": "p.1",
                          "suggested_old": "", "suggested_new": "", "confidence": 0.8}]
    calls = install_fake_cli(monkeypatch, [payload, response("insufficient_evidence"), response()])
    precheck = Precheck(flow)
    precheck.run()
    precheck.resolve({"I01": "keep"})
    flow.save_draft(flow.draft_text().replace("| C01 | 实验 | 结论 |", "| C01 | 实验 | 修改 |"))
    result = precheck.run()
    assert result["decisions"] == {} and result["issues"] == []
    assert result["blockers"] == [{"id": "C01", "reason": "insufficient_evidence"}]
    with pytest.raises(ValueError, match="C01"):
        flow.approve(flow.state["draft_hash"], dict.fromkeys(CHECKS, True))
    previous = precheck.path.read_bytes()
    flow.save_draft(flow.draft_text().replace("| C02 | 实验 | 结论 |", "| C02 | 实验 | 修改 |"))
    with pytest.raises(ValueError, match="不属于当前草稿"):
        precheck.run()
    assert precheck.path.read_bytes() == previous
    assert len(calls) == 3
