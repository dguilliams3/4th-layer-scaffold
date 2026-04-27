#!/usr/bin/env python3
"""Codex adapter for shared session run-state context."""
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
        return None
    repo_root = Path(result.stdout.strip())
    sys.path.insert(0, str(repo_root / ".agent-harness"))
    return repo_root


def main():
    try:
        repo_root = add_shared_hooks_to_path()
        if repo_root is None:
            sys.exit(0)

        from hooks.run_state import build_session_context

        context = build_session_context(
            repo_root=repo_root,
            runtime_name="Codex",
            local_state_names=["AGENTS.local.md", "CLAUDE.local.md"],
            disabled_paths=[
                Path(".codex/task-tracking.disabled"),
                Path(".claude/task-tracking.disabled"),
            ],
            skill_reference="`$task-tracking`",
            disable_instruction=(
                "To disable for Codex in this repo, create `.codex/task-tracking.disabled`."
            ),
            require_local_state=False,
        )
        if context is None:
            sys.exit(0)

        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            }
        }))
    except Exception as e:
        sys.stderr.write(f"Hook error (codex session-run-prompt): {e}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
