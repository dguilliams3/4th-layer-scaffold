# Monthly Archival Guide

> Instructions for AI agents (Claude Code, etc.) performing monthly RUN archival.

## When to Run

Execute on the **1st of each month** (or first working session of the month).

**Rolling Window Rule:**
- **Active**: Current month + prior month stay in `CLAUDE-RUNS/`
- **Historical**: (Current - 2 months) and older move to `CLAUDE-RUNS-HISTORICAL/`

Example (if today is February 1, 2026):
- Active: January 2026, December 2025
- Move to Historical: November 2025 (if not already moved)

---

## Pre-Flight Checklist

- [ ] Verify current date: `date "+%Y-%m-%d"`
- [ ] Identify month to archive: (current - 2)
- [ ] Count directories to move: `ls -1 | grep "RUN-YYYYMM" | wc -l`
- [ ] Confirm ARCHIVE-YYYY-MM.md exists for that month

---

## Step-by-Step Process

### Step 1: Create Historical Directory

```bash
mkdir -p runs/CLAUDE-RUNS-HISTORICAL/YYYY-MM
```

### Step 2: Move Directories

```bash
cd runs/CLAUDE-RUNS

# Move RUN- prefixed directories
mv RUN-YYYYMM* ../CLAUDE-RUNS-HISTORICAL/YYYY-MM/

# Move legacy directories (no RUN- prefix) if any
mv YYYYMM* ../CLAUDE-RUNS-HISTORICAL/YYYY-MM/
```

### Step 3: Move Monthly Archive File

```bash
mv ARCHIVE-YYYY-MM.md ../CLAUDE-RUNS-HISTORICAL/YYYY-MM/
```

### Step 4: Update Links in Moved Archive

The moved archive file needs links updated from:
```
`runs/CLAUDE-RUNS/RUN-YYYYMM...`
```
To:
```
`./RUN-YYYYMM...`
```

**Commands:**
```bash
cd runs/CLAUDE-RUNS-HISTORICAL/YYYY-MM

# Update RUN- prefixed paths
sed -i 's|runs/CLAUDE-RUNS/RUN-YYYYMM|./RUN-YYYYMM|g' ARCHIVE-YYYY-MM.md

# Update legacy paths (no RUN- prefix)
sed -i 's|runs/CLAUDE-RUNS/YYYYMM|./YYYYMM|g' ARCHIVE-YYYY-MM.md

# Update header to show new location
sed -i 's|Part of:.*|Location: `runs/CLAUDE-RUNS-HISTORICAL/YYYY-MM/`\n**Part of:** [ARCHIVE Index](../../CLAUDE-RUNS/ARCHIVE.md)|' ARCHIVE-YYYY-MM.md
```

### Step 5: Update ARCHIVE.md Index

Edit `runs/CLAUDE-RUNS/ARCHIVE.md`:

1. Remove the month from the "Active" table
2. Add to the "Historical" table:

```markdown
### Historical (in `runs/CLAUDE-RUNS-HISTORICAL/`)

| Month | File | Entries | Notes |
|-------|------|---------|-------|
| December 2025 | [ARCHIVE-2025-12.md](../CLAUDE-RUNS-HISTORICAL/2025-12/ARCHIVE-2025-12.md) | 32 | Moved YYYY-MM-DD |
| November 2025 | [ARCHIVE-2025-11.md](../CLAUDE-RUNS-HISTORICAL/2025-11/ARCHIVE-2025-11.md) | 7 | First archived month |
```

### Step 6: Check Parent CLAUDE.md

Search for any Active Tasks referencing moved directories:

```bash
grep -n "RUN-YYYYMM" ../../CLAUDE.md
```

If found, either:
- Update links to HISTORICAL location, OR
- Archive the task if marked "Ready for Review"

### Step 7: Verify

```bash
# Check moved files exist
ls runs/CLAUDE-RUNS-HISTORICAL/YYYY-MM/

# Check no old directories remain in source
ls runs/CLAUDE-RUNS/ | grep "RUN-YYYYMM" | wc -l  # Should be 0

# Test link resolution from ARCHIVE.md
cd runs/CLAUDE-RUNS
test -f "../CLAUDE-RUNS-HISTORICAL/YYYY-MM/ARCHIVE-YYYY-MM.md" && echo "Index link OK"

# Test link resolution within moved archive
cd ../CLAUDE-RUNS-HISTORICAL/YYYY-MM
test -d "./RUN-YYYYMMDD-HHMM-first-run-slug" && echo "Internal links OK"
```

---

## Link Pattern Reference

| Location | Old Pattern | New Pattern |
|----------|-------------|-------------|
| ARCHIVE-YYYY-MM.md (after move) | `` `runs/CLAUDE-RUNS/RUN-...` `` | `` `./RUN-...` `` |
| ARCHIVE.md index | `./ARCHIVE-YYYY-MM.md` | `../CLAUDE-RUNS-HISTORICAL/YYYY-MM/ARCHIVE-YYYY-MM.md` |
| Parent CLAUDE.md (if applicable) | `./runs/CLAUDE-RUNS/RUN-...` | `./runs/CLAUDE-RUNS-HISTORICAL/YYYY-MM/RUN-...` |

---

## Common Issues

### Orphan Active Tasks in Parent CLAUDE.md

If a parent `CLAUDE.md` has Active Tasks referencing moved directories:

1. **If "Ready for Review"**: Consider archiving the task entirely
2. **If "In Progress"**: Update links to HISTORICAL location (task may be stale)
3. **If directory doesn't exist**: Remove the orphan entry

### Legacy Directories (no RUN- prefix)

Early runs from November 2025 lack the `RUN-` prefix. Include them explicitly:

```bash
# These need separate move commands
mv 20251110-1031-sample-legacy-run ../CLAUDE-RUNS-HISTORICAL/2025-11/
```

### Partial Month Archives

If a month wasn't archived when it should have been, archive it now:

```bash
# Example: It's March 2026 and December 2025 wasn't archived in February
# Archive both November AND December if needed
```

---

## Month-Specific Notes

### November 2025 (Archived 2026-01-02)
- 15 directories (5 legacy without RUN- prefix)
- First month to use this archival system

### December 2025 (Archive by 2026-02-01)
- 52 directories (all have RUN- prefix)
- Highest activity month

---

## Example Session Log

```markdown
### 2026-02-01 - Monthly Archival

**Agent:** Claude Code
**Month Archived:** December 2025

**Pre-flight:**
- Current date: 2026-02-01
- Active window: January + February 2026
- Archive candidate: December 2025 (52 directories)

**Execution:**
1. Created CLAUDE-RUNS-HISTORICAL/2025-12/
2. Moved 52 RUN-202512* directories
3. Moved ARCHIVE-2025-12.md
4. Updated 32 links in archive file
5. Updated ARCHIVE.md index
6. Verified all links

**Issues:** None

**Time:** ~15 minutes
```

---

## Quick Reference Card

```
MONTHLY ARCHIVAL CHECKLIST
==========================
□ date "+%Y-%m-%d"                    # Verify date
□ mkdir -p HISTORICAL/YYYY-MM         # Create target
□ mv RUN-YYYYMM* HISTORICAL/YYYY-MM/  # Move directories
□ mv ARCHIVE-YYYY-MM.md HISTORICAL/   # Move archive file
□ sed -i 's|old|new|g' ARCHIVE-*.md   # Fix links
□ Edit ARCHIVE.md index               # Update tables
□ grep parent CLAUDE.md               # Check for orphans
□ ls / test -f / test -d              # Verify
```

---

*Created: 2026-01-02*
*Last updated: 2026-01-02*
