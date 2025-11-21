"""Typer CLI entrypoint."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer

from sbp_observability.ai.report_generator import build_weekly_report
from sbp_observability.config import AppConfig, load_config
from sbp_observability.exporter.server import start_metrics_server
from sbp_observability.parsing import csv_log_parser, json_log_parser, nginx_access_parser, normalizer

app = typer.Typer(help="SBP observability lab CLI")


@app.command()
def parse_logs(log_path: Path, format: str = "nginx", config_path: Optional[Path] = None):
    """Parse logs and print aggregated stats to stdout."""
    config = load_config(config_path)
    if format == "nginx":
        with log_path.open() as handle:
            events = nginx_access_parser.parse_lines(handle.readlines())
    elif format == "json":
        with log_path.open() as handle:
            events = json_log_parser.parse_lines(handle.readlines())
    else:
        events = csv_log_parser.parse_file(log_path, config.parser)
    normalized = normalizer.normalize_events(events)
    typer.echo(json.dumps([event.__dict__ for event in normalized], default=str))


@app.command()
def run_proxy(host: str = "0.0.0.0", port: int = 8080):
    """Dummy proxy placeholder (no actual upstream forward)."""
    app_config = AppConfig()
    from sbp_observability.proxy.http_proxy import start_proxy

    server = start_proxy(host, port, app_config, handler=lambda event: None)
    typer.echo(f"Proxy listening on {host}:{port}")
    server.serve_forever()


@app.command()
def run_exporter(host: str = "0.0.0.0", port: int = 8000):
    """Run Prometheus metrics endpoint."""
    server = start_metrics_server(host, port)
    typer.echo(f"Exporter listening on {host}:{port}")
    server.serve_forever()


@app.command()
def generate_weekly_report(input_path: Path):
    """Generate a weekly markdown report from a file containing error codes/messages."""
    with input_path.open() as handle:
        errors = [line.strip() for line in handle if line.strip()]
    report = build_weekly_report(errors)
    typer.echo(report)


if __name__ == "__main__":
    app()
