from sbp_observability.parsing import json_log_parser


def test_parse_valid_json_lines():
    lines = [
        '{"timestamp": "2024-01-01T00:00:00", "bank": "alpha", "status": "success"}',
        '{"timestamp": "2024-01-01T00:00:01", "bank": "beta", "status": "failed", "error_code": "decline"}',
    ]
    events = json_log_parser.parse_lines(lines)
    assert len(events) == 2
    assert events[0].bank_id == "alpha"
    assert events[1].error_code == "decline"


def test_invalid_json_returns_empty():
    events = json_log_parser.parse_lines(["not json"])
    assert events == []
