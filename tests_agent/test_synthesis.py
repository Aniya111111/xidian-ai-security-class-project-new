import json
from pathlib import Path

import pytest

from agent_ifc.storage import file_hash, read_text, render_card, split_card
from agent_ifc.synthesis import BEGIN, END, SynthesisWorkflow


@pytest.fixture
def library(tmp_path):
    root = tmp_path / "vault" / "Agent-IFC"
    for folder in ("10_Papers", "20_Themes", "90_Runs"):
        (root / folder).mkdir(parents=True)
    config = {"project_root": str(root), "vault_root": str(root.parent),
              "synthesis": {"target": "20_Themes/幻觉防御.md", "keywords": ["幻觉", "hallucination"]}}
    def paper(name="a", status="reviewed", title="幻觉防御方法", **extra):
        meta = {"schema_version": 1, "type": "paper", "paper_id": name, "title": title,
                "year": 2024, "status": status, "topics": ["hallucination"], **extra}
        body = "\n\n".join(f"## {i:02} 章节\n\n原文 {i}：中文 • ✅ 证据，尚不能推出通用结论。"
                            for i in range(1, 17))
        path = root / "10_Papers" / (name + ".md")
        path.write_text(render_card(meta, body), encoding="utf-8")
        return path
    return config, root, paper


def test_reviewed_only_filter_and_single_paper_warning(library, tmp_path):
    config, root, paper = library
    included = paper()
    paper("reading", "reading")
    paper("used", "used")
    paper("unrelated", title="课程知识图谱", topics=["知识图谱"])
    before = {p.name: p.read_bytes() for p in (root / "10_Papers").iterdir()}
    flow = SynthesisWorkflow.create(config, tmp_path / "runs")
    assert flow.state["source_count"] == 1
    assert flow.state["sources"][0]["path"] == str(included)
    assert "当前仅 1 篇" in flow.draft_text()
    assert "未明确记录，待确认" in flow.draft_text()
    assert "不能直接排名" in flow.draft_text()
    assert "中文 • ✅" in flow.draft_text()
    assert not flow.state["validation"]["fatal"]
    assert not flow.target().exists()
    assert json.loads(read_text(flow.run_dir / "approvals.json")) == []
    assert {p.name: p.read_bytes() for p in (root / "10_Papers").iterdir()} == before


def test_confirmed_publish_backup_and_managed_region_preserves_handwritten_notes(library):
    config, root, paper = library
    source = paper()
    paper("b", comparison={"defense_stage": "生成前预防", "external_resources": "需核对资源边界",
                           "model_access": "卡片明示白盒"})
    target = root / "20_Themes/幻觉防御.md"
    original = "---\ntype: theme\ncustom: 保留\n---\n# 我的主题\n\n手写内容 •\n" + BEGIN + "\n旧表\n" + END + "\n\n尾部用户笔记\n"
    target.write_text(original, encoding="utf-8")
    source_bytes = source.read_bytes()
    flow = SynthesisWorkflow.create(config)
    assert "生成前预防" in read_text(flow.run_dir / "comparison.md")
    assert "当前仅 1 篇" not in flow.draft_text()
    assert flow.draft_text().startswith(original[:original.index(BEGIN)])
    assert flow.draft_text().endswith(original[original.index(END) + len(END):])
    assert "旧表" not in flow.draft_text()
    before = target.read_bytes()
    with pytest.raises(ValueError, match="明确确认"):
        flow.publish(flow.state["draft_hash"], confirmed=False)
    assert target.read_bytes() == before
    flow.publish(flow.state["draft_hash"], confirmed=True)
    flow.publish(flow.state["draft_hash"], confirmed=True)
    assert flow.state["status"] == "published"
    backups = list(flow.run_dir.glob("original_theme_*.md"))
    assert len(backups) == 1 and backups[0].read_bytes() == before
    assert source.read_bytes() == source_bytes
    assert split_card(read_text(source))[0]["status"] == "reviewed"
    actions = json.loads(read_text(flow.run_dir / "approvals.json"))
    assert len(actions) == 1 and actions[0]["action"] == "publish_synthesis"
    assert actions[0]["details"]["sources"][0]["sha256"] == file_hash(source)


def test_appends_block_to_existing_theme_without_erasing_user_content(library):
    config, root, paper = library
    paper()
    target = root / "20_Themes/幻觉防御.md"
    original = "# 幻觉防御\n\n我的自定义笔记\n"
    target.write_text(original, encoding="utf-8")
    flow = SynthesisWorkflow.create(config)
    assert flow.draft_text().startswith(original)
    flow.publish(flow.state["draft_hash"], confirmed=True)
    assert read_text(target).count(BEGIN) == 1


@pytest.mark.parametrize("change", ["body", "status", "delete"])
def test_changed_source_prevents_publication(library, change):
    config, root, paper = library
    source = paper()
    flow = SynthesisWorkflow.create(config)
    if change == "body":
        source.write_text(read_text(source) + "\n新的人工修改", encoding="utf-8")
    elif change == "status":
        source.write_text(read_text(source).replace("status: reviewed", "status: reading"), encoding="utf-8")
    else:
        source.unlink()
    with pytest.raises(ValueError, match="来源卡片已变化"):
        flow.publish(flow.state["draft_hash"], confirmed=True)
    assert not flow.target().exists()


def test_changed_theme_and_stale_draft_prevent_overwrite(library):
    config, root, paper = library
    paper()
    flow = SynthesisWorkflow.create(config)
    old = flow.state["draft_hash"]
    flow.save_draft(flow.draft_text() + "\n新增研究问题\n")
    with pytest.raises(ValueError, match="草稿已修改"):
        flow.publish(old, confirmed=True)
    flow.target().write_text("用户刚创建的笔记", encoding="utf-8")
    with pytest.raises(ValueError, match="主题笔记已被其他操作修改"):
        flow.publish(flow.state["draft_hash"], confirmed=True)
    assert read_text(flow.target()) == "用户刚创建的笔记"


def test_resume_does_not_publish_or_approve(library):
    config, root, paper = library
    paper()
    flow = SynthesisWorkflow.create(config)
    resumed = SynthesisWorkflow.resume(flow.run_dir)
    assert resumed.state["status"] == "waiting_for_approval"
    assert resumed.draft_text() == flow.draft_text()
    assert json.loads(read_text(flow.run_dir / "approvals.json")) == []
    assert not resumed.target().exists()


def test_source_selection_is_enforced(library):
    config, root, paper = library
    a, b = paper("a"), paper("b")
    flow = SynthesisWorkflow.create(config, selected=[str(b)])
    assert [s["paper_id"] for s in flow.state["sources"]] == ["b"]
    with pytest.raises(ValueError, match="选择的卡片已变化"):
        SynthesisWorkflow.create(config, selected=[str(root / "10_Papers/missing.md")])


@pytest.mark.parametrize("target", ["../escape.md", "10_Papers/论文.md", "20_Themes/file.txt"])
def test_target_path_boundary(library, target):
    config, root, paper = library
    paper()
    config["synthesis"]["target"] = target
    with pytest.raises(ValueError):
        SynthesisWorkflow.create(config)


def test_marker_and_source_link_guards(library):
    config, root, paper = library
    paper()
    flow = SynthesisWorkflow.create(config)
    with pytest.raises(ValueError, match="标记"):
        flow.save_draft(flow.draft_text().replace(END, ""))
    with pytest.raises(ValueError, match="来源链接"):
        flow.save_draft(flow.draft_text().replace("Agent-IFC/10_Papers/a", "另一个来源"))


def test_empty_library_and_duplicate_markers_fail(library):
    config, root, paper = library
    paper(status="reading")
    with pytest.raises(ValueError, match="没有符合主题"):
        SynthesisWorkflow.create(config)
    paper(status="reviewed")
    (root / "20_Themes/幻觉防御.md").write_text(BEGIN + BEGIN + END, encoding="utf-8")
    with pytest.raises(ValueError, match="标记"):
        SynthesisWorkflow.create(config)


def test_table_pipes_are_escaped_and_no_model_is_called(library, monkeypatch):
    config, root, paper = library
    paper(comparison={"defense_stage": "A | B"})
    def forbidden(*args, **kwargs):
        raise AssertionError("synthesis must not invoke a model")
    monkeypatch.setattr("agent_ifc.workflow.Workflow.analyze_live", forbidden)
    flow = SynthesisWorkflow.create(config)
    comparison = read_text(flow.run_dir / "comparison.md")
    assert "A \\| B" in comparison
    assert "a\\|" in comparison  # Wiki alias pipe is escaped in Markdown tables.


def test_configurable_multi_agent_security_topic_requires_collaboration_and_security(library):
    config, root, paper = library
    config["synthesis"] = {
        "theme_id": "multi-agent-security",
        "title": "多Agent协作的安全防护",
        "target": "20_Themes/多Agent协作的安全防护.md",
        "keywords": ["agent", "代理"],
        "required_keyword_groups": [["security", "安全", "attack"]],
        "comparison_columns": [
            {"key": "attacker_capability", "label": "攻击者能力", "labels": ["攻击者能力"]},
            {"key": "trust_boundary", "label": "信任边界与权限", "labels": ["信任边界"]},
        ],
        "comparison_boundary": "威胁模型不同，不直接排名。",
        "followup": "补齐共谋和共享记忆攻击论文。",
    }
    included = paper("included", title="Security of Multi-Agent Collaboration",
                     comparison={"attacker_capability": "恶意成员", "trust_boundary": "编排器边界"})
    paper("security-only", title="LLM Security")
    paper("agents-only", title="Multi-Agent Planning")
    flow = SynthesisWorkflow.create(config)
    assert [source["path"] for source in flow.state["sources"]] == [str(included)]
    assert flow.target().name == "多Agent协作的安全防护.md"
    assert "title: 多Agent协作的安全防护" in flow.draft_text()
    assert "tags:\n- theme\n- multi-agent-security" in flow.draft_text()
    assert "<!-- Agent-IFC:multi-agent-security-synthesis:begin -->" in flow.draft_text()
    assert "### 多Agent协作的安全防护对比表" in flow.draft_text()
    assert "| 论文 | 攻击者能力 | 信任边界与权限 | 数据与评估摘录 | 结论摘录 | 局限摘录 |" in flow.draft_text()
    assert "恶意成员" in flow.draft_text() and "编排器边界" in flow.draft_text()
    assert "威胁模型不同，不直接排名。" in flow.draft_text()
    assert "补齐共谋和共享记忆攻击论文。" in flow.draft_text()


@pytest.mark.parametrize("bad", [
    {"title": "坏\n标题"},
    {"theme_id": "Bad ID"},
    {"comparison_columns": []},
    {"required_keyword_groups": ["security"]},
])
def test_invalid_topic_configuration_is_rejected(library, bad):
    config, root, paper = library
    paper(title="Agent Security")
    config["synthesis"].update(bad)
    with pytest.raises(ValueError):
        SynthesisWorkflow.discover(config)
