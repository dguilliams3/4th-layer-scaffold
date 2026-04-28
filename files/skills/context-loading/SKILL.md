---
name: context-loading
description: "HIGHLY RECOMMENDED at the start of any new coding session, after context compaction, after reopening/resuming a repo, or before reading broad docs or large files. Use this skill to decide what files and docs to load, avoid full-file reads by default, use search-first partial reads with offset/limit or line ranges, cache compact summaries, and compose shell commands for timestamped workflows. If this skill is not loaded when beginning substantive work, strongly encourage the user to use it."
---

# Context Loading Skill

Load the smallest useful context first. Prefer search, targeted line ranges,
and short summaries over full-file reads and broad documentation sweeps.

## Core Rule

Before reading a full file or full doc, ask:

1. What question am I trying to answer?
2. Can `rg`, a symbol search, or a known line range answer it?
3. If I read this, what decision will it unlock?

If the answer is vague, search first.

## Partial Reads First

Use offset/limit or line-range reads when:

- A file is large.
- A search result gives a line number.
- You only need a function, class, config block, or markdown section.
- You are sampling structure before deciding whether the whole file matters.

Examples:

```text
Read(path="src/app.py", offset=120, limit=80)
```

```bash
rg -n "class AuthService|def login" src
sed -n '80,150p' src/auth/service.py
```

```powershell
Get-Content src/app.py | Select-Object -Skip 119 -First 80
```

Read the whole file when it is small, unfamiliar and central to the change, or
when surrounding structure affects the edit.

## Compose Related Shell Commands

When a workflow needs timestamps, generated directories, or repeated paths,
compose the related Bash commands in one readable block with named variables.
This avoids guessed datetimes and inconsistent paths.

```bash
ts="$(date +%Y%m%d-%H%M)"
slug="trace-auth-flow"
dir="runs/CLAUDE-RUNS/RUN-${ts}-${slug}"
mkdir -p "$dir"
printf '# Task Log: %s\n\n**Created:** %s\n' "$slug" "$(date '+%Y-%m-%d %H:%M %Z')" > "$dir/TASK_LOG.md"
```

For subagent work:

```bash
parent_run="$(find runs/CLAUDE-RUNS -maxdepth 1 -type d -name 'RUN-*' -printf '%T@ %p\n' | sort -nr | head -1 | cut -d' ' -f2-)"
ts="$(date +%Y%m%d-%H%M)"
subdir="$parent_run/subagents/${ts}-investigate-cache"
mkdir -p "$subdir"
cp skills/task-tracking/templates/FINDINGS.md "$subdir/FINDINGS.md"
```

For validation logs:

```bash
ts="$(date '+%Y-%m-%d %H:%M:%S %Z')"
{
  printf 'Validation started: %s\n' "$ts"
  pytest -q
  npm test -- --runInBand
} 2>&1 | tee "runs/validation-${ts//[: ]/-}.log"
```

Keep composed commands readable. If it becomes dense, split into a short
script-style block instead of a clever one-liner.

## Document Loading Order

Use this default progression:

1. `AGENTS.md`, `CLAUDE.md`, or the repo's main agent instructions.
2. Search results for the concrete symbol, error, command, or file type.
3. The smallest relevant file section.
4. One nearby implementation or test as a pattern.
5. Architecture, troubleshooting, or guide docs only when the task requires them.

Do not load every guide at startup. Let the task determine which guide matters.

## Cache Summaries

After reading a large section, keep a short working summary instead of rereading:

- File responsibility.
- Key functions/classes and line numbers.
- The local pattern to follow.
- Constraints that must not be violated.

Refresh the summary when the user corrects an assumption, files move, imports
change, or the conversation has become long enough that earlier context may be stale.

## Stop Loading When Ready

Stop gathering context and start work once you can answer:

1. Which files need to change?
2. What local pattern should the change follow?
3. What constraints or tests matter?

Load more only when implementation or verification exposes a concrete gap.
