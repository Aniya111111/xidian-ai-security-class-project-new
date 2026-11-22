"""Local one-use handoffs. This module never imports a model or starts work."""
import json
import math
from pathlib import Path
import re
import threading
import time

LOCK = threading.Lock()
MODE = 'Obsidian Evidence-Grounded Ideation'

def consume_handoff_payload(token, root=None, now=None):
    if not isinstance(token, str) or not re.fullmatch(r'[a-f0-9]{32}', token):
        return None
    directory = Path(root) if root is not None else Path(__file__).resolve().parent / 'cache/workflow_handoffs'
    path = directory / f'{token}.json'
    with LOCK:
        try:
            if path.is_symlink() or not path.is_file() or path.stat().st_size > 2_100_000:
                return None
            with path.open('rb') as stream:
                raw = stream.read(2_100_001)
            if len(raw) > 2_100_000:
                return None
            value = json.loads(raw)
            if not isinstance(value, dict):
                return None
            expiry = value.get('expires_at')
            if type(expiry) not in (int, float) or not math.isfinite(expiry):
                return None
            if expiry <= (time.time() if now is None else now):
                path.unlink()
                return None
            prompt, reference = value.get('prompt'), value.get('reference')
            if (value.get('token') != token or not isinstance(prompt, str) or not prompt.strip()
                    or len(prompt) > 12000 or not isinstance(reference, str) or not reference.strip()
                    or len(reference.encode('utf-8')) > 2_000_000):
                return None
            path.unlink()
            return prompt, reference, MODE
        except (OSError, ValueError, TypeError):
            return None
