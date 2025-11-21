#!/usr/bin/env bash
set -euo pipefail
ruff sbp_observability tests || true
mypy sbp_observability || true
