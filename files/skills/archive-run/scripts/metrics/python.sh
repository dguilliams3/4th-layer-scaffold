#!/usr/bin/env bash
# python.sh — Python project metrics collector
# Usage: python.sh <repo-root> <run-directory>
# Requires: Python project with pytest/ruff/mypy available

REPO_ROOT="$1"
cd "$REPO_ROOT"

# pytest
if command -v pytest &>/dev/null; then
  echo "pytest:"
  RESULT="$(pytest --tb=no -q 2>&1 | tail -1)" || true
  echo "  $RESULT"
else
  echo "pytest: not found (skipped)"
fi

# ruff
if command -v ruff &>/dev/null; then
  COUNT="$(ruff check . --quiet 2>&1 | wc -l | xargs)"
  echo "ruff errors: $COUNT"
else
  echo "ruff: not found (skipped)"
fi

# mypy
if command -v mypy &>/dev/null; then
  RESULT="$(mypy . --no-error-summary 2>&1 | tail -1)" || true
  echo "mypy: $RESULT"
else
  echo "mypy: not found (skipped)"
fi

# coverage (if .coverage file exists)
if [ -f ".coverage" ] && command -v coverage &>/dev/null; then
  TOTAL="$(coverage report 2>&1 | tail -1 | awk '{print $NF}')" || true
  echo "coverage: $TOTAL"
fi
