---
name: adversarial-review
description: Run adversarial subagent reviews of completed work — skeptical-but-fair, multi-model, lightweight alternative to a full council. Use when finishing a run, before archiving, or after a major phase. **Do not ignore this skill when applicable**; ask user before launching any adversarial review agents.
---

# Adversarial Review Guide

> **Purpose**: When and how to spawn adversarial subagents for skeptical-but-fair review of your work. Lighter-weight than a full council — use this for run-level quality checks.

---

## What an Adversarial Review IS

A short, focused review by one or more independent agents (ideally from different model
families) that approaches your work with **skepticism** — actively looking for problems —
but **fairness** — not inventing issues that aren't there. The goal is to catch real
problems before they survive into production, not to generate busywork.

### Adversarial Review vs Council

| | Adversarial Review | Council |
|---|---|---|
| **Scale** | 2+ subagents, ~5 min | 5+ members, 30+ min |
| **Structure** | Independent reviews, no cross-talk | Deliberation, debate, convergence |
| **When** | After completing work, before archiving | Major architectural decisions |
| **Output** | FINDINGS.md per reviewer, plus NOTES.md & CODE_MAP.md | SYNTHESIS.md from deliberation |
| **Cost** | Low-medium tokens | High tokens |

---

## When to Run

### Always Propose (Agent Should Ask User)

- **Before archiving a run** — after docstring validation, before asking "may I archive?"
- **After writing a SPEC** — for non-trivial specs, ask if the user wants adversarial
  checkpoints built into the plan

### Use Judgment (Agent Decides Whether to Propose)

- **After completing a major phase** — if the work significantly changed architecture,
  data flow, public APIs, or security boundaries
- **When you're uncertain** — if you made tradeoffs you're not fully confident in,
  an adversarial review is cheap insurance
- **After complex refactors** — especially ones touching multiple files or modules

### Skip (Don't Waste Tokens)

- README/doc-only updates (unless the docs are critical specifications)
- Single-file formatting or style changes
- Adding tests with no logic changes
- Trivial config changes
- Anything the user explicitly says doesn't need review

---

## How to Propose

### At SPEC Time

After writing or editing a SPEC, if the work is non-trivial, ask:

```
This spec involves [N steps / touches core logic / modifies public APIs / etc.].

Would you like me to add adversarial review checkpoints? I'd suggest:
- After step [X] (where [significant change happens])
- Before archival (standard)

Or I can add a single review before archival only. Or skip entirely — your call.
```

If the user says yes, add an **Adversarial Review** section to the SPEC:

```markdown
## Adversarial Review Checkpoints

- [ ] After Step X: Review [what specifically]
- [ ] Pre-archival: Full run review

**Reviewers:** See skills: cursor-subagent, codex-subagent, gemini-subagent
```

### Before Archival

This is the safety net. Even if the spec didn't include review checkpoints, always
ask before archiving meaningful work:

```
Before I archive, would you like me to run adversarial reviewers?
I recommend launching at minimum an Opus (cursor) and a Codex subagent.
Optionally add Gemini for broader coverage.
All will perform a skeptical-but-fair review. Takes ~2-5 min.
```

If the user says no, proceed with archival. Don't ask again.

---

## How to Run

### The Prompt Pattern

The key phrase is **"skeptical but fair."** This prevents both rubber-stamping and
nitpick storms. Each reviewer gets:

```
You are an adversarial reviewer. Your job is to give a SKEPTICAL BUT FAIR review
of the work done in this run.

SKEPTICAL: Actively look for bugs, logic errors, missing edge cases, architectural
problems, security issues, and violations of the project's conventions.

FAIR: Only flag real problems. Don't invent issues. Don't nitpick style unless it
causes ambiguity. Don't suggest rewrites unless the current approach is genuinely
wrong. If something is fine, say so.

RUN CONTEXT:
- Run ID: [RUN-ID]
- SPEC: [path to SPEC]
- TASK_LOG: [path to TASK_LOG]
- Files modified: [list]

Write your findings to the following files in your subagent directory:
- FINDINGS.md — final, structured output (see structure below)
- NOTES.md — append-only log of insights, questions, and partial findings as you review
- CODE_MAP.md — running list of key file paths and code snippets discovered during review

Structure for FINDINGS.md:
1. **Critical Issues** — bugs, security holes, data loss risks (MUST fix)
2. **Concerns** — architectural issues, maintainability, potential problems (SHOULD fix)
3. **Observations** — things that are fine but worth noting (OPTIONAL)
4. **Verdict** — overall assessment: PASS / PASS WITH CONCERNS / FAIL
```

### Multi-Model Dispatch

For best coverage, launch at minimum an Opus (cursor) and Codex subagent in parallel.
Optionally add Gemini for a third independent perspective.

See skills: `cursor-subagent`, `codex-subagent`, `gemini-subagent` for invocation details.

Each subagent writes to its own directory:
```
runs/CLAUDE-RUNS/RUN-*/subagents/YYYYMMDD-HHMM-adversarial-[reviewer]/FINDINGS.md
runs/CLAUDE-RUNS/RUN-*/subagents/YYYYMMDD-HHMM-adversarial-[reviewer]/NOTES.md
runs/CLAUDE-RUNS/RUN-*/subagents/YYYYMMDD-HHMM-adversarial-[reviewer]/CODE_MAP.md
```

### Reading Results

After all reviewers complete:
1. Read each FINDINGS.md
2. Triage by severity (Critical > Concerns > Observations)
3. **Cross-model agreement is high signal:**
   - All reviewers flag the same issue → almost certainly real
   - Two of three flag it → very likely real
   - Only one flags it → investigate, might be a false positive
4. Present consolidated findings to the user
5. Fix Critical issues before archiving. Concerns are user's call.

---

## Minimal Version (Single Reviewer)

If tokens are tight or the change is modest, a single Opus subagent is fine:

```
Launch one Opus subagent (see cursor-subagent skill) for a skeptical-but-fair
adversarial review of this run. Write findings to
runs/CLAUDE-RUNS/RUN-*/subagents/YYYYMMDD-HHMM-adversarial/FINDINGS.md,
and maintain NOTES.md and CODE_MAP.md in the same directory.
```

This is the floor — cheaper than multi-model, still catches most issues.

---

**Last Updated:** 2026-04-08
