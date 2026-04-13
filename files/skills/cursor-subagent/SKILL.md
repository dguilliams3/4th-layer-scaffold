---
name: cursor-subagent
description: Use when spawning Cursor agent as a subagent for investigation, search, or codebase exploration — includes verified Windows invocation flags and do/don't patterns
---

# Cursor Agent as Subagent

## Overview

Use `agent --print` to isolate noisy investigative work (grep traversals, multi-file reads, dependency traces) from the main context window. This is about **context hygiene**, not capability.

**Prerequisite:** `~/bin/agent` in PATH (already configured on this machine)

## Verified Invocation (Windows / Git Bash)

```bash
agent --force --trust --model composer-2-fast --output-format stream-json --print "your full task here" 2>&1
```

Run with `run_in_background: true`. To peek at output:
```bash
head -n 50 <output-file>   # peek at the output FILE — never pipe the launch command
```

`permissionMode: "default"` in the stream-json output is normal — not an error.

## Task Description IS the Full Prompt

Include directly in `--print "..."`:
- Absolute directory paths for files to read/write
- Path to write `FINDINGS.md`
- Expected output format

No injection wrapper needed.

## Available Models

| Model | Use Case |
|-------|----------|
| `composer-2-fast` | Default — fast recon/investigation (effectively unlimited monthly usage) |
| `composer-2` | Higher quality, slower |
| `claude-4.6-sonnet-medium` | When Claude's reasoning is preferable |

## DO NOT

- **DO NOT** use `agent.cmd` directly — Windows CMD shim truncates multi-line prompts
- **DO NOT** pipe the launch command (`| tail`, `| head`) — kills the background process
- **DO NOT** use stdin pipe (`echo "..." | agent ... -`) — broken on Windows, produces empty output; use `--print "prompt"` positional arg instead
- **DO NOT** use `--workspace` unless explicitly overriding the working directory

## When to Use

- Path to the answer is noisy (grep traversals, multi-file reads, dependency traces)
- Task is self-contained with a clear objective and a FINDINGS.md output
- You want intermediate traversal work isolated from your context window
