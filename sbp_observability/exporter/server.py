"""Simple metrics HTTP server."""
from __future__ import annotations

from http.server import HTTPServer

from prometheus_client import make_wsgi_app
from wsgiref.simple_server import make_server


def start_metrics_server(host: str = "0.0.0.0", port: int = 8000):
    app = make_wsgi_app()
    httpd = make_server(host, port, app)
    return httpd
