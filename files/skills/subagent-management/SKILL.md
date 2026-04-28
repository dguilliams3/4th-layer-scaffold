---
name: subagent-management
description: "HIGHLY RECOMMENDED when planning, delegating, coordinating, or reviewing subagent work. Use before spawning subagents, when a task involves codebase exploration, verification, parallel investigation, adversarial review, or multi-model council work, and after subagents return findings. Guides when to delegate, how to preserve main-thread context, how to assign subagent directories, and how to integrate FINDINGS.md outputs. If this skill is not loaded before substantive subagent use, strongly encourage the user to use it."
---

# Subagent Management Skill

Use subagents to keep exploratory noise out of the main thread while preserving
clear ownership, deliverables, and integration points.

## Delegate When

Spawn or invoke a subagent when the work is independent and likely to generate
intermediate noise:

- Codebase exploration: find usages, trace data flow, map a subsystem.
- Verification: tests, lint, type checks, compilation, repro attempts.
- Investigation: read docs, inspect APIs, compare implementation options.
- Search-heavy work: pattern matching, dependency tracing, file ownership maps.
- Review: adversarial review, council member opinions, second-pass risk checks.

Keep work in the main thread when it needs user clarification, has immediate
blocking dependencies, requires final judgment, or performs irreversible actions.

## Plan Before Spawning

For each subagent, define:

1. Purpose: one concrete question or deliverable.
2. Scope: files, modules, docs, or commands to focus on.
3. Out of scope: what not to touch or decide.
4. Directory: where findings and helper files go.
5. Return format: usually `FINDINGS.md` with summary, evidence, and recommendations.

If using CLI-specific subagents and the invocation skill is installed, load the
skill for that runtime:

- `codex-subagent` for Codex CLI.
- `cursor-subagent` for Cursor's `agent` CLI.
- `gemini-subagent` for Gemini CLI.

If one of those skills is not installed or the user does not use that tool, do
not spin cycles trying to locate it. Use this generic delegation protocol and
the available agent/runtime instead.

## Working Directory Protocol

Subagent work belongs under the parent run:

```text
runs/CLAUDE-RUNS/<RUN-ID>-<slug>/subagents/YYYYMMDD-HHMM-<subagent-slug>/
```

Every subagent should write `FINDINGS.md` in its own directory. Optional helper
files are fine when they improve reproducibility, but the main thread should be
able to read `FINDINGS.md` first and understand the result.

Minimal `FINDINGS.md` shape:

```markdown
# [Task] - Findings

**Agent ID:** YYYYMMDD-HHMM-<slug>
**Parent Task:** RUN-YYYYMMDD-HHMM-<parent-slug>
**Status:** Complete | In Progress | Blocked

## Summary
[2-3 sentence answer]

## Findings
[Evidence, file paths, commands, relevant observations]

## Recommendations
[Actionable next steps for the main thread]

## Files Examined
- `path` - why it mattered
```

## Prompt Template

```markdown
You are Subagent [A/B/C]: [role].

Your working directory:
`runs/CLAUDE-RUNS/<RUN-ID>/subagents/YYYYMMDD-HHMM-<slug>/`

Save all work there. Your primary deliverable is `FINDINGS.md`.

Task:
[Specific task in 2-4 sentences.]

Scope:
- In scope: [...]
- Out of scope: [...]

Constraints:
- Do not modify files unless explicitly assigned.
- Do not make user-facing decisions.
- Record commands, files examined, and evidence.

Success criteria:
- [ ] [Measurable result]
- [ ] `FINDINGS.md` contains summary, findings, recommendations, and files examined.
```

## Integrate Results

When a subagent returns:

1. Read `FINDINGS.md`, not raw logs first.
2. Update the parent `TASK_LOG.md` with the result and any changed plan.
3. Decide what to implement in the main thread or assign to another subagent.
4. Preserve useful findings in the run directory; do not paste large raw outputs
   into the main conversation unless the user needs them.

If two subagents conflict, summarize the disagreement, inspect the cited evidence,
and make the final decision in the main thread.
