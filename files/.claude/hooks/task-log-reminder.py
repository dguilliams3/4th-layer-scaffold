#!/usr/bin/env python3
"""
Task log reminder hook.
Injects the user's current local date/time and a gentle nudge to update TASK_LOG.md.

Triggers on: UserPromptSubmit
"""
import json
import sys
from datetime import datetime


def get_local_timestamp():
    """Get current local time with timezone abbreviation. Pure stdlib, cross-platform."""
    now = datetime.now().astimezone()
    return now.strftime("%Y-%m-%d %H:%M %Z")


REMINDER = """If you are in an active run, consider whether you have updated TASK_LOG.md with your recent action(s)."""


def main():
    try:
        timestamp = get_local_timestamp()
        context = f"Current user local time: {timestamp}\n{REMINDER}"

        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context,
            }
        }
        print(json.dumps(output))

    except Exception as e:
        sys.stderr.write(f"Hook error (task-log-reminder): {e}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
