#!/usr/bin/env bash
# Rebuild every table, figure and recommendation from the retained public data.
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-.venv/bin/python}"
for step in fetch_data build_costs prepare_data explore_data design_space check_gp compare_models select_batch memo_figures; do
  echo "== $step"
  "$PY" "scripts/$step.py"
done
echo "Done. Recommendation: outputs/next_experiments.csv"
if command -v git >/dev/null && git rev-parse --git-dir >/dev/null 2>&1; then
  echo "== files that differ from the committed version (empty means identical)"
  git diff --stat -- outputs reports/tables data/processed
fi
