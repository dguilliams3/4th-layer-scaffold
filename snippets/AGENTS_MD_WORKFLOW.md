<!-- PASTE THIS INTO YOUR AGENTS.md -->
<!-- Delete this comment block before committing -->

---

## Task Execution Protocol

This repo uses structured run tracking via the `task-tracking` skill. Enabled by default.

- **Session/context loading:** invoke `$context-loading` at session start, after
  compaction/resume, or before broad repo/doc exploration.
- **Docstrings/navigation:** invoke `$docstring-guide` before any task that
  writes or edits actual code.
- **Start a run:** invoke `$task-tracking` with a slug, or run the installed `init-run.sh`
- **Archive a run:** invoke `$archive-run` with the RUN-ID
- **Opt out permanently for Codex:** create `.codex/task-tracking.disabled`

The `task-tracking` skill contains the full protocol: SPEC versioning, TASK_LOG updates,
HANDOFF docs, memory promotion, subagent directory conventions, and completion checklists.

Codex automatically reads `AGENTS.md`, not `CLAUDE.md`, `CLAUDE.local.md`, or
`AGENTS.local.md`. Keep Codex-facing workflow pointers in `AGENTS.md`. Keep
per-machine Codex runtime state in `AGENTS.local.md`; the 4th Layer `SessionStart`
hook reads it when Codex hooks are enabled.

---

## Subagent Usage

Use subagents when a task is independent enough to run in parallel and will materially
advance the main task. Keep immediate blocking work in the main thread.

For delegation decisions, prompt structure, working directories, and result
integration, see skill: `subagent-management`.

### Codex Subagents

If installed and relevant, see skill: `codex-subagent`

### Cursor Agent as Subagent

If installed and relevant, see skill: `cursor-subagent`

### Gemini CLI as Subagent

If installed and relevant, see skill: `gemini-subagent`

---

## Background Process Guidelines

- Synchronous by default for short commands.
- Long-running commands should be started deliberately, tracked, and stopped when done.
- Do not repeatedly poll output unless you need new information.

---

## Timestamps

AI agents do not have access to real-time clocks. When timestamps are needed:

1. Run a terminal date/time command.
2. Do not guess timestamps.
3. Format: `YYYY-MM-DD HH:MM EST` for documentation, `YYYYMMDD-HHMM` for file/directory names.

---

## Harness Setup Completeness

This workflow assumes the 4th Layer agent harness is fully installed for Codex:

- Codex skills are discoverable under the user's global `~/.agents/skills/` path,
  or under `.agents/skills/` only if the user requested repo-specific skills.
- Shared hook logic exists under `.agent-harness/hooks/`.
- Codex hooks are wired in `.codex/hooks.json`.
- Codex hooks are enabled with `[features] codex_hooks = true` in `.codex/config.toml`
  or another active Codex config layer.

If referenced skills are missing, do not pretend the workflow is active. Review the
harness repository and ask the user whether they want to install or sync skills.

If `.codex/hooks/` exists but `.agent-harness/hooks/` is missing, or hooks are not
wired/enabled, treat Codex hooks as inactive until the user syncs the shared hook logic
and merges the hook configuration. In that state, `AGENTS.local.md` is also not injected
automatically.

<!-- END PASTE -->
