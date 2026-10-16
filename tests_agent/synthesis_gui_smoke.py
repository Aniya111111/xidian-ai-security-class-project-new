"""Exercise real Tk dialogs and publication using a temporary vault only."""
import json
from pathlib import Path
import tempfile
import time
import tkinter as tk
from tkinter import ttk

from agent_ifc.storage import read_text, render_card, split_card
from agent_ifc.synthesis import SynthesisWorkflow
from agent_ifc.synthesis_gui import SynthesisWindow


def main():
    original_tk = tk.Tk.__init__
    original_top = tk.Toplevel.__init__
    def hidden_tk(self, *args, **kwargs):
        original_tk(self, *args, **kwargs)
        self.withdraw()
    def hidden_top(self, *args, **kwargs):
        original_top(self, *args, **kwargs)
        self.withdraw()
    tk.Tk.__init__ = hidden_tk
    tk.Toplevel.__init__ = hidden_top
    with tempfile.TemporaryDirectory(prefix="agent-ifc-synthesis-ui-") as directory:
        root = Path(directory) / "vault/Agent-IFC"
        (root / "10_Papers").mkdir(parents=True)
        config = {"project_root": str(root), "vault_root": str(root.parent)}
        paper = root / "10_Papers/paper.md"
        paper.write_text(render_card({"type": "paper", "status": "reviewed", "paper_id": "test",
                                      "title": "幻觉防御测试", "year": 2024},
                                     "\n\n".join(f"## {i:02} 章节\n\n中文证据 {i}。"
                                                 for i in range(1, 17))), encoding="utf-8")
        original_paper = paper.read_bytes()
        flow = SynthesisWorkflow.create(config)
        window = SynthesisWindow(config, flow)
        def dismiss():
            for child in window.root.winfo_children():
                if isinstance(child, tk.Toplevel):
                    child.destroy()
        try:
            window.root.update()
            assert "幻觉防御测试" in window.editor.get("1.0", "end")
            assert "仅 1 篇" in window.sources.get("1.0", "end")
            assert "reviewed" in window.sources.get("1.0", "end")
            window.root.after(50, dismiss)
            assert window.choose_sources(*SynthesisWorkflow.discover(config)) is None
            window.root.after(50, dismiss)
            assert window.diff_popup(confirm=True) is False
            assert not flow.target().exists()
            assert json.loads(read_text(flow.run_dir / "approvals.json")) == []
            window.editor.insert("end", "\n人工补充的主题备注。\n")
            assert window.save_editor()
            def accept():
                for popup in window.root.winfo_children():
                    if isinstance(popup, tk.Toplevel):
                        for control in popup.winfo_children():
                            if isinstance(control, ttk.Checkbutton):
                                control.invoke()
                        for control in popup.winfo_children():
                            if isinstance(control, ttk.Button) and control.cget("text") == "确认写入":
                                control.invoke()
                                return
                raise AssertionError("confirmation popup missing")
            window.root.after(50, accept)
            window.publish()
            deadline = time.monotonic() + 5
            while window.busy and time.monotonic() < deadline:
                window.root.update()
                time.sleep(0.02)
            assert not window.busy
            assert flow.state["status"] == "published"
            assert "人工补充" in read_text(flow.target())
            assert paper.read_bytes() == original_paper
            assert split_card(read_text(paper))[0]["status"] == "reviewed"
            assert len(json.loads(read_text(flow.run_dir / "approvals.json"))) == 1
            print(json.dumps({"gui_created": True, "cancel_did_not_publish": True,
                              "confirmed_popup_published": True, "source_unchanged": True}))
        finally:
            window.root.destroy()


if __name__ == "__main__":
    main()
