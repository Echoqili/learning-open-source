---
name: "devlog"
description: "Maintains a per-project DEVLOG.md with change history, plans, and lessons learned. Invoke when starting a coding task, completing work, making architectural decisions, or fixing tricky bugs."
---

# DEVLOG Skill

## Purpose

Maintain a per-project `DEVLOG.md` that records:

- What changed and why
- Planned / upcoming work
- Lessons learned (gotchas, patterns, library quirks)

The file is **local-only** — it must never reach the remote repository, and the
ignore rule for it must not be committed either. This is achieved with
`.git/info/exclude` (a Git-controlled, never-tracked file), **not** `.gitignore`.

## When to Invoke

Invoke this skill when any of the following happen:

- Starting a new coding task in a project (initialize or refresh the log)
- Completing a coding task or a significant sub-step
- Making an architectural or design decision
- Fixing a tricky bug
- Discovering a library / framework gotcha
- User says things like "log this", "记一下", "记到日志里", "记录到 DEVLOG"

## First-Run Setup (idempotent)

When `DEVLOG.md` is missing in the project root:

1. Create it from the **Template** section below.
2. Make sure `DEVLOG.md` is locally ignored, **without** touching `.gitignore`:
   - Append a rule to `.git/info/exclude`:
     - `Add-Content .git/info/exclude 'DEVLOG.md'` (PowerShell)
     - or: `printf '%s\n' 'DEVLOG.md' >> .git/info/exclude` (POSIX)
3. Verify with: `git check-ignore -v -- DEVLOG.md`
   - Expected: `.git/info/exclude:NN:DEVLOG.md	DEVLOG.md`
4. Tell the user the file is intentionally local-only.

If the file already exists, just read it for context and append.

### Why `.git/info/exclude` and not `.gitignore`?

| Mechanism | Versioned? | Scope | Use when |
|---|---|---|---|
| `.gitignore` | Yes (tracked) | Whole repo, all clones | Team-shared rules (e.g. `node_modules/`) |
| `.git/info/exclude` | **No** (in `.git/`) | This repo, this machine | Personal notes / local-only files |
| `core.excludesFile` | No | Global, all repos | Personal rules everywhere (e.g. `.DS_Store`) |

The user explicitly wants the ignore rule to stay off the remote. The only
correct location is `.git/info/exclude`.

## Entry Format

Append-only. One block per logical change. Newest at the bottom.

```markdown
## [YYYY-MM-DD] Brief title

**What:** One sentence describing what was done.
**Why:** The trigger, problem, or motivation.
**How:** Key implementation details (non-obvious only).
**Learned:** Gotchas, patterns, follow-ups, or open questions.
```

Conventions:

- Date in user's local timezone, ISO `YYYY-MM-DD`.
- Title: short noun phrase, no period.
- Bullets are fine inside any field.
- Never edit or delete old entries — only append.

## Workflow

### On task start

1. `Read DEVLOG.md` (if present) for context and the `## Planned` section.
2. If a `## Planned` item matches the current task, note it in the upcoming entry.

### On task completion / decision

1. Read the current `DEVLOG.md`.
2. Append a new `## [YYYY-MM-DD]` block under the existing content.
3. If a planned item is now done, move it from `## Planned` into a dated entry
   with a `[Done]` prefix in the title (do not delete the original line — strike
   it through or annotate it).
4. Add follow-up items to `## Planned` if any.

### Hygiene

- If the file grows past ~300 entries, split by year (`DEVLOG-2026.md`) and keep
  `DEVLOG.md` as an index.
- Never include secrets — treat it as plain text even though it's local.

## Template (used on first run)

```markdown
# DEVLOG

> Local-only development log. Intentionally **not** tracked by git
> (configured via `.git/info/exclude`, never via `.gitignore`).

Conventions:

- One `## [YYYY-MM-DD] Title` block per logical change.
- Fields: **What**, **Why**, **How**, **Learned**.
- Append-only — never rewrite history.

---

## Planned

- (in-progress or upcoming work goes here)

---
```

## Anti-Patterns

- Do **not** add `DEVLOG.md` to `.gitignore` — that would push the ignore rule
  to the remote, which the user explicitly does not want.
- Do **not** commit `DEVLOG.md` "just this once" — once tracked, ignore rules
  no longer hide it. If it ever gets tracked, use `git rm --cached DEVLOG.md`
  and warn the user.
- Do **not** rewrite or delete past entries.
- Do **not** store secrets, tokens, or credentials.
