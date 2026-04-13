#!/usr/bin/env bash
# go.sh — Go project metrics collector
# Usage: go.sh <repo-root> <run-directory>
# Requires: Go project with go toolchain available

REPO_ROOT="$1"
cd "$REPO_ROOT"

if ! command -v go &>/dev/null || [ ! -f "go.mod" ]; then
  echo "go: not a Go project (skipped)"
  exit 0
fi

# go test
echo "go test:"
RESULT="$(go test ./... -count=1 -short 2>&1 | tail -5)" || true
echo "$RESULT" | sed 's/^/  /'

# go vet
echo "go vet:"
VET="$(go vet ./... 2>&1)" || true
if [ -z "$VET" ]; then
  echo "  clean"
else
  COUNT="$(echo "$VET" | wc -l | xargs)"
  echo "  $COUNT issues"
fi
