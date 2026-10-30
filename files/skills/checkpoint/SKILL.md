---
name: checkpoint
description: "Create a CHECKPOINT-0N-<slug>.md pre-compaction state snapshot in the current run's checkpoints/. Captures TL;DR for the post-compact agent, current focus, deltas since prior checkpoint, new artifacts (SPECs, subagent dirs), critical refs and numbers, don't-retry, open questions, and recovery reading order. Also serves to lock major design decisions at phase boundaries. Invoke when the user says 'checkpoint' / 'make a checkpoint' / 'snapshot the run' / 'save state' / 'pre-compaction note', OR proactively when context is approaching compaction risk (large tool result imminent, long subagent dispatch, end of major phase, working memory holds derived facts that would be expensive to rebuild). Pairs with task-tracking — checkpoints live in the run dir's checkpoints/ subdir that init-run.sh creates."
---

# Checkpoint Skill

Create pre-compaction state snapshots in the active run's `checkpoints/`
subdirectory. A checkpoint is a deliberately-written trail for post-compaction
you, capturing what working memory would otherwise lose.

---

## Quick Start

```bash
# From this skill's scripts/ directory (or wherever checkpoint.sh was installed)
./checkpoint.sh <slug>
# Example: ./checkpoint.sh pre-launch-readiness
# Creates: runs/CLAUDE-RUNS/<latest-run>/checkpoints/CHECKPOINT-0N-pre-launch-readiness.md
```

The script auto-detects the active run (newest `RUN-*` by mtime) and
auto-increments `N` based on existing checkpoints. Pass a second arg to target
a specific run:

```bash
./checkpoint.sh midday-state RUN-20260513-1404
```

**Always written to:** `runs/CLAUDE-RUNS/<RUN>/checkpoints/` — the script
refuses to write anywhere else. If your active run dir doesn't have a
`checkpoints/` subdir yet, the script creates it (newer runs get it
automatically from `task-tracking/scripts/init-run.sh`).

### CRITICAL: Read-before-Edit (Claude Code harness invariant)

After the script creates the file, **you (the Claude instance) MUST use the
Read tool on the new file path before you Edit it.** Claude Code's harness
rejects Edit/Write operations on files that have not been Read in the current
session. The script prints the file path explicitly so you can pass it
straight to Read.

Workflow:

1. `./checkpoint.sh <slug>` — file created, path printed.
2. **Read** the printed path (Claude Code Read tool).
3. **Edit** to fill in the sections — verbose and comprehensive by default
   (see "Writing Style" below).

If you skip step 2, every Edit attempt in step 3 will be rejected. The
template's writing-guidance comment block at the top reiterates this so you
catch it on Read.

---

## When to Checkpoint

A checkpoint is worth writing when **any** of the following is true:

1. **Context window is approaching compaction.** Common triggers:
   - About to invoke a long-running subagent (council, codex, gemini)
   - About to read a large file or run a tool with a huge output
   - End of a substantive work phase where working memory holds derived facts
2. **A major decision or phase boundary is reached.** Lock the decisions in
   one place so subsequent SPECs can reference back (ADR-style use).
3. **You've accumulated enough "if-I-lost-this-now-I'd-be-in-trouble" facts**
   that the cost of writing a checkpoint is less than the cost of re-deriving
   them after a compact.

**Rule of thumb for frequency:** ~30-60 minutes of substantive work, OR before
any tool call that risks pulling >10KB into context, OR before any subagent
dispatch.

**Do NOT checkpoint for:** doc-only edits, single-line config changes,
read-only Q&A, or any task where compaction wouldn't cost you anything.

---

## Naming Convention

```
CHECKPOINT-0N-<descriptive-slug>.md
```

- **N** is zero-padded to 2 digits, monotonically increasing within a run.
- **Slug** is kebab-case, short but descriptive (`pre-launch-readiness`,
  `post-codex-rebase-sweep`, `midday-state-after-standup`).
- The slug is REQUIRED — bare `CHECKPOINT-0N.md` is legacy. Latest practice
  uses the slug because a directory listing becomes self-navigating:
  ```
  CHECKPOINT-01-schema-pr-and-api-launch.md
  CHECKPOINT-02-auth-typing-prep.md
  CHECKPOINT-03-worker-typing-prep.md
  ...
  CHECKPOINT-11-pre-launch-readiness.md
  ```
  Each line tells you what's inside without opening it.

Special files:
- `CHECKPOINT-FINAL.md` — optional summative checkpoint at run end, separate
  from HANDOFF.md. Use only when a run ends mid-phase and you want a snapshot
  distinct from the formal handoff.

---

## Template Structure

The template lives at `templates/CHECKPOINT.md` in this skill. Sections (in order):

| Section                            | Purpose                                                                    |
| ---------------------------------- | -------------------------------------------------------------------------- |
| Header                             | N, label, timestamp, run ID, predecessor, status, trigger                   |
| **TL;DR for next agent**           | 2-5 bullets — what post-compact agent needs first                          |
| **Where I am right now**           | Current focus, geographic refs                                              |
| **What changed since {prev}**      | Concrete deltas, not running totals                                         |
| **New artifacts since {prev}**     | New SPECs, new subagent dirs, new run-internal directories                  |
| **What's next (priority order)**   | Numbered concrete actions                                                   |
| **Critical refs (file:line)**      | 5-15 paths a post-compact agent would re-grep for                           |
| **Critical numbers / facts**       | Values that would be expensive to re-derive                                 |
| **Don't retry**                    | Pruned approaches, with brief WHY                                           |
| **Open questions / hypotheses**    | Half-formed thoughts; mark (testing | waiting on X | unresolved)            |
| **Pending external dependencies**  | Things blocked on other people, services, or background runs                |
| **Recovery reading order**         | Numbered list of what to read after THIS checkpoint                         |
| **Personal / stakeholder context** | Deadlines, social scripts; reference voice/style memory if relevant         |
| **Cross-references**               | Sister checkpoints, parent runs, sibling worktrees, companion docs          |

**On empty sections:** if a section is genuinely empty, say so explicitly —
e.g. "No new SPEC versions since CHECKPOINT-0(N-1)" or "No external blockers
right now". An empty section communicates "I checked and there's nothing
here," which is itself useful. Don't leave bare bullet markers — they read as
"I forgot to fill this in."

### Writing Style

**Default is verbose and comprehensive.** The reader is an agent that has lost
its working-memory context (or has never had it — a fresh session). Over-
explain rather than under-explain. The cost of writing 200 extra words is
small; the cost of re-deriving lost context is large.

- Multi-paragraph narrative is fine in "Where I am right now" and
  "What changed since".
- Tables for structured data (variance experiments, audit chains, version
  rationales) — encouraged.
- File paths, line numbers, function names, error messages, exact commands —
  inline them.
- Don't abbreviate hypotheses or rationales. State them as full thoughts.
- Critical refs section typically has 10-30 entries, not 5.
- Critical numbers section: include the value, a context line, and the
  derivation path where applicable.

The template's HTML comments at each section give per-section guidance.
Re-read them as you fill the file.

---

## Script Usage

### Auto-detection

```bash
./checkpoint.sh pre-launch-readiness
# Auto-detected run: RUN-20260513-1404-dashboard-demo-and-release-prep
# ✅ Created: ...checkpoints/CHECKPOINT-09-pre-launch-readiness.md
```

### Explicit run targeting (when multiple active runs)

```bash
./checkpoint.sh midday-state RUN-20260513-1404
# Prefix matching also works:
./checkpoint.sh midday-state RUN-20260513
```

### What the script does

1. Resolves the target run (exact match → prefix match → newest by mtime).
2. Counts existing `CHECKPOINT-NN-*.md` files in `<run>/checkpoints/`.
3. Increments N, zero-pads to 2 digits.
4. Resolves the predecessor filename (or "N/A" for first checkpoint).
5. `sed`-substitutes the template's `{{N}}`, `{{LABEL}}`, `{{RUN_ID}}`,
   `{{TIMESTAMP}}`, `{{PREV_CHECKPOINT}}` placeholders.
6. Writes the file. The agent (or user) then opens it and fills in content.

The script does NOT fill content sections — those require judgment about
what's actually in working memory at checkpoint time.

---

## Recovery Flow (how to USE a checkpoint after compaction)

When you (the agent) wake up post-compaction and need to recover state:

1. **Find the latest checkpoint:**
   ```bash
   ls -1 runs/CLAUDE-RUNS/<RUN>/checkpoints/ | tail -1
   ```
2. **Read it FULLY.** Don't skim — the TL;DR is the entry point but the rest
   has the facts that compaction stripped.
3. **Follow the Recovery Reading Order** section. It tells you what to read
   next and in what order.
4. **Check What's Next.** Resume the highest-priority action — don't re-derive
   the plan.
5. **Check Don't Retry.** Avoid re-running approaches the previous you already
   ruled out.
6. **If the user is talking to you immediately**, the Personal/Stakeholder
   Context section tells you how to respond (deadlines, voice, social scripts).

---

## Checkpoint vs SPEC vs TASK_LOG vs HANDOFF

Confusing because they all sound similar — here's the distinction:

| Artifact     | Audience               | Mutability        | Trigger                                        |
| ------------ | ---------------------- | ----------------- | ---------------------------------------------- |
| `TASK_LOG`   | future-you (any time)  | Continuously appended | every meaningful action                    |
| `SPEC_vN`    | future-you, reviewers  | Immutable per version | scope/approach/constraint change           |
| `CHECKPOINT` | post-compact agent     | Immutable per number  | compaction risk, phase boundary, decision lock |
| `HANDOFF`    | next session, reviewer | Written once at end   | run completion                             |

**Checkpoint is the only one explicitly addressed to a context-stripped reader.**
That shapes every section: don't assume the reader has anything beyond the
checkpoint file itself loaded.

---

## Automatic Reminders (Hook Integration)

The harness ships a `UserPromptSubmit` hook that injects an imperative
reminder when context is approaching compaction. This is the safety net for
"I forgot to checkpoint" — the hook fires on every prompt while you're in
the warning window and tells you to STOP and checkpoint before the next
compaction strips your working memory.

### What the hook does

On every user prompt:

1. Reads the session's transcript JSONL to find the most recent assistant
   message's `usage.input_tokens` from the API metadata. That value is the
   literal context-window size at that moment (not an estimate).
2. If that value is between the configured lower and upper thresholds
   (default 900K–920K of 1M), and no checkpoint has been written in the
   active run within the dedupe window (default 5 minutes), injects a
   `<system-reminder>` into the prompt:
   - Token count + window
   - Imperative "STOP and write CHECKPOINT now" instruction
   - Detected active run path
   - Last checkpoint in that run (or "none")
   - Current local timestamp
   - Step-by-step recipe to invoke `checkpoint.sh` + Read + Edit

3. Outside the window, or if a recent checkpoint already exists, exits
   silently.

### Configuration (env vars)

Override defaults via shell env:

| Variable | Default | Purpose |
|---|---|---|
| `HARNESS_CHECKPOINT_LOWER` | `900000` | Lower threshold (tokens) |
| `HARNESS_CHECKPOINT_UPPER` | `920000` | Upper threshold (tokens). Above this, compaction is likely already mid-flight; no reminder. |
| `HARNESS_CHECKPOINT_DEDUPE_SECONDS` | `300` | Suppress reminder if a checkpoint in the active run was modified this many seconds ago. Set to `0` to disable dedupe (ping every prompt in window). |

### Wiring

**Codex:** auto-wired via the bundled `.codex/hooks.json`. No action needed.

**Claude Code:** register the hook in your `.claude/settings.json` under
the `hooks.UserPromptSubmit` key:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python \"$(git rev-parse --show-toplevel)/.claude/hooks/checkpoint-window-reminder.py\""
          }
        ]
      }
    ]
  }
}
```

If you already have `UserPromptSubmit` hooks (e.g. `task-log-reminder`),
add the checkpoint reminder as an additional entry in the same `hooks`
array — they run in sequence.

### Why the reminder is imperative, not advisory

Earlier drafts used "consider writing a checkpoint" softness. The user
preference is the imperative form ("STOP and write your CHECKPOINT now")
because checkpoints are a forcing function — if the agent treats the nudge
as optional, they tend to "finish what I'm doing first" and then compaction
hits mid-thought. The imperative phrasing breaks that procrastination loop.

The `if you are NOT in an active run, ignore` escape clause keeps the
reminder safe in sessions where no run is active.

---

## Related Skills

- **`task-tracking`** — owns the run directory structure; creates `checkpoints/`
  at run init via `init-run.sh`.
- **`archive-run`** — at archival time, checkpoints stay in the run dir alongside
  TASK_LOG/SPEC/HANDOFF.
- **`adversarial-review`** — note the terminology overlap: that skill's
  "checkpoints" are workflow phases for review, NOT filesystem snapshots.
  These are different concepts despite the name collision.

---

**Last Updated:** 2026-05-15
