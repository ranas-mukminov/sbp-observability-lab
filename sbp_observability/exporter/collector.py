"""Collector utilities."""
from __future__ import annotations

from sbp_observability.models import TransactionEvent
from sbp_observability.exporter import metrics


def record_event(event: TransactionEvent):
    """Record metrics for a transaction event."""
    labels = {
        "bank": event.bank_id,
        "channel": event.channel,
        "operation_type": event.operation_type,
    }
    metrics.sbp_requests_total.labels(status=event.status, **labels).inc()
    metrics.sbp_request_latency_seconds.labels(**labels).observe(event.latency_ms / 1000)
    if event.status not in {"success", "ok"}:
        metrics.sbp_request_errors_total.labels(error_class=event.error_code or "unknown", **labels).inc()


def set_gateway_up(gateway: str, up: bool):
    metrics.sbp_gateway_up.labels(gateway=gateway).set(1 if up else 0)
