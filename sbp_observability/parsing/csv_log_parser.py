"""CSV log parser."""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

from sbp_observability.config import ParserConfig
from sbp_observability.models import TransactionEvent


DEFAULT_COLUMNS = {
    "timestamp": "timestamp",
    "bank_id": "bank_id",
    "channel": "channel",
    "operation_type": "operation_type",
    "status": "status",
    "error_code": "error_code",
    "latency_ms": "latency_ms",
}


def parse_file(path: str | Path, config: ParserConfig | None = None) -> List[TransactionEvent]:
    mapping = DEFAULT_COLUMNS | ((config.column_mapping if config else {}))
    events: List[TransactionEvent] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            try:
                ts_str = row[mapping["timestamp"]]
                timestamp = datetime.fromisoformat(ts_str)
            except (KeyError, ValueError):
                continue
            events.append(
                TransactionEvent(
                    timestamp=timestamp,
                    bank_id=row.get(mapping["bank_id"], "unknown"),
                    channel=row.get(mapping["channel"], "unknown"),
                    operation_type=row.get(mapping["operation_type"], "unknown"),
                    status=row.get(mapping["status"], "unknown"),
                    error_code=row.get(mapping["error_code"]),
                    latency_ms=float(row.get(mapping["latency_ms"], 0) or 0),
                )
            )
    return events


def parse_lines(lines: Iterable[str], config: ParserConfig | None = None) -> List[TransactionEvent]:
    from io import StringIO

    buffer = StringIO("\n".join(lines))
    mapping = DEFAULT_COLUMNS | ((config.column_mapping if config else {}))
    events: List[TransactionEvent] = []
    reader = csv.DictReader(buffer)
    for row in reader:
        try:
            ts_str = row[mapping["timestamp"]]
            timestamp = datetime.fromisoformat(ts_str)
        except (KeyError, ValueError):
            continue
        events.append(
            TransactionEvent(
                timestamp=timestamp,
                bank_id=row.get(mapping["bank_id"], "unknown"),
                channel=row.get(mapping["channel"], "unknown"),
                operation_type=row.get(mapping["operation_type"], "unknown"),
                status=row.get(mapping["status"], "unknown"),
                error_code=row.get(mapping["error_code"]),
                latency_ms=float(row.get(mapping["latency_ms"], 0) or 0),
            )
        )
    return events
