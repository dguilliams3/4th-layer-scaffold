# Skills

Self-contained knowledge packages that teach Claude, Codex, and related coding agents
how to perform specialized tasks. Each skill directory can be installed into the
agent-specific skill location or referenced directly from project guidance.

## Available Skills

| Skill | Directory | Purpose |
|-------|-----------|---------|
| `task-tracking` | `task-tracking/` | **HIGHLY RECOMMENDED.** Structured run tracking — SPEC versioning, TASK_LOG, HANDOFF docs, memory promotion, init-run scaffolding. Opt-out, not opt-in. |
| `context-loading` | `context-loading/` | **HIGHLY RECOMMENDED.** Load at new session start, after compaction/resume, or before broad repo/doc reading — partial reads, cached summaries, composed shell commands. |
| `docstring-guide` | `docstring-guide/` | **HIGHLY RECOMMENDED.** Load before any task that will write or edit actual code — keeps docstrings, navigation refs, and test traceability accurate. |
| `archive-run` | `archive-run/` | **HIGHLY RECOMMENDED.** Archival checklist, project-specific metric collection, ARCHIVE.md entry format. Load fresh at archival time. Pairs with `task-tracking`. |
| `subagent-management` | `subagent-management/` | **HIGHLY RECOMMENDED.** Delegation decisions, subagent prompt structure, run-directory protocol, FINDINGS.md integration. |
| `cursor-subagent` | `cursor-subagent/` | Spawn Cursor's `agent` CLI as a subagent for investigation/exploration — Windows/Git Bash invocation, model selection, do/don't patterns |
| `codex-subagent` | `codex-subagent/` | Spawn Codex CLI as a subagent for long implementation tasks — SPEC.md pattern, stdin prompt, Windows invocation, do/don't patterns |
| `gemini-subagent` | `gemini-subagent/` | Spawn Gemini CLI as a subagent — headless invocation, model selection, auth setup, output formats, all-four-CLIs comparison table |
| `adversarial-review` | `adversarial-review/` | Run skeptical-but-fair multi-model review before archiving or after major phases — when to propose, prompt pattern, multi-model dispatch, triage |
| `council-guide` | `council-guide/` | Run a full quad-model council for major architectural decisions — 7-phase execution flow, anti-patterns, CLI quick ref |

## Skill Structure

Each skill directory follows this layout:

```
skill-name/
  SKILL.md              <- Main guide. The agent reads this first after skill trigger.
  references/           <- Supporting docs (field maps, design rules, glossaries)
  templates/            <- Template files (PPTX, DOCX, etc.)
  scripts/              <- Reference implementations (helpers, not rigid pipelines)
```

## How to Use

### Claude Desktop
Zip the skill directory and upload it as a Project Knowledge file. Claude will read SKILL.md and the references to understand how to perform the task.

### Claude Code
Install global skills under `~/.claude/skills/<name>/` by default. Only keep
project-local copies under `skills/<name>/` when the user explicitly asks for
repo-specific skills.

### Codex
Install global skills under `~/.agents/skills/<name>/` by default. Only keep
project-local copies under `.agents/skills/<name>/` when the user explicitly asks
for repo-specific skills. Codex discovers skills from those locations and loads
`SKILL.md` when the skill triggers.
