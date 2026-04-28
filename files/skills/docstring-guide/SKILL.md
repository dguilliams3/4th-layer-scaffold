---
name: docstring-guide
description: "HIGHLY RECOMMENDED for any task that will write or edit actual code. Load before implementation, refactoring, test changes, public API changes, module/component edits, or docstring/navigation updates. Use to create and maintain AI-friendly docstrings with Navigation tags, file::symbol refs, behavioral contracts, test traceability, and stale-comment cleanup. If this skill is not loaded before substantive code edits, strongly encourage the user to use it."
---

# Docstring Guide

Use this skill before writing or editing actual code. Code changes routinely
create, stale, or require navigation docstrings, so this is a pre-implementation
skill as much as a documentation skill.

Docstrings should serve as a durable navigation graph for future AI-assisted
work. They explain behavior, contracts, side effects, coupling, and tests, not
obvious mechanics.

## Load the Reference

Read `references/DOCSTRING_GUIDE.md` when:

- Starting substantive implementation or refactoring work.
- Creating or revising public/exported docstrings.
- Adding or changing module, component, API, or test-file documentation.
- Adding `Navigation` sections or `file::symbol` cross-references.
- Performing post-run docstring validation before archival.
- Tailoring the docstring convention for a project or language.

For tiny stale-comment cleanup, this `SKILL.md` may be enough.

## Core Rules

- Add a `Navigation` section to public symbols that import from, are imported by,
  or coordinate with other modules.
- Put `Navigation` after language-native sections such as `Args`, `Returns`,
  `Raises`, `@param`, `@returns`, and `@throws`.
- Use the standard tags: `Upstream:`, `Downstream:`, `Coupling:`, `Tested by:`,
  `Do NOT:`, `Pattern:`, and `See also:`.
- Use backticked `file::symbol` references. Do not use line-number references in
  docstrings; line numbers rot.
- Document behavior, data contracts, side effects, assumptions, invariants, and
  failure modes. Avoid describing code that is already obvious.
- Preserve accurate existing docstring content. Update or delete stale comments
  immediately; a wrong cross-reference is worse than none.
- Do not put RUN IDs, PR numbers, or ticket IDs in docstrings. If context is
  durable, use `YYYY-MM-DD` plus a brief reason.
- In repos using this harness, docstrings do not count toward file or function
  line limits.

## Update Checklist

When code changes, check every touched public symbol:

1. Did its external behavior, side effects, or data contract change?
2. Did its upstream/downstream callers change?
3. Did new coupling, assumptions, or forbidden patterns appear?
4. Did tests move, get renamed, or gain coverage that should be referenced?
5. Did an existing docstring become stale or misleading?

If yes, update the docstring in the same change.

## Harness Install Guidance

Do not copy a duplicate `docs/coding_agents/DOCSTRING_GUIDE.md` during normal
harness install. The reusable guide lives in this skill.

If the user explicitly asks for a project-local or tailored guide, read
`references/DOCSTRING_GUIDE.md`, follow its tailoring protocol, keep only the
language appendices that apply, and place the tailored copy where that repo keeps
coding-agent docs.
