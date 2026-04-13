#!/usr/bin/env python3
"""
Post-edit function length check.
After editing a Python source file, checks if any functions exceed 50 LOC
and injects a warning into Claude's context.

Triggers on: PostToolUse (Edit, Write)

Uses AST parsing for accurate function detection (not regex line counting).
Only checks the edited file, not the whole codebase.
Skips test files — test functions are often long by nature (setup + assertions).
"""
import ast
import json
import sys
import os

MAX_FUNCTION_LINES = 50

# Skip test files — test functions can be legitimately long
SKIP_PATH_PATTERNS = ['tests/', 'test_', 'conftest.py']


def get_long_functions(file_path, max_lines=MAX_FUNCTION_LINES):
    """Parse a Python file and return functions exceeding max_lines."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()

        tree = ast.parse(source, filename=file_path)
    except (SyntaxError, FileNotFoundError, UnicodeDecodeError):
        return []

    long_functions = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Calculate function length from first to last line
            if hasattr(node, 'end_lineno') and node.end_lineno:
                length = node.end_lineno - node.lineno + 1
                if length > max_lines:
                    long_functions.append({
                        'name': node.name,
                        'line': node.lineno,
                        'length': length,
                    })

    return long_functions


def main():
    try:
        input_data = json.load(sys.stdin)

        # PostToolUse gets tool_input (what was requested) and tool_response
        tool_input = input_data.get('tool_input', {})
        tool_response = input_data.get('tool_response', {})

        # Get file path from tool input or response
        file_path = (
            tool_input.get('file_path')
            or tool_input.get('filePath')
            or tool_response.get('filePath')
            or ''
        )

        if not file_path or not file_path.endswith('.py'):
            sys.exit(0)

        if not os.path.exists(file_path):
            sys.exit(0)

        # Skip test files
        for skip in SKIP_PATH_PATTERNS:
            if skip in file_path:
                sys.exit(0)

        long_functions = get_long_functions(file_path)

        if not long_functions:
            sys.exit(0)

        # Build warning message
        warnings = []
        for func in long_functions:
            warnings.append(
                f"  - {func['name']}() at line {func['line']}: "
                f"{func['length']} lines (limit: {MAX_FUNCTION_LINES})"
            )

        basename = os.path.basename(file_path)
        message = (
            f"Function length warning in {basename}:\n"
            + "\n".join(warnings)
            + "\nConsider extracting helpers to keep functions under "
            + f"{MAX_FUNCTION_LINES} LOC."
        )

        output = {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": message,
            }
        }
        print(json.dumps(output))

    except Exception as e:
        sys.stderr.write(f"Hook error (post-edit-length-check): {e}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
