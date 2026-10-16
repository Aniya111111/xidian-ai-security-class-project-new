from dataclasses import asdict
from io import BytesIO
import json
from pathlib import Path
import threading
from urllib.error import HTTPError, URLError

import pytest
from pypdf import PdfWriter

from agent_ifc.inbox import InboxManager
from agent_ifc.scholarfeed import (API_BASE, FeedError, SafeRedirect, ScholarFeedClient,
                                  ScholarFeedManager, ScholarPaper, arxiv_id, paper_key, short_filename)
from agent_ifc.storage import file_hash, read_text, render_card, write_json


def paper(identity="2610.05640v1", title="Multi-agent security 中文•", **extras):
    return {"arxiv_id": identity, "title": title, "authors": ["作者", "A. Author"],
            "abstract": "LLM multi-agent prompt injection defense with shared memory.",
            "published_date": "2026-10-10T00:00:00Z", "categories": ["cs.AI"], **extras}


def pdf_bytes():
    buffer = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.write(buffer)
    return buffer.getvalue()


class Response(BytesIO):
    def __init__(self, value, headers=None):
        super().__init__(value)
        self.headers = headers or {}


class Opener:
    def __init__(self, responses):
        self.responses = list(responses)
        self.requests = []

    def open(self, request, **kwargs):
        self.requests.append(request)
        result = self.responses.pop(0)
        if isinstance(result, Exception):
            raise result
        return result


class FakeClient:
    def __init__(self, results=None):
        self.cancel = threading.Event()
        self.calls = []
        self.results = list(results or [{"papers": [paper()], "next_cursor": None}])
        self.downloads = []

    def search(self, query, **kwargs):
        self.calls.append((query, kwargs))
        result = self.results.pop(0)
        if isinstance(result, Exception):
            raise result
        return result

    def download(self, value, target):
        self.downloads.append(value.arxiv_id)
        target.write_bytes(pdf_bytes())


@pytest.fixture
def manager(tmp_path):
    root = tmp_path / "vault/Agent-IFC"
    (root / "00_Project").mkdir(parents=True)
    (root / "10_Papers").mkdir()
    (root / "00_Project/Research_Profile.md").write_text(render_card(
        {"keywords_en": ["shared memory"], "keywords_zh": ["安全"]}, "研究方向"), encoding="utf-8")
    config = {"project_root": str(root), "vault_root": str(root.parent),
              "scholarfeed": {"queries": ["multi-agent security"], "max_pages_per_query": 2},
              "synthesis": {"keywords": ["multi-agent"], "required_keyword_groups": [["security", "injection"]]}}
    return ScholarFeedManager(config, client=FakeClient(), clock=lambda: 1000)


def test_search_uses_official_endpoint_and_utf8(monkeypatch):
    monkeypatch.setenv("SF_API_KEY", "sf_test_secret")
    result = {"papers": [paper()], "next_cursor": "abc"}
    transport = Opener([Response(json.dumps(result, ensure_ascii=False).encode("utf-8"))])
    client = ScholarFeedClient(opener=transport)
    value = client.search("多 Agent 安全", limit=2)
    assert ScholarPaper.parse(value["papers"][0]).title.endswith("中文•")
    request = transport.requests[0]
    assert request.full_url.startswith(API_BASE + "/papers/search?")
    assert "%E5%A4%9A" in request.full_url
    assert request.get_header("Authorization") == "Bearer sf_test_secret"
    assert "sf_test_secret" not in request.full_url


@pytest.mark.parametrize("identity", ["../../file", "123", "2610.05640?token=a", "https://evil.org/x", "2610.05640\nX", "CON"])
def test_arxiv_identity_rejects_paths_and_urls(identity):
    with pytest.raises(ValueError):
        arxiv_id(identity)


def test_short_filename_and_version_identity():
    assert short_filename("https://arxiv.org/abs/2610.05640v2") == "arxiv_2610.05640v2.pdf"
    assert short_filename("hep-th/9901001v2") == "arxiv_hep-th_9901001v2.pdf"
    assert paper_key("2610.05640v1") == paper_key("2610.05640v2")


@pytest.mark.parametrize("raw", [b"{broken", "中文".encode("gbk"), b"[]"])
def test_bad_json_or_encoding_stops_import(raw):
    client = ScholarFeedClient(opener=Opener([Response(raw)]))
    with pytest.raises(FeedError):
        client.health()


def test_long_rate_limit_does_not_sleep_and_records_retry():
    error = HTTPError(API_BASE, 429, "quota", {"Retry-After": "3600"}, BytesIO())
    client = ScholarFeedClient(opener=Opener([error]))
    with pytest.raises(FeedError) as caught:
        client.health()
    assert caught.value.retry_after == 3600


def test_transient_errors_retry_and_auth_error_is_redacted(monkeypatch):
    transport = Opener([URLError("contains secret"), Response(b'{"status":"ok"}')])
    client = ScholarFeedClient(opener=transport)
    waits = []
    monkeypatch.setattr(client.cancel, "wait", lambda seconds: waits.append(seconds) or False)
    assert client.health()["status"] == "ok" and waits == [1]
    error = HTTPError(API_BASE, 401, "sf_secret", {}, BytesIO(b"sf_secret"))
    client = ScholarFeedClient(opener=Opener([error]))
    with pytest.raises(FeedError, match="SF_API_KEY") as caught:
        client.health()
    assert "sf_secret" not in str(caught.value)
    assert len(client.opener.requests) == 1


def test_redirect_cannot_forward_credentials_to_another_host():
    from urllib.request import Request
    redirect = SafeRedirect({"api.scholarfeed.org"})
    for url in ("https://evil.org/", "http://api.scholarfeed.org/v1", "https://api.scholarfeed.org:8000/v1"):
        with pytest.raises(FeedError):
            redirect.redirect_request(Request(API_BASE), None, 302, "", {}, url)


def test_search_dedupes_cursor_and_reads_profile(manager):
    manager.client.results = [{"papers": [paper()], "next_cursor": "abc"},
                              {"papers": [paper("2610.05640v2")], "next_cursor": "abc"}]
    result = manager.search()
    assert result["new_count"] == 1
    state = manager.state()
    assert len(state["papers"]) == 1
    entry = state["papers"]["2610.05640"]
    assert entry["recommended"] and "shared memory" in entry["matched_terms"]
    assert entry["profile_hash"]
    assert manager.client.calls[1][1]["cursor"] == "abc"
    assert manager.search()["skipped"]
    assert len(manager.client.calls) == 2


def test_partial_search_failure_keeps_candidates_and_cooldown(manager):
    manager.client.results = [{"papers": [paper()], "next_cursor": "abc"}, FeedError("quota", retry_after=3600)]
    with pytest.raises(FeedError):
        manager.search()
    assert len(manager.state()["papers"]) == 1
    assert manager.state()["next_poll_at"] == 4600


def test_unmatched_candidates_are_retained_and_dismissal_survives(manager):
    manager.client.results = [{"papers": [paper(title="Traditional robot planning", abstract="control")]}]
    manager.search()
    entry = manager.state()["papers"]["2610.05640"]
    assert not entry["recommended"] and entry["status"] == "new"
    manager.dismiss(["2610.05640"])
    manager.client.results = [{"papers": [paper()]}]
    manager.search(force=True)
    assert manager.state()["papers"]["2610.05640"]["status"] == "dismissed"


def test_existing_card_skips_duplicate_download(manager):
    card = manager.root / "10_Papers/existing.md"
    card.write_text(render_card({"type": "paper", "arxiv_id": "2610.05640v3", "status": "reviewed"}, "证据"), encoding="utf-8")
    assert manager.search()["new_count"] == 0
    result = manager.download_selected(["2610.05640"], confirmed=True)
    assert result[0]["status"] == "archived" and not manager.client.downloads


def test_download_requires_confirmation_and_writes_hashed_metadata(manager, monkeypatch):
    manager.search()
    with pytest.raises(ValueError, match="用户确认"):
        manager.download_selected(["2610.05640"])
    result = manager.download_selected(["2610.05640"], confirmed=True)
    assert result[0]["status"] == "downloaded"
    target = Path(result[0]["path"])
    assert target.name == "arxiv_2610.05640v1.pdf"
    metadata = json.loads(read_text(target.with_suffix(".metadata.json")))
    assert metadata["sha256"] == file_hash(target)
    assert not list(manager.attachments.glob("*.part"))
    monkeypatch.setattr("agent_ifc.inbox._run_text", lambda command: "Title: extraction suggestion\n" if command[0] == "pdfinfo" else "PDF text")
    candidate = InboxManager(manager.config).discover()[0]
    assert candidate.title == paper()["title"] and candidate.authors == ("作者", "A. Author")
    assert candidate.status == "new"  # remote metadata never grants review
    manager.download_selected(["2610.05640"], confirmed=True)
    assert len(manager.client.downloads) == 1
    target.write_bytes(b"user changed")
    result = manager.download_selected(["2610.05640"], confirmed=True)
    assert result[0]["status"] == "failed" and target.read_bytes() == b"user changed"


def test_invalid_pdf_never_reaches_inbox(manager):
    manager.search()
    manager.client.download = lambda paper, path: path.write_bytes(b"<html>error</html>")
    result = manager.download_selected(["2610.05640"], confirmed=True)
    assert result[0]["status"] == "failed"
    assert not list(manager.attachments.glob("*.pdf"))
    assert not list(manager.attachments.glob("*.part"))


def test_download_transport_does_not_send_key_and_rejects_truncation(tmp_path, monkeypatch):
    monkeypatch.setenv("SF_API_KEY", "sf_secret")
    data = pdf_bytes()
    opener = Opener([Response(data, {"Content-Length": str(len(data))})])
    client = ScholarFeedClient(pdf_opener=opener)
    client.download(ScholarPaper.parse(paper()), tmp_path / "download.part")
    assert opener.requests[0].get_header("Authorization") is None
    assert opener.requests[0].full_url == "https://arxiv.org/pdf/2610.05640v1"
    broken = Opener([Response(data, {"Content-Length": str(len(data) + 10)})])
    with pytest.raises(FeedError):
        ScholarFeedClient({"max_attempts": 1}, pdf_opener=broken).download(ScholarPaper.parse(paper()), tmp_path / "broken.part")


def test_bad_sidecar_hash_not_trusted(manager, monkeypatch):
    manager.search()
    result = manager.download_selected(["2610.05640"], confirmed=True)
    path = Path(result[0]["path"])
    sidecar = path.with_suffix(".metadata.json")
    value = json.loads(read_text(sidecar))
    value["sha256"] = "bad"
    write_json(sidecar, value)
    monkeypatch.setattr("agent_ifc.inbox._run_text", lambda command: "Title: original\nAuthor: source author" if command[0] == "pdfinfo" else "text")
    inbox = InboxManager(manager.config)
    candidate = inbox.discover()[0]
    assert candidate.title == "original" and inbox.notices


def test_long_paths_fail_before_network(manager, monkeypatch):
    manager.search()
    monkeypatch.setattr("agent_ifc.scholarfeed.check_path", lambda *args, **kwargs: (_ for _ in ()).throw(ValueError("完整路径过长")))
    result = manager.download_selected(["2610.05640"], confirmed=True)
    assert result[0]["status"] == "failed" and not manager.client.downloads


def test_downloaded_version_is_not_silently_changed(manager):
    manager.search()
    manager.download_selected(["2610.05640"], confirmed=True)
    manager.client.results = [{"papers": [paper("2610.05640v2")]}]
    manager.search(force=True)
    assert manager.state()["papers"]["2610.05640"]["paper"]["arxiv_id"] == "2610.05640v1"


def test_pdf_size_and_cancel_limits(tmp_path):
    opener = Opener([Response(b"%PDF", {"Content-Length": "999999999"})])
    with pytest.raises(FeedError, match="上限"):
        ScholarFeedClient(pdf_opener=opener).download(ScholarPaper.parse(paper()), tmp_path / "large.part")
    client = ScholarFeedClient(opener=Opener([]))
    client.cancel.set()
    with pytest.raises(InterruptedError):
        client.health()


def test_tls_verification_failure_is_explicit_and_not_retried():
    import ssl
    transport = Opener([URLError(ssl.SSLCertVerificationError("untrusted"))])
    with pytest.raises(FeedError, match="truststore"):
        ScholarFeedClient(opener=transport).health()
    assert len(transport.requests) == 1


def test_windows_limits_count_utf16_units():
    import os
    from agent_ifc.deeptutor import needs_request_file
    from agent_ifc.workflow import safe_filename
    assert len(safe_filename("😀" * 130).encode("utf-16-le")) // 2 <= 130
    assert needs_request_file(["run", "😀" * 13000]) is (os.name == "nt")


@pytest.mark.skipif(__import__("os").name != "nt", reason="Windows rename semantics")
def test_windows_download_works_when_hard_links_unsupported(manager, monkeypatch):
    import os
    manager.search()
    def unsupported(*args, **kwargs):
        raise OSError(1, "函数不正确")
    monkeypatch.setattr("agent_ifc.scholarfeed.os.link", unsupported)
    original_rename = os.rename
    publications = []
    def rename(source, target):
        assert source.parent == target.parent == manager.attachments
        assert source.suffix == ".part" and target.suffix == ".pdf"
        assert not list(manager.attachments.glob("*.pdf"))
        publications.append((source, target))
        return original_rename(source, target)
    monkeypatch.setattr("agent_ifc.scholarfeed.os.rename", rename)
    result = manager.download_selected(["2610.05640"], confirmed=True)
    assert result[0]["status"] == "downloaded"
    assert len(publications) == 1 and Path(result[0]["path"]).is_file()
    assert not list(manager.attachments.glob("*.part"))


def test_publication_collision_preserves_existing_pdf_and_cleans_temp(manager, monkeypatch):
    from agent_ifc.scholarfeed import install_pdf
    manager.search()
    def concurrent_file(staging, target):
        target.write_bytes(b"user-owned concurrent file")
        return install_pdf(staging, target)
    monkeypatch.setattr("agent_ifc.scholarfeed.install_pdf", concurrent_file)
    result = manager.download_selected(["2610.05640"], confirmed=True)
    assert result[0]["status"] == "failed"
    target = manager.attachments / "arxiv_2610.05640v1.pdf"
    assert target.read_bytes() == b"user-owned concurrent file"
    assert not list(manager.attachments.glob("*.part"))


def test_failed_install_can_retry_with_previous_metadata(manager, monkeypatch):
    from agent_ifc.scholarfeed import install_pdf
    manager.search()
    monkeypatch.setattr("agent_ifc.scholarfeed.install_pdf", lambda *args: (_ for _ in ()).throw(OSError(1, "函数不正确")))
    assert manager.download_selected(["2610.05640"], confirmed=True)[0]["status"] == "failed"
    assert list(manager.attachments.glob("*.metadata.json"))
    assert not list(manager.attachments.glob("*.pdf"))
    assert not list(manager.attachments.glob("*.part"))
    monkeypatch.setattr("agent_ifc.scholarfeed.install_pdf", install_pdf)
    result = manager.download_selected(["2610.05640"], confirmed=True)
    assert result[0]["status"] == "downloaded"
