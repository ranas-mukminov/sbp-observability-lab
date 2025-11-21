from datetime import datetime

from sbp_observability.models import TransactionEvent
from sbp_observability.parsing import normalizer


def test_normalize_status_mapping():
    events = [
        TransactionEvent(
            timestamp=datetime.now(),
            bank_id="alpha",
            channel="mobile",
            operation_type="payment",
            status="ok",
            error_code=None,
            latency_ms=100,
        )
    ]
    normalized = normalizer.normalize_events(events)
    assert normalized[0].status == "success"
