"""Lightweight HTTP proxy placeholder."""
from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Callable, Dict, Tuple
from urllib.parse import urlparse

from sbp_observability.config import AppConfig
from sbp_observability.models import TransactionEvent


class MaskingMixin:
    @staticmethod
    def mask_payload(body: Dict[str, str], keys: Tuple[str, ...]) -> Dict[str, str]:
        return {k: ("***" if k in keys else v) for k, v in body.items()}


class ProxyRequestHandler(BaseHTTPRequestHandler, MaskingMixin):
    upstream_handler: Callable[[TransactionEvent], None] | None = None
    app_config: AppConfig = AppConfig()

    def _send_json(self, payload: dict, status: int = 200):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length).decode("utf-8")
        try:
            body = json.loads(raw_body or "{}")
        except json.JSONDecodeError:
            self._send_json({"error": "invalid json"}, status=400)
            return
        masked = self.mask_payload(body, self.app_config.mask_keys)
        parsed = urlparse(self.path)
        event = TransactionEvent(
            timestamp=datetime.now(tz=timezone.utc),
            bank_id=masked.get("bank_id", "unknown"),
            channel=masked.get("channel", "unknown"),
            operation_type=masked.get("operation_type", parsed.path.strip("/")),
            status="success",
            error_code=None,
            latency_ms=float(masked.get("latency_ms", 0)),
        )
        if self.upstream_handler:
            self.upstream_handler(event)  # type: ignore[arg-type]
        self._send_json({"proxied": True, "event": asdict(event)})

    def log_message(self, format: str, *args):  # noqa: A003
        return


def start_proxy(host: str, port: int, app_config: AppConfig, handler: Callable[[TransactionEvent], None]):
    ProxyRequestHandler.upstream_handler = handler
    ProxyRequestHandler.app_config = app_config
    server = HTTPServer((host, port), ProxyRequestHandler)
    return server
