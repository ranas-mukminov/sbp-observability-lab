"""Parser for nginx-style access logs."""
from __future__ import annotations

import re
from datetime import datetime
from typing import Iterable, List

from sbp_observability.models import TransactionEvent

LOG_PATTERN = re.compile(
    r"^(?P<ts>[^ ]+) \[(?P<bank>[\w-]+)\] \[(?P<channel>[\w-]+)\] "
    r"(?P<operation>[\w-]+) (?P<status>\d{3}) (?P<latency>[\d\.]+)"
)


def parse_line(line: str) -> TransactionEvent | None:
    """Parse a single nginx access log line into TransactionEvent."""
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None
    status_code = int(match.group("status"))
    status = "success" if 200 <= status_code < 400 else "failed"
    latency_seconds = float(match.group("latency"))
    return TransactionEvent(
        timestamp=datetime.fromisoformat(match.group("ts")),
        bank_id=match.group("bank"),
        channel=match.group("channel"),
        operation_type=match.group("operation"),
        status=status,
        error_code=None if status == "success" else str(status_code),
        latency_ms=latency_seconds * 1000,
    )


def parse_lines(lines: Iterable[str]) -> List[TransactionEvent]:
    """Parse multiple nginx log lines."""
    events = []
    for line in lines:
        event = parse_line(line)
        if event:
            events.append(event)
    return events
