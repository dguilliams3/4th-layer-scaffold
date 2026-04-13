#!/usr/bin/env bash
# git.sh — Universal git metrics collector
# Usage: git.sh <repo-root> <run-directory>
# Always available — no project-specific dependencies.

REPO_ROOT="$1"
RUN_DIR="$2"

cd "$REPO_ROOT"

BRANCH="$(git branch --show-current 2>/dev/null || echo 'detached')"
echo "Branch: $BRANCH"

# Try to find the merge base with main/master
BASE_BRANCH=""
for candidate in main master develop; do
  if git rev-parse --verify "$candidate" &>/dev/null; then
    BASE_BRANCH="$candidate"
    break
  fi
done

if [ -n "$BASE_BRANCH" ]; then
  MERGE_BASE="$(git merge-base "$BASE_BRANCH" HEAD 2>/dev/null || true)"
  if [ -n "$MERGE_BASE" ]; then
    COMMITS="$(git rev-list --count "$MERGE_BASE..HEAD" 2>/dev/null || echo '?')"
    echo "Commits ahead of $BASE_BRANCH: $COMMITS"

    DIFFSTAT="$(git diff --stat "$MERGE_BASE..HEAD" 2>/dev/null | tail -1)"
    echo "Diff stat: $DIFFSTAT"

    FILES_CHANGED="$(git diff --name-only "$MERGE_BASE..HEAD" 2>/dev/null | wc -l | xargs)"
    echo "Files changed: $FILES_CHANGED"
  fi
else
  echo "Commits: (no base branch found for comparison)"
fi
