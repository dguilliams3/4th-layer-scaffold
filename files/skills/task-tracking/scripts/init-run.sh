#!/usr/bin/env bash
# init-run.sh — Initialize a new Claude Code run directory
#
# Usage: ./init-run.sh <slug>
# Example: ./init-run.sh fix-auth-bug
#   Creates: RUN-YYYYMMDD-HHMM-fix-auth-bug/ with TASK_LOG.md, SPEC_v1.md, HANDOFF.md
#
# Templates sourced from: ../templates/ (relative to this script)
# Run directories created in: runs/CLAUDE-RUNS/ (relative to repo root)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$(cd "$SCRIPT_DIR/../templates" && pwd)"

# Find repo root via git
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "ERROR: Not inside a git repository"
  exit 1
}

RUNS_DIR="$REPO_ROOT/runs/CLAUDE-RUNS"

if [ $# -lt 1 ]; then
  echo "Usage: ./init-run.sh <slug>"
  echo "Example: ./init-run.sh fix-auth-bug"
  exit 1
fi

SLUG="$1"
RUN_ID="$(date +%Y%m%d-%H%M)"
TIMESTAMP="$(date +'%Y-%m-%d %H:%M') EST"
DESCRIPTION="[Describe objective here]"

RUN_DIR="$RUNS_DIR/RUN-${RUN_ID}-${SLUG}"

if [ -d "$RUN_DIR" ]; then
  echo "ERROR: Directory already exists: $RUN_DIR"
  exit 1
fi

# Ensure runs directory exists
mkdir -p "$RUNS_DIR"
mkdir -p "$RUN_DIR"

# Generate TASK_LOG.md from template
if [ -f "$TEMPLATE_DIR/TASK_LOG.md" ]; then
  sed -e "s/{{RUN_ID}}/$RUN_ID/g" \
      -e "s/{{SLUG}}/$SLUG/g" \
      -e "s/{{TIMESTAMP}}/$TIMESTAMP/g" \
      -e "s/{{DESCRIPTION}}/$DESCRIPTION/g" \
      "$TEMPLATE_DIR/TASK_LOG.md" > "$RUN_DIR/TASK_LOG.md"
else
  echo "WARNING: TASK_LOG template not found at $TEMPLATE_DIR/TASK_LOG.md"
fi

# Generate SPEC_v1.md from template
if [ -f "$TEMPLATE_DIR/SPEC_v1.md" ]; then
  sed -e "s/{{RUN_ID}}/$RUN_ID/g" \
      -e "s/{{SLUG}}/$SLUG/g" \
      -e "s/{{TIMESTAMP}}/$TIMESTAMP/g" \
      -e "s/{{DESCRIPTION}}/$DESCRIPTION/g" \
      "$TEMPLATE_DIR/SPEC_v1.md" > "$RUN_DIR/SPEC_v1.md"
else
  echo "WARNING: SPEC template not found at $TEMPLATE_DIR/SPEC_v1.md"
fi

# Generate HANDOFF.md from template (filled at run completion, not now)
if [ -f "$TEMPLATE_DIR/HANDOFF.md" ]; then
  sed -e "s/{{RUN_ID}}/$RUN_ID/g" \
      -e "s/{{SLUG}}/$SLUG/g" \
      -e "s/{{TIMESTAMP}}/$TIMESTAMP/g" \
      -e "s/{{DESCRIPTION}}/$DESCRIPTION/g" \
      "$TEMPLATE_DIR/HANDOFF.md" > "$RUN_DIR/HANDOFF.md"
else
  echo "WARNING: HANDOFF template not found at $TEMPLATE_DIR/HANDOFF.md"
fi

echo "✅ Created: $RUN_DIR"
echo "   TASK_LOG.md"
echo "   SPEC_v1.md"
echo "   HANDOFF.md (fill at completion)"
echo ""
echo "Run ID: RUN-$RUN_ID"
