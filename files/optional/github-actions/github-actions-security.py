#!/usr/bin/env python3
"""
Inject GitHub Actions security guidance when editing CI workflow files.
Reminds Claude to SHA-pin all actions instead of using mutable tags.

Triggers on: PreToolUse (Edit, Write)

Only fires for .yml/.yaml files under .github/.
"""
import json
import sys

GUIDANCE = """\
GITHUB ACTIONS SECURITY — Supply Chain Protection:

All GitHub Actions MUST be pinned by commit SHA, not tag. Tags are mutable — \
an attacker can force-push a tag to point at malicious code (e.g. TeamPCP/Trivy 2026-03-19).

Required format:
  WRONG:   uses: actions/checkout@v4
  CORRECT: uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4

When adding or updating a GitHub Action:
1. Find the commit SHA for the desired version tag
2. Use the full 40-character SHA in the uses: line
3. Add a trailing # vN comment for human readability\
"""


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_input = input_data.get("tool_input", {})

        file_path = tool_input.get("file_path") or tool_input.get("filePath", "")

        # Only fire for YAML files under .github/
        if not file_path:
            sys.exit(0)

        # Normalize separators
        normalized = file_path.replace("\\", "/")

        if "/.github/" not in normalized and not normalized.startswith(".github/"):
            sys.exit(0)

        if not (normalized.endswith(".yml") or normalized.endswith(".yaml")):
            sys.exit(0)

        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": GUIDANCE,
            }
        }
        print(json.dumps(output))

    except Exception as e:
        sys.stderr.write(f"Hook error (github-actions-security): {e}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
