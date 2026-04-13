#!/usr/bin/env bash
# archive-run.sh — Collect metrics for a completed run
#
# Usage: ./archive-run.sh <run-directory-path>
# Example: ./archive-run.sh /path/to/repo/runs/CLAUDE-RUNS/RUN-20260412-0516-fix-auth-bug
#
# Reads .claude/archive-run.config to determine which collectors to run.
# Falls back to git-only if no config exists.
# Output: prints metric summary to stdout (paste into ARCHIVE.md entry).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
METRICS_DIR="$SCRIPT_DIR/metrics"

# Find repo root via git
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "ERROR: Not inside a git repository"
  exit 1
}

CONFIG_FILE="$REPO_ROOT/.claude/archive-run.config"

if [ $# -lt 1 ]; then
  echo "Usage: ./archive-run.sh <run-directory-path>"
  echo "Example: ./archive-run.sh runs/CLAUDE-RUNS/RUN-20260412-0516-fix-auth-bug"
  exit 1
fi

RUN_DIR="$1"

# Resolve relative paths against repo root
if [[ ! "$RUN_DIR" = /* ]]; then
  RUN_DIR="$REPO_ROOT/$RUN_DIR"
fi

if [ ! -d "$RUN_DIR" ]; then
  echo "ERROR: Run directory not found: $RUN_DIR"
  exit 1
fi

# Determine which collectors to run
COLLECTORS=()
if [ -f "$CONFIG_FILE" ]; then
  while IFS= read -r line; do
    # Skip comments and blank lines
    line="$(echo "$line" | sed 's/#.*//' | xargs)"
    [ -z "$line" ] && continue
    COLLECTORS+=("$line")
  done < "$CONFIG_FILE"
else
  # Default: git only
  COLLECTORS=("git")
fi

echo "=== Archive Metrics for $(basename "$RUN_DIR") ==="
echo ""

for collector in "${COLLECTORS[@]}"; do
  collector_script="$METRICS_DIR/${collector}.sh"
  if [ -f "$collector_script" ]; then
    echo "--- $collector ---"
    bash "$collector_script" "$REPO_ROOT" "$RUN_DIR" 2>&1 || echo "  (collector failed)"
    echo ""
  else
    echo "WARNING: Collector not found: $collector_script"
  fi
done

echo "=== End Metrics ==="
