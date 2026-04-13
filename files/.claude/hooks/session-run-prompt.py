#!/usr/bin/env python3
"""
Session startup hook: task-tracking protocol enforcement + active run detection.

Behavior:
    1. If .claude/task-tracking.disabled exists → exit silently (user opted out)
    2. Otherwise → inject task-tracking directive + any active/recent run context

The task-tracking protocol is OPT-OUT, not opt-in. This hook is the enforcement
muscle — it tells Claude to load the task-tracking skill for non-trivial work
and to ask the user if they want to opt out (not opt in).

Triggers on: SessionStart

Safety:
    - Only runs inside a git repo (exits cleanly otherwise)
    - Uses git rev-parse for repo root (works from any subdirectory)
    - Fast path: exits immediately if no CLAUDE.md
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


def get_repo_root():
    """Get git repo root, or None if not in a git repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return Path(result.stdout.strip())
    except Exception:
        pass
    return None


def parse_active_tasks(claude_md_path):
    """Extract active tasks from CLAUDE.local.md's Active Tasks table."""
    try:
        text = claude_md_path.read_text(encoding="utf-8")
    except Exception:
        return []

    # Find the Active Tasks section and parse table rows
    in_table = False
    tasks = []
    for line in text.splitlines():
        if "Active Tasks" in line and "#" in line:
            in_table = True
            continue
        if in_table:
            # Skip header row and separator
            if line.strip().startswith("|") and "Run ID" not in line and "---" not in line:
                cells = [c.strip() for c in line.split("|")[1:-1]]
                if len(cells) >= 3 and cells[0] and cells[0] != "(none)":
                    tasks.append({
                        "run_id": cells[0],
                        "description": cells[1] if len(cells) > 1 else "",
                        "status": cells[2] if len(cells) > 2 else "",
                    })
            # End of table
            elif not line.strip().startswith("|") and line.strip() and in_table and tasks:
                break
            elif line.strip().startswith("---") and not line.strip().startswith("| ---"):
                break

    return tasks


def find_recent_runs(runs_dir, hours=48):
    """Find RUN directories modified in the last N hours."""
    if not runs_dir.exists():
        return []

    cutoff = datetime.now() - timedelta(hours=hours)
    recent = []

    for entry in sorted(runs_dir.iterdir(), reverse=True):
        if not entry.is_dir() or not entry.name.startswith("RUN-"):
            continue

        # Check modification time of TASK_LOG.md if it exists
        task_log = entry / "TASK_LOG.md"
        check_path = task_log if task_log.exists() else entry

        try:
            mtime = datetime.fromtimestamp(check_path.stat().st_mtime)
            if mtime > cutoff:
                # Try to read status from TASK_LOG
                status = "Unknown"
                if task_log.exists():
                    try:
                        content = task_log.read_text(encoding="utf-8")
                        status_match = re.search(r"\*\*Status:\*\*\s*(.+)", content)
                        if status_match:
                            status = status_match.group(1).strip()
                    except Exception:
                        pass

                recent.append({
                    "name": entry.name,
                    "status": status,
                    "last_modified": mtime.strftime("%Y-%m-%d %H:%M"),
                })
        except Exception:
            continue

    return recent[:5]  # Cap at 5 most recent


def main():
    # Guard: only run inside a git repo
    repo_root = get_repo_root()
    if repo_root is None:
        sys.exit(0)

    claude_local = repo_root / "CLAUDE.local.md"
    runs_dir = repo_root / "runs" / "CLAUDE-RUNS"

    # OPT-OUT CHECK: if user has explicitly disabled task-tracking, exit silently
    disabled_file = repo_root / ".claude" / "task-tracking.disabled"
    if disabled_file.exists():
        sys.exit(0)

    # Fast path: no CLAUDE.local.md means no active tasks to check
    if not claude_local.exists():
        sys.exit(0)

    # Build context message
    parts = []

    # Task-tracking directive (always injected unless opted out)
    parts.append(
        "TASK-TRACKING PROTOCOL is enabled for this repo (opt-out, not opt-in).\n"
        "You MUST invoke the `task-tracking` skill before starting any non-trivial work.\n"
        "If the user is doing a quick one-off question or throwaway task, ask them:\n"
        "\"Want to skip task-tracking for this session?\"\n"
        "If they want to disable permanently for this repo: create .claude/task-tracking.disabled"
    )

    # Active tasks from CLAUDE.local.md
    active_tasks = parse_active_tasks(claude_local)
    if active_tasks:
        task_lines = []
        for t in active_tasks:
            task_lines.append(f"  - {t['run_id']}: {t['description']} [{t['status']}]")
        parts.append("ACTIVE TASKS in CLAUDE.local.md:\n" + "\n".join(task_lines))

    # Recent run directories
    recent_runs = find_recent_runs(runs_dir)
    if recent_runs:
        run_lines = []
        for r in recent_runs:
            run_lines.append(f"  - {r['name']} (status: {r['status']}, last active: {r['last_modified']})")
        parts.append("RECENT RUN DIRECTORIES (last 48h):\n" + "\n".join(run_lines))

    # If there are active tasks or recent runs, ask about resuming
    if active_tasks or recent_runs:
        parts.append(
            "Before starting work, ask the user: Are you continuing one of these runs, "
            "or would you like to start fresh? If continuing, re-read the relevant SPEC and TASK_LOG."
        )

    context = "SESSION START — Task-tracking check:\n" + "\n\n".join(parts)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
