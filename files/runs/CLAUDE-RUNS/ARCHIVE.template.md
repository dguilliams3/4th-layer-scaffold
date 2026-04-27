# Run Archive

Completed runs are logged here (newest first). Working directories remain in
`runs/CLAUDE-RUNS/<RUN-ID>-<slug>/` indefinitely — never auto-deleted.

**Rotation:** Entries older than 2 calendar months automatically roll to
`ARCHIVE-YYYY-MM.md` files in this same directory during archival (see the
`archive-run` skill's Step 4.5). Look at the bottom of this file for the
Monthly Archives index once rotation has fired.

**This file (`ARCHIVE.md`) and any `ARCHIVE-YYYY-MM.md` files are per-developer
working state (gitignored).** Only `ARCHIVE.template.md` is tracked.

---

## Entry Template

```markdown
### [RUN-YYYYMMDD-HHMM] Brief Description

**Archived:** YYYY-MM-DD HH:MM EST
**Created:** YYYY-MM-DD HH:MM EST
**Completed:** YYYY-MM-DD HH:MM EST (optional)
**Duration:** ~X hours/minutes (optional)
**Working Directory:** `runs/CLAUDE-RUNS/<RUN-ID>-<slug>/`
**Branch:** branch-name (optional)

**Code Duplication:** X.XX% (optional — project-specific metric)

**Summary:**
[Brief description of what was accomplished]

**Deliverables:**
- [List of key files created/modified]

**Notes:** (optional)

**Outcome:** [Final result and any follow-up context]

---
```

---

<!-- Entries go above this line, newest first -->
