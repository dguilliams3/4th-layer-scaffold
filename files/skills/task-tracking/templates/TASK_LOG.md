# Task Log: RUN-{{RUN_ID}} - {{DESCRIPTION}}

**Created:** {{TIMESTAMP}}
**Status:** In Progress
**Working Directory:** runs/CLAUDE-RUNS/RUN-{{RUN_ID}}-{{SLUG}}/

---

## Objective

[Clear statement of what this task aims to accomplish]

---

## Progress Timeline

### {{TIMESTAMP}} - Task Started

- Generated Run ID: RUN-{{RUN_ID}}
- Created working directory
- Initial context: [brief description]

---

## Subagent Spawns

*Log subagent spawns and their findings here*

| Timestamp | Agent ID | Purpose | Status | Findings Link |
|-----------|----------|---------|--------|---------------|
| | | | | |

---

## Files Created/Modified

- `path/to/file` - [NEW|MODIFIED|DELETED] - [brief description]

---

## Decisions Made

*Updated as decisions are made*

---

## Blockers / Tech Debt Discovered

*Track issues discovered during work that block progress or require future attention.
Use TD codes for issues that need tracking beyond this task.*

| TD Code | Issue | Severity | Workaround Used | Follow-up Needed |
|---------|-------|----------|-----------------|------------------|
| TD-YYYYMMDD-01 | [Description] | BLOCKING/HIGH/MED/LOW | [How you worked around it] | YES/NO |

<!-- For BLOCKING or HIGH items, expand with a detail block:

#### TD-YYYYMMDD-NN — [Short Title]
**Category:** BUG | ARCHITECTURE | DEPENDENCY | PERFORMANCE | SECURITY
**Problem:** [Detailed description]
**Impact:** [What this blocks or affects]
**Proposed Fix:** [If known]
-->

---

## Don't Retry (Failed Approaches)

*Approaches tried and failed — prevents future agents from repeating dead ends.
Also captured in SPEC_vN.md "Don't Retry" section.*

<!-- For each failed approach:
### [Approach Name]
**Tried:** [timestamp]
**Outcome:** FAILED | PARTIALLY WORKED
**What was attempted:** [description]
**Why it failed:** [root cause]
**Evidence:** [error messages, unexpected behavior]
-->

---

## Next Steps

*Updated as progress is made*

---

## Archive Checklist

*Before requesting archival, verify:*

- [ ] All tests pass
- [ ] Docstring validation completed (if code was modified)
- [ ] Length audit completed (if code was modified)
- [ ] Blockers section filled out (or marked N/A)
- [ ] Don't Retry section filled out (or marked N/A)
- [ ] HANDOFF.md completed with lessons + memory candidates
- [ ] Follow-up tasks created for any TD codes marked "Follow-up Needed: YES"
