from sbp_observability.exporter import collector, metrics
from sbp_observability.proxy.http_proxy import MaskingMixin
from sbp_observability.models import TransactionEvent
from datetime import datetime


def test_masking_and_metrics_record():
    masked = MaskingMixin.mask_payload({"pan": "123", "bank_id": "alpha"}, ("pan",))
    assert masked["pan"] == "***"
    event = TransactionEvent(
        timestamp=datetime.now(),
        bank_id="alpha",
        channel="mobile",
        operation_type="payment",
        status="failed",
        error_code="timeout",
        latency_ms=300,
    )
    collector.record_event(event)
    value = metrics.sbp_request_errors_total.labels(
        bank="alpha", channel="mobile", operation_type="payment", error_class="timeout"
    )._value.get()
    assert value >= 1
