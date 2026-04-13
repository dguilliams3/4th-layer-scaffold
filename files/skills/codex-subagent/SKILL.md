---
name: codex-subagent
description: Use when spawning Codex CLI as a subagent for long, focused implementation tasks — includes correct Windows invocation, model selection, and do/don't patterns
---

# Codex as Implementation Subagent

## Overview

Codex runs independently with full file access. Best for mechanical, long-horizon implementation where the SPEC can carry all context. Bottleneck is SPEC quality, not model capability.

## Setup (before invoking)

1. Create subagent directory: `runs/CLAUDE-RUNS/RUN-*/subagents/YYYYMMDD-HHMM-subtask/`
2. Write `SPEC.md` there — objective, constraints, deliverables, success criteria
3. **SPEC.md is the primary interface.** All context goes there, NOT in the CLI prompt.
4. Include the absolute working directory path **inside the SPEC.md or prompt** (not via `-C`)

## The Correct Invocation (Windows / Git Bash)

```bash
echo "Working directory: /c/Users/YourUser/path/to/your-repo. Read <relative/path/to/SPEC.md> and follow the instructions." | \
  codex exec --model gpt-5.3-codex --dangerously-bypass-approvals-and-sandbox - 2>&1
```

Run with `run_in_background: true`. Read output with `TaskOutput` after completion.

## Key Flags

| Flag                                         | Purpose                | Required?                           |
| -------------------------------------------- | ---------------------- | ----------------------------------- |
| `exec`                                       | Non-interactive mode   | YES                                 |
| `-`                                          | Read prompt from stdin | YES — avoids Windows quoting issues |
| `--model gpt-5.3-codex`                      | Current best model     | YES                                 |
| `--dangerously-bypass-approvals-and-sandbox` | Full file access       | YES for implementation              |

## DO NOT

- **DO NOT** use `-C <dir>` — spaces in paths (e.g. `OneDrive`) break it on Windows. Put working dir in the prompt instead.
- **DO NOT** pipe output to `| head`, `| tail`, or `> logfile &` when using `run_in_background` — creates a subshell that kills Codex mid-run
- **DO NOT** use `cmd //c` wrapper — Git Bash POSIX-to-Win32 quote mangling will break it
- **DO NOT** put the full task prompt in the CLI — use SPEC.md instead
