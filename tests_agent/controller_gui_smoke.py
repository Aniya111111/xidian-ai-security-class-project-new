"""Run the automatic Tk coordinator and its approval path in a temporary vault."""
import json
from pathlib import Path
import tempfile
import time
import tkinter as tk
from tkinter import ttk

from agent_ifc.controller_gui import ControllerWindow
from agent_ifc.storage import read_text, render_card


def main():
    original_tk, original_top = tk.Tk.__init__, tk.Toplevel.__init__
    def hidden_tk(self, *args, **kwargs):
        original_tk(self, *args, **kwargs)
        self.withdraw()
    def hidden_top(self, *args, **kwargs):
        original_top(self, *args, **kwargs)
        self.withdraw()
    tk.Tk.__init__, tk.Toplevel.__init__ = hidden_tk, hidden_top
    with tempfile.TemporaryDirectory(prefix="agent-ifc-controller-ui-") as directory:
        root = Path(directory) / "vault/Agent-IFC"
        (root / "10_Papers").mkdir(parents=True)
        source = root / "10_Papers/a.md"
        def paper(status):
            source.write_text(render_card({"type": "paper", "paper_id": "a", "title": "多Agent协作的安全防护测试",
                                           "status": status, "year": 2024},
                                          "\n\n".join(f"## {n:02} 章节\n\n中文方法证据 {n}。"
                                                      for n in range(1, 17))), encoding="utf-8")
        paper("reading")
        config = {"project_root": str(root), "vault_root": str(root.parent),
                  "synthesis": {"theme_id": "multi-agent-security", "title": "多Agent协作的安全防护",
                                "target": "20_Themes/多Agent协作的安全防护.md",
                                "keywords": ["多agent"], "required_keyword_groups": [["安全"]],
                                "comparison_columns": [{"key": "trust_boundary", "label": "信任边界",
                                                        "labels": ["信任边界"]}]},
                  "controller": {"scan_interval_seconds": 1, "settle_seconds": 0}}
        app = ControllerWindow(config)
        def pump_until(predicate, seconds=6):
            deadline = time.monotonic() + seconds
            while time.monotonic() < deadline:
                app.root.update()
                if predicate():
                    return
                time.sleep(0.02)
            raise AssertionError("GUI condition timed out")
        def dismiss_previews():
            for window in app.views.values():
                if window.root.winfo_exists():
                    for child in window.root.winfo_children():
                        if isinstance(child, tk.Toplevel) and child.title() == "主题笔记差异":
                            child.destroy()
            if not app.closing:
                app.root.after(50, dismiss_previews)
        app.root.after(50, dismiss_previews)
        try:
            pump_until(lambda: not app.busy and app.controller.state["status"] == "no_sources")
            assert not app.controller.state["jobs"]
            paper("reviewed")
            original = source.read_bytes()
            pump_until(lambda: bool(app.views))
            job_id = next(iter(app.views))
            view = app.views[job_id]
            assert "多Agent协作的安全防护" in view.root.title()
            assert "多Agent协作的安全防护对比表" in view.editor.get("1.0", "end")
            assert "| 信任边界 |" in view.editor.get("1.0", "end")
            pump_until(lambda: view.flow.state["version"] >= 2)  # automatic difference popup ran
            assert str(view.buttons[0].cget("state")) == "disabled"
            assert str(view.buttons[1].cget("state")) == "disabled"
            def close_confirmation():
                for popup in view.root.winfo_children():
                    if isinstance(popup, tk.Toplevel) and popup.title() == "确认发布主题综合":
                        popup.destroy()
            view.root.after(50, close_confirmation)
            view.publish()
            assert app.controller.job(job_id)["status"] == "waiting_for_approval"
            assert not view.flow.target().exists()
            view.close()
            old_scan = app.controller.state["last_scan_at"]
            pump_until(lambda: not app.busy and app.controller.state["last_scan_at"] > old_scan)
            assert not any(window.root.winfo_exists() for window in app.views.values())
            assert len(app.controller.state["jobs"]) == 1
            app.open_review(job_id)
            view = app.views[job_id]
            def accept():
                for popup in view.root.winfo_children():
                    if isinstance(popup, tk.Toplevel) and popup.title() == "确认发布主题综合":
                        for control in popup.winfo_children():
                            if isinstance(control, ttk.Checkbutton):
                                control.invoke()
                        for control in popup.winfo_children():
                            if isinstance(control, ttk.Button) and control.cget("text") == "确认写入":
                                control.invoke()
                                return
                raise AssertionError("confirmation popup missing")
            view.root.after(100, accept)
            view.publish()
            pump_until(lambda: not view.busy and view.flow.state["status"] == "published")
            pump_until(lambda: not app.busy and app.controller.state["status"] == "idle")
            assert app.controller.job(job_id)["status"] == "published"
            assert len(app.controller.state["jobs"]) == 1
            assert source.read_bytes() == original
            approvals = json.loads(read_text(view.flow.run_dir / "approvals.json"))
            assert len(approvals) == 1 and approvals[0]["details"]["confirmed"] is True
            print(json.dumps({"automatic_reviewed_detection": True, "automatic_review_popup": True,
                              "cancel_did_not_publish": True, "no_repeated_popup": True,
                              "confirmed_publication_recorded": True, "no_duplicate_after_publish": True}))
        finally:
            app.closing = True
            app.root.destroy()


if __name__ == "__main__":
    main()
