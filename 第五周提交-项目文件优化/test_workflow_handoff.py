import ast
import json
from pathlib import Path
import pytest
from workflow_handoff import consume_handoff_payload, MODE

TOKEN = 'a' * 32

@pytest.fixture
def payload(tmp_path):
    value = dict(token=TOKEN, prompt='研究目标', reference='证据', expires_at=200)
    path = tmp_path / f'{TOKEN}.json'
    path.write_text(json.dumps(value), encoding='utf-8')
    return path, value

def test_once(payload, tmp_path):
    path, _ = payload
    assert consume_handoff_payload(TOKEN, tmp_path, 100) == ('研究目标', '证据', MODE)
    assert not path.exists()
    assert consume_handoff_payload(TOKEN, tmp_path, 100) is None

@pytest.mark.parametrize('token', ['', None, '../x', 'A'*32, 'a'*31])
def test_bad_token(token, tmp_path):
    assert consume_handoff_payload(token, tmp_path, 100) is None

@pytest.mark.parametrize('field,value', [('token','b'*32), ('prompt',None), ('prompt',' '), ('prompt','a'*12001), ('reference',[]), ('expires_at',float('nan')), ('expires_at',True)])
def test_bad_fields(payload, tmp_path, field, value):
    path, data = payload
    data[field] = value
    path.write_text(json.dumps(data), encoding='utf-8')
    assert consume_handoff_payload(TOKEN, tmp_path, 100) is None

def test_expired(payload, tmp_path):
    path, _ = payload
    assert consume_handoff_payload(TOKEN, tmp_path, 200) is None
    assert not path.exists()

@pytest.mark.parametrize('content', ['{', '{}', '[]', 'x'*2100001], ids=['malformed','missing-fields','array','oversized'])
def test_bad_json(payload, tmp_path, content):
    path, _ = payload
    path.write_text(content, encoding='utf-8')
    assert consume_handoff_payload(TOKEN, tmp_path, 100) is None

def test_callback_only_prefills(monkeypatch, tmp_path, payload):
    import workflow_handoff
    original = workflow_handoff.consume_handoff_payload
    monkeypatch.setattr(workflow_handoff, 'consume_handoff_payload', lambda token: original(token, tmp_path, 100))
    source = Path(__file__).resolve().parents[1] / 'web_ai_researcher.py'
    tree = ast.parse(source.read_text(encoding='utf-8'))
    callback = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'consume_workflow_handoff')
    class Gr:
        Request = object
        @staticmethod
        def update(): return 'unchanged'
        @staticmethod
        def Info(message): pass
    namespace = {'gr': Gr}
    exec(compile(ast.Module(body=[callback], type_ignores=[]), str(source), 'exec'), namespace)
    request = type('Request', (), {'query_params': {'workflow_handoff': TOKEN}})()
    assert namespace['consume_workflow_handoff'](request) == ('研究目标', '证据', MODE)
    assert namespace['consume_workflow_handoff'](request) == ('unchanged',)*3
