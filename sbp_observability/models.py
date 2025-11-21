"""Domain models for SBP observability."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TransactionEvent:
    timestamp: datetime
    bank_id: str
    channel: str
    operation_type: str
    status: str
    error_code: Optional[str]
    latency_ms: float


@dataclass
class ErrorClass:
    name: str
    pattern: str
    severity: str
    description_ru: str


@dataclass
class BankChannelStats:
    bank_id: str
    channel: str
    success_count: int
    failure_count: int
    p95_latency_ms: float
