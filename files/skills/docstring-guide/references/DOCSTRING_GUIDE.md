# Docstring & Navigation Guide

> **Code is Context.** Docstrings are the primary interface for AI-assisted
> development — they survive context compaction, power cross-project synthesis,
> and create a machine-parseable dependency graph over your codebase. Verbosity
> in navigation sections is intentional and non-negotiable. **Docstrings do NOT
> count toward file or function line limits.**

---

## How to Read This Guide

This guide has three parts:

| Part                                       | Applies to                                   | What to do when installing into a project                        |
| ------------------------------------------ | -------------------------------------------- | ---------------------------------------------------------------- |
| **Part I — Universal** (§1–§8)             | Every language, every project                | Keep verbatim. These are the invariants.                         |
| **Part II — Language Appendices** (§9–§10) | One or more specific languages               | Keep the appendix that matches the project. Delete the others.   |
| **Part III — Tailoring Protocol** (§11)    | The agent copying this guide into a new repo | Execute §11 once at copy-time, then delete §11 from the project copy. |

The **invention** this guide captures is the navigation-tag grammar in §3 —
`Upstream:`, `Downstream:`, `Coupling:`, `Tested by:`, `Do NOT:`, `Pattern:`,
`See also:` — plus the `` `file::symbol` `` cross-reference format. That is
language-agnostic. Everything else in Parts II–III is either syntax or
project-specific window-dressing.

---

# PART I — UNIVERSAL

These sections apply to every project in every language. Preserve verbatim when
tailoring. Customize only Part II (language) and Part III (project paths).

---

## §1 — Why This Exists: The Navigation Graph

Every docstring with cross-module references is a node in a typed graph:

- **Nodes** = exported symbols (functions, classes, methods, components, types, constants)
- **Edges** = navigation tags (`Upstream:`, `Downstream:`, `Coupling:`, etc.)
- **Anchors** = `` `file::symbol` `` cross-references

AI agents traverse this graph faster than they grep, because grep finds
occurrences but the graph carries **intent** — "this is the caller," "this is
the contract you must not break," "this is the known failure mode."

A repo with good navigation docstrings compounds: every new agent picks up
where the last one left off, without re-reading every file, because the graph
carries institutional knowledge forward.

A repo without navigation docstrings forces every agent to re-derive the
dependency graph from imports and grep — expensive, error-prone, and
non-transferable.

---

## §2 — Seven Principles

1. **Document behavior, not mechanics.** Explain side effects (DB writes, Kafka
   events, store mutations, network calls). Don't restate what the code
   obviously does.
2. **Keep comments close to code.** Prefer block docstrings on public symbols;
   reserve inline comments for genuinely non-obvious logic.
3. **Describe data contracts.** Clarify the shape of anything that crosses a
   module boundary: DB rows, API payloads, message schemas, store objects.
4. **Note assumptions.** E.g., "Assumes bearer token is set," "Caller must have
   acquired the lock," "Requires `ARTEMIS_DB_URL` env var."
5. **Update or delete stale comments immediately.** A wrong cross-reference is
   worse than none — it actively misleads future agents.
6. **Navigation is additive.** When enriching an existing docstring with a
   Navigation section, preserve all existing content. Add Navigation at the
   end, after language-native sections (Args/Returns/Raises or
   @param/@returns/@throws).
7. **No ticket IDs, RUN IDs, or PR numbers in docstrings.** They rot on contact.
   If a decision needs context, use `date (YYYY-MM-DD) + brief why`. E.g.,
   *"Switched from polling to WebSocket (2026-03-04) — polling caused 3x queue
   lag under load."*

---

## §3 — The Navigation Grammar

Every public symbol that imports from or is imported by other modules gets a
Navigation section with one or more of these tags.

### §3.1 — Tag Vocabulary

| Tag          | Purpose                                 | When Required                                         |
| ------------ | --------------------------------------- | ----------------------------------------------------- |
| `Upstream:`  | What calls or triggers this symbol      | Always for exports with cross-module callers          |
| `Downstream:`| What this symbol calls or delegates to  | Always for symbols that call into other modules       |
| `Coupling:`  | Files/symbols that must change together | When two files have a tight, hidden contract          |
| `Tested by:` | Path(s) to test file(s)                 | **Always when tests exist** (bidirectional — see §5) |
| `Do NOT:`    | Known failure mode or antipattern       | When a discovered mistake should not be repeated      |
| `Pattern:`   | Named convention being followed         | When following a project-specific pattern             |
| `See also:`  | Related code or documentation           | When relevant context lives elsewhere                 |

**Domain-extensible.** Projects can add their own tags. Examples from the field:

- `Models:` — pairs an API handler with its request/response models (FastAPI)
- `Schema:` — pairs a resolver with its GraphQL schema entry
- `CRD:` — pairs a Kubernetes controller with its Custom Resource Definition
- `Table:` — pairs a data-access method with its underlying DB table

Adopt what your repo needs. Document additions in the project's tailored copy.

### §3.2 — Cross-Reference Format: `file::symbol`

Always use `` `file::symbol` `` with backticks. Paths are relative to the
project root (or the language-conventional source root — see Part II).

```
`shared/core/database.py::get_connection`
`pwa/src/store/index.ts::fetchAndSet`
`internal/auth/session.go::ValidateToken`
```

**Rules:**
- `::` (double colon) separates file from symbol.
- Backticks around the whole reference for IDE/tooling highlighting.
- For methods: `file.ext::ClassName.method_name`.
- For module-level references with no specific symbol: `` `file.ext` `` (no `::`).

### §3.3 — Line Numbers Are Forbidden

**Never write `file.ext:123`.** Line numbers rot on the next edit. Symbol
names survive refactoring, renames tracked by every IDE, and grep. If a symbol
moves within a file, the reference still finds it. If a line moves, the
reference silently points at something unrelated.

### §3.4 — When NOT to Add Navigation

Navigation is valuable where it reduces cognitive load, not as ritual. Skip it for:

- **Private/unexported symbols** (names starting with `_` in Python, unexported
  in Go, `private` in TS/Java) — add only if coupling is non-obvious.
- **Trivial symbols** — barrel re-exports, simple constants, obvious wrappers.
- **Pure data types** — Pydantic models, dataclasses, TypeScript interfaces,
  Go structs whose fields are self-documenting.
- **Single-use helpers** — functions defined and consumed in the same file.
- **Generated code** — don't hand-edit; fix the generator instead.

---

## §4 — Module (File-Level) Docstrings

Every source file gets a module-level docstring at the top, before any imports
or code. This is the file's identity card.

### §4.1 — Required Content

| Section       | Purpose                                                                  |
| ------------- | ------------------------------------------------------------------------ |
| Summary line  | One sentence: what this file is                                          |
| Semantic hook | `MAIN ENTRY POINT`, `STABLE CONTRACT`, `PRESENTATIONAL`, etc. (see §6)   |
| `Used by:`    | Who imports or depends on this file (esp. for shared libraries)          |
| `See also:`   | Related files, docs, specs                                               |
| `Do NOT:`     | File-level antipatterns, architectural constraints                       |

### §4.2 — Why Module Docstrings Matter

Module docstrings are where the **architecture speaks**. Function-level
docstrings describe local behavior; module docstrings describe the role this
file plays in the larger system. When an agent lands in an unfamiliar file,
the module docstring is what tells them *why* it exists before they read
*what* it does.

---

## §5 — Test Traceability (Bidirectional)

Tests and source reference each other. This creates bidirectional navigation:
function → tests AND tests → function. Essential for coverage audits,
refactor impact analysis, and AI-assisted debugging.

**In the source file:** add `Tested by:` to the function's Navigation section.

**In the test file:** add a module docstring with `Tests:` referencing the
source as `` `file::symbol` ``.

### §5.1 — Rules

- Every function with tests gets a `Tested by:` tag.
- Every test file gets a module docstring with `Tests:` referencing source(s).
- When writing new tests, update BOTH source and test docstrings in the same
  commit. A one-sided reference is a stale reference waiting to happen.
- Multiple test files? List them all: `` Tested by: `foo.test.ts`, `foo.integration.test.ts` ``.

---

## §6 — Semantic Hooks for AI Discovery

Embed discoverable terms in docstrings to help AI agents locate critical code
by semantic search, not just grep. These are deliberately *branded* phrases —
grep-able, memorable, unambiguous.

### §6.1 — Common Hooks (starter set)

| Hook                | Meaning                                                                    |
| ------------------- | -------------------------------------------------------------------------- |
| `MAIN ENTRY POINT`  | Primary entry point for a subsystem (app factories, request routers, etc.) |
| `STABLE CONTRACT`   | Interface that external consumers depend on; change requires migration     |
| `PRESENTATIONAL`    | Pure display component, no side effects (UI)                               |
| `STORE-FIRST`       | Pattern: hook/handler writes to store; components read from store only     |
| `HOT PATH`          | Performance-critical code; optimize carefully, profile before changing     |
| `SECURITY BOUNDARY` | Code that enforces auth/authz/validation; changes require review           |

**Customize for your project.** Invent hooks that capture *your* architecture's
distinctive patterns. The value is in consistency within a project, not
standardization across projects. Document your project's hook vocabulary in
the tailored copy of this guide.

---

## §7 — Inline Comment Conventions

Inline comments explain **why**, never **what**. The code shows what; comments
exist only when a reader would otherwise be puzzled.

### §7.1 — Standard Prefixes

Use these prefixes for grep-able, high-signal comments:

- **`WORKAROUND:`** — temporary fix with context and removal condition.
  ```
  # WORKAROUND: psycopg2 doesn't support async context managers.
  # Remove when migrating to psycopg3 (tracked in backlog).
  ```

- **`DO NOT:`** — inline guard against a specific known antipattern.
  ```
  // DO NOT: Use f-strings for SQL — always use parameterized queries.
  ```

- **`SAFETY:`** — invariant that must hold; reader should not break it casually.
  ```
  // SAFETY: caller holds the mutex; release in finally block below.
  ```

### §7.2 — Avoid

- Comments that restate code (`// increment counter` above `counter++`)
- Comments referencing tickets/PRs (`// fixes JIRA-1234`) — see Principle 7
- Multi-paragraph comment blocks — move that content into the docstring

---

## §8 — Checklist Before Closing a Run

Before archiving any run that touched code:

- [ ] All new exported symbols have docstrings.
- [ ] Navigation sections added to any symbol with cross-module dependencies.
- [ ] Side effects, DB tables, API endpoints, queues/topics touched are mentioned.
- [ ] `Tested by:` references point to test files that exist (bidirectional verified).
- [ ] Removed/renamed symbols had their old docstrings deleted.
- [ ] `Do NOT:` tags added for any discovered failure modes.
- [ ] Cross-references use `file::symbol` format (not `file:linenum`).
- [ ] No ticket IDs or RUN IDs appear in any docstring.
- [ ] File-level module docstrings present on all new/modified files.
- [ ] Semantic hooks (§6) applied where appropriate.

---

# PART II — LANGUAGE APPENDICES

Keep the appendix (or appendices) that match your project's primary language(s).
Delete the rest.

---

## §9 — Appendix A: TypeScript / JSDoc

> **Keep this appendix if:** your project uses TypeScript (or JavaScript).
> Syntax uses JSDoc `/** */` blocks — recognized natively by TS/JS IDEs.

### §9.1 — Section Order Inside a JSDoc Block

```typescript
/**
 * [Summary line — one sentence]
 *
 * [Extended description — behavior, side effects, context]
 *
 * @param name - Description
 * @returns Description
 * @throws Description
 *
 * Upstream: `path/to/caller.ts::callerSymbol`
 * Downstream: `path/to/callee.ts::calleeSymbol`
 * Tested by: `path/to/test.test.ts`
 * Do NOT: [specific antipattern]
 */
export function someFunction(...) { ... }
```

### §9.2 — React Components

```typescript
/**
 * SectionCard renders a collapsible briefing section with severity indicators.
 * Uses CSS grid-template-rows for smooth expand/collapse animation.
 *
 * @param section - Briefing section data (key, label, content, severity)
 * @param defaultOpen - Whether section starts expanded
 *
 * Upstream: `pwa/src/components/TodayView.tsx::TodayView`
 * Downstream: `pwa/src/components/Markdown.tsx::Markdown`
 * Pattern: grid-collapse — `section-collapse` CSS with `data-open` attribute
 * Do NOT: Use conditional rendering (`{open && ...}`) — breaks collapse animation
 */
export function SectionCard({ section, defaultOpen }: Props) { ... }
```

### §9.3 — Store Actions (Zustand / Redux)

```typescript
/**
 * Triggers a new briefing generation via the API tunnel.
 * Polls for completion every 15s until a new briefing ID appears.
 *
 * Upstream: `pwa/src/components/AppHeader.tsx::AppHeader` — "New Briefing" button
 * Downstream: `pwa/src/api.ts::triggerBriefing`
 * Coupling: `pwa/src/store/index.ts::silentRefresh` — polling calls this
 * Do NOT: Call when `triggering` is already true — early-return guard exists
 * Do NOT: Reduce poll interval below 15s — tunnel latency makes faster polling wasteful
 */
async triggerBriefing() { ... }
```

### §9.4 — Types and Interfaces

Only document types when the name + fields aren't self-documenting, or when
there's a coupling constraint (DB schema, external API, cross-module contract).

```typescript
/**
 * Shape of a briefing list item returned by `GET /briefings`.
 * Intentionally lighter than full Briefing — no sections or sessionId.
 *
 * Coupling: `worker/src/routes/briefings.ts` — must match D1 query projection
 * See also: `pwa/src/types/briefing.ts::Briefing` — full object shape
 */
export interface BriefingListItem { ... }
```

### §9.5 — Named-Parameter (Options-Object) Convention

All exported functions use options objects for parameters, including
single-param functions. This makes call sites self-documenting at grep time:

```typescript
// YES — self-documenting at call site and in grep results:
fetchBriefingById({ id })
sendFollowUp({ sessionId, question })

// NO — positional args hide meaning:
fetchBriefingById(id)
sendFollowUp(sessionId, question)
```

**Exceptions:** React component props (already destructured), simple setters
(`setAuthToken(token)`), private/internal helpers where the function name
makes the parameter obvious.

### §9.6 — Required Tags by File Type (ILLUSTRATIVE)

Example from one production codebase. **Adapt for your repo** — a monorepo,
a single-page app, and a Worker-based edge project all have different
file-type archetypes.

| File Type                         | Required Tags                   |
| --------------------------------- | ------------------------------- |
| **Store** (`store/index.ts`)      | Upstream, Downstream, Do NOT, Pattern |
| **API client** (`api.ts`)         | Upstream, Downstream, Coupling   |
| **Worker routes** (`worker/src/`) | Upstream, Downstream, Do NOT    |
| **Components** (all `.tsx`)       | Upstream, Downstream, Do NOT (if known) |
| **Hooks** (`hooks/*.ts`)          | Upstream, Downstream, Pattern    |
| **Types** (`types/*.ts`)          | Coupling, See also              |
| **Scripts** (`scripts/`)          | Do NOT, See also                |

---

## §10 — Appendix B: Python / Google-style

> **Keep this appendix if:** your project uses Python. Syntax uses Google-style
> docstrings inside `""" """` triple-quoted strings.

### §10.1 — Section Order Inside a Google-style Docstring

```python
def execute_signal_run(request: SignalRequest) -> SignalResponse:
    """Execute a signal-driven analysis run.

    [Extended description — behavior, side effects, context.]

    Args:
        request: Signal request containing signal_id.

    Returns:
        SignalResponse with analysis and metadata.

    Raises:
        HTTPException: If signal_id is not found or config is invalid.

    Example:
        >>> response = execute_signal_run(SignalRequest(signal_id=42))
        >>> response.status
        'completed'

    Navigation:
        Upstream: `services/summary_agent/app/main.py` (FastAPI routing)
        Downstream: `shared/runconfig/runconfig_builder.py::build_run_config`
        Coupling: `shared/persistence/agent_output_writer.py::finalize_run`
            (must call on success — context manager handles failure)
        Tested by: tests/unit/api/v1/test_runs.py
        Do NOT: Pass week/plant filters in the request body — use env vars.
    """
```

### §10.2 — FastAPI Endpoint Handlers

Endpoint handlers MUST reference their request/response models via a `Models:` tag.

```python
@router.post("/execute", response_model=SignalResponse)
async def execute_signal_run(request: SignalRequest) -> SignalResponse:
    """Execute a signal run for the summary agent.

    Navigation:
        Upstream: `services/summary_agent/api/v1/router.py` (route registration)
        Downstream: `shared/runconfig/runconfig_builder.py::build_run_config`
        Models: `shared/api/signal_models.py::SignalRequest`, `SignalResponse`
        Tested by: tests/unit/api/v1/test_runs.py
    """
```

### §10.3 — Message Handlers (Kafka, SQS, etc.)

```python
async def execute_analysis(run_config: RunConfig) -> dict:
    """Handle a Kafka-triggered analysis execution.

    Navigation:
        Upstream: `shared/messaging/kafka_request_handler.py::create_kafka_request_handler`
            (factory that wires this into the Kafka consumer)
        Downstream: `services/analysis_agent/core/__init__.py::run_database_agent`
        Coupling: `shared/messaging/agent_events.py::AgentResponseEvent`
            (response published back to Kafka after execution)
        Do NOT: Call this directly — it's invoked by the Kafka consumer framework.
    """
```

### §10.4 — Factory Functions

Factories MUST document what they produce:

```python
def create_security_validator(config: dict) -> SecurityValidator:
    """Create a security validator for the summary agent.

    Navigation:
        Downstream: `SecurityValidator` (produced type)
        Upstream: `shared/core/app_factory.py::create_app`
        Pattern: factory-method — one factory per agent service
    """
```

### §10.5 — Classes

```python
class SummaryAgent:
    """Single-table analysis agent using smolagents.

    Manages LLM provider lifecycle, tool configuration, and schema-driven
    prompt assembly. Instantiated once at startup via `initialize_agent()`,
    retrieved per-request via `get_agent_instance()`.

    Navigation:
        Upstream: `services/summary_agent/api/v1/endpoints/runs.py::execute_signal_run`
        Upstream: `services/summary_agent/kafka/request_handler.py::execute_summary`
        Downstream: `shared/llm/factory.py::ProviderFactory`
        Coupling: `services/summary_agent/app/config.py::ServiceConfig`
            (reads settings for provider defaults and allowed tables)
        Tested by: tests/unit/core/test_agent.py
        Pattern: singleton-with-reset — single instance, reset between tests
    """
```

### §10.6 — Required Tags by File Type (ILLUSTRATIVE)

Example from one Python microservices codebase. **Adapt for your repo.**

| File Type                                 | Required Tags                        |
| ----------------------------------------- | ------------------------------------ |
| **Shared library** (`shared/**`)          | Upstream, Downstream, Do NOT         |
| **FastAPI endpoint** (`api/v*/endpoints/`) | Upstream, Downstream, Models, Tested by |
| **Kafka handler** (`*/kafka/`)            | Upstream, Downstream, Coupling, Do NOT |
| **Factory** (`*factory*.py`)              | Upstream, Downstream, Pattern        |
| **Agent core** (`*/core/agent.py`)        | Upstream, Downstream, Coupling, Tested by |
| **Pydantic models** (`*models*.py`)       | Coupling, See also                   |
| **DB access** (`*/persistence/`)          | Upstream, Table (custom), Do NOT     |

---

# PART III — TAILORING PROTOCOL

<!-- DELETE THIS ENTIRE PART III AFTER TAILORING THE PROJECT-LOCAL COPY -->

## §11 — Tailoring This Guide for a New Project

**Audience:** the Claude (or other AI agent) installing the 4th-layer harness
into a target repository. Run through this checklist once, then delete Part III
from the project-local copy. The scaffold retains the full multi-language
version; projects carry only what they need.

### §11.1 — Tailoring Steps

**Step 1 — Detect primary language(s).**
Check for language manifests in the target repo:

```bash
ls pyproject.toml setup.py requirements.txt         # → Python
ls package.json tsconfig.json                       # → TypeScript / JavaScript
ls go.mod                                           # → Go
ls Cargo.toml                                       # → Rust
ls pom.xml build.gradle                             # → Java / Kotlin
```

If the repo is polyglot (Python + TypeScript is common), ask the user which
languages are **primary**. Keep appendices for every primary language; delete
the rest.

**Step 2 — Delete non-matching appendices.**
A Python-only repo keeps §10 and deletes §9. A TS-only repo keeps §9 and
deletes §10. A polyglot repo keeps both. Leave a single line where deleted
appendices stood:

```markdown
<!-- TS appendix removed during tailoring (2026-04-17). See scaffold for reference. -->
```

**Step 3 — Replace path examples in the kept appendix(es).**
Run a lightweight survey of the target repo:

```bash
find . -maxdepth 3 -type d -not -path '*/node_modules/*' -not -path '*/.venv/*'
cat README.md | head -100
```

Then replace generic path stems in examples. For example, change:

- `services/summary_agent/...` → whatever the actual service path is
- `shared/runconfig/...` → wherever shared libs actually live
- `pwa/src/...` → the actual frontend root (might be `app/`, `client/`, `web/`)

The concepts in the examples stay the same; only the paths change.

**Step 4 — Preserve Part I (§1–§8) unchanged.**
These are the invariants. Do not paraphrase. Do not "improve." Consistency
across projects is the value proposition — if every team rewrites the
principles, the harness loses its coherence.

**Step 5 — Add project-specific domain tags to §3.1 if applicable.**
Examples:

- GraphQL project → add `Schema:` tag
- Kubernetes operators → add `CRD:` tag
- Data platforms → add `Table:` tag
- Event-sourced systems → add `Event:` tag

Document the addition in §3.1 of the project copy; update the file-type
required-tags table in §9.6 or §10.6 accordingly.

**Step 6 — Update §6 (Semantic Hooks) with project-specific hooks.**
The starter set (`MAIN ENTRY POINT`, `STABLE CONTRACT`, etc.) is useful. But
every mature codebase has its own branded patterns worth codifying as hooks.
Examples from real projects:

- `SAGA ORCHESTRATOR` (event-sourced systems)
- `FEATURE FLAG GATE` (gradual rollout heavy projects)
- `TENANT BOUNDARY` (multi-tenant SaaS)

**Step 7 — Link from the project's instruction-file Documentation Map.**
If you create a tailored project-local guide, add or update a row like:

```markdown
| "How do I write docstrings?" | [`<path-to-tailored-guide>`](<path-to-tailored-guide>) |
```

**Step 8 — Update the footer.**
At the bottom of the project copy, add:

```markdown
---
**Tailored for:** [project-name] — [language(s)]
**Tailored on:** YYYY-MM-DD
**Scaffold source:** 4th-layer-scaffold DOCSTRING_GUIDE.md (canonical)
```

**Step 9 — Delete Part III from the project copy.**
Once tailoring is complete, remove this entire section. It has no ongoing
value in the project — it exists only to guide the installation.

### §11.2 — When in Doubt, Ask

If you're unsure whether to keep an appendix, rename a semantic hook, or add
a custom tag, **ask the user**. This guide is load-bearing; getting the
tailoring wrong forces every future agent to work from broken documentation.
The cost of one clarifying question is trivial; the cost of a confidently
wrong guide is compounding.

### §11.3 — The Maxim

> **Distill in the scaffold. Tailor at the destination. Preserve the
> invariants. Customize the surface.**

The scaffold holds the canonical multi-language source so the invention is
never lost. The project-local copy holds only what that project needs so
working agents are never distracted. Both are correct — they serve different
audiences at different times.

---

**Last Updated:** 2026-04-17
**Scaffold source file.** When copied into a project, update the footer per §11.8.
