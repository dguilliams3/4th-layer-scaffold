#!/usr/bin/env python3
"""
Post-edit linting hook.
Runs ruff and black on edited Python files.
"""
import json
import subprocess
import sys
import os


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_input = input_data.get('tool_input', {})
        
        # Get file path from tool input
        file_path = tool_input.get('file_path') or tool_input.get('filePath')
        
        if not file_path:
            sys.exit(0)
        
        # Only lint Python files
        if not file_path.endswith('.py'):
            sys.exit(0)
        
        if not os.path.exists(file_path):
            sys.exit(0)
        
        # Get project directory
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
        
        # Run ruff (fix mode, suppress errors)
        try:
            subprocess.run(
                ['poetry', 'run', 'ruff', 'check', '--fix', file_path],
                cwd=project_dir,
                capture_output=True,
                timeout=30
            )
        except Exception:
            pass
        
        # Run black (suppress errors)
        try:
            subprocess.run(
                ['poetry', 'run', 'black', file_path],
                cwd=project_dir,
                capture_output=True,
                timeout=30
            )
        except Exception:
            pass
        
    except Exception as e:
        # Never fail the hook
        sys.stderr.write(f"Lint hook error: {e}\n")
    
    sys.exit(0)


if __name__ == '__main__':
    main()
