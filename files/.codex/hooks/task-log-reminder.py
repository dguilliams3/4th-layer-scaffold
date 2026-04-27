#!/usr/bin/env python3
"""Codex adapter for shared TASK_LOG reminder context."""
import json
import subprocess
import sys
from pathlib import Path


def add_shared_hooks_to_path():
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        return False
    repo_root = Path(result.stdout.strip())
    sys.path.insert(0, str(repo_root / ".agent-harness"))
    return True


def main():
    try:
        if not add_shared_hooks_to_path():
            sys.exit(0)

        from hooks.task_log import task_log_context

        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": task_log_context(),
            }
        }))
    except Exception as e:
        sys.stderr.write(f"Hook error (codex task-log-reminder): {e}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
