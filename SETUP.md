# Post-Install Checklist

After the 4th-layer-agent-harness skill has copied its files, complete these steps.

---

## Step 1: Force-add tracked files through .gitignore

The `runs/` directory is gitignored (by design — run contents are local only).
But the scaffolding files need to be tracked. Force-add them:

```bash
git add -f runs/.gitkeep
git add -f runs/CLAUDE-RUNS/.gitkeep
git add -f runs/CLAUDE-RUNS/ARCHIVE.template.md
# Do NOT force-add ARCHIVE.md — it is intentionally gitignored (per-dev archive log)
```

Also create the local working archive if it does not exist:

```bash
cp runs/CLAUDE-RUNS/ARCHIVE.template.md runs/CLAUDE-RUNS/ARCHIVE.md
```

Verify they're staged:
```bash
git status
```

Do not stage `CLAUDE.local.md`. It is per-machine runtime state and should remain
present locally but ignored by git.

Do not stage `AGENTS.local.md` either when installing Codex support.

## Step 2: Verify skills are installed

Check that skills are installed globally unless the user explicitly requested
project-local skills:

```bash
# Claude Code global default:
ls \
  ~/.claude/skills/task-tracking/SKILL.md \
  ~/.claude/skills/context-loading/SKILL.md \
  ~/.claude/skills/docstring-guide/SKILL.md \
  ~/.claude/skills/archive-run/SKILL.md \
  ~/.claude/skills/subagent-management/SKILL.md \
  ~/.claude/skills/codex-subagent/SKILL.md \
  ~/.claude/skills/cursor-subagent/SKILL.md \
  ~/.claude/skills/gemini-subagent/SKILL.md \
  ~/.claude/skills/adversarial-review/SKILL.md \
  ~/.claude/skills/council-guide/SKILL.md
```

If project-local Claude skills were explicitly requested, also verify:

```bash
ls \
  skills/task-tracking/SKILL.md \
  skills/context-loading/SKILL.md \
  skills/docstring-guide/SKILL.md \
  skills/archive-run/SKILL.md \
  skills/subagent-management/SKILL.md \
  skills/codex-subagent/SKILL.md \
  skills/cursor-subagent/SKILL.md \
  skills/gemini-subagent/SKILL.md \
  skills/adversarial-review/SKILL.md \
  skills/council-guide/SKILL.md
```

Make scripts executable:
```bash
# Claude Code global default:
chmod +x ~/.claude/skills/task-tracking/scripts/init-run.sh
chmod +x ~/.claude/skills/archive-run/scripts/archive-run.sh
chmod +x ~/.claude/skills/archive-run/scripts/metrics/*.sh
```

If project-local Claude skills were explicitly requested:

```bash
chmod +x skills/task-tracking/scripts/init-run.sh
chmod +x skills/archive-run/scripts/archive-run.sh
chmod +x skills/archive-run/scripts/metrics/*.sh
```

For Codex, verify the same skills are discoverable globally under
`~/.agents/skills/` unless the user explicitly requested project-local Codex skills:

```bash
# Codex global default:
ls \
  ~/.agents/skills/task-tracking/SKILL.md \
  ~/.agents/skills/context-loading/SKILL.md \
  ~/.agents/skills/docstring-guide/SKILL.md \
  ~/.agents/skills/archive-run/SKILL.md \
  ~/.agents/skills/subagent-management/SKILL.md \
  ~/.agents/skills/codex-subagent/SKILL.md \
  ~/.agents/skills/cursor-subagent/SKILL.md \
  ~/.agents/skills/gemini-subagent/SKILL.md \
  ~/.agents/skills/adversarial-review/SKILL.md \
  ~/.agents/skills/council-guide/SKILL.md
```

If project-local Codex skills were explicitly requested, also verify:

```bash
ls \
  .agents/skills/task-tracking/SKILL.md \
  .agents/skills/context-loading/SKILL.md \
  .agents/skills/docstring-guide/SKILL.md \
  .agents/skills/archive-run/SKILL.md \
  .agents/skills/subagent-management/SKILL.md \
  .agents/skills/codex-subagent/SKILL.md \
  .agents/skills/cursor-subagent/SKILL.md \
  .agents/skills/gemini-subagent/SKILL.md \
  .agents/skills/adversarial-review/SKILL.md \
  .agents/skills/council-guide/SKILL.md
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
- Subagent Usage section

Verify `CLAUDE.local.md` exists in the repo root. If the target repo did not already
have one, it should have been copied from the harness template at `files/CLAUDE.local.md`.
Confirm `.gitignore` includes `/CLAUDE.local.md` and do not commit it.

If using Codex, integrate `snippets/AGENTS_MD_WORKFLOW.md` into `AGENTS.md` the same
way. Verify `AGENTS.local.md` exists in the repo root, copy it from
`files/AGENTS.local.md` if missing, and confirm `.gitignore` includes
`/AGENTS.local.md`. Codex does not auto-load `AGENTS.local.md`; the harness
`SessionStart` hook reads it when Codex hooks are enabled.

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

Verify shared hook support was copied:

```bash
ls .agent-harness/hooks/git_safety.py .agent-harness/hooks/run_state.py .agent-harness/hooks/task_log.py
```

## Step 5b: Configure Codex hooks

If using Codex, verify these files exist:

```bash
ls .codex/hooks.json
ls .codex/hooks/block-destructive-git.py .codex/hooks/session-run-prompt.py .codex/hooks/task-log-reminder.py
```

Merge `.codex/config-hooks-template.toml` into `.codex/config.toml` without
overwriting other Codex settings:

```toml
[features]
codex_hooks = true
```

After merging, delete the template:

```bash
rm .codex/config-hooks-template.toml
```

Restart Codex if hooks or newly installed skills do not appear active.
Project-local hooks load only when Codex trusts the project `.codex/` config
layer; if Codex prompts about trust, review the hook scripts before accepting.

## Step 6: Configure archive metrics

Copy the example config and uncomment the collectors relevant to your project:

```bash
cp ~/.claude/skills/archive-run/scripts/archive-run.config.example .claude/archive-run.config
```

If the user explicitly requested project-local Claude skills, use
`skills/archive-run/scripts/archive-run.config.example` instead.

Edit `.claude/archive-run.config` to uncomment the collectors you want (python, node,
go, rust). The `git` collector is always enabled by default.

For code duplication (jscpd), see the `archive-run` skill for the recommended command
pattern with `--min-lines 5 --min-tokens 50` and repo-specific ignore patterns.

## Step 7: Customize repo instruction files

The former `docs/coding_agents/` workflow docs now live in skills. Customize
`CLAUDE.md` and/or `AGENTS.md` after merging the workflow snippets, and keep
project-specific context loading, docstring, or subagent notes in those
instruction files only when the repo needs them.

## Step 8: Test the run infrastructure

```bash
# Claude Code global default:
~/.claude/skills/task-tracking/scripts/init-run.sh test-tent
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

For Codex global skills, use:

```bash
~/.agents/skills/task-tracking/scripts/init-run.sh test-tent
```

If the user explicitly requested project-local skills, use the project-local path
for that runtime:

```bash
skills/task-tracking/scripts/init-run.sh test-tent
.agents/skills/task-tracking/scripts/init-run.sh test-tent
```

## Step 9: Verify hooks are wired

Open `.claude/settings.local.json` and confirm the `"hooks"` key is present with
the 7 hook commands.

Test by spawning a subagent — it should receive the context header and
the directory protocol automatically.

For Codex, open `.codex/hooks.json` and confirm the three hook commands are present.
Confirm `.agent-harness/hooks/` exists, since the Codex hook scripts import shared
logic from there. Also confirm `.codex/config.toml` or another active Codex config
layer enables:

```toml
[features]
codex_hooks = true
```

Codex hook coverage is intentionally narrower than Claude Code: the scaffold ports
git safety, session continuity, and task-log reminders. Claude hooks that mutate
subagent prompts are not ported because Codex hooks currently do not support that
same input-rewriting behavior.

---

## You're done.

Your repo now has the 4th Layer Engineering workflow scaffolded:

- `task-tracking` skill — invoke to start a tracked run with `init-run.sh`
- `context-loading` skill — load at session start, after compaction, or before broad repo/doc reading
- `docstring-guide` skill — load before any task that writes or edits actual code
- `archive-run` skill — invoke to archive a completed run with metrics
- `subagent-management` skill — use before delegating or integrating subagent work
- `.claude/hooks/` — 7 hooks enforcing agent protocol automatically
- `.codex/hooks/` — 3 Codex-compatible guardrail/context hooks
- `.claude/archive-run.config` — metric collectors for this project
- `snippets/CLAUDE_MD_WORKFLOW.md` — Slim pointer section for CLAUDE.md
- `snippets/AGENTS_MD_WORKFLOW.md` — Slim pointer section for Codex AGENTS.md

First real run: invoke the `task-tracking` skill and give it your first task slug.
