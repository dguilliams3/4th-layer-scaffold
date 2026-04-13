#!/usr/bin/env bash
# node.sh — Node.js project metrics collector
# Usage: node.sh <repo-root> <run-directory>
# Requires: Node.js project with eslint/jest available

REPO_ROOT="$1"
cd "$REPO_ROOT"

# eslint
if command -v npx &>/dev/null && [ -f "package.json" ]; then
  if npx --no eslint --version &>/dev/null 2>&1; then
    ERRORS="$(npx --no eslint . --format compact 2>&1 | grep -c ' Error -' || echo '0')"
    WARNINGS="$(npx --no eslint . --format compact 2>&1 | grep -c ' Warning -' || echo '0')"
    echo "eslint: $ERRORS errors, $WARNINGS warnings"
  else
    echo "eslint: not configured (skipped)"
  fi
else
  echo "eslint: no package.json (skipped)"
fi

# jest
if [ -f "package.json" ] && command -v npx &>/dev/null; then
  if grep -q '"jest"' package.json 2>/dev/null || [ -f "jest.config.js" ] || [ -f "jest.config.ts" ]; then
    RESULT="$(npx --no jest --passWithNoTests --silent 2>&1 | tail -3)" || true
    echo "jest:"
    echo "$RESULT" | sed 's/^/  /'
  else
    echo "jest: not configured (skipped)"
  fi
fi
