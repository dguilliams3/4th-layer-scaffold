# CHECKPOINT-{{N}} — {{LABEL}}

**Created:** {{TIMESTAMP}}
**Run:** {{RUN_ID}}
**Predecessor:** {{PREV_CHECKPOINT}}
**Status:** <!-- in-flight | locked | launch-ready | ship-ready | abandoned -->
**Trigger:** <!-- compaction-imminent | phase-boundary | major-decision | manual -->

---

<!--
WRITING GUIDANCE — read before filling sections.

Default is VERBOSE AND COMPREHENSIVE. The reader is an agent that has lost
its working-memory context to compaction (or has never had it — a fresh
session resuming this run). Over-explain rather than under-explain. Multi-
paragraph narrative is fine. Tables for structured data are encouraged.
Inline file paths, line numbers, function names, error messages, decision
rationales. The goal: someone reading only this checkpoint + the docs it
points to could act correctly on the next user message.

If a section is genuinely empty (e.g. no new SPEC versions since the prior
checkpoint), say so explicitly — "No new SPEC versions since CHECKPOINT-0(N-1)"
is itself a useful fact. Don't leave bullet markers empty.

NEVER edit this file before you have Read it via the Claude Code Read tool —
the harness rejects Edits to files that have not been Read in the current
session.
-->

## TL;DR for next agent

<!-- The post-compact agent reads this FIRST. Cover comprehensively:
     - What is the active work right now?
     - What state are we in (mid-implementation, awaiting review, debugging,
       blocked on external)?
     - What single thing should the agent do first when they wake up here?
     - Any critical pivots, surprises, or context-changes since the prior
       checkpoint that they MUST know about.

     Fully-formed bullets, not telegraph-style. Length serves clarity. -->

-

---

## Where I am right now

<!-- Multi-paragraph encouraged. Be geographic — point to paths, line ranges,
     functions, and the specific file/decision/feature in active focus. What's
     "loaded in my head" that I'd lose on compaction? Include the implicit
     mental model: what hypotheses am I currently working under, what's the
     story I'm telling myself about the work, what context did I just absorb
     from a tool call or user message that hasn't been written down anywhere
     else yet?

     The reader has zero working memory. Reconstruct enough scaffolding here
     that they can re-enter the same mental frame you were in. -->

---

## What changed since {{PREV_CHECKPOINT}}

<!-- Comprehensive list of every concrete delta since the prior checkpoint
     (or run start if this is the first). Decisions made, code written, tools
     run, subagents dispatched, hypotheses confirmed or falsified, external
     events that affected the work (PR merged, user provided new info,
     teammate pinged you).

     Don't omit anything that took thought to derive — the cost of writing
     "we figured out X means Y" is small; the cost of re-deriving it after
     compaction is large. -->

-

---

## New artifacts since {{PREV_CHECKPOINT}}

<!-- Files and directories created in this run since the last checkpoint.
     Inline the path verbatim so a post-compact agent can grep/cat directly
     without searching. Annotate each entry with purpose AND status. -->

### New SPEC versions

<!-- e.g. SPEC_v3.md — created 14:30 EDT, supersedes v2. Trigger: scope
     widened to include error-path testing per user clarification. Diff
     against v2: added Section 4 (error-path scenarios), revised acceptance
     criteria in Section 2.

     If none: "No new SPEC versions since CHECKPOINT-0(N-1)." -->

-

### New subagent directories

<!-- e.g. subagents/20260515-0915-sonnet-fixture-cleanup/
       - Purpose: replace hard-coded sample ids (ITEM-A, SKU-000001)
         with placeholders in test fixtures
       - SPEC: <subagent dir>/SPEC.md
       - Status: in-flight, dispatched 09:15 EDT, 20 min budget
       - FINDINGS expected at: <subagent dir>/FINDINGS.md when complete

     If none: "No new subagent dirs since CHECKPOINT-0(N-1)." -->

-

### Other new run artifacts

<!-- iterations/, council/, review-notes/, iteration-logs/, or any
     other run-internal directories or top-level run files. Same format:
     path, purpose, status. -->

-

---

## What's next (priority order)

<!-- Numbered list of concrete actions, NOT goals. Tag each with P0/P1/P2
     (or your priority scheme). Include enough detail that the next agent
     can execute without re-planning: which file to edit, which command to
     run, which user to ping. If a step has a non-obvious rationale, include
     a brief WHY.

     Be comprehensive — list everything queued, not just the top 2-3. -->

1.

---

## Critical refs (file:line — note)

<!-- The 10-30 paths a post-compact agent would otherwise have to re-grep
     for. Format: `path/to/file.ext:LINE — one-line annotation of why this
     matters`. Include external paths (sibling worktrees, sibling runs,
     parent project dirs) when relevant. Don't skimp — these are the cheap-
     to-write, expensive-to-rediscover items. -->

-

---

## Critical numbers / facts to preserve

<!-- Specific values that would be expensive or impossible to re-derive, or
     that compaction is likely to lose. Examples: precise dollar amounts,
     measured rates, version SHAs, test pass/fail counts, branch SHAs,
     hostnames, IDs from external systems.

     For each: the value, a brief context line, and (where applicable) the
     derivation path so it can be re-checked. -->

-

---

## Don't retry

<!-- Approaches/tools/args/hypotheses already ruled out, with brief WHY.
     Be specific — paste the exact failed approach (the actual command, the
     actual edit, the actual line of reasoning), not an abstraction. The
     goal is preventing the next agent from re-running the same dead end.

     Format: "Tried X. Failed because Y. Don't retry unless Z changes." -->

-

---

## Open questions / hypotheses in flight

<!-- Half-formed thoughts that don't belong in SPEC yet but must survive
     compaction. For each: state the question or hypothesis as a full
     thought, the evidence in either direction, and the status:
       (testing) — actively gathering evidence
       (waiting on X) — blocked on external input
       (unresolved) — stalled or low-priority

     These are the threads the next agent should consider picking up. -->

-

---

## Pending external dependencies

<!-- Anything blocked on people, services, or background processes. Be
     specific: WHO is blocking, WHAT they need to deliver, EXPECTED timing,
     IMPACT if delayed. Example:
       "Waiting on a reviewer's sign-off on PR #12. Expected by end of day.
        Without it, can't merge FEAT-47; downstream PR 4 invocation is
        blocked. Mitigation: FEAT-47 worktree is independently testable;
        can proceed with implementation against FEAT-45 tip in the
        meantime." -->

-

---

## Recovery reading order (for post-compact agent)

<!-- Numbered, comprehensive list of what to read after THIS checkpoint, in
     order. Include the WHY for each entry so the agent doesn't waste time
     reading docs that aren't load-bearing.

     Typical order: this file → latest SPEC → TASK_LOG tail → active code
     file → companion docs (REHYDRATE.md, ITERATION-ROADMAP.md, FINDINGS.md
     from in-flight subagents). -->

1. This file (you are here).
2. SPEC_v<latest>.md — current contract for the run.
3. TASK_LOG.md (tail, ~50-100 lines) — recent chronology.
4.
5.

---

## Personal / stakeholder context

<!-- The social and business layer that compaction strips. Don't elide.
     Include:
       - Active deadlines (what, when, why)
       - Who is waiting on what (specifically — names, not roles)
       - Business stakes (deal value, demo timing, contract terms)
       - "If the user asks 'where are we?', say X" social scripts
       - Reference to voice/style memory (e.g. "use ★ Insight blocks,
         no emoji, tight responses ≤100 words for body") if the
         run-specific context overrides defaults

     The voice/style cheat-sheet should reference memory files rather than
     inline them, unless this run has specific overrides. -->

---

## Cross-references

<!-- Comprehensive list. Sister checkpoints (predecessor and any siblings),
     parent runs, child subagent dirs, sibling worktrees, memory files
     touching this work, companion docs (REHYDRATE.md, ITERATION-ROADMAP.md,
     PROGRESS.md). One-line note per entry on what it's for. -->

-
