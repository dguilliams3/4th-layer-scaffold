---
name: council-guide
description: Run a multi-agent council for major architectural decisions — quad-model deliberation with Claude teammates (Opus) plus Codex, Gemini, and Cursor as independent external analysts. Use when a decision is too complex or high-stakes for a single agent or adversarial review.
---

# Council Deliberation Guide

> **Purpose**: Operational guide for running multi-agent councils with cross-model deliberation. Councils use Claude teammates (Opus) for structured debate, plus Codex (OpenAI), Gemini (Google), and Cursor (Composer-2) as independent external analysts.

---

## What a Council IS

A council is a **deliberation**, not parallel reviews. The value comes from members
seeing each other's positions, challenging them, and converging on refined recommendations.
Without cross-member discussion, you just have independent reviewers — the synthesis
is aggregation, not deliberation.

---

## Mandatory Members

| Member | Role | Runtime |
|--------|------|---------|
| **4th Layer Advocate** | Agent navigability, disambiguation, structural clarity | Claude teammate (Opus) |
| **Visionary** | Scalability, YIGNI, known future trajectory | Claude teammate (Opus) |
| **Devil's Advocate** | Find holes, challenge assumptions, surface what everyone missed | Claude teammate (Opus) |
| **Codex** | Independent autonomous analysis, no assigned role, full freedom | Background CLI (OpenAI) |
| **Gemini** | Independent autonomous analysis, no assigned role, full freedom | Background CLI (Google) |
| **Cursor** | Independent autonomous analysis, no assigned role, full freedom | Background agent (`~/bin/agent`, model: Composer-2) |

**Optional members** added per-council based on domain:
- **Data Engineer**, **Speed**, **Security**, **UX**, etc.

### Why Four Model Families

Codex, Gemini, and Cursor provide **cross-model diversity** — three independent analyses from
different model families (OpenAI, Google, Cursor/Composer-2) that neither share context with
each other nor with the Claude teammates. This surfaces blind spots that a single model family misses.

When external analysts **agree** on something Claude members missed → high-confidence gap.
When external analysts **disagree** with each other → highest-signal finding in the council.

---

## Infrastructure

Create a `council/` subdirectory in the active RUN:

```
council/
├── README.md                    # Members, process, key context files
├── SYNTHESIS.md                 # Final synthesis (written by lead after deliberation)
├── <member-slug>/
│   ├── SPEC.md                  # Role mandate, evaluation criteria, key files to read
│   └── NOTES.md                 # Append-only assessment log
```

### Claude Teammates

Use TeamCreate to create the team. Each member is an Agent teammate (all Opus).

### External Agents (Codex + Gemini + Cursor)

All three run in background via CLI — launched with `run_in_background: true` in the Bash tool.

```bash
# Codex (OpenAI)
codex -p "council prompt here" --force --model auto --output-format stream-json 2>&1

# Gemini (Google)
gemini -p "council prompt here" --yolo -m gemini-2.5-pro --output-format stream-json 2>&1

# Cursor (Composer-2)
agent --force --trust --model composer-2 --output-format stream-json --print "council prompt here" 2>&1
```

**Rules for external agents:**
- Launch all three at the same time as Claude teammates (Phase 1)
- Use `stream-json` output format
- Peek with `head -n 50` on output file — NEVER read the full stream
- They receive the same high-level council prompt but NO role assignment
- They do NOT see each other's work or the Claude members' work
- Their independence is the point — don't contaminate it

### External Agent Prompt Template

Give all three external agents the same prompt (adjusted only for CLI syntax):

```
You are an independent analyst on a multi-agent council. Your job is to analyze
the following topic with complete autonomy — no assigned role, no constraints
on what you focus on.

TOPIC: [council topic]

CONTEXT FILES TO READ:
- [list of key files]

DELIVERABLE: Write your analysis to council/external-[codex|gemini|cursor]/NOTES.md
Include: key observations, concerns, recommendations, and anything surprising.

There are other council members analyzing the same topic independently.
Your value is your unique perspective — don't try to be comprehensive,
focus on what YOU find most important.
```

---

## Execution Flow (CRITICAL — Do Not Skip Steps)

### Phase 1: Independent Review

1. Launch Codex, Gemini, AND Cursor in background (full autonomy, no role, no coordination)
2. Spawn all Claude teammates in parallel
3. Each Claude member reads their SPEC, reads context files, writes NOTES.md, sends summary to lead
4. **DO NOT shut anyone down yet**

### Phase 2: Pre-External Synthesis

1. Lead writes a PRELIMINARY synthesis based on Claude members' assessments
2. **Broadcast** the preliminary synthesis to all Claude teammates
3. Include: consensus items, disagreements, open questions
4. Purpose: members see each other's positions for the first time

### Phase 3: Cross-Member Discussion

1. Members respond to the synthesis — challenge, agree, refine, debate
2. Members can message each other directly (not just the lead)
3. Lead monitors and captures key exchanges
4. This is where real deliberation happens — positions evolve, disagreements resolve

### Phase 4: Post-External Review

1. When external agents complete, share ALL findings with all Claude teammates
2. Present them as "External Agent A/B/C" — let members react to each
3. Key questions to surface:
   - Did any external agent catch something no Claude member did?
   - Do the external agents agree with each other? Disagreements between them are high-signal.
   - Does any external analysis change a Claude member's position?
4. Allow a round of reactions from Claude members before moving to synthesis

### Phase 5: Final Synthesis

1. Lead writes SYNTHESIS.md incorporating the full deliberation arc:
   - Initial positions → cross-member debate → external agent reactions → final positions
2. Note where external agents **converged** (high confidence) vs **diverged** (needs attention)
3. Note where external agents agreed with Claude members vs surfaced novel concerns
4. This reflects actual deliberation, not just aggregation of independent reports

### Phase 6: User Discussion

1. Present synthesis to the user
2. User discusses, pushes back, asks questions
3. Council members are **STILL ALIVE** during this phase — user can probe any position
4. External agent output is available for reference but agents themselves are done

### Phase 7: Shutdown

1. Only after user approves the synthesis or has no more questions
2. Send shutdown requests to all teammates
3. Clean up team

---

## Anti-Patterns (Mistakes Made, Don't Repeat)

| Anti-Pattern | Why It's Wrong |
|-------------|----------------|
| **Shutting down members after Phase 1** | Kills the deliberation before it starts. Individual reports are the STARTING POINT, not the output. |
| **Synthesizing without cross-member discussion** | Produces aggregation, not deliberation. Synthesis should reflect positions that EVOLVED through debate. |
| **Treating council like parallel subagents** | Subagents do independent work and report. Council members DISCUSS, DISAGREE, and CONVERGE. |
| **Ignoring external agent disagreements** | When two independent external models disagree, that's the highest-signal finding. Always surface and resolve. |
| **Contaminating external agents** | Don't share Claude members' work with Codex/Gemini/Cursor. Their value is independent perspective from a different model family. |
| **Skipping Phase 4 if externals are slow** | Wait for them. The cross-model check is a core part of the protocol, not optional. |

---

## Quick Reference: CLI Commands

```bash
# Codex — headless, full permissions, background
codex -p "prompt" --force --model auto --output-format stream-json 2>&1
# run_in_background: true

# Gemini — headless, full permissions, background
gemini -p "prompt" --yolo -m gemini-2.5-pro --output-format stream-json 2>&1
# run_in_background: true

# Cursor — headless, full permissions, background
agent --force --trust --model composer-2 --output-format stream-json --print "prompt" 2>&1
# run_in_background: true

# Peek at output (all three)
head -n 50 /path/to/output/file
```

---

## Lessons from First Council (RUN-20260304-1112, eda-architecture-council)

- 6 members produced excellent independent assessments
- But no member ever saw another's work
- No cross-pollination, no debate, no position evolution
- Synthesis was lead aggregating 6 independent reports
- Value left on the table: Speed vs Data Engineer on taxonomy,
  Devil's Advocate vs 4th Layer Advocate on parser validation approach,
  Codex insights never challenged or adopted by the group

**Takeaway:** The protocol exists because this mistake was made. Follow every phase.

---

**Last Updated:** 2026-04-08
