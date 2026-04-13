#!/usr/bin/env bash
# rust.sh — Rust project metrics collector
# Usage: rust.sh <repo-root> <run-directory>
# Requires: Rust project with cargo available

REPO_ROOT="$1"
cd "$REPO_ROOT"

if ! command -v cargo &>/dev/null || [ ! -f "Cargo.toml" ]; then
  echo "cargo: not a Rust project (skipped)"
  exit 0
fi

# cargo test
echo "cargo test:"
RESULT="$(cargo test --no-fail-fast 2>&1 | grep '^test result:')" || true
if [ -n "$RESULT" ]; then
  echo "  $RESULT"
else
  echo "  (no test output captured)"
fi

# clippy
if cargo clippy --version &>/dev/null 2>&1; then
  WARNINGS="$(cargo clippy --message-format=short 2>&1 | grep -c 'warning\[' || echo '0')"
  echo "clippy warnings: $WARNINGS"
else
  echo "clippy: not available (skipped)"
fi
