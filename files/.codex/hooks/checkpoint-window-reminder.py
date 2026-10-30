#!/usr/bin/env python3
"""Codex adapter for shared checkpoint-window reminder context.

Fires on UserPromptSubmit. When the conversation's context is in the
configured warning window (default 900K-920K of 1M), injects an imperative
reminder telling the agent to stop and write a CHECKPOINT-0N-<slug>.md before
the imminent compaction strips working memory.
"""
import json
import subprocess
import sys
from pathlib import Path


def add_shared_hooks_to_path() -> bool:
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

        from hooks.checkpoint_window import checkpoint_window_context

        try:
            input_data = json.load(sys.stdin)
        except json.JSONDecodeError:
            input_data = {}

        transcript_path = input_data.get("transcript_path")
        reminder = checkpoint_window_context(transcript_path)
        if not reminder:
            sys.exit(0)

        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": reminder,
            }
        }))
    except Exception as e:
        # Non-blocking — never let a hook error crash the prompt cycle.
        sys.stderr.write(f"Hook error (codex checkpoint-window-reminder): {e}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
