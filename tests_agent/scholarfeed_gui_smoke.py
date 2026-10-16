"""Real candidate/download dialogs in a temporary vault; no network/models."""
import json
from pathlib import Path
import tempfile
import time
import tkinter as tk
from unittest.mock import patch

from agent_ifc.controller_gui import ControllerWindow
from agent_ifc.gui import ReviewWindow
from agent_ifc.scholarfeed import ScholarFeedClient
from tests_agent.test_scholarfeed import paper, pdf_bytes


def main():
    original_tk, original_top = tk.Tk.__init__, tk.Toplevel.__init__
    def hidden_tk(self, *args, **kwargs):
        original_tk(self, *args, **kwargs)
        self.withdraw()
    def hidden_top(self, *args, **kwargs):
        original_top(self, *args, **kwargs)
        self.withdraw()
    downloads, identities, searches = [], [], []
    def search(self, query, **kwargs):
        searches.append(query)
        return {"papers": [paper()], "next_cursor": None}
    def download(self, candidate, path):
        downloads.append(candidate.arxiv_id)
        path.write_bytes(pdf_bytes())
    def identity(self, candidate):
        identities.append(candidate)
        return None  # verify the next approval boundary without calling DeepTutor
    with tempfile.TemporaryDirectory(prefix="agent-ifc-scholarfeed-ui-") as directory:
        root = Path(directory) / "vault/Agent-IFC"
        (root / "10_Papers").mkdir(parents=True)
        (root / "90_Attachments").mkdir()
        config = {"project_root": str(root), "vault_root": str(root.parent),
                  "scholarfeed": {"enabled": True, "queries": ["multi-agent security"]},
                  "inbox": {"enabled": True, "scan_interval_seconds": 1, "settle_seconds": 1},
                  "controller": {"scan_interval_seconds": 1, "settle_seconds": 0},
                  "synthesis": {"title": "多Agent协作的安全防护", "theme_id": "multi-agent-security",
                                "target": "20_Themes/theme.md", "keywords": ["multi-agent"]}}
        with patch.object(tk.Tk, "__init__", hidden_tk), patch.object(tk.Toplevel, "__init__", hidden_top), \
                patch.object(ScholarFeedClient, "search", search), patch.object(ScholarFeedClient, "download", download), \
                patch.object(ReviewWindow, "edit_inbox_metadata", identity):
            app = ControllerWindow(config)
            def pump_until(predicate, seconds=8):
                deadline = time.monotonic() + seconds
                while time.monotonic() < deadline:
                    app.root.update()
                    if predicate():
                        return
                    time.sleep(.02)
                raise AssertionError("GUI condition timed out")
            try:
                pump_until(lambda: app.feed_view and bool(app.feed_view.entries) and not app.feed_view.busy)
                view = app.feed_view
                key = next(iter(view.entries))
                view.tree.selection_set(key)
                view.preview()
                assert "prompt injection" in view.details.get("1.0", "end")
                assert not downloads and not list((root / "90_Attachments").glob("*.pdf"))
                with patch("agent_ifc.scholarfeed_gui.messagebox.askyesno", return_value=False):
                    view.download()
                assert not downloads
                with patch("agent_ifc.scholarfeed_gui.messagebox.askyesno", return_value=True):
                    view.download()
                pump_until(lambda: len(downloads) == 1 and not view.busy)
                assert view.entries[key]["status"] == "downloaded"
                pump_until(lambda: bool(identities))
                assert identities[0].title == paper()["title"]
                assert identities[0].authors == ("作者", "A. Author")
                assert not list((root / "90_Runs").glob("agent_*"))
                assert len(searches) == 1
                print(json.dumps({"automatic_search": True, "cancel_does_not_download": True,
                                  "selection_downloads_short_filename": True, "metadata_reaches_identity_popup": True,
                                  "cancel_identity_starts_no_model": True, "no_repeated_search": True}))
            finally:
                app.closing = True
                for child in (app.inbox_view, app.feed_view):
                    if child:
                        child.closing = True
                app.root.destroy()


if __name__ == "__main__":
    main()
