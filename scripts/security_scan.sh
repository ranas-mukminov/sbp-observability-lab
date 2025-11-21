#!/usr/bin/env bash
set -euo pipefail
pip-audit || true
bandit -q -r sbp_observability || true
