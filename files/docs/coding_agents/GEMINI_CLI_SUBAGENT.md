# Gemini CLI — Headless Subagent Reference

> **Purpose**: How to invoke Google's Gemini CLI as a headless subagent from Claude Code, with full auto-accept permissions — analogous to Codex CLI usage.

---

## Installation

```bash
npm install -g @google/gemini-cli
```

Binary name: `gemini`
Version (as of 2026-03-13): 0.33.1

First run creates `~/.gemini/` for config/session storage. If it errors on Windows, `mkdir -p ~/.gemini` first.

---

## Authentication

Gemini CLI authenticates via Google account (OAuth browser flow on first run) or API key:

```bash
# Option 1: OAuth (interactive first-time, then cached)
gemini -p "hello"  # triggers browser auth on first use

# Option 2: API key (headless-friendly)
export GEMINI_API_KEY="your-key-here"
gemini -p "hello"
```

For subagent usage, set `GEMINI_API_KEY` in your shell profile so background invocations don't hang waiting for OAuth.

---

## Headless Invocation (Non-Interactive)

### Core Pattern

```bash
gemini -p "Your task description" --yolo --output-format text
```

| Flag | Short | Purpose |
|------|-------|---------|
| `--prompt` | `-p` | Non-interactive mode — run prompt and exit |
| `--yolo` | `-y` | Auto-accept ALL tool/action confirmations |
| `--output-format` | `-o` | `text` (default), `json`, or `stream-json` |
| `--model` | `-m` | Model override (e.g., `gemini-3.1-pro-preview`, `gemini-2.5-flash`) |

### Approval Modes (Granular Alternative to --yolo)

```bash
--approval-mode default     # prompt for every action (interactive only)
--approval-mode auto_edit   # auto-approve file edits, prompt for other actions
--approval-mode yolo        # auto-approve everything (same as --yolo)
--approval-mode plan        # read-only — no edits, no actions
```

---

## Launching from Claude Code

### Background Task (Recommended)

```bash
# Run with run_in_background: true — same pattern as Codex
gemini -p "Analyze the authentication flow in src/auth/ and summarize findings" \
  --yolo \
  --output-format stream-json \
  2>&1
```

**Key rules (same as Codex):**
- Launch with `run_in_background: true` in Bash tool
- Use `stream-json` for real-time output
- Peek with `head -n 50` on the output file — NEVER read the full stream
- No timeout needed; background mode handles it

### Foreground Task (Quick Queries)

```bash
gemini -p "What does the function calculate_score do in utils.py?" \
  --yolo \
  --output-format text \
  2>&1
```

Use foreground when the result is needed before the next step and the task is fast (<30 seconds).

---

## Output Formats

### `text` — Human-readable (default)
Best for: quick answers, summaries, code review feedback.

### `json` — Structured response
Best for: parsing results programmatically, extracting specific fields.

### `stream-json` — Newline-delimited events
Best for: long-running background tasks with real-time monitoring.
Same peek pattern as Codex: `head -n 50` on the output file.

---

## Model Selection

```bash
gemini -p "task" --yolo -m gemini-3.1-pro-preview  # most capable
gemini -p "task" --yolo -m gemini-2.5-flash        # fast + cheap
```

**When to use which:**
- **3.1 Pro Preview**: Complex analysis, code review, architectural reasoning, council deliberation
- **2.5 Flash**: Quick searches, simple summaries, verification checks, high-volume parallel tasks

---

## Workspace and Directory Control

```bash
# Gemini runs in CWD by default (like Codex)
# Add extra directories to its workspace:
gemini -p "task" --yolo --include-directories /path/to/other/dir
```

---

## Additional Useful Flags

| Flag | Purpose |
|------|---------|
| `--sandbox` / `-s` | Run in Docker/Podman sandbox (safer for untrusted tasks) |
| `--resume` / `-r` | Resume previous session (`latest` or index number) |
| `--extensions` / `-e` | Limit which extensions (tools) are available |
| `--debug` / `-d` | Debug mode (opens debug console with F12) |
| `--policy` | Load additional policy files for tool restrictions |
| `--raw-output` | Disable output sanitization (use with caution) |

---

## Comparison: Gemini CLI vs Codex CLI vs Claude Code Subagent

| Capability | `gemini` | `agent` (Cursor) | `codex` (OpenAI) | Claude Code `Agent` tool |
|------------|----------|-------------------|-------------------|--------------------------|
| Headless flag | `-p "prompt"` | `-p "prompt"` | `-p "prompt"` | N/A (native subagent) |
| Auto-accept | `--yolo` | `--force --trust` | `--force` | `mode: "bypassPermissions"` |
| Output format | `--output-format stream-json` | `--output-format text` | `--output-format stream-json` | Returns message directly |
| Model select | `-m gemini-3.1-pro-preview` | `--model composer-2` | model via CLI | `model: "opus"` / `"sonnet"` |
| Background | `run_in_background: true` | `run_in_background: true` | `run_in_background: true` | `run_in_background: true` |
| Peek pattern | `head -n 50` on output | Read output file | `head -n 50` on output | N/A (auto-notifies) |
| Workspace | CWD + `--include-directories` | CWD (or `--workspace`) | CWD | CWD (inherits parent) |
| Usage tier | Metered | **Unlimited** (Composer-2) | Metered | Metered |

---

## Example: Dispatching Gemini as Adversarial Reviewer

```bash
# From Claude Code, launch Gemini to review code Claude just wrote
gemini -p "Review the changes in src/pipeline.py for correctness, edge cases, \
and potential bugs. Be adversarial — assume the author made mistakes. \
Output a structured list of issues found, ranked by severity." \
  --yolo \
  -m gemini-3.1-pro-preview \
  --output-format text \
  2>&1
```

This gives you cross-model adversarial review — Gemini reviewing Claude's work (or vice versa).

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ENOENT: .gemini/projects.json` | Run `mkdir -p ~/.gemini` |
| Auth hangs in background | Set `GEMINI_API_KEY` env var instead of OAuth |
| No output / timeout | Check `gemini --version` works; ensure network access |
| Permission denied on tools | Use `--yolo` or `--approval-mode yolo` |

---

**Last Updated:** 2026-03-13
