---
name: 4th-layer-agent-harness
description: Installs the 4th Layer Engineering harness into a repository. Hooks, run tracking, multi-agent council protocol, subagent guides, handoff templates with memory promotion, and a CLAUDE.md workflow section. Use when setting up a new repo for agent-driven development, or when adding structured run tracking and multi-agent workflow support to an existing project.
---

# 4th Layer Agent Harness — Engineering Workflow

This skill installs the 4th Layer Engineering workflow infrastructure into the current
repository. It takes ~10 minutes and leaves you with a complete agent operating environment:
run tracking, subagent protocol, hooks, templates, and a CLAUDE.md workflow section.

---

## Prerequisites

Before proceeding, confirm:

- [ ] You are in the root directory of the target repository
- [ ] Git is initialized (`git init` if not)
- [ ] Python 3 is available (for hooks — they use stdlib only)
- [ ] `~/bin/agent` is set up if you plan to use Cursor as a subagent (see SETUP.md)

**Skill package location:**
This SKILL.md and all accompanying files are in `4th-layer-scaffold/` at the
Code Projects root. All `files/` paths below are relative to that directory.

---

## What Gets Installed

| Artifact                              | Destination in Target Repo                                             | Purpose                                                                                                                                                                          |
| ------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 7 hook scripts                        | `.claude/hooks/`                                                       | Agent type enforcement, git safety, session continuity, subagent protocol, TASK_LOG reminders                                                                                    |
| Hook settings template                | `.claude/settings-hooks-template.json`                                 | Hooks wiring to merge into settings.local.json                                                                                                                                   |
| `CLAUDE.local.md` template            | Project root                                                           | Active Tasks table + Agent Voice (gitignored runtime state)                                                                                                                      |
| Blank `ARCHIVE.md`                    | `runs/CLAUDE-RUNS/`                                                    | Log of completed runs                                                                                                                                                            |
| `SUBAGENT_GUIDE.md`                   | `docs/coding_agents/`                                                  | When/how to spawn subagents                                                                                                                                                      |
| `GEMINI_CLI_SUBAGENT.md`              | `docs/coding_agents/`                                                  | Gemini CLI headless invocation reference                                                                                                                                         |
| `COUNCIL_GUIDE.md`                    | `docs/coding_agents/`                                                  | Multi-agent council deliberation protocol                                                                                                                                        |
| `ADVERSARIAL_REVIEW.md`               | `docs/coding_agents/`                                                  | Skeptical-but-fair review protocol and quad-model dispatch                                                                                                                       |
| `MEMORY_OPTIMIZATION.md`              | `docs/coding_agents/`                                                  | Context loading strategies                                                                                                                                                       |
| `skills/README.md`                    | `skills/`                                                              | Scaffold for domain skills                                                                                                                                                       |
| `skills/task-tracking/`               | `skills/task-tracking/` or `~/.claude/skills/task-tracking/`           | **HIGHLY RECOMMENDED.** Run tracking protocol, templates (TASK_LOG, SPEC, HANDOFF, FINDINGS), init-run.sh, docstring validation — user chooses global vs project-local in Step 7 |
| `skills/archive-run/`                 | `skills/archive-run/` or `~/.claude/skills/archive-run/`               | **HIGHLY RECOMMENDED.** Archival checklist, metric collectors, ARCHIVE.md entry format — user chooses global vs project-local in Step 7                                          |
| `skills/cursor-subagent/SKILL.md`     | `skills/cursor-subagent/` or `~/.claude/skills/cursor-subagent/`       | Cursor agent subagent invocation (Windows/Git Bash) — user chooses global vs project-local in Step 7                                                                             |
| `skills/codex-subagent/SKILL.md`      | `skills/codex-subagent/` or `~/.claude/skills/codex-subagent/`         | Codex CLI subagent invocation (Windows/Git Bash) — user chooses global vs project-local in Step 7                                                                                |
| `skills/gemini-subagent/SKILL.md`     | `skills/gemini-subagent/` or `~/.claude/skills/gemini-subagent/`       | Gemini CLI subagent invocation — user chooses global vs project-local in Step 7                                                                                                  |
| `skills/adversarial-review/SKILL.md`  | `skills/adversarial-review/` or `~/.claude/skills/adversarial-review/` | Adversarial review protocol — user chooses global vs project-local in Step 7                                                                                                     |
| `skills/council-guide/SKILL.md`       | `skills/council-guide/` or `~/.claude/skills/council-guide/`           | Quad-model council protocol — user chooses global vs project-local in Step 7                                                                                                     |
| `snippets/CLAUDE_MD_WORKFLOW.md`      | `snippets/` (in target repo)                                           | Slim workflow pointer for CLAUDE.md (full protocol lives in task-tracking skill)                                                                                                 |
| **Optional addons**                   | `optional/` (pick what applies)                                        | Language/CI-specific hooks                                                                                                                                                       |
| ↳ `optional/python/` (2 hooks)        | `.claude/hooks/`                                                       | Post-edit length check + ruff/black linting (Python only)                                                                                                                        |
| ↳ `optional/github-actions/` (1 hook) | `.claude/hooks/`                                                       | SHA-pinning enforcement for CI workflows                                                                                                                                         |
| ↳ `optional/spec-quality-gate.py`     | `.claude/hooks/`                                                       | SPEC quality checklist on write (for council-style repos)                                                                                                                        |

---

## Installation

Work through these steps in order. Do not skip steps.

---

### Step 1: Create directories

Create all required directories in the target repo:

```bash
mkdir -p .claude/hooks
mkdir -p runs/CLAUDE-RUNS
mkdir -p docs/coding_agents
mkdir -p skills
mkdir -p snippets
```

---

### Step 2: Copy hook scripts

Read each file from the skill package and write it to the target repo:

| Source (in skill package)                            | Destination (in target repo)                   |
| ---------------------------------------------------- | ---------------------------------------------- |
| `files/.claude/hooks/force-general-purpose-agent.py` | `.claude/hooks/force-general-purpose-agent.py` |
| `files/.claude/hooks/block-destructive-git.py`       | `.claude/hooks/block-destructive-git.py`       |
| `files/.claude/hooks/session-run-prompt.py`          | `.claude/hooks/session-run-prompt.py`          |
| `files/.claude/hooks/subagent-context.py`            | `.claude/hooks/subagent-context.py`            |
| `files/.claude/hooks/subagent-directory-protocol.py` | `.claude/hooks/subagent-directory-protocol.py` |
| `files/.claude/hooks/plan-mode-reminder.py`          | `.claude/hooks/plan-mode-reminder.py`          |
| `files/.claude/hooks/task-log-reminder.py`           | `.claude/hooks/task-log-reminder.py`           |

---

### Step 3: Copy settings template

Read `files/.claude/settings-hooks-template.json` from the skill package and write it
to `.claude/settings-hooks-template.json` in the target repo.

This contains only the `"hooks"` section. The user will merge it into their
`settings.local.json` (Step 10).

---

### Step 4: Copy run infrastructure

| Source                              | Destination                              |
| ----------------------------------- | ---------------------------------------- |
| `files/runs/.gitkeep`               | `runs/.gitkeep` (empty file)             |
| `files/runs/CLAUDE-RUNS/.gitkeep`   | `runs/CLAUDE-RUNS/.gitkeep` (empty file) |
| `files/runs/CLAUDE-RUNS/ARCHIVE.md` | `runs/CLAUDE-RUNS/ARCHIVE.md`            |

**Note:** `init-run.sh` and all run templates (TASK_LOG, SPEC, HANDOFF, FINDINGS)
now live inside the `task-tracking` skill and are installed in Step 7. The skill's
`scripts/init-run.sh` resolves templates from `../templates/` relative to itself.

---

### Step 5: Copy CLAUDE.local.md

| Source                  | Destination       |
| ----------------------- | ----------------- |
| `files/CLAUDE.local.md` | `CLAUDE.local.md` |

This file holds per-machine runtime state (Active Tasks table, optional Agent Voice).
It is loaded into the system prompt alongside CLAUDE.md but is gitignored in the target
repo to prevent merge conflicts.

---

### Step 6: Copy documentation

| Source                                            | Destination                                 |
| ------------------------------------------------- | ------------------------------------------- |
| `files/docs/coding_agents/SUBAGENT_GUIDE.md`      | `docs/coding_agents/SUBAGENT_GUIDE.md`      |
| `files/docs/coding_agents/GEMINI_CLI_SUBAGENT.md` | `docs/coding_agents/GEMINI_CLI_SUBAGENT.md` |
| `files/docs/coding_agents/COUNCIL_GUIDE.md`       | `docs/coding_agents/COUNCIL_GUIDE.md`       |
| `files/docs/coding_agents/ADVERSARIAL_REVIEW.md`  | `docs/coding_agents/ADVERSARIAL_REVIEW.md`  |
| `files/docs/coding_agents/MEMORY_OPTIMIZATION.md` | `docs/coding_agents/MEMORY_OPTIMIZATION.md` |

**Note:** `docstring_validation_template.md` now lives inside the `task-tracking` skill
at `templates/docstring_validation_template.md` and is installed in Step 7.

---

### Step 7: Install skills

This harness ships 7 skills. The first two (`task-tracking` and `archive-run`) are
**HIGHLY RECOMMENDED** and should be installed for all projects. The rest are optional
depending on which subagent CLIs you use.

**Core skills (install for all projects):**

- `task-tracking` — run tracking protocol, templates, init-run.sh, docstring validation
- `archive-run` — archival checklist, metric collectors, ARCHIVE.md entry format

**Subagent skills (install based on your tooling):**

- `cursor-subagent` — invocation patterns for Cursor's `agent` CLI
- `codex-subagent` — invocation patterns for Codex CLI
- `gemini-subagent` — invocation patterns for Gemini CLI
- `adversarial-review` — skeptical-but-fair multi-model review protocol
- `council-guide` — quad-model council deliberation protocol

**Ask the user before proceeding:**

> "Where would you like the skills installed?
>
> **A) Global** — copied to `~/.claude/skills/<name>/`. Available across all your projects automatically. Best if you use these tools everywhere.
>
> **B) Project-local** — copied to `skills/<name>/` inside this repo. Only available when working in this project. Best if you want the repo to be self-contained or you work across multiple machines.
>
> **C) Both** — install globally AND keep a copy in the project `skills/` directory.
>
> **D) Skip subagent skills** — install only `task-tracking` and `archive-run`; you can install the rest manually later."

Then execute the chosen option:

**A / C — Global install:**

```bash
mkdir -p ~/.claude/skills/task-tracking/{templates,scripts}
mkdir -p ~/.claude/skills/archive-run/scripts/metrics
mkdir -p ~/.claude/skills/cursor-subagent
mkdir -p ~/.claude/skills/codex-subagent
mkdir -p ~/.claude/skills/gemini-subagent
mkdir -p ~/.claude/skills/adversarial-review
mkdir -p ~/.claude/skills/council-guide
```

For `task-tracking`, copy the entire skill directory:

- `files/skills/task-tracking/SKILL.md` → `~/.claude/skills/task-tracking/SKILL.md`
- `files/skills/task-tracking/templates/*` → `~/.claude/skills/task-tracking/templates/`
- `files/skills/task-tracking/scripts/init-run.sh` → `~/.claude/skills/task-tracking/scripts/init-run.sh`
- `chmod +x ~/.claude/skills/task-tracking/scripts/init-run.sh`

For `archive-run`, copy the entire skill directory:

- `files/skills/archive-run/SKILL.md` → `~/.claude/skills/archive-run/SKILL.md`
- `files/skills/archive-run/scripts/*` → `~/.claude/skills/archive-run/scripts/`
- `chmod +x ~/.claude/skills/archive-run/scripts/archive-run.sh`
- `chmod +x ~/.claude/skills/archive-run/scripts/metrics/*.sh`

For other skills, copy each `files/skills/<name>/SKILL.md` → `~/.claude/skills/<name>/SKILL.md`

**B / C — Project-local install:**

| Source                                     | Destination                          |
| ------------------------------------------ | ------------------------------------ |
| `files/skills/README.md`                   | `skills/README.md`                   |
| `files/skills/task-tracking/` (entire dir) | `skills/task-tracking/`              |
| `files/skills/archive-run/` (entire dir)   | `skills/archive-run/`                |
| `files/skills/cursor-subagent/SKILL.md`    | `skills/cursor-subagent/SKILL.md`    |
| `files/skills/codex-subagent/SKILL.md`     | `skills/codex-subagent/SKILL.md`     |
| `files/skills/gemini-subagent/SKILL.md`    | `skills/gemini-subagent/SKILL.md`    |
| `files/skills/adversarial-review/SKILL.md` | `skills/adversarial-review/SKILL.md` |
| `files/skills/council-guide/SKILL.md`      | `skills/council-guide/SKILL.md`      |

After copying, make scripts executable:

```bash
chmod +x skills/task-tracking/scripts/init-run.sh
chmod +x skills/archive-run/scripts/archive-run.sh
chmod +x skills/archive-run/scripts/metrics/*.sh
```

---

### Step 7b: Configure archive metrics

**Ask the user:**

> "What metrics should be collected when archiving a run?
>
> I'll create `.claude/archive-run.config` with the collectors you want.
> The `git` collector (files changed, lines +/-, commits) is always included.
>
> What applies to this project?
>
> 1. **Python** — pytest summary, ruff errors, mypy errors, coverage %
> 2. **Node.js** — eslint counts, jest summary
> 3. **Go** — go test, govet
> 4. **Rust** — cargo test, clippy
> 5. **Code duplication** (jscpd) — run manually with repo-specific ignore patterns
> 6. **None of the above** — git metrics only"

Based on the answer, create `.claude/archive-run.config` with the appropriate collectors
uncommented. Use `files/skills/archive-run/scripts/archive-run.config.example` as the base.

If the user isn't sure yet, copy the example file as-is (git-only default) and note they
can uncomment collectors later.

---

### Step 8: Copy snippets

| Source                                    | Destination                      |
| ----------------------------------------- | -------------------------------- |
| `files/../snippets/CLAUDE_MD_WORKFLOW.md` | `snippets/CLAUDE_MD_WORKFLOW.md` |

(The snippets directory is at `4th-layer-scaffold/snippets/`, not inside `files/`.)

---

### Step 9: Update .gitignore

Append the following to `.gitignore` (create the file if it doesn't exist):

```
# Claude agent runtime state (per-machine, never committed)
CLAUDE.local.md

# Claude agent run directories (local only — contents never committed)
runs/
!runs/.gitkeep

# Log files
*.log
```

Do NOT replace an existing `.gitignore` — append only.

---

### Step 10: Force-add tracked files

```bash
git add -f runs/.gitkeep
git add -f runs/CLAUDE-RUNS/.gitkeep
git add -f runs/CLAUDE-RUNS/ARCHIVE.md
```

**Note:** `init-run.sh` is no longer at `runs/CLAUDE-RUNS/` — it lives inside the
`task-tracking` skill directory (installed in Step 7). The skill's `scripts/init-run.sh`
was already made executable in Step 7.

---

### Step 11: Test run infrastructure

Run `init-run.sh` from wherever it was installed (global or project-local):

```bash
# If project-local:
skills/task-tracking/scripts/init-run.sh test-tent
# If global:
~/.claude/skills/task-tracking/scripts/init-run.sh test-tent
```

Expected output: `✅ Created: runs/CLAUDE-RUNS/RUN-YYYYMMDD-HHMM-test-tent/` with
`TASK_LOG.md`, `SPEC_v1.md`, and `HANDOFF.md` present with timestamps substituted
(not `{{RUN_ID}}` literals).

If template variables aren't substituted, check that the `templates/` directory
inside the `task-tracking` skill is populated correctly from Step 7.

---

## Customization Pass

The infrastructure is now installed. This pass fills in the project-specific
`[TODO]` markers so the docs accurately reflect _this_ project.

Work through each file. For each `[TODO]`, decide whether to fill it in now
(if you know the answer) or mark it for later (add `[TODO: revisit]`).

---

### Customize: MEMORY_OPTIMIZATION.md

Open `docs/coding_agents/MEMORY_OPTIMIZATION.md`.

**Fill in these sections:**

1. **Progressive Disclosure table** (top of file) — replace `[your quick reference doc]`,
   `[your troubleshooting doc]`, etc. with your project's actual documentation file names.

2. **Tier 1 Constants block** — add your project's:
   - Service/port mappings
   - Import path pattern (e.g., `from mypackage.` not `from src.mypackage.`)
   - Core architectural rules (e.g., "Config DB for metadata only, never for client data")

3. **Tier 2 table** — fill in your actual doc names and approximate sizes.

4. **Decision trees** — replace `[quick reference doc]`, `[troubleshooting doc]`, etc.
   with your actual file names.

5. **Tip 2: Cache Constants** — list your project's key constants (ports, import patterns,
   critical rules) so agents know what to cache.

6. **Update the "Last Updated" line** at the bottom.

If you don't know the answers yet, that's fine — leave the `[TODO]` markers and fill
them in during your first few runs on the project.

---

### Customize: SUBAGENT_GUIDE.md

Open `docs/coding_agents/SUBAGENT_GUIDE.md`.

**Fill in this section:**

1. **§3 Example Prompt** — there is a `[TODO]` comment at the bottom of §3. Replace the
   generic "users table" example with one relevant to your project (a real table, a real
   investigation scenario, or a real verification task you'd actually run).

2. **Update the "Last Updated" line** at the bottom.

---

### Customize: CLAUDE.md workflow section

The file `snippets/CLAUDE_MD_WORKFLOW.md` contains a slim workflow pointer section
ready to paste into CLAUDE.md. The full task-tracking protocol now lives in the
`task-tracking` skill (installed in Step 7), so CLAUDE.md only needs a pointer.

Ask the user: **"Do you have an existing CLAUDE.md, or should I create a new one?"**

**If creating new:** Copy `snippets/CLAUDE_MD_WORKFLOW.md` to `CLAUDE.md`. Then add
a project-specific header section above the workflow section covering:

- Project name and purpose
- Documentation map (what docs exist and when to use them)
- Key architectural concepts
- Quick reference (ports, commands, critical file locations)
- Common pitfalls

**If merging with existing:** Paste the workflow sections from
`snippets/CLAUDE_MD_WORKFLOW.md` into the appropriate place in the existing CLAUDE.md.
At minimum, ensure these sections are present:

- Task Execution Protocol (pointer to `task-tracking` skill)
- Subagent Usage + Codex + Cursor sections
- Background Process Guidelines
- Timestamp reminder

Then ensure `CLAUDE.local.md` exists with the Active Tasks table (and optionally
the Agent Voice section). This file is gitignored — it holds per-machine runtime state.

After merging, fill in all `[TODO: project-specific]` markers in CLAUDE.md.

---

### Finalize: Configure settings.local.json

Merge `.claude/settings-hooks-template.json` into `.claude/settings.local.json`:

- If no `settings.local.json` exists: rename the template to `settings.local.json`
- If it exists: merge the `"hooks"` key into the existing file without overwriting
  other keys (`permissions`, `enabledMcpjsonServers`, `additionalDirectories`, etc.)

After merging, delete `.claude/settings-hooks-template.json`.

---

## Completion Checklist

Verify everything before starting work:

- [ ] `task-tracking` and `archive-run` skills installed (global or project-local)
- [ ] `init-run.sh test-tent` generates TASK_LOG.md, SPEC_v1.md, and HANDOFF.md with substituted timestamps
- [ ] `.claude/settings.local.json` has `"hooks"` key with 7 core hooks + SessionStart
- [ ] `.claude/archive-run.config` created with appropriate metric collectors
- [ ] `MEMORY_OPTIMIZATION.md` — Tier 1 constants filled in (or `[TODO]` markers left intentionally)
- [ ] `SUBAGENT_GUIDE.md` — project example added (or `[TODO]` left intentionally)
- [ ] CLAUDE.md has the workflow pointer section (skill references, subagent section)
- [ ] CLAUDE.local.md has the Active Tasks table (and Agent Voice if used)
- [ ] `.gitignore` has `runs/` + `!runs/.gitkeep` appended
- [ ] `runs/.gitkeep`, `runs/CLAUDE-RUNS/.gitkeep`, `ARCHIVE.md` force-added to git

---

## What's NOT installed (by design)

The following were intentionally excluded. Add them yourself if needed:

| What                                                | Why excluded                                                                                           | Available as optional addon?                               |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------- |
| `post-edit-lint.py` hook                            | Python/ruff/black specific                                                                             | Yes — `optional/python/post-edit-lint.py`                  |
| `post-edit-length-check.py` hook                    | Python AST specific                                                                                    | Yes — `optional/python/post-edit-length-check.py`          |
| `github-actions-security.py` hook                   | GitHub Actions specific                                                                                | Yes — `optional/github-actions/github-actions-security.py` |
| `spec-quality-gate.py` hook                         | Opinionated for council-style repos                                                                    | Yes — `optional/spec-quality-gate.py`                      |
| Project-specific permissions in settings.local.json | You know your project's allowed bash commands.                                                         | No                                                         |
| `AGENTS.md`                                         | Project-specific repository guidelines. Write your own.                                                | No                                                         |
| `EXAMPLES.md`, `VISUAL_DIAGRAMS.md`                 | Project-specific code examples. Write your own.                                                        | No                                                         |
| `GEMINI-RUNS/`                                      | Add `runs/GEMINI-RUNS/` yourself if you use Gemini agents.                                             | No                                                         |
| MCP query templates                                 | Specific to your database tooling.                                                                     | No                                                         |
| `DOCSTRING_GUIDE.md`                                | Conventions vary by team/language. Write your own.                                                     | No (TODO template planned)                                 |
| `ARCHITECTURE_CONSTRAINTS.md`                       | Project-specific hard rules. Write your own.                                                           | No (TODO template planned)                                 |
| `health-pulse.sh`                                   | Language-specific metrics gathering. Now partially covered by `archive-run` skill's metric collectors. | Partially — see `archive-run` skill                        |
