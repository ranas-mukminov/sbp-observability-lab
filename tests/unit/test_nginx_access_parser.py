from sbp_observability.parsing import nginx_access_parser


def test_parse_valid_lines():
    lines = [
        "2024-01-01T00:00:00 [alpha] [mobile] payment 200 0.120",
        "2024-01-01T00:00:01 [beta] [qr] refund 504 1.200",
    ]
    events = nginx_access_parser.parse_lines(lines)
    assert len(events) == 2
    assert events[0].status == "success"
    assert events[1].error_code == "504"


def test_parse_invalid_line_returns_none():
    assert nginx_access_parser.parse_line("broken line") is None
