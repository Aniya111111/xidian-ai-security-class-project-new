"""Real Tk inbox dialogs in a temporary vault, with no provider requests."""
from dataclasses import replace
import json
from pathlib import Path
import tempfile
import time
import tkinter as tk
from unittest.mock import patch

from agent_ifc.controller_gui import ControllerWindow
from agent_ifc.gui import ReviewWindow
from agent_ifc.inbox import InboxManager, PaperCandidate
from agent_ifc.storage import file_hash, read_text, render_card, write_text
from agent_ifc.workflow import Workflow


def main():
    tk_init, top_init = tk.Tk.__init__, tk.Toplevel.__init__
    def hidden_tk(self, *args, **kwargs):
        tk_init(self, *args, **kwargs)
        self.withdraw()
    def hidden_top(self, *args, **kwargs):
        top_init(self, *args, **kwargs)
        self.withdraw()
    with tempfile.TemporaryDirectory(prefix="agent-ifc-inbox-ui-") as directory:
        root = Path(directory) / "vault/Agent-IFC"
        (root / "90_Attachments").mkdir(parents=True)
        (root / "10_Papers").mkdir()
        (root / "90_Attachments/新论文.PDF").write_bytes(b"%PDF-1.7\nexample")
        config = {"project_root": str(root), "vault_root": str(root.parent),
                  "inbox": {"enabled": True, "scan_interval_seconds": 1, "settle_seconds": 1},
                  "controller": {"scan_interval_seconds": 1, "settle_seconds": 0},
                  "synthesis": {"title": "多Agent协作的安全防护", "theme_id": "multi-agent-security",
                                "target": "20_Themes/theme.md", "keywords": ["多agent"]}}
        def inspect(manager, path):
            return PaperCandidate(str(path.resolve()), file_hash(path), "多Agent安全论文",
                                  ("测试作者",), 2026, "", "", "", excerpt="首页证据")
        calls = []
        def fake_import(manager, candidate, report, on_created):
            calls.append(candidate.sha256)
            flow = Workflow.create(manager.build_config(candidate, "test-kb"))
            flow.state.update(status="waiting_for_approval", validation={"fatal": [], "review_blockers": []},
                              draft_hash="placeholder")
            write_text(flow.run_dir / "draft.md", render_card({"type": "paper", "title": candidate.title}, "测试正文"))
            flow.save()
            manager.save_state(candidate, run_dir=str(flow.run_dir), status="waiting_for_approval")
            on_created(flow)
            report("测试分析已完成，等待审核")
            return flow
        with patch.object(tk.Tk, "__init__", hidden_tk), patch.object(tk.Toplevel, "__init__", hidden_top), \
                patch.object(InboxManager, "inspect", inspect), patch.object(InboxManager, "import_paper", fake_import):
            app = ControllerWindow(config)
            def pump_until(predicate, seconds=8):
                deadline = time.monotonic() + seconds
                while time.monotonic() < deadline:
                    app.root.update()
                    if predicate():
                        return
                    time.sleep(.02)
                raise AssertionError("GUI condition timed out")
            cancelled = []
            def dismiss_identity():
                for view in app.root.winfo_children():
                    for child in view.winfo_children():
                        for popup in child.winfo_children():
                            if isinstance(popup, tk.Toplevel) and popup.title() == "确认论文身份":
                                cancelled.append(True)
                                popup.destroy()
                if not cancelled:
                    app.root.after(50, dismiss_identity)
            app.root.after(50, dismiss_identity)
            def dismiss_differences():
                for view in app.views.values():
                    if view.root.winfo_exists():
                        for popup in view.root.winfo_children():
                            if isinstance(popup, tk.Toplevel) and popup.title() == "主题笔记差异":
                                popup.destroy()
                if not app.closing:
                    app.root.after(50, dismiss_differences)
            app.root.after(50, dismiss_differences)
            try:
                pump_until(lambda: bool(cancelled) and app.inbox_view and not app.inbox_view.selecting)
                inbox = app.inbox_view
                assert not calls and not inbox.manager.state_path.exists()
                assert not list((root / "90_Runs").glob("agent_*"))
                candidate = next(iter(inbox.candidates.values()))
                with patch.object(ReviewWindow, "edit_inbox_metadata", lambda self, value: replace(value, title="已确认论文")):
                    inbox.open_candidate(candidate)
                pump_until(lambda: len(calls) == 1 and not inbox.busy)
                view = inbox.views[0]
                assert str(view.flow.run_dir) in view.run_path.get()
                assert "已确认论文" in view.editor.get("1.0", "end")
                assert not any(variable.get() for variable in view.confirmations.values())
                view.flow.state["status"] = "reviewed"
                view.flow.save()
                # Simulate the reviewed source produced by the existing approval code.
                card = root / "10_Papers/reviewed.md"
                card.write_text(render_card({"type": "paper", "status": "reviewed", "paper_id": "test",
                                            "title": "多Agent安全论文", "source_hash": candidate.sha256},
                                           "\n\n".join(f"## {n:02} 章节\n\n原文摘录 {n}" for n in range(1, 17))), encoding="utf-8")
                view.root.destroy()
                inbox.next_scan = 0
                pump_until(lambda: inbox.candidates[candidate.sha256].status == "reviewed")
                inbox.open_candidate(inbox.candidates[candidate.sha256])
                assert len(calls) == 1 and len(inbox.views) == 2
                assert inbox.views[1].flow.state["status"] == "reviewed"
                inbox.views[1].root.destroy()
                pump_until(lambda: bool(app.views))
                assert app.controller.state["jobs"][0]["status"] == "waiting_for_approval"
                assert not (root / "20_Themes/theme.md").exists()
                print(json.dumps({"auto_inbox": True, "cancel_starts_no_request": True,
                                  "identity_starts_one_run": True, "resume_reuses_run": True,
                                  "reviewed_triggers_theme_approval": True, "theme_published": False}))
            finally:
                app.closing = True
                if app.inbox_view:
                    app.inbox_view.closing = True
                app.root.destroy()


if __name__ == "__main__":
    main()
