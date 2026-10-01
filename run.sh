#!/usr/bin/env bash
# One-shot local run. Usage: ./run.sh [pytest args]
set -euo pipefail

export PYTHONPATH=.
mkdir -p reports

echo "==> Python:     $(python3 --version)"
echo "==> Playwright: $(python3 -m playwright --version)"
echo "==> Running suite..."

python3 -m pytest "$@"

echo "==> Report: reports/report.html"
