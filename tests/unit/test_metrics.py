from sbp_observability.exporter import collector, metrics
from sbp_observability.models import TransactionEvent
from datetime import datetime


def test_record_event_increments_counters():
    event = TransactionEvent(
        timestamp=datetime.now(),
        bank_id="alpha",
        channel="mobile",
        operation_type="payment",
        status="failed",
        error_code="timeout",
        latency_ms=500,
    )
    collector.record_event(event)
    sample = metrics.sbp_requests_total.labels(bank="alpha", channel="mobile", operation_type="payment", status="failed")
    assert sample._value.get() >= 1
