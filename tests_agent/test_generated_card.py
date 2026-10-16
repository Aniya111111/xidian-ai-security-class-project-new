import pytest

from agent_ifc.generated_card import parse_generated_card
from agent_ifc.storage import split_card


def test_repairs_only_generated_comparison_quotes_and_preserves_body():
    text = ('---\nstatus: reading\ncomparison:\n'
            '  trust_boundary: "必须维持"不可信内容"边界；已有 \\"引号\\"。"\n'
            '---\n\n# 原文\n\n正文 "引号" 和 [Paper: PDF p. 3]。')
    metadata, body, repairs = parse_generated_card(text)
    assert metadata["comparison"]["trust_boundary"] == '必须维持"不可信内容"边界；已有 "引号"。'
    assert body == '# 原文\n\n正文 "引号" 和 [Paper: PDF p. 3]。'
    assert repairs["changes"] == [{"field": "comparison.trust_boundary", "line": 4,
                                   "escaped_quotes": 2}]
    assert repairs["original_hash"] != repairs["repaired_hash"]
    with pytest.raises(ValueError, match="第 4 行"):
        split_card(text)  # Editable/user-authored cards remain strict.


def test_valid_escaped_and_block_strings_need_no_repair():
    text = ('---\ncomparison:\n  trust_boundary: "已有 \\"引号\\" 和 \\\\ 路径"\n'
            '  defense_mechanism: |-\n    保留 "引号": 以及冒号\n---\n正文')
    assert parse_generated_card(text) == (*split_card(text), None)


@pytest.mark.parametrize("header", [
    'title: "题目"破损""',
    'comparison:\n  status: "reading"破损""',
    'comparison:\n  trust_boundary: ["不完整"',
    'comparison:\n  trust_boundary: "无效 \\q 转义"',
    'other:\n  trust_boundary: "不能"改动""',
    'comparison:\n  trust_boundary: "可修复"引号""\nauthors: [未闭合',
])
def test_unknown_or_structural_errors_still_fail(header):
    with pytest.raises(ValueError, match="YAML 属性格式错误"):
        parse_generated_card("---\n" + header + "\n---\n正文")
