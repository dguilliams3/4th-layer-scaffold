"""Shared run-state discovery for agent hook adapters."""
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path


def get_repo_root():
    """Get git repo root, or None if not inside a git repository."""
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


def parse_active_tasks(local_state_path):
    """Extract active tasks from a local runtime-state Active Tasks table."""
    try:
        text = local_state_path.read_text(encoding="utf-8")
    except Exception:
        return []

    in_table = False
    tasks = []
    for line in text.splitlines():
        if "Active Tasks" in line and "#" in line:
            in_table = True
            continue
        if not in_table:
            continue

        if line.strip().startswith("|") and "Run ID" not in line and "---" not in line:
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 3 and cells[0] and cells[0] != "(none)":
                tasks.append({
                    "run_id": cells[0],
                    "description": cells[1] if len(cells) > 1 else "",
                    "status": cells[2] if len(cells) > 2 else "",
                })
        elif not line.strip().startswith("|") and line.strip() and tasks:
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

        task_log = entry / "TASK_LOG.md"
        check_path = task_log if task_log.exists() else entry

        try:
            mtime = datetime.fromtimestamp(check_path.stat().st_mtime)
            if mtime <= cutoff:
                continue

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

    return recent[:5]


def first_existing(root, relative_paths):
    """Return the first existing path from a list of repo-relative paths."""
    for relative_path in relative_paths:
        candidate = root / relative_path
        if candidate.exists():
            return candidate
    return None


def build_session_context(
    repo_root,
    runtime_name,
    local_state_names,
    disabled_paths,
    skill_reference,
    disable_instruction,
    require_local_state=False,
):
    """Build session-start context, or None when disabled/not applicable."""
    if any((repo_root / path).exists() for path in disabled_paths):
        return None

    local_state = first_existing(repo_root, [Path(name) for name in local_state_names])
    if require_local_state and local_state is None:
        return None

    runs_dir = repo_root / "runs" / "CLAUDE-RUNS"
    active_tasks = parse_active_tasks(local_state) if local_state is not None else []
    recent_runs = find_recent_runs(runs_dir)

    parts = [
        "TASK-TRACKING PROTOCOL is enabled for this repo when using the 4th Layer agent harness.\n"
        f"For non-trivial work, invoke {skill_reference} if available or create a tracked run manually.\n"
        "If this is a quick one-off question, ask whether the user wants to skip run tracking.\n"
        f"{disable_instruction}"
    ]

    if active_tasks:
        lines = [
            f"  - {task['run_id']}: {task['description']} [{task['status']}]"
            for task in active_tasks
        ]
        parts.append(f"ACTIVE TASKS in {local_state.name}:\n" + "\n".join(lines))

    if recent_runs:
        lines = [
            f"  - {run['name']} (status: {run['status']}, last active: {run['last_modified']})"
            for run in recent_runs
        ]
        parts.append("RECENT RUN DIRECTORIES (last 48h):\n" + "\n".join(lines))

    if active_tasks or recent_runs:
        parts.append(
            "Before starting work, ask whether the user is continuing one of these runs "
            "or starting fresh. If continuing, re-read the relevant SPEC and TASK_LOG."
        )

    return f"SESSION START - 4th Layer harness check ({runtime_name}):\n" + "\n\n".join(parts)
