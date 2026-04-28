<!-- PASTE THIS INTO YOUR CLAUDE.md -->
<!-- Delete this comment block before committing -->

---

## Task Execution Protocol

This repo uses structured run tracking via the `task-tracking` skill. Enabled by default.

- **Session/context loading:** invoke the `context-loading` skill at session start,
  after compaction/resume, or before broad repo/doc exploration.
- **Docstrings/navigation:** use the `docstring-guide` skill before any task
  that writes or edits actual code.
- **Start a run:** invoke the `task-tracking` skill with a slug
- **Archive a run:** invoke the `archive-run` skill with the RUN-ID
- **Opt out permanently:** create `.claude/task-tracking.disabled`

The `task-tracking` skill contains the full protocol: SPEC versioning, TASK_LOG updates,
HANDOFF docs, memory promotion, subagent directory conventions, and completion checklists.

---

## Subagent Usage

Use subagents PROACTIVELY. The cost of spawning is low; the cost of context pollution is high.

For delegation decisions, prompt structure, working directories, and result
integration, use the `subagent-management` skill.

**Always delegate:**

- Codebase exploration: "How is X implemented?", "Find all usages of Y", "Trace data flow"
- Verification tasks: Running tests, type-checking, linting, compilation checks
- Investigation: Reading docs, understanding APIs, summarizing file responsibilities
- Search: Pattern matching, file location, dependency tracing

**Delegation heuristic:** Before any investigative or verification task, ask:
"Will this generate intermediate noise that pollutes my main context?" If yes → subagent.

**Do NOT delegate:**

- Tasks requiring iterative user clarification
- Multi-step operations with interdependencies
- Judgment calls that should surface to main conversation

### Spawning Subagents (Main Thread Responsibility)

1. **Create a subdirectory** for the subagent in your current run:

   ```
   runs/CLAUDE-RUNS/RUN-YYYYMMDD-HHMM-<your-task>/subagents/YYYYMMDD-HHMM-<subagent-slug>/
   ```

2. **Tell the subagent its directory path** in the spawn prompt:

   ```
   Your working directory: runs/CLAUDE-RUNS/RUN-20251228-1400-fix-bug/subagents/20251228-1430-trace-auth/
   Write your FINDINGS.md and any helper files there.
   ```

3. **Read `FINDINGS.md`** after the subagent completes.

> **Backup:** Hook `.claude/hooks/subagent-directory-protocol.py` reinforces these
> instructions to subagents automatically.

### Codex as Implementation Subagent

If installed and relevant, see skill: `codex-subagent`

### Cursor Agent as Subagent

If installed and relevant, see skill: `cursor-subagent`

### Gemini CLI as Subagent

If installed and relevant, see skill: `gemini-subagent`

---

## Background Process Guidelines

- **Never Auto-Check Output:** Don't call TaskOutput just because the system reports
  new output available. Only check when you need specific information.
- **Synchronous by Default:** For short commands (<30 seconds), run synchronously.
- **Long commands:** Run in background, check output ONCE when ready — not on every notification.
- **Record the task ID** for background processes.
- **Kill processes when done** to prevent lingering jobs.

---

## Code Quality Standards

### **GitHub Actions Security (MUST follow — supply chain protection)**

```yaml
# ❌ Tag-based pin — vulnerable to tag-force-push attacks (e.g. TeamPCP/Trivy 2026-03-19)
uses: actions/checkout@v4

# ✅ SHA-pin with version comment — immutable, immune to tag hijacking
uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4
```

**All GitHub Actions MUST be pinned by commit SHA, not tag.** Tags are mutable — an attacker who compromises a repo can force-push a tag to point at malicious code. SHA pins are immutable. Always include a `# vN` trailing comment for readability.

When adding or updating a GitHub Action:

1. Find the commit SHA for the desired version tag
2. Use full 40-char SHA in the `uses:` line
3. Add trailing comment with the human-readable version

---

## Timestamps

AI agents do NOT have access to real-time clocks. When timestamps are needed:

1. **Run `date` in terminal** to get accurate system time
2. **Never hallucinate/guess timestamps** — always verify via command
3. **Format:** `YYYY-MM-DD HH:MM EST` for documentation, `YYYYMMDD-HHMM` for file/directory names

---

## Harness setup completeness (read before relying on skills or hooks)

This workflow assumes the **4th Layer agent harness** is fully installed: skills globally available under `~/.claude/skills/` unless the user requested project-local `skills/`, shared hook logic in `.agent-harness/hooks/`, and Claude Code **hooks** wired in `.claude/settings.local.json`.

**If you (the agent) cannot load or invoke skills the project references** — e.g. slash-invoked skills like `/task-tracking` or `/adversarial-review` are missing from the environment — **do not pretend the workflow is active.** Review the 4th Layer scaffold repository and **ask the user** whether they want to install or sync the harness (skills + docs + hooks) into this repo.

**If the repo contains `.claude/hooks/` (hook scripts present) but `.agent-harness/hooks/` is missing or `.claude/settings.local.json` does not register those hooks** (or there is no merged `settings-hooks-template.json` wiring), treat hooks as **not active** until the user syncs shared hook logic and merges hook configuration. **Ask the user** before assuming session reminders, subagent protocol injection, or git-safety hooks will run.

> **Note for humans:** `.claude/settings.local.json` is usually gitignored; it is expected that PRs may not include it even when the harness files are committed. Agents should still flag a hooks/scripts vs settings mismatch when they see it.

<!-- END PASTE -->
