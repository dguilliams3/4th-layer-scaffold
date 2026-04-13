# Post-Install Checklist

After the agent harness skill has copied its files, complete these steps.

---

## Step 1: Force-add tracked files through .gitignore

The `runs/` directory is gitignored (by design — run contents are local only).
But the scaffolding files need to be tracked. Force-add them:

```bash
git add -f runs/.gitkeep
git add -f runs/CLAUDE-RUNS/.gitkeep
git add -f runs/CLAUDE-RUNS/ARCHIVE.md
```

Verify they're staged:

```bash
git status
```

## Step 2: Verify skills are installed

Check that the `task-tracking` and `archive-run` skills are installed (global or project-local):

```bash
# If project-local:
ls skills/task-tracking/SKILL.md skills/archive-run/SKILL.md
# If global:
ls ~/.claude/skills/task-tracking/SKILL.md ~/.claude/skills/archive-run/SKILL.md
```

Make scripts executable:

```bash
# Adjust path based on where skills were installed
chmod +x skills/task-tracking/scripts/init-run.sh
chmod +x skills/archive-run/scripts/archive-run.sh
chmod +x skills/archive-run/scripts/metrics/*.sh
```

## Step 3: Set up ~/bin/agent (Cursor CLI — if using Cursor)

This is a one-time machine setup. Skip if already done.

The `~/bin/agent` script is a bash launcher that resolves the Cursor agent binary
and puts it in your PATH. Required for running Cursor as a subagent from Claude Code.

**Create `~/bin/agent`:**

```bash
#!/usr/bin/env bash
INSTALL_DIR="/c/Users/<YourUsername>/AppData/Local/cursor-agent"
export CURSOR_INVOKED_AS="${CURSOR_INVOKED_AS:-agent}"
export NODE_COMPILE_CACHE="${NODE_COMPILE_CACHE:-/c/Users/<YourUsername>/AppData/Local/cursor-compile-cache}"
latest="$(ls -1d "$INSTALL_DIR/versions/"[0-9]*.* 2>/dev/null \
  | sort -t. -k1,1rn -k2,2rn -k3,3rn \
  | head -1)"
if [[ -z "$latest" || ! -f "$latest/node.exe" || ! -f "$latest/index.js" ]]; then
  echo "ERROR: Cursor agent binary not found in $INSTALL_DIR/versions/" >&2; exit 1
fi
exec "$latest/node.exe" "$latest/index.js" "$@"
```

Make it executable and verify:

```bash
chmod +x ~/bin/agent
which agent  # Should show ~/bin/agent
agent -p "Say exactly: ready" --force --trust --model composer-2 --output-format text  # Smoke test
```

## Step 4: Integrate CLAUDE.md workflow section

The file `snippets/CLAUDE_MD_WORKFLOW.md` contains a slim workflow pointer section
ready to paste into CLAUDE.md. The full protocol lives in the `task-tracking` skill.

**If no CLAUDE.md exists:**

```bash
cp snippets/CLAUDE_MD_WORKFLOW.md CLAUDE.md
```

Then edit CLAUDE.md to add your project-specific sections (see `[TODO]` markers).

**If CLAUDE.md already exists:**
Open `snippets/CLAUDE_MD_WORKFLOW.md` and paste the relevant sections into your
existing CLAUDE.md. At minimum, paste:

- Task Execution Protocol (pointer to `task-tracking` skill)
- Active Tasks table
- Subagent Usage section

## Step 5: Configure settings.local.json

The file `files/.claude/settings-hooks-template.json` was copied to
`.claude/settings-hooks-template.json`. It contains only the hooks wiring.

**If no settings.local.json exists:**

```bash
cp .claude/settings-hooks-template.json .claude/settings.local.json
```

**If settings.local.json already exists:**
Merge the `"hooks"` key from the template into your existing file.
Do NOT overwrite your existing `permissions`, `enabledMcpjsonServers`, etc.

After merging, delete the template:

```bash
rm .claude/settings-hooks-template.json
```

## Step 6: Configure archive metrics

Copy the example config and uncomment the collectors relevant to your project:

```bash
cp skills/archive-run/scripts/archive-run.config.example .claude/archive-run.config
```

Edit `.claude/archive-run.config` to uncomment the collectors you want (python, node,
go, rust). The `git` collector is always enabled by default.

For code duplication (jscpd), see the `archive-run` skill for the recommended command
pattern with `--min-lines 5 --min-tokens 50` and repo-specific ignore patterns.

## Step 7: Customize documentation (fill in [TODO] markers)

Open these files and fill in the `[TODO]` sections with project-specific content:

1. `docs/coding_agents/MEMORY_OPTIMIZATION.md`
   - Replace `[your quick reference doc]` etc. with your actual doc names
   - Fill in Tier 1 constants (ports, import patterns, core rules)
   - Update decision trees with your actual file names
   - Add project-specific cached constants in Tip 2

2. `docs/coding_agents/SUBAGENT_GUIDE.md`
   - Replace the generic example in §3 with a project-relevant one
   - Update the "Last Updated" line

3. `CLAUDE.md` (after merging from snippets/CLAUDE_MD_WORKFLOW.md)
   - Fill all `[TODO: project-specific]` markers

## Step 8: Test the run infrastructure

```bash
# Adjust path based on where the skill was installed
skills/task-tracking/scripts/init-run.sh test-tent
```

Expected output:

```
✅ Created: runs/CLAUDE-RUNS/RUN-YYYYMMDD-HHMM-test-tent/
   TASK_LOG.md
   SPEC_v1.md
   HANDOFF.md (fill at completion)

Run ID: RUN-YYYYMMDD-HHMM
```

Verify all three files were created with substituted timestamps (not `{{RUN_ID}}` literals).

## Step 9: Verify hooks are wired

Open `.claude/settings.local.json` and confirm the `"hooks"` key is present with
the 7 hook commands.

Test by spawning a subagent — it should receive the context header and
the directory protocol automatically.

---

## You're done.

Your repo now has the 4th Layer Engineering workflow scaffolded:

- `task-tracking` skill — invoke to start a tracked run with `init-run.sh`
- `archive-run` skill — invoke to archive a completed run with metrics
- `.claude/hooks/` — 7 hooks enforcing agent protocol automatically
- `.claude/archive-run.config` — metric collectors for this project
- `docs/coding_agents/` — Subagent guide and context optimization strategies
- `snippets/CLAUDE_MD_WORKFLOW.md` — Slim pointer section for CLAUDE.md

First real run: invoke the `task-tracking` skill and give it your first task slug.
