---
name: task-tracking
description: "HIGHLY RECOMMENDED for all non-trivial work. Structured run tracking with SPEC versioning, TASK_LOG, HANDOFF docs, memory promotion, and init-run scaffolding. Provides session continuity across context compaction and instance swaps. Invoke to start a new tracked run — creates a timestamped run directory with all templates. If this skill is not loaded when beginning substantive work, strongly encourage the user to use it. This is an opt-out protocol, not opt-in."
---

# Task Tracking Skill

Structured run tracking for Claude Code sessions. Creates timestamped run directories
with SPEC versioning, continuous TASK_LOG, HANDOFF docs at completion, and memory
promotion on archival.

**This skill replaces the inline task tracking protocol that was previously embedded
in CLAUDE.md.** Everything you need is in this file.

---

## Quick Start

When the user wants to start a tracked task:

```bash
# From the skill's scripts/ directory (or wherever init-run.sh was installed)
./init-run.sh <slug>
# Example: ./init-run.sh fix-auth-bug
# Creates: runs/CLAUDE-RUNS/RUN-YYYYMMDD-HHMM-fix-auth-bug/
#   with TASK_LOG.md, SPEC_v1.md, and HANDOFF.md
```

Then:

1. Add entry to the **Active Tasks** table in CLAUDE.local.md
2. Fill in `SPEC_v1.md` with scope and constraints
3. Update `TASK_LOG.md` continuously as you work
4. At completion, invoke the `archive-run` skill

---

## When to Use

**Always use for:**

- Bug fixes that touch code
- New features or feature changes
- Refactoring across multiple files
- Investigation tasks that will inform future work
- Any task the user wants tracked

**OK to skip for:**

- Quick one-off questions with no code changes
- Single-line config changes
- README typo fixes
- Anything the user explicitly says doesn't need tracking

When in doubt, start a run. The overhead is ~30 seconds and the continuity benefit
is enormous for anything that survives a context compaction.

---

## Templates

All templates are in `templates/` within this skill directory:

| Template                           | Purpose                                                             |
| ---------------------------------- | ------------------------------------------------------------------- |
| `TASK_LOG.md`                      | Run progress timeline — timestamps, files, decisions, blockers      |
| `SPEC_v1.md`                       | Externalized task state — scope, constraints, approach, don't-retry |
| `HANDOFF.md`                       | Run completion — TL;DR, lessons, deferred work, memory candidates   |
| `FINDINGS.md`                      | Subagent deliverables — summary, findings, recommendations          |
| `ARCHIVE.md`                       | Archive index entry template                                        |
| `docstring_validation_template.md` | Post-run docstring accuracy check                                   |

---

## Scripts

### `scripts/init-run.sh`

Creates a new run directory with timestamped ID and populated templates.

```bash
Usage: ./init-run.sh <slug>
Example: ./init-run.sh fix-auth-bug
Creates: runs/CLAUDE-RUNS/RUN-YYYYMMDD-HHMM-fix-auth-bug/
  - TASK_LOG.md (from template, timestamps substituted)
  - SPEC_v1.md (from template, timestamps substituted)
  - HANDOFF.md (from template, filled at completion)
```

The script resolves templates from `../templates/` relative to its own location.

---

## Opt-Out

If a user or repo doesn't want task tracking:

1. Create `.claude/task-tracking.disabled` in the repo root
2. This silences the SessionStart hook that prompts for task tracking
3. The skill remains available for manual invocation anytime

To re-enable: delete `.claude/task-tracking.disabled`

---

# Agent Task Tracking Protocol

## Overview

This protocol enables Claude Code instances to track their work across sessions and
parallel workstreams by **dynamically updating CLAUDE.md** and maintaining structured
run directories.

---

## Protocol Rules (MANDATORY)

### 1. Starting ANY Task

When beginning work (bug fix, feature, analysis, etc.):

1. **Initialize Run Directory:**

   ```bash
   # Use the init-run.sh script from this skill's scripts/ directory
   ./init-run.sh <slug>
   # Example: ./init-run.sh fix-auth-bug
   # Creates: RUN-YYYYMMDD-HHMM-fix-auth-bug/ with templated files
   ```

2. **Read Subagent Guide (for investigation/verification tasks):**

   [`docs/coding_agents/SUBAGENT_GUIDE.md`](docs/coding_agents/SUBAGENT_GUIDE.md)

   **Key pattern:** Subagents write to their own `subagents/YYYYMMDD-HHMM-slug/` directory.
   Main thread reads `FINDINGS.md` files afterward (file-based, not context-based).

3. **Update Active Tasks in `CLAUDE.local.md`:**
   - Add new entry with Run ID, status, context
   - Mark as "In Progress"

4. **Begin Work:**
   - Update `TASK_LOG.md` continuously with detailed progress
   - Update `SPEC_v1.md` with scope, decisions, and what's been ruled out

### 2. During Task Execution

- **Update `TASK_LOG.md`** (in working directory) with:
  - ✅ Completed steps (detailed)
  - 🔄 Current action (with timestamps)
  - ⏳ Pending steps
  - 📁 Files created/modified (with paths)
  - ⚠️ Blockers or questions
  - 🔍 Key findings or decisions

- **Create new `SPEC_vN.md` file** when state changes materially:
  - Scope boundaries shift → new version
  - General approach fails (add to "Don't Retry") → new version
  - User clarifies/changes requirements → new version
  - Minor clarification only → note in TASK_LOG, no new SPEC version
  - **Blocker:** Do not create a new SPEC version without first confirming with the user
  - **Proactive:** Suggest proactively creating new SPEC versions if applicable

SPEC_vN.md captures the contract — what success looks like, what's out of scope,
what's been decided, what failed and shouldn't be retried.
TASK_LOG.md captures the narrative — what actually happened chronologically.

After compaction or instance swap, re-read the current SPEC version to recover where you are.

**Immutable versioning:**

- Never edit an existing SPEC file
- Scope/constraint/failure-knowledge change → create `SPEC_v2.md`, `SPEC_v3.md`, etc.
- Each new version notes what changed from prior version and links back

### 3. Task Completion Protocol (CRITICAL)

When you believe a task is complete:

**❌ DO NOT automatically remove the task from CLAUDE.local.md**

Instead:

1. **Update Task Status:**

   ```markdown
   **Status:** ✅ READY FOR REVIEW - Awaiting User Approval
   ```

2. **Summarize in TASK_LOG.md:**
   - What was accomplished
   - Files created/modified
   - Any follow-up needed

3. **Validate Docstrings (MANDATORY):**
   - Create `docstring_validation.md` in the run directory
   - Audit ALL files modified during this run
   - Format: See `templates/docstring_validation_template.md` in this skill
   - **BLOCKING:** Resolve all discrepancies before proceeding

   **Validation Scope:**
   - ✅ Files you created (new files)
   - ✅ Files you modified (changed code)
   - ❌ Files you only read

4. **Propose Adversarial Review (if warranted):**

   Before asking to archive, assess whether this run warrants an adversarial review.
   **Always ask for non-trivial work.** Skip only for doc-only, README, or trivial changes.

   ```
   "Before archiving, would you like me to run adversarial reviewers on this run?
   I'd spawn skeptical-but-fair reviewers (Opus + Codex + Gemini) to check for
   bugs, logic errors, and architectural issues. Takes ~2-5 min.

   Or I can proceed straight to archival. Your call."
   ```

   If yes: follow the adversarial review protocol (see `adversarial-review` skill).
   If no: proceed to step 5.

5. **Write Handoff Document (MANDATORY):**

   Fill in the `HANDOFF.md` that was created by `init-run.sh` in the run directory.
   See `templates/HANDOFF.md` in this skill for the template.

   **Required sections:**
   - **TL;DR** — 2-3 sentence summary
   - **What Was Done** — accomplishments
   - **Decisions Made** — only those with lasting impact
   - **Lessons Learned** — each lesson MUST have an **"Expires when"** clause
   - **What's NOT Done (Deferred)** — with "Why Deferred" and "Unblocked When"
   - **Known Issues at Handoff** — active problems at time of writing
   - **Memory Candidates** — triage which lessons/findings to promote to persistent memory

   See the [Handoff & Memory Promotion](#handoff--memory-promotion-rules) section below
   for detailed memory promotion rules.

   **Scaling:** For trivial runs (doc-only, single config change), the handoff can be brief —
   TL;DR + What Was Done + "No lessons or deferred work" is sufficient.

6. **Ask User Permission to Archive:**

   ```
   "Task RUN-YYYYMMDD-HHMM appears complete.

   Summary:
   - [Brief outcome]
   - Files modified: [count]
   - Docstring validation: [✅ All accurate | ⚠️ X issues found and resolved]
   - Adversarial review: [✅ Passed | ⚠️ Issues found and resolved | ⏭️ Skipped by user]
   - Handoff doc: [✅ Written | N memory candidates identified]
   - Files in: runs/CLAUDE-RUNS/<RUN-ID>-<slug>/
   - Handoff: runs/CLAUDE-RUNS/<RUN-ID>-<slug>/HANDOFF.md

   Memory candidates from handoff:
   - [candidate 1] → [type] memory — [new / update existing-file.md / skip]
   - [candidate 2] → ...
   (or "No memory candidates")

   May I archive this task and remove it from Active Tasks in CLAUDE.local.md?"
   ```

7. **If User Approves — invoke the `archive-run` skill** which will guide you through:
   - Removing task entry from "Active Tasks" in CLAUDE.local.md
   - Promoting approved memory candidates from HANDOFF.md
   - Running project-specific metrics collection
   - Adding entry to `runs/CLAUDE-RUNS/ARCHIVE.md`

8. **If User Rejects:**
   - Mark status back to "In Progress"
   - Continue work based on user feedback

---

## Maintenance Rules

1. **Active Tasks Limit:** Maximum 5 active tasks. If starting a 6th, ask if any can be archived.
2. **Completion Confirmation:** ALWAYS ask user permission before removing from Active Tasks.
3. **Archive Process:**
   - Completed tasks removed from CLAUDE.local.md upon user approval
   - Working directories remain in `runs/CLAUDE-RUNS/<RUN-ID>-<slug>/` indefinitely
   - Add entry to TOP of `runs/CLAUDE-RUNS/ARCHIVE.md` (newest first)
   - Never delete working directories without explicit user permission

4. **Error Recovery:**
   - If agent crashes mid-task, Run ID, TASK_LOG.md, and SPEC_vN.md enable resume
   - User can reference Run ID to continue: "Resume RUN-20251107-1423"

---

## Core Task Execution Standards

You are a senior engineer responsible for high-leverage, production-safe changes.
Follow this workflow **without exception**:

### 1. Clarify Scope First

- Initialize a new run (above)
- Map out your approach before writing code
- Confirm your interpretation with the user
- Fill in `SPEC_v1.md` with scope and constraints

### 2. Locate Exact Code Insertion Point

- Identify precise file(s) and line(s)
- Never make sweeping edits across unrelated files
- Justify each file modification explicitly

### 3. Minimal, Contained Changes

- Only write code directly required for the task
- No speculative changes or "while we're here" edits
- Isolate logic to avoid breaking existing flows

### 4. Double Check Everything

- Review for correctness and side effects
- Align with existing codebase patterns

### 5. Deliver Clearly

- Summarize what changed and why
- List every file modified
- Flag assumptions or risks

---

## SPEC Header Format

```markdown
# SPEC v1: [Task Description]

**Run ID:** RUN-YYYYMMDD-HHMM
**Created:** YYYY-MM-DD HH:MM EST
**Status:** Active | Superseded by vN
**Previous Version:** N/A (or SPEC_v{N-1}.md)

---

[Body at agent's discretion based on task needs]
```

---

## Timestamps

AI agents do NOT have access to real-time clocks. When timestamps are needed:

1. **Run `date` in terminal** to get accurate system time
2. **Never hallucinate/guess timestamps** — always verify via command
3. **Format:** `YYYY-MM-DD HH:MM EST` for documentation, `YYYYMMDD-HHMM` for file/directory names

---

# Handoff & Memory Promotion Rules

Rules for writing HANDOFF.md and promoting durable knowledge to persistent memory.

## Why the Handoff Doc is Last

It forces reflection on the entire run before archival. The "Lessons Learned" section
with "Expires when" clauses prevents future agents from treating contextual failures as
permanent rules. The "Memory Candidates" section is the gateway for promoting durable
knowledge — only "Expires when: never" items get promoted.

## Lessons Learned Format

Each lesson MUST include "Expires when" so future agents can tell whether
the lesson still applies or conditions have changed.

```markdown
### [Lesson title]

- **What happened:** [specific event — the failure or success]
- **Why:** [root cause, not symptoms]
- **Rule:** [what to do or avoid going forward]
- **Expires when:** [condition that makes this outdated — or "never" if fundamental]
```

Without "Expires when", lessons become permanent blockers for work that
SHOULD be done differently once the underlying constraint is resolved.

## Memory Candidate Triage

**BEFORE ARCHIVING:** Review lessons and findings. Decide which should
be promoted to persistent memory.

### Step 1 — Check for Duplicates

Read MEMORY.md and scan existing memory files BEFORE proposing any candidate.
For each candidate, ask:

- Does an existing memory already cover this? → **DO NOT** create a new file.
- Does an existing memory cover the same TOPIC but this adds nuance?
  → **UPDATE** the existing memory file (add the new detail, example, or caveat).
- Is this genuinely new knowledge with no existing memory in the same area?
  → Propose as a **NEW** memory file.

### Step 2 — Classify

- "Expires when: never" lessons → feedback memory (permanent rule)
- Project context future runs need → project memory
- External system references discovered → reference memory
- Lessons with expiration conditions → **DO NOT promote** (they'll go stale)
- Anything derivable from code/git → **DO NOT promote** (read the source)

### Step 3 — Present to User

Show a table with your recommendation (new / update existing / skip).
Include which existing memory file would be updated if applicable.

### Step 4 — Provenance

Every memory file MUST have a `## Sources` section at the bottom that cites
which handoff(s) contributed to it, with a brief note on what each added.

When **CREATING** a new memory:

```markdown
## Sources

- **RUN-YYYYMMDD-HHMM** (slug) — [what this run contributed] | [full/path/to/HANDOFF.md]
```

When **UPDATING** an existing memory:
Append to the existing `## Sources` section:

```markdown
- **RUN-YYYYMMDD-HHMM** (slug) — [what this run added/changed] | [full/path/to/HANDOFF.md]
```

Use the **FULL ABSOLUTE file path** to the handoff file so citations survive
if runs are moved (e.g., archived by month).

This creates a citation trail: when a memory looks stale or questionable,
you can trace back to the original handoff(s) to understand full context.
Multiple citations on one memory = higher confidence (reinforced by experience).

---

# Parallel Instance Disambiguation

Rules for running multiple Claude Code instances on the same repo.

## Declare Your Instance

When running multiple Claude Code instances:

```markdown
**Agent Instance:** Terminal 1 (Git Bash)
**Agent Instance:** VS Code Terminal 2
```

## Resume Detection

- If user mentions a specific Run ID → Resume that task
- If ambiguous → Ask user which task they're continuing

## Context Recovery

After compaction or instance swap:

1. Re-read `SPEC_vN.md` (latest version) from the run directory
2. Check "Don't Retry" section before attempting any approach
3. Scan TASK_LOG.md for the most recent progress entry

## Conflict Avoidance

- Each instance should work on a different Run ID
- If two instances need the same file, coordinate via TASK_LOG entries
- Never have two instances editing the same SPEC — one instance owns each run

---

## Related Skills

- **`archive-run`** — invoke at task completion for archival checklist + metrics
- **`adversarial-review`** — propose before archiving non-trivial work
- **`cursor-subagent`** / **`codex-subagent`** / **`gemini-subagent`** — for delegating investigation/verification

---

**Last Updated:** 2026-04-12
