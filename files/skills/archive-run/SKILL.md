---
name: archive-run
description: "HIGHLY RECOMMENDED when completing a run. Load this skill fresh at archival time to get the completion checklist, project-specific metric collection, ARCHIVE.md entry format, monthly-rotation policy (entries >2mo age roll to ARCHIVE-YYYY-MM.md files), and memory promotion steps with clean context. Pairs with the task-tracking skill. Invoke when a run reaches READY FOR REVIEW status and the user approves archival."
---

# Archive Run Skill

Guides the archival of a completed task-tracking run. Load this skill **fresh at
archival time** so you have clean context for the checklist, metric collection,
and memory promotion steps.

---

## When to Invoke

Invoke this skill when:

1. A run's status is `✅ READY FOR REVIEW - Awaiting User Approval`
2. The user has approved archival
3. You need to collect metrics, write the ARCHIVE.md entry, and promote memory candidates

---

## Archival Checklist

Work through these steps in order after the user approves archival:

### 1. Remove from Active Tasks

Delete the task's row from the **Active Tasks** table in `CLAUDE.local.md`
(Claude) or `AGENTS.local.md` (Codex).

### 2. Promote Memory Candidates

Read the **Memory Candidates** table from `HANDOFF.md` in the run directory.
For each approved candidate:

- **First**: Read MEMORY.md and scan existing memory files for overlap
- If candidate overlaps an existing memory → **update** that file (add nuance, not a new file)
- If candidate is genuinely new → **create** new memory file + add to MEMORY.md index
- If candidate duplicates exactly → **skip**
- **Provenance**: Every memory file must have a `## Sources` section citing the handoff(s)

See the "Handoff & Memory Promotion Rules" section in the `task-tracking` skill's SKILL.md.

### 3. Collect Metrics

Run the metric collection script if configured:

```bash
# From this skill's scripts/ directory
./archive-run.sh <RUN-DIR-PATH>
```

The script reads `.claude/archive-run.config` to determine which collectors to run.
If no config exists, it runs only the universal `git.sh` collector.

**Available collectors** (in `scripts/metrics/`):

| Collector   | What it captures                                         | Requires        |
| ----------- | -------------------------------------------------------- | --------------- |
| `git.sh`    | Files changed, lines +/-, commits on branch, branch name | git (universal) |
| `python.sh` | pytest summary, ruff errors, mypy errors, coverage %     | Python project  |
| `node.sh`   | eslint error/warning counts, jest test summary           | Node.js project |
| `go.sh`     | go test summary, govet issues                            | Go project      |
| `rust.sh`   | cargo test summary, clippy warning count                 | Rust project    |

#### Code Duplication (jscpd)

Not a script — run this manually and tailor the ignore patterns to the repo.
Use your judgment on what directories to ignore (vendor, generated code, test fixtures, etc.).

**Recommended command:**

```bash
jscpd . --min-lines 5 --min-tokens 50 \
  --ignore "node_modules,vendor,dist,build,.git,runs,docs,*.min.js,*.generated.*" \
  --reporters consoleFull
```

- `--min-lines 5` and `--min-tokens 50` set strictness thresholds
- `--ignore` should be tailored per-repo — add generated directories, vendored
  dependencies, test fixtures with intentional repetition, etc.
- Review the output and include the duplication % in the ARCHIVE.md entry

The agent should decide what to ignore based on the repo structure — check for
`vendor/`, `dist/`, `build/`, `generated/`, lock files, etc. before running.

### 4. Write ARCHIVE.md Entry

Add an entry to the **TOP** of `runs/CLAUDE-RUNS/ARCHIVE.md` (newest first).

**Entry format:**

```markdown
### [RUN-YYYYMMDD-HHMM] Brief Description

**Archived:** YYYY-MM-DD HH:MM EST
**Created:** YYYY-MM-DD HH:MM EST
**Completed:** YYYY-MM-DD HH:MM EST
**Duration:** ~X hours/minutes
**Working Directory:** `runs/CLAUDE-RUNS/<RUN-ID>-<slug>/`
**Branch:** branch-name

**Metrics:**
[Output from metric collectors — paste relevant lines]

**Summary:**
[Brief description of what was accomplished]

**Deliverables:**

- [List of key files created/modified]

**Outcome:** [Final result and any follow-up context]

---
```

### 4.5. Rotate Aged Entries to Monthly Archives

**Policy:** Entries older than **2 calendar months** get moved out of
`ARCHIVE.md` into dated monthly files (`ARCHIVE-YYYY-MM.md`). This keeps
`ARCHIVE.md` focused on recent history while preserving the full audit trail.

**When to rotate:** Check at the end of every archival. Most archivals will
rotate zero entries (only when a month boundary has aged out).

**Threshold calculation:**
- Today's date minus 2 months = rotation threshold
- Example: today is 2026-04-17 → threshold is 2026-02-17
- Any entry with `Archived:` (or `Created:` if Archived is missing) before the
  threshold gets rotated to its month's file

**Rotation procedure:**

1. Scan `ARCHIVE.md` for entries dated before the threshold
2. For each aged entry, determine its month from the `Archived:` date
   (e.g., 2026-01-15 → `2026-01`)
3. Append the entry to `runs/CLAUDE-RUNS/ARCHIVE-YYYY-MM.md` (create if
   missing, using the monthly file template below)
4. Remove the entry from `ARCHIVE.md`
5. Add or update an Index section at the bottom of `ARCHIVE.md` listing the
   monthly files that now exist (newest first):

   ```markdown
   ---

   ## Monthly Archives

   Older entries are rotated to per-month files after they exceed 2 months of age.

   - [`ARCHIVE-2026-02.md`](./ARCHIVE-2026-02.md)
   - [`ARCHIVE-2026-01.md`](./ARCHIVE-2026-01.md)
   - [`ARCHIVE-2025-12.md`](./ARCHIVE-2025-12.md)
   ```

**Monthly file template** (use when creating `ARCHIVE-YYYY-MM.md`):

```markdown
# Archived Tasks — [Month Year]

> Monthly archive of completed runs. See `ARCHIVE.md` for the master index of
> current and recent runs. Entries rotated here after 2 months of age per the
> archive-run skill's rotation policy.

---

<!-- Entries below this line, newest first -->
```

**Rationale:**
- `ARCHIVE.md` stays a reasonable size even on long-lived projects
- Monthly files are naturally narratively coherent (a month's worth of work)
- Full history is preserved; nothing is ever lost
- Rotation is deterministic and idempotent — running it multiple times produces
  the same result

**Gitignore:** Both `ARCHIVE.md` AND `ARCHIVE-YYYY-MM.md` files are
per-developer working state (gitignored). Only `ARCHIVE.template.md` is
tracked. Each developer's machine has its own rotation history.

**Skip rotation if:**
- No entries are older than the threshold (common case — no-op)
- The user has explicitly opted out (not currently a settings option; add if requested)

### 5. Verify

- [ ] Task removed from Active Tasks in local runtime state
- [ ] Memory candidates promoted (or marked skip)
- [ ] Metrics collected (or N/A if no config)
- [ ] ARCHIVE.md entry added at top
- [ ] **Aged entries rotated to monthly files** (or no-op if none aged out)
- [ ] Working directory kept intact (never auto-delete)

---

## Configuring Metrics

During harness installation, the `archive-run.config` file is created via an interview.
To reconfigure later, edit `.claude/archive-run.config` directly:

```ini
# .claude/archive-run.config
# Which metric collectors to run at archival time.
# Each line is a collector name (filename without .sh extension).
# Lines starting with # are comments.

git
# python
# node
# go
# rust
```

The `archive-run.config.example` in this skill's `scripts/` directory shows all options.

---

## Related Skills

- **`task-tracking`** — the protocol that creates runs; invoke first
- **`adversarial-review`** — propose before archiving non-trivial work

---

**Last Updated:** 2026-04-12
