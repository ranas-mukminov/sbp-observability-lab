"""Parser for JSON logs."""
from __future__ import annotations

import json
from datetime import datetime
from typing import Iterable, List

from sbp_observability.models import TransactionEvent


KEY_MAPPING = {
    "timestamp": ["timestamp", "ts", "time"],
    "bank_id": ["bank", "bank_id"],
    "channel": ["channel"],
    "operation_type": ["sbp_operation", "operation", "type"],
    "status": ["status", "result"],
    "error_code": ["error_code", "error"],
    "latency_ms": ["duration_ms", "latency_ms", "latency"],
}


class MalformedLog(RuntimeError):
    """Raised when a log line cannot be parsed."""


def _get_value(data: dict, keys: list[str], default=None):
    for key in keys:
        if key in data:
            return data[key]
    return default


def parse_line(line: str) -> TransactionEvent | None:
    """Parse a JSON log line into TransactionEvent if possible."""
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return None
    timestamp_raw = _get_value(data, KEY_MAPPING["timestamp"])
    if not timestamp_raw:
        return None
    try:
        timestamp = datetime.fromisoformat(str(timestamp_raw))
    except ValueError as exc:
        raise MalformedLog("Invalid timestamp") from exc
    bank_id = _get_value(data, KEY_MAPPING["bank_id"], "unknown")
    channel = _get_value(data, KEY_MAPPING["channel"], "unknown")
    operation_type = _get_value(data, KEY_MAPPING["operation_type"], "unknown")
    status = str(_get_value(data, KEY_MAPPING["status"], "unknown"))
    error_code = _get_value(data, KEY_MAPPING["error_code"], None)
    latency_raw = _get_value(data, KEY_MAPPING["latency_ms"], 0)
    latency_ms = float(latency_raw)
    return TransactionEvent(
        timestamp=timestamp,
        bank_id=str(bank_id),
        channel=str(channel),
        operation_type=str(operation_type),
        status=status,
        error_code=str(error_code) if error_code is not None else None,
        latency_ms=latency_ms,
    )


def parse_lines(lines: Iterable[str]) -> List[TransactionEvent]:
    events: List[TransactionEvent] = []
    for line in lines:
        event = parse_line(line)
        if event:
            events.append(event)
    return events
