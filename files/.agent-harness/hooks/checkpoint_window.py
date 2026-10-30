"""Shared checkpoint-window reminder context for agent hook adapters.

Detects when the conversation is in a configurable token window approaching
context compaction. When triggered, returns an imperative reminder telling the
agent to STOP and write a CHECKPOINT-0N-<slug>.md immediately.

Mechanism:
    Reads the session's transcript JSONL (path passed in by the harness via
    the hook's stdin payload), finds the most recent assistant message, and
    sums its `usage.input_tokens` + `cache_creation_input_tokens` +
    `cache_read_input_tokens` from the API response metadata. Those three
    counts are separate and non-overlapping; their sum is the literal context
    size at the moment of that API call — i.e. exactly "how full is the
    context window right now." (input_tokens alone is only the uncached
    portion, which is small after a cache hit.) No estimation required.

Behavior:
    - If `input_tokens` is between the lower and upper thresholds, returns
      an imperative reminder string for the harness to inject as additional
      context on the next prompt.
    - Otherwise returns None (no reminder).
    - Suppresses the reminder if a checkpoint was written in the active run
      within the dedupe window (default: 5 minutes) — prevents spamming
      after the agent has already acted on a previous nudge.

Defaults:
    - Lower threshold: 900_000 tokens
    - Upper threshold: 920_000 tokens (no reminder above this — compaction
      is likely already triggered and the model is mid-summary)
    - Dedupe window: 300 seconds (5 minutes)

Override via env vars:
    - HARNESS_CHECKPOINT_LOWER
    - HARNESS_CHECKPOINT_UPPER
    - HARNESS_CHECKPOINT_DEDUPE_SECONDS
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


LOWER_DEFAULT = 900_000
UPPER_DEFAULT = 920_000
DEDUPE_SECONDS_DEFAULT = 300  # 5 minutes


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _repo_root() -> Optional[Path]:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (subprocess.SubprocessError, OSError):
        return None
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip())


def _latest_input_tokens(transcript_path: Optional[str]) -> Optional[int]:
    """Return the most recent assistant message's total context tokens.

    Sums the three non-overlapping counts the API reports in `message.usage`:
    `input_tokens` (the uncached portion) + `cache_creation_input_tokens` +
    `cache_read_input_tokens`. That sum is the literal context-window size at
    the moment of that API call; input_tokens alone undercounts because cached
    prefix tokens are billed separately.
    """
    if not transcript_path:
        return None
    path = Path(transcript_path)
    if not path.is_file():
        return None
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return None
    for line in reversed(lines):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        msg = obj.get("message", {})
        if not isinstance(msg, dict):
            continue
        if msg.get("role") != "assistant":
            continue
        usage = msg.get("usage", {})
        if not isinstance(usage, dict):
            continue
        toks = usage.get("input_tokens")
        if not isinstance(toks, int) or toks <= 0:
            continue
        total = toks
        for k in ("cache_creation_input_tokens", "cache_read_input_tokens"):
            v = usage.get(k)
            if isinstance(v, int) and v > 0:
                total += v
        return total
    return None


def _in_progress_run_ids(repo_root: Path) -> set:
    """Run IDs (RUN-YYYYMMDD-HHMM) marked in-progress in the Active Tasks tables.

    Scans CLAUDE.local.md (per-machine) then CLAUDE.md for lines that mention a
    run ID alongside an "in progress" / "active" status, so dedupe can target the
    run the user is actually working in rather than whichever RUN-* dir happens
    to have the newest mtime. Returns an empty set if neither file is readable or
    nothing matches (callers fall back to newest-by-mtime).
    """
    ids: set = set()
    for name in ("CLAUDE.local.md", "CLAUDE.md"):
        path = repo_root / name
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line in text.splitlines():
            if not re.search(r"in\s*progress|active", line, re.IGNORECASE):
                continue
            ids.update(re.findall(r"RUN-\d{8}-\d{4}", line))
    return ids


def _active_run(repo_root: Path) -> Optional[Path]:
    """Return the active RUN-* dir under runs/CLAUDE-RUNS/ (modified within 7 days).

    Prefers the newest run that Active Tasks (CLAUDE.local.md / CLAUDE.md) marks
    in-progress, so dedupe follows the run the user is working in rather than
    whichever directory has the newest mtime. Falls back to newest-by-mtime when
    Active Tasks lists nothing matching.
    """
    runs_dir = repo_root / "runs" / "CLAUDE-RUNS"
    if not runs_dir.is_dir():
        return None
    candidates = []
    try:
        for entry in runs_dir.iterdir():
            if not entry.is_dir() or not entry.name.startswith("RUN-"):
                continue
            try:
                candidates.append((entry.stat().st_mtime, entry))
            except OSError:
                continue
    except OSError:
        return None
    if not candidates:
        return None
    candidates.sort(reverse=True)

    fresh = 7 * 86400
    in_progress = _in_progress_run_ids(repo_root)
    if in_progress:
        for mtime, entry in candidates:
            if (time.time() - mtime) > fresh:
                continue
            if any(entry.name.startswith(run_id) for run_id in in_progress):
                return entry

    newest_mtime, newest = candidates[0]
    # Fallback: only consider it "active" if modified within last 7 days
    if (time.time() - newest_mtime) > fresh:
        return None
    return newest


def _last_checkpoint_info(run_dir: Path) -> Tuple[Optional[str], Optional[float]]:
    """Return (filename, mtime) for the newest checkpoint in this run, else (None, None)."""
    cp_dir = run_dir / "checkpoints"
    if not cp_dir.is_dir():
        return None, None
    cps = []
    try:
        for entry in cp_dir.iterdir():
            if not entry.is_file() or not entry.name.startswith("CHECKPOINT-"):
                continue
            try:
                cps.append((entry.stat().st_mtime, entry.name))
            except OSError:
                continue
    except OSError:
        return None, None
    if not cps:
        return None, None
    cps.sort(reverse=True)
    mtime, name = cps[0]
    return name, mtime


def _local_timestamp() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")


def _checkpoint_script_path(repo_root: Path) -> str:
    """Repo-relative path to checkpoint.sh for whichever skill layout exists here.

    The checkpoint skill is vendored under .claude/skills/ and/or .codex/skills/,
    not a generic files/skills/ path. Return whichever is present so the reminder
    points agents at a path that actually exists in this repo.
    """
    for prefix in (".claude", ".codex"):
        rel = f"{prefix}/skills/checkpoint/scripts/checkpoint.sh"
        if (repo_root / rel).is_file():
            return rel
    return ".claude/skills/checkpoint/scripts/checkpoint.sh"


def checkpoint_window_context(transcript_path: Optional[str] = None) -> Optional[str]:
    """Return imperative reminder text if context is in the warning window, else None."""
    lower = _env_int("HARNESS_CHECKPOINT_LOWER", LOWER_DEFAULT)
    upper = _env_int("HARNESS_CHECKPOINT_UPPER", UPPER_DEFAULT)
    dedupe_secs = _env_int("HARNESS_CHECKPOINT_DEDUPE_SECONDS", DEDUPE_SECONDS_DEFAULT)

    tokens = _latest_input_tokens(transcript_path)
    if tokens is None or not (lower <= tokens <= upper):
        return None

    repo = _repo_root()
    if repo is None:
        return None

    script_path = _checkpoint_script_path(repo)
    run_dir = _active_run(repo)
    last_cp_name: Optional[str] = None
    last_cp_mtime: Optional[float] = None
    if run_dir is not None:
        last_cp_name, last_cp_mtime = _last_checkpoint_info(run_dir)

    # Dedupe: suppress if a checkpoint was written recently
    if last_cp_mtime is not None and dedupe_secs > 0:
        if (time.time() - last_cp_mtime) < dedupe_secs:
            return None

    run_label = (
        run_dir.name
        if run_dir is not None
        else "(no active run detected in last 7 days)"
    )
    last_cp_str = last_cp_name if last_cp_name else "(none in this run yet)"
    tokens_k = tokens / 1000
    lower_k = lower // 1000
    upper_k = upper // 1000

    return (
        f"🛑 **CHECKPOINT REQUIRED — context at ~{tokens_k:.0f}K / 1M tokens "
        f"(in compaction window {lower_k}K–{upper_k}K).**\n\n"
        f"If you are currently working in a RUN, STOP everything else and write a "
        f"CHECKPOINT-0N-<slug>.md immediately. Compaction will strip your working "
        f"memory soon — write the trail now while you still have the context to do so.\n\n"
        f"- Detected active run: `{run_label}`\n"
        f"- Last checkpoint in this run: `{last_cp_str}`\n"
        f"- Current local time: {_local_timestamp()}\n\n"
        f"Steps:\n"
        f"1. Run: `bash {script_path} <short-descriptive-slug>` "
        f"(slug captures what's in your working memory right now).\n"
        f"2. Use the Read tool on the new file path — Claude Code rejects Edit without prior Read.\n"
        f"3. Edit to fill every section. Default style: verbose and comprehensive — "
        f"over-explain rather than under-explain. The reader is post-compact-you.\n\n"
        f"If you are NOT in an active run, ignore this reminder."
    )
