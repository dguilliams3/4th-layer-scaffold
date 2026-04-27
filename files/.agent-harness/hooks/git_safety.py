"""Shared git safety checks for agent hook adapters."""
import re


BLOCKED_PATTERNS = [
    (
        re.compile(r"git\s+reset\s+.*--hard"),
        "git reset --hard destroys uncommitted work. Use git stash or ask the user first.",
    ),
    (
        re.compile(r"git\s+clean\s+.*-[a-zA-Z]*f"),
        "git clean -f permanently deletes untracked files. Ask the user before removing untracked files.",
    ),
    (
        re.compile(r"git\s+checkout\s+--\s+\."),
        "git checkout -- . discards all unstaged changes. Target specific files instead, or ask the user.",
    ),
    (
        re.compile(r"git\s+restore\s+\."),
        "git restore . discards all unstaged changes. Target specific files instead, or ask the user.",
    ),
]


def destructive_git_reason(command):
    """Return a block reason if command matches a destructive git pattern."""
    for pattern, reason in BLOCKED_PATTERNS:
        if pattern.search(command or ""):
            return reason
    return None
