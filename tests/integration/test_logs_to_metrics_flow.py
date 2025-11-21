from sbp_observability.parsing import nginx_access_parser, normalizer
from sbp_observability.exporter import collector, metrics


def test_log_to_metrics_roundtrip():
    lines = ["2024-01-01T00:00:00 [alpha] [mobile] payment 500 1.2"]
    events = nginx_access_parser.parse_lines(lines)
    normalized = normalizer.normalize_events(events)
    for event in normalized:
        collector.record_event(event)
    value = metrics.sbp_requests_total.labels(
        bank="alpha", channel="mobile", operation_type="payment", status="failed"
    )._value.get()
    assert value >= 1
