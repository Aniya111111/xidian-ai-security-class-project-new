import asyncio
import io
import logging
import sys
from dataclasses import dataclass, field

import pytest

from agent_ifc.deeptutor_file_runner import short_kb_seed, route_diagnostics_to_stderr


@dataclass
class Context:
    user_message: str
    knowledge_bases: list = field(default_factory=lambda: ["paper-kb"])


def test_short_seed_preserves_full_message_and_knowledge_base_mount():
    calls = []
    class Pipeline:
        async def _retrieve_kb_seed_block(self, context, stream):
            calls.append((context.user_message, context.knowledge_bases))
            return "retrieved source"
    original = Pipeline._retrieve_kb_seed_block
    context = Context("very long full paper card")
    with short_kb_seed(Pipeline, "ORBIT security"):
        assert asyncio.run(Pipeline()._retrieve_kb_seed_block(context, None)) == "retrieved source"
    assert calls == [("ORBIT security", ["paper-kb"])]
    assert context.user_message == "very long full paper card"
    assert Pipeline._retrieve_kb_seed_block is original


def test_seed_adapter_restores_method_after_error():
    class Pipeline:
        async def _retrieve_kb_seed_block(self, context, stream):
            raise RuntimeError("offline")
    original = Pipeline._retrieve_kb_seed_block
    with pytest.raises(RuntimeError):
        with short_kb_seed(Pipeline, "ORBIT"):
            asyncio.run(Pipeline()._retrieve_kb_seed_block(Context("full"), None))
    assert Pipeline._retrieve_kb_seed_block is original


def test_diagnostic_logging_keeps_stdout_clean(monkeypatch):
    stdout, stderr = io.StringIO(), io.StringIO()
    monkeypatch.setattr(sys, "stdout", stdout)
    monkeypatch.setattr(sys, "stderr", stderr)
    handler = logging.StreamHandler(stdout)
    other_stream = io.StringIO()
    other = logging.StreamHandler(other_stream)
    root = logging.getLogger()
    monkeypatch.setattr(root, "handlers", [handler, other])
    route_diagnostics_to_stderr()
    record = logging.LogRecord("deeptutor.test", logging.ERROR, "test", 1, "transport failed", (), None)
    handler.handle(record)
    assert stdout.getvalue() == ""
    assert "transport failed" in stderr.getvalue()
    assert other.stream is other_stream
