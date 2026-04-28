"""Shared task log reminder context for agent hook adapters."""
from datetime import datetime


def local_timestamp():
    """Get current local time with timezone abbreviation."""
    now = datetime.now().astimezone()
    return now.strftime("%Y-%m-%d %H:%M %Z")


def task_log_context():
    """Return reminder text injected on user prompt submission."""
    return (
        f"Current user local time: {local_timestamp()}\n"
        "If you are in an active harness run, consider whether TASK_LOG.md "
        "needs an update before proceeding."
    )
