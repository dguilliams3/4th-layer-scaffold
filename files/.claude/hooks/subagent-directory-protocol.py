#!/usr/bin/env python3
"""
Subagent directory protocol hook.
Injects working directory instructions for subagents to write findings to their own directory.

Runs AFTER subagent-context.py in the hook chain.
"""
import json
import sys

DIRECTORY_PROTOCOL = """
## Subagent Working Directory Protocol

You are a subagent. Your work products go in YOUR directory, not the main conversation context.

**Directory Assignment:**
- If your prompt specifies a working directory path → Use it exactly
- If NO directory specified → You MUST find the correct parent RUN directory:
  1. List `runs/CLAUDE-RUNS/` sorted by modification time (most recent first)
  2. Pick the most recent `RUN-*` directory whose name/timestamp plausibly matches your task
  3. Create your subagent dir inside it: `runs/CLAUDE-RUNS/RUN-XXXXXXXX-XXXX-<slug>/subagents/YYYYMMDD-HHMM-<task-slug>/`
  4. Get timestamp via `date +%Y%m%d-%H%M` command
  - **NEVER** create a bare `subagents/` directory at the top of `runs/CLAUDE-RUNS/` — this creates orphans
  - If no RUN directory seems to match, use the single most recent one

**Required Deliverable:**
Create `FINDINGS.md` in your directory with this structure:
```markdown
# [Task Description] - Findings

**Agent ID:** YYYYMMDD-HHMM-<slug>
**Created:** YYYY-MM-DD HH:MM EST
**Parent Task:** [from prompt if provided]
**Status:** Complete | In Progress | Blocked

## Summary
[2-3 sentence executive summary]

## Findings
[Your investigation results]

## Recommendations
[Actionable items for main thread]

## Files Examined
[List of files you looked at]
```

**Optional Files (in your directory):**
- Test scripts, SQL queries, debug output, intermediate data
- These help reproducibility but stay in YOUR directory

**Template Reference:** `skills/task-tracking/templates/FINDINGS.md` when the task-tracking
skill is installed project-local, or the global `task-tracking` skill's `templates/FINDINGS.md`.

---

"""

# Candidate field names for the subagent prompt
PROMPT_FIELDS = ["prompt", "description", "task", "instructions", "message"]


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_input = input_data.get("tool_input", {})

        # Find and modify the prompt field (append after existing content)
        modified = False
        for field in PROMPT_FIELDS:
            if field in tool_input and isinstance(tool_input[field], str):
                # Append directory protocol after existing prompt
                # (subagent-context.py already prepended Ms. Frizzle voice)
                tool_input[field] = tool_input[field] + DIRECTORY_PROTOCOL
                modified = True
                break

        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": (
                    "Directory protocol appended"
                    if modified
                    else "No prompt field found"
                ),
                "updatedInput": tool_input,
            }
        }

        print(json.dumps(output))

    except Exception as e:
        # Non-blocking error - let it through unmodified
        sys.stderr.write(f"Hook error (directory-protocol): {e}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
