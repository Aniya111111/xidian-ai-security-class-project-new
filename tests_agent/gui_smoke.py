"""Create the real review UI without displaying a window or granting approval."""

import json
from pathlib import Path
import tkinter as tk

from agent_ifc.gui import ReviewWindow
from agent_ifc.workflow import Workflow


def main():
    base = Path(__file__).resolve().parents[1]
    preview = max((base / "work/agent-preview").glob("agent_*"))
    flow = Workflow.resume(preview)
    original_init = tk.Tk.__init__
    original_top_init = tk.Toplevel.__init__
    def hidden_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        self.withdraw()
    tk.Tk.__init__ = hidden_init
    def hidden_top_init(self, *args, **kwargs):
        original_top_init(self, *args, **kwargs)
        self.withdraw()
    tk.Toplevel.__init__ = hidden_top_init
    window = ReviewWindow(flow=flow)
    try:
        window.root.update()
        assert "Zero-Resource" in window.editor.get("1.0", "end")
        assert "C01" in window.validation.get("1.0", "end")
        assert "文献定位" in window.analysis.get("1.0", "end")
        assert all(not item.get() for item in window.confirmations.values())
        assert flow.state["status"] == "waiting_for_approval"
        window.busy = True
        window.messages.put(("run_created", "new-supplement-run"))
        window.report("模型推理中，已接收 4000 条事件，已运行 300 秒")
        window.poll()
        assert "new-supplement-run" in window.run_path.get()
        assert "4000" in window.status.get()
        assert window.busy is True
        window.messages.put(("complete", None))
        window.poll()
        assert window.busy is False
        assert str(flow.run_dir) in window.run_path.get()
        def dismiss_popup():
            for child in window.root.winfo_children():
                if isinstance(child, tk.Toplevel):
                    child.destroy()
        window.root.after(100, dismiss_popup)
        assert window.confirm_publication(existing=True) is False
        assert flow.state["status"] == "waiting_for_approval"
        print(json.dumps({"gui_created": True, "human_checks_default_false": True,
                          "closed_popup_approved": False, "published": False,
                          "progress_and_run_path_update": True}))
    finally:
        window.root.destroy()


if __name__ == "__main__":
    main()
