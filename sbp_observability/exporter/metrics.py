"""Prometheus metrics definitions."""
from __future__ import annotations

from prometheus_client import Counter, Gauge, Histogram

REQUEST_BUCKETS = (
    0.05,
    0.1,
    0.2,
    0.3,
    0.5,
    0.75,
    1,
    2,
    3,
    5,
)

sbp_requests_total = Counter(
    "sbp_requests_total",
    "Total SBP requests",
    ["bank", "channel", "operation_type", "status"],
)

sbp_request_errors_total = Counter(
    "sbp_request_errors_total",
    "Total SBP errors",
    ["bank", "channel", "operation_type", "error_class"],
)

sbp_rate_limit_events_total = Counter(
    "sbp_rate_limit_events_total",
    "Rate limit events",
    ["bank", "channel"],
)

sbp_request_latency_seconds = Histogram(
    "sbp_request_latency_seconds",
    "SBP request latency",
    ["bank", "channel", "operation_type"],
    buckets=REQUEST_BUCKETS,
)

sbp_gateway_up = Gauge(
    "sbp_gateway_up",
    "Gateway availability",
    ["gateway"],
)

sbp_error_rate_5m = Gauge(
    "sbp_error_rate_5m",
    "Error rate computed externally",
    ["bank", "channel"],
)


__all__ = [
    "sbp_requests_total",
    "sbp_request_errors_total",
    "sbp_rate_limit_events_total",
    "sbp_request_latency_seconds",
    "sbp_gateway_up",
    "sbp_error_rate_5m",
    "REQUEST_BUCKETS",
]
