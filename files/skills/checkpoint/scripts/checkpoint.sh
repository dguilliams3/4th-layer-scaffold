#!/usr/bin/env bash
# checkpoint.sh — Create a CHECKPOINT-0N-<slug>.md from template in the current run.
#
# Usage:
#   ./checkpoint.sh <slug> [<run-id-or-prefix>]
# Examples:
#   ./checkpoint.sh pre-launch-readiness
#   ./checkpoint.sh post-codex-completion RUN-20260513-1404-dashboard-demo-and-release-prep
#   ./checkpoint.sh midday-state RUN-20260513-1404  # prefix match also works
#
# Creates: runs/CLAUDE-RUNS/<RUN>/checkpoints/CHECKPOINT-0N-<slug>.md
#
# Defaults:
#   - Auto-detects active run as the newest RUN-* directory under runs/CLAUDE-RUNS/ by mtime.
#   - Auto-increments N (zero-padded to 2 digits) based on existing CHECKPOINT-NN-*.md.
#   - Resolves PREV_CHECKPOINT by finding the file for N-1.
#
# Template sourced from: ../templates/CHECKPOINT.md (relative to this script).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$(cd "$SCRIPT_DIR/../templates" && pwd)"

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "ERROR: Not inside a git repository"
  exit 1
}

RUNS_DIR="$REPO_ROOT/runs/CLAUDE-RUNS"

if [ $# -lt 1 ]; then
  echo "Usage: ./checkpoint.sh <slug> [<run-id-or-prefix>]"
  echo "Example: ./checkpoint.sh pre-launch-readiness"
  exit 1
fi

SLUG="$1"
RUN_ARG="${2:-}"

# --- Resolve run directory ---------------------------------------------------

if [ -n "$RUN_ARG" ]; then
  # Exact match first
  if [ -d "$RUNS_DIR/$RUN_ARG" ]; then
    RUN_DIR="$RUNS_DIR/$RUN_ARG"
  else
    # Prefix match (e.g. "RUN-20260513-1404" matches the full slug)
    MATCHES="$(find "$RUNS_DIR" -maxdepth 1 -type d -name "${RUN_ARG}*" 2>/dev/null)"
    MATCH_COUNT="$(echo "$MATCHES" | grep -c . || true)"
    if [ "$MATCH_COUNT" = "0" ]; then
      echo "ERROR: No run matching '$RUN_ARG' under $RUNS_DIR"
      exit 1
    elif [ "$MATCH_COUNT" -gt 1 ]; then
      echo "ERROR: Multiple runs match '$RUN_ARG':"
      echo "$MATCHES"
      echo "Use a longer prefix."
      exit 1
    fi
    RUN_DIR="$MATCHES"
  fi
else
  # Auto-detect: newest RUN-* by mtime
  # Portable newest-by-mtime (BSD/macOS find lacks -printf): ls -t sorts by mtime.
  RUN_DIR="$(ls -dt "$RUNS_DIR"/RUN-*/ 2>/dev/null | head -1)"
  RUN_DIR="${RUN_DIR%/}"
  if [ -z "$RUN_DIR" ] || [ ! -d "$RUN_DIR" ]; then
    echo "ERROR: No run directories found in $RUNS_DIR"
    echo "Hint: Use task-tracking/scripts/init-run.sh to create one first."
    exit 1
  fi
  echo "Auto-detected run: $(basename "$RUN_DIR")"
fi

CHECKPOINTS_DIR="$RUN_DIR/checkpoints"
mkdir -p "$CHECKPOINTS_DIR"

# --- Compute next N + predecessor --------------------------------------------

LAST_N=0
if [ -d "$CHECKPOINTS_DIR" ]; then
  LAST_N=$(find "$CHECKPOINTS_DIR" -maxdepth 1 -name 'CHECKPOINT-[0-9][0-9]*.md' 2>/dev/null \
           | sed 's|.*/||' \
           | sed -E 's/^CHECKPOINT-([0-9]+).*/\1/' \
           | sort -n \
           | tail -1)
  LAST_N=${LAST_N:-0}
fi

NEXT_N=$((10#$LAST_N + 1))
N_PADDED=$(printf '%02d' "$NEXT_N")

if [ "$LAST_N" = "0" ]; then
  PREV_CHECKPOINT="N/A (first checkpoint of this run)"
else
  PREV_PADDED=$(printf '%02d' "$((10#$LAST_N))")
  PREV_FILE="$(find "$CHECKPOINTS_DIR" -maxdepth 1 -name "CHECKPOINT-${PREV_PADDED}-*.md" 2>/dev/null | sed 's|.*/||' | head -1)"
  if [ -z "$PREV_FILE" ]; then
    # Bare CHECKPOINT-NN.md form (no slug)
    PREV_FILE="$(find "$CHECKPOINTS_DIR" -maxdepth 1 -name "CHECKPOINT-${PREV_PADDED}.md" 2>/dev/null | sed 's|.*/||' | head -1)"
  fi
  PREV_CHECKPOINT="${PREV_FILE:-CHECKPOINT-${PREV_PADDED}.md}"
fi

# --- Generate the checkpoint file --------------------------------------------

RUN_ID="$(basename "$RUN_DIR")"
TIMESTAMP="$(date +'%Y-%m-%d %H:%M') EST"
LABEL="${SLUG//-/ }"  # dashes -> spaces for the H1; user edits casing if desired

CHECKPOINT_FILE="$CHECKPOINTS_DIR/CHECKPOINT-${N_PADDED}-${SLUG}.md"

if [ -e "$CHECKPOINT_FILE" ]; then
  echo "ERROR: Checkpoint already exists: $CHECKPOINT_FILE"
  exit 1
fi

if [ ! -f "$TEMPLATE_DIR/CHECKPOINT.md" ]; then
  echo "ERROR: Template not found at $TEMPLATE_DIR/CHECKPOINT.md"
  exit 1
fi

# Substitute placeholders.
# Using | as sed delimiter for paths so /-bearing values (run IDs with dashes) work.
sed -e "s|{{N}}|${N_PADDED}|g" \
    -e "s|{{LABEL}}|${LABEL}|g" \
    -e "s|{{RUN_ID}}|${RUN_ID}|g" \
    -e "s|{{TIMESTAMP}}|${TIMESTAMP}|g" \
    -e "s|{{PREV_CHECKPOINT}}|${PREV_CHECKPOINT}|g" \
    "$TEMPLATE_DIR/CHECKPOINT.md" > "$CHECKPOINT_FILE"

echo "✅ Created: $CHECKPOINT_FILE"
echo "   Run:        $RUN_ID"
echo "   Predecessor: $PREV_CHECKPOINT"
echo ""
echo "Next steps (Claude Code workflow):"
echo "  1. Read the file via the Read tool — REQUIRED before any Edit."
echo "  2. Edit to fill sections. Default style: verbose and comprehensive."
echo "  3. The reader is post-compact-you. Over-explain rather than under-explain."
