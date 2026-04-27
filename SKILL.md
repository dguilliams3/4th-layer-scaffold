---
name: 4th-layer-agent-harness
description: Installs the 4th Layer Engineering harness into a repository. Claude Code and Codex hooks, run tracking, multi-agent council protocol, subagent guides, handoff templates with memory promotion, and CLAUDE.md/AGENTS.md workflow sections. Use when setting up a new repo for agent-driven development, or when adding structured run tracking and multi-agent workflow support to an existing project.
---

# 4th Layer Agent Harness — Engineering Workflow

This skill installs the 4th Layer Engineering workflow infrastructure into the current
repository. It takes ~10 minutes and leaves you with a complete agent operating environment:
run tracking, subagent protocol, hooks, templates, and Claude/Codex workflow sections.

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
| 3 Codex hook scripts                   | `.codex/hooks/`                                                        | Git safety, session continuity, TASK_LOG reminders                                                                                                                               |
| Codex hooks template                   | `.codex/hooks.json`                                                    | Codex hook wiring                                                                                                                                                                |
| Codex hooks config template            | `.codex/config-hooks-template.toml`                                     | Enables Codex hooks via `[features] codex_hooks = true`                                                                                                                          |
| Shared hook logic                      | `.agent-harness/hooks/`                                                | Runtime-neutral Python logic imported by Claude and Codex hook adapters                                                                                                          |
| `CLAUDE.local.md` template            | Project root                                                           | Active Tasks table + Agent Voice (gitignored runtime state)                                                                                                                      |
| `AGENTS.local.md` template             | Project root                                                           | Active Tasks table + Codex local notes read by the harness `SessionStart` hook (gitignored runtime state)                                                                        |
| `ARCHIVE.template.md` (tracked) + `ARCHIVE.md` (gitignored) | `runs/CLAUDE-RUNS/` | Template stays tracked as the blank canonical form; `ARCHIVE.md` is the per-developer working log (gitignored so multi-dev archive histories don't conflict). |
| `skills/README.md`                    | Optional project-local `skills/` or `.agents/skills/`                  | Scaffold for domain skills when the user explicitly requests repo-specific skills                                                                                                |
| `skills/task-tracking/`               | Global by default; project-local only on request                       | **HIGHLY RECOMMENDED.** Run tracking protocol, templates (TASK_LOG, SPEC, HANDOFF, FINDINGS), init-run.sh, docstring validation                                                  |
| `skills/context-loading/`             | Global by default; project-local only on request                       | **HIGHLY RECOMMENDED.** Minimal file/doc loading strategy, partial reads, cached summaries, composed shell command patterns                                                       |
| `skills/docstring-guide/`             | Global by default; project-local only on request                       | **HIGHLY RECOMMENDED.** Load before any task that writes or edits actual code; keeps docstrings, navigation refs, and test traceability accurate                                  |
| `skills/archive-run/`                 | Global by default; project-local only on request                       | **HIGHLY RECOMMENDED.** Archival checklist, metric collectors, ARCHIVE.md entry format                                                                                           |
| `skills/subagent-management/`          | Global by default; project-local only on request                       | **HIGHLY RECOMMENDED.** Subagent delegation decisions, prompt structure, run-directory protocol, FINDINGS.md integration                                                          |
| `skills/cursor-subagent/SKILL.md`     | Global by default; project-local only on request                       | Cursor agent subagent invocation (Windows/Git Bash)                                                                                                                             |
| `skills/codex-subagent/SKILL.md`      | Global by default; project-local only on request                       | Codex CLI subagent invocation (Windows/Git Bash)                                                                                                                                |
| `skills/gemini-subagent/SKILL.md`     | Global by default; project-local only on request                       | Gemini CLI subagent invocation                                                                                                                                                   |
| `skills/adversarial-review/SKILL.md`  | Global by default; project-local only on request                       | Adversarial review protocol                                                                                                                                                      |
| `skills/council-guide/SKILL.md`       | Global by default; project-local only on request                       | Quad-model council protocol                                                                                                                                                      |
| `snippets/CLAUDE_MD_WORKFLOW.md`      | `snippets/` (in target repo)                                           | Slim workflow pointer for CLAUDE.md (full protocol lives in task-tracking skill)                                                                                                 |
| `snippets/AGENTS_MD_WORKFLOW.md`      | `snippets/` (in target repo)                                           | Slim workflow pointer for Codex AGENTS.md                                                                                                                                        |
| **Optional addons**                   | `optional/` (pick what applies)                                        | Language/CI-specific hooks                                                                                                                                                       |
| ↳ `optional/python/` (2 hooks)        | `.claude/hooks/`                                                       | Post-edit length check + ruff/black linting (Python only)                                                                                                                        |
| ↳ `optional/github-actions/` (1 hook) | `.claude/hooks/`                                                       | SHA-pinning enforcement for CI workflows                                                                                                                                         |
| ↳ `optional/spec-quality-gate.py`     | `.claude/hooks/`                                                       | SPEC quality checklist on write (for council-style repos)                                                                                                                        |

Install skills globally by default: `~/.claude/skills/<name>/` for Claude Code
and `~/.agents/skills/<name>/` for Codex. Only copy skills into the target repo
when the user explicitly asks for project-specific skills. The same
`files/skills/<name>/` payload is used for both Claude and Codex.

---

## Installation

Work through these steps in order. Do not skip steps.

---

### Step 1: Create directories

Create all required directories in the target repo:

```bash
mkdir -p .claude/hooks
mkdir -p .codex/hooks
mkdir -p .agent-harness/hooks
mkdir -p runs/CLAUDE-RUNS
mkdir -p snippets
```

Do not create `skills/` or `.agents/skills/` in the target repo unless the user
explicitly requests project-specific skills.

---

### Step 2: Copy shared hook support

The Claude and Codex hook files are thin runtime-specific adapters. Copy the shared
Python hook logic first:

| Source (in skill package)                         | Destination (in target repo)                    |
| ------------------------------------------------- | ----------------------------------------------- |
| `files/.agent-harness/hooks/__init__.py`          | `.agent-harness/hooks/__init__.py`              |
| `files/.agent-harness/hooks/git_safety.py`        | `.agent-harness/hooks/git_safety.py`            |
| `files/.agent-harness/hooks/run_state.py`         | `.agent-harness/hooks/run_state.py`             |
| `files/.agent-harness/hooks/task_log.py`          | `.agent-harness/hooks/task_log.py`              |

Do not put shared hook logic under `.claude/` or `.codex/`; those directories hold
runtime-specific adapters only.

---

### Step 2b: Copy Claude Code hook scripts

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

### Step 3b: Copy Codex hook scripts and templates

If the target repo will be used with Codex, copy these files:

| Source (in skill package)                       | Destination (in target repo)                  |
| ----------------------------------------------- | --------------------------------------------- |
| `files/.codex/hooks/block-destructive-git.py`   | `.codex/hooks/block-destructive-git.py`       |
| `files/.codex/hooks/session-run-prompt.py`      | `.codex/hooks/session-run-prompt.py`          |
| `files/.codex/hooks/task-log-reminder.py`       | `.codex/hooks/task-log-reminder.py`           |
| `files/.codex/hooks.json`                       | `.codex/hooks.json`                           |
| `files/.codex/config-hooks-template.toml`       | `.codex/config-hooks-template.toml`           |

Codex hooks are behind a feature flag. In the target repo, merge the template's
contents into `.codex/config.toml` or another active Codex config layer:

```toml
[features]
codex_hooks = true
```

If `.codex/config.toml` already exists, do not overwrite it. Merge only the
`[features]` value.

Codex hooks are guardrails, not a security boundary. Keep Codex sandboxing and
approval settings in place.

Project-local Codex hooks load only when the project `.codex/` config layer is
trusted by Codex. If Codex prompts about trusting project config, trust it only
after reviewing the hook scripts and config.

---

### Step 4: Copy run infrastructure

| Source                              | Destination                              |
| ----------------------------------- | ---------------------------------------- |
| `files/runs/.gitkeep`                        | `runs/.gitkeep` (empty file)                       |
| `files/runs/CLAUDE-RUNS/.gitkeep`            | `runs/CLAUDE-RUNS/.gitkeep` (empty file)           |
| `files/runs/CLAUDE-RUNS/ARCHIVE.template.md` | `runs/CLAUDE-RUNS/ARCHIVE.template.md` (tracked)   |
| `files/runs/CLAUDE-RUNS/ARCHIVE.template.md` | `runs/CLAUDE-RUNS/ARCHIVE.md` (copy of template; becomes the dev's local working log — gitignored) |

**Why the split:** `ARCHIVE.template.md` is the scaffold-canonical blank form — tracked, shared, rarely changes. `ARCHIVE.md` is the per-developer archive history — gitignored so each dev can archive runs on their machine without creating merge conflicts or leaking private run history into the shared repo.

**Note:** `init-run.sh` and all run templates (TASK_LOG, SPEC, HANDOFF, FINDINGS)
now live inside the `task-tracking` skill and are installed in Step 7. The skill's
`scripts/init-run.sh` resolves templates from `../templates/` relative to itself.

---

### Step 5: Copy local runtime state template

`CLAUDE.local.md` is per-machine runtime state. It belongs in the target repo root,
but it must stay gitignored and should not be committed.

| Source                  | Destination       | Runtime |
| ----------------------- | ----------------- | ------- |
| `files/CLAUDE.local.md` | `CLAUDE.local.md` | Claude Code |
| `files/AGENTS.local.md` | `AGENTS.local.md` | Codex |

If `CLAUDE.local.md` does **not** already exist in the target repo, copy the template
from `files/CLAUDE.local.md`.

If `CLAUDE.local.md` already exists, do **not** overwrite it. Verify it has the
Active Tasks table, and merge only the missing table/template pieces if needed while
preserving any existing Agent Voice or per-machine notes.

For Codex, do the same with `AGENTS.local.md`: copy `files/AGENTS.local.md` only if
the target repo does not already have one. Codex does not auto-load this file; the
4th Layer Codex `SessionStart` hook reads it when hooks are enabled.

---

### Step 6: Documentation now lives in skills

Do not copy duplicate `docs/coding_agents/` versions of agent workflow guides.
The harness keeps those protocols in skills so Claude Code and Codex can load
them on demand:

- `context-loading` replaces `MEMORY_OPTIMIZATION.md`
- `docstring-guide` replaces `DOCSTRING_GUIDE.md`
- `subagent-management` replaces `SUBAGENT_GUIDE.md`
- `gemini-subagent` replaces `GEMINI_CLI_SUBAGENT.md`
- `adversarial-review` replaces `ADVERSARIAL_REVIEW.md`
- `council-guide` replaces `COUNCIL_GUIDE.md`

**Note:** `docstring_validation_template.md` also lives inside the `task-tracking`
skill at `templates/docstring_validation_template.md` and is installed in Step 7.

---

### Step 7: Install skills

This harness ships 10 skills. Install all skills globally by default for the
agent runtime(s) being configured. Project-local copies are only for users who
explicitly ask for repo-specific skills.

**Core skills:**

- `task-tracking` — run tracking protocol, templates, init-run.sh, docstring validation
- `context-loading` — minimal file/doc loading, partial reads, cached summaries, composed shell commands
- `docstring-guide` — load before any task that writes or edits actual code; AI-friendly docstring navigation, `file::symbol` refs, stale-comment cleanup
- `archive-run` — archival checklist, metric collectors, ARCHIVE.md entry format
- `subagent-management` — delegation decisions, subagent prompts, directories, FINDINGS.md integration

**Invocation and review skills:**

- `cursor-subagent` — invocation patterns for Cursor's `agent` CLI
- `codex-subagent` — invocation patterns for Codex CLI
- `gemini-subagent` — invocation patterns for Gemini CLI
- `adversarial-review` — skeptical-but-fair multi-model review protocol
- `council-guide` — quad-model council deliberation protocol

**Default:** install skills globally for the agent runtime(s) being configured.
Do not add project-local `skills/` or `.agents/skills/` directories unless the
user explicitly asks for repo-specific skills.

**Ask the user before proceeding:**

> "I'll install the harness skills globally by default.
>
> **A) Global** - copied to the relevant global skills directory:
> `~/.claude/skills/<name>/` for Claude Code and/or
> `~/.agents/skills/<name>/` for Codex.
>
> **B) Project-local too** - also copy to the active agent's project-local skills
> directory (`skills/<name>/` for Claude Code, `.agents/skills/<name>/` for
> Codex). Choose this only if you want repo-specific skill copies."

Then execute the chosen option:

For Claude Code, use `~/.claude/skills/` for global install. Use `skills/`
only if the user explicitly requests project-local Claude skills.

For Codex, use `~/.agents/skills/` for global install. Use `.agents/skills/`
only if the user explicitly requests project-local Codex skills. Codex does not
use `~/.claude/skills/`, `CLAUDE.md`, or `CLAUDE.local.md` automatically.

**A — Claude Code global install:**

```bash
mkdir -p ~/.claude/skills/task-tracking/{templates,scripts}
mkdir -p ~/.claude/skills/context-loading/agents
mkdir -p ~/.claude/skills/docstring-guide/{agents,references}
mkdir -p ~/.claude/skills/archive-run/scripts/metrics
mkdir -p ~/.claude/skills/subagent-management/agents
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

For `context-loading`, copy the entire skill directory:

- `files/skills/context-loading/SKILL.md` → `~/.claude/skills/context-loading/SKILL.md`
- `files/skills/context-loading/agents/openai.yaml` → `~/.claude/skills/context-loading/agents/openai.yaml`

For `docstring-guide`, copy the entire skill directory:

- `files/skills/docstring-guide/SKILL.md` → `~/.claude/skills/docstring-guide/SKILL.md`
- `files/skills/docstring-guide/agents/openai.yaml` → `~/.claude/skills/docstring-guide/agents/openai.yaml`
- `files/skills/docstring-guide/references/DOCSTRING_GUIDE.md` → `~/.claude/skills/docstring-guide/references/DOCSTRING_GUIDE.md`

For `archive-run`, copy the entire skill directory:

- `files/skills/archive-run/SKILL.md` → `~/.claude/skills/archive-run/SKILL.md`
- `files/skills/archive-run/scripts/*` → `~/.claude/skills/archive-run/scripts/`
- `chmod +x ~/.claude/skills/archive-run/scripts/archive-run.sh`
- `chmod +x ~/.claude/skills/archive-run/scripts/metrics/*.sh`

For `subagent-management`, copy the entire skill directory:

- `files/skills/subagent-management/SKILL.md` → `~/.claude/skills/subagent-management/SKILL.md`
- `files/skills/subagent-management/agents/openai.yaml` → `~/.claude/skills/subagent-management/agents/openai.yaml`

For lightweight invocation/review skills, copy each `files/skills/<name>/SKILL.md`
→ `~/.claude/skills/<name>/SKILL.md`.

**B — Claude Code project-local install, only if explicitly requested:**

| Source                                     | Destination                          |
| ------------------------------------------ | ------------------------------------ |
| `files/skills/README.md`                   | `skills/README.md`                   |
| `files/skills/task-tracking/` (entire dir) | `skills/task-tracking/`              |
| `files/skills/context-loading/` (entire dir) | `skills/context-loading/`          |
| `files/skills/docstring-guide/` (entire dir) | `skills/docstring-guide/`          |
| `files/skills/archive-run/` (entire dir)   | `skills/archive-run/`                |
| `files/skills/subagent-management/` (entire dir) | `skills/subagent-management/`    |
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

**A — Codex global install:**

Create the Codex global skill directories and copy the same skill payload to
`~/.agents/skills/<name>/`:

```bash
mkdir -p ~/.agents/skills/task-tracking/{templates,scripts}
mkdir -p ~/.agents/skills/context-loading/agents
mkdir -p ~/.agents/skills/docstring-guide/{agents,references}
mkdir -p ~/.agents/skills/archive-run/scripts/metrics
mkdir -p ~/.agents/skills/subagent-management/agents
mkdir -p ~/.agents/skills/cursor-subagent
mkdir -p ~/.agents/skills/codex-subagent
mkdir -p ~/.agents/skills/gemini-subagent
mkdir -p ~/.agents/skills/adversarial-review
mkdir -p ~/.agents/skills/council-guide
```

Use the same source files listed in the Claude Code global install section, but
replace `~/.claude/skills/` with `~/.agents/skills/`.

Restart Codex if newly installed skills do not appear.

**B — Codex project-local install, only if explicitly requested:**

Copy the same skill payload into `.agents/skills/`:

| Source                                     | Destination                                  |
| ------------------------------------------ | -------------------------------------------- |
| `files/skills/task-tracking/` (entire dir) | `.agents/skills/task-tracking/`              |
| `files/skills/context-loading/` (entire dir) | `.agents/skills/context-loading/`          |
| `files/skills/docstring-guide/` (entire dir) | `.agents/skills/docstring-guide/`          |
| `files/skills/archive-run/` (entire dir)   | `.agents/skills/archive-run/`                |
| `files/skills/subagent-management/` (entire dir) | `.agents/skills/subagent-management/`    |
| `files/skills/cursor-subagent/SKILL.md`    | `.agents/skills/cursor-subagent/SKILL.md`    |
| `files/skills/codex-subagent/SKILL.md`     | `.agents/skills/codex-subagent/SKILL.md`     |
| `files/skills/gemini-subagent/SKILL.md`    | `.agents/skills/gemini-subagent/SKILL.md`    |
| `files/skills/adversarial-review/SKILL.md` | `.agents/skills/adversarial-review/SKILL.md` |
| `files/skills/council-guide/SKILL.md`      | `.agents/skills/council-guide/SKILL.md`      |

Make scripts executable:

```bash
chmod +x .agents/skills/task-tracking/scripts/init-run.sh
chmod +x .agents/skills/archive-run/scripts/archive-run.sh
chmod +x .agents/skills/archive-run/scripts/metrics/*.sh
```

**Codex compatibility note:** The skill format is shared. The existing
`files/skills/<name>/SKILL.md` files are valid Codex skills because they use the
standard `name` and `description` frontmatter plus Markdown instructions.

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
| `files/../snippets/AGENTS_MD_WORKFLOW.md` | `snippets/AGENTS_MD_WORKFLOW.md` |

(The snippets directory is at `4th-layer-scaffold/snippets/`, not inside `files/`.)

---

### Step 9: Update .gitignore

Append the following to `.gitignore` (create the file if it doesn't exist):

```
# Claude agent run directories (local only — contents never committed)
runs/
!runs/.gitkeep
!runs/CLAUDE-RUNS/.gitkeep
!runs/CLAUDE-RUNS/ARCHIVE.template.md

# Per-machine Claude runtime state
/CLAUDE.local.md

# Per-machine Codex runtime state
/AGENTS.local.md

# Log files
*.log
```

Do NOT replace an existing `.gitignore` — append only. Do NOT force-add
`CLAUDE.local.md`. If the target repo already tracks `CLAUDE.local.md`, ask the user
before running `git rm --cached CLAUDE.local.md` so the file remains locally but is
removed from version control.

Do the same for `AGENTS.local.md` if it already exists and is tracked.

---

### Step 10: Force-add tracked files

```bash
git add -f runs/.gitkeep
git add -f runs/CLAUDE-RUNS/.gitkeep
git add -f runs/CLAUDE-RUNS/ARCHIVE.template.md
# NOTE: Do NOT force-add runs/CLAUDE-RUNS/ARCHIVE.md — it is intentionally
# gitignored as a per-developer archive log.
```

**Note:** `init-run.sh` is no longer at `runs/CLAUDE-RUNS/` — it lives inside the
`task-tracking` skill directory (installed in Step 7). The skill's `scripts/init-run.sh`
was already made executable in Step 7.

---

### Step 11: Test run infrastructure

Run `init-run.sh` from the global skill install by default:

```bash
# Claude Code global default:
~/.claude/skills/task-tracking/scripts/init-run.sh test-tent
# Codex global default:
~/.agents/skills/task-tracking/scripts/init-run.sh test-tent
```

If the user explicitly requested project-local skills, use the project-local path
for that runtime instead:

```bash
skills/task-tracking/scripts/init-run.sh test-tent
.agents/skills/task-tracking/scripts/init-run.sh test-tent
```

Expected output: `✅ Created: runs/CLAUDE-RUNS/RUN-YYYYMMDD-HHMM-test-tent/` with
`TASK_LOG.md`, `SPEC_v1.md`, and `HANDOFF.md` present with timestamps substituted
(not `{{RUN_ID}}` literals).

If template variables aren't substituted, check that the `templates/` directory
inside the `task-tracking` skill is populated correctly from Step 7.

---

## Customization Pass

The infrastructure is now installed. The former `docs/coding_agents/` workflow
guides now live in skills, so this pass focuses on repo instruction files and
any project-specific notes the user wants to add.

### Customize: CLAUDE.md workflow section

The former context-loading checklist now lives in the `context-loading` skill,
the former docstring guide now lives in the `docstring-guide` skill, and the
former subagent guide now lives in the `subagent-management` skill.

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
the Agent Voice section). If missing, copy `files/CLAUDE.local.md` to `CLAUDE.local.md`.
This file is gitignored — it holds per-machine runtime state.

After merging, fill in all `[TODO: project-specific]` markers in CLAUDE.md.

### Customize: AGENTS.md workflow section

If the repo will be used with Codex, use `snippets/AGENTS_MD_WORKFLOW.md`.

**If no AGENTS.md exists:** Copy `snippets/AGENTS_MD_WORKFLOW.md` to `AGENTS.md`.
Then add project-specific repository guidance above the workflow section.

**If AGENTS.md already exists:** Merge the workflow sections from
`snippets/AGENTS_MD_WORKFLOW.md` into the existing file.

Then ensure `AGENTS.local.md` exists with the Active Tasks table. If missing, copy
`files/AGENTS.local.md` to `AGENTS.local.md`. This file is gitignored.

---

### Finalize: Configure settings.local.json

Merge `.claude/settings-hooks-template.json` into `.claude/settings.local.json`:

- If no `settings.local.json` exists: rename the template to `settings.local.json`
- If it exists: merge the `"hooks"` key into the existing file without overwriting
  other keys (`permissions`, `enabledMcpjsonServers`, `additionalDirectories`, etc.)

After merging, delete `.claude/settings-hooks-template.json`.

### Finalize: Configure Codex hooks

If using Codex, ensure `.codex/hooks.json` exists and `.codex/config.toml` enables hooks:

```toml
[features]
codex_hooks = true
```

If `.codex/config.toml` already exists, merge the feature flag without overwriting
other Codex settings.

---

## Completion Checklist

Verify everything before starting work:

- [ ] `task-tracking`, `context-loading`, `docstring-guide`, `archive-run`, and `subagent-management` skills installed globally, unless the user explicitly requested project-local skill copies
- [ ] `init-run.sh test-tent` generates TASK_LOG.md, SPEC_v1.md, and HANDOFF.md with substituted timestamps
- [ ] `.agent-harness/hooks/` exists with shared hook logic
- [ ] `.claude/settings.local.json` has `"hooks"` key with 7 core hooks + SessionStart
- [ ] `.codex/hooks.json` has SessionStart, UserPromptSubmit, and PreToolUse hook wiring (if using Codex)
- [ ] `.codex/config.toml` or another active Codex config layer has `[features] codex_hooks = true` (if using Codex)
- [ ] `.claude/archive-run.config` created with appropriate metric collectors
- [ ] `context-loading` skill installed and referenced by CLAUDE.md/AGENTS.md workflow section
- [ ] `docstring-guide` skill installed and referenced by CLAUDE.md/AGENTS.md workflow section
- [ ] `subagent-management` skill installed and referenced by CLAUDE.md/AGENTS.md workflow section
- [ ] CLAUDE.md has the workflow pointer section (skill references, subagent section)
- [ ] AGENTS.md has the workflow pointer section (if using Codex)
- [ ] CLAUDE.local.md has the Active Tasks table (and Agent Voice if used)
- [ ] AGENTS.local.md has the Active Tasks table (if using Codex)
- [ ] `.gitignore` has `runs/`, `!runs/.gitkeep`, `/CLAUDE.local.md`, and `/AGENTS.local.md` appended
- [ ] `CLAUDE.local.md` exists locally but is not tracked by git
- [ ] `AGENTS.local.md` exists locally but is not tracked by git (if using Codex)
- [ ] `runs/.gitkeep`, `runs/CLAUDE-RUNS/.gitkeep`, `ARCHIVE.template.md` force-added to git
- [ ] `runs/CLAUDE-RUNS/ARCHIVE.md` exists locally and is not tracked

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
| Full `AGENTS.md`                                    | Project-specific repository guidelines. Scaffold only provides a workflow snippet.                      | Snippet only — `snippets/AGENTS_MD_WORKFLOW.md`            |
| `EXAMPLES.md`, `VISUAL_DIAGRAMS.md`                 | Project-specific code examples. Write your own.                                                        | No                                                         |
| `GEMINI-RUNS/`                                      | Add `runs/GEMINI-RUNS/` yourself if you use Gemini agents.                                             | No                                                         |
| MCP query templates                                 | Specific to your database tooling.                                                                     | No                                                         |
| Project-tailored `DOCSTRING_GUIDE.md`               | The reusable guide lives in the `docstring-guide` skill; copy/tailor a repo doc only on explicit request. | Skill: `docstring-guide`                                  |
| `ARCHITECTURE_CONSTRAINTS.md`                       | Project-specific hard rules. Write your own.                                                           | No (TODO template planned)                                 |
| `health-pulse.sh`                                   | Language-specific metrics gathering. Now partially covered by `archive-run` skill's metric collectors. | Partially — see `archive-run` skill                        |
