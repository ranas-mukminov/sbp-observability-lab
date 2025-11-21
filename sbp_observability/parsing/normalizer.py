"""Normalization utilities."""
from __future__ import annotations

from typing import Iterable, List

from sbp_observability.models import TransactionEvent


STATUS_MAP = {
    "ok": "success",
    "success": "success",
    "failed": "failed",
    "error": "failed",
    "timeout": "timeout",
}


def normalize_status(status: str) -> str:
    return STATUS_MAP.get(status.lower(), status)


def normalize_events(events: Iterable[TransactionEvent]) -> List[TransactionEvent]:
    normalized: List[TransactionEvent] = []
    for event in events:
        normalized.append(
            TransactionEvent(
                timestamp=event.timestamp,
                bank_id=event.bank_id or "unknown",
                channel=event.channel or "unknown",
                operation_type=event.operation_type or "unknown",
                status=normalize_status(event.status),
                error_code=event.error_code,
                latency_ms=event.latency_ms,
            )
        )
    return normalized
