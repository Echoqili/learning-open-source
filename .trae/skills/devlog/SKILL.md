---
name: "devlog"
description: "Maintains per-project DEVLOG.md (chronological changes/plans) and LESSON.md (aggregated problems and solutions). Both stay local-only via .git/info/exclude. Invoke when starting/completing coding tasks, making architectural decisions, or fixing tricky bugs."
---

# DEVLOG Skill

## Purpose

Maintain **two** local-only project files that work together:

| File | Role | Style |
|---|---|---|
| `DEVLOG.md` | Chronological log of what was done, planned, and learned | Append-only, dated entries |
| `LESSON.md` | Aggregated knowledge base of problems → root causes → solutions | Indexed, category-organized, reusable |

Rule of thumb: **DEVLOG.md records the journey; LESSON.md records the wisdom**.

Both files are **local-only** — they must never reach the remote repository, and
the ignore rules for them must not be committed either. This is achieved with
`.git/info/exclude` (a per-repo, never-tracked file), **not** `.gitignore`.

## When to Invoke

Invoke this skill when any of the following happen:

- Starting a new coding task in a project (initialize or refresh the log)
- Completing a coding task or a significant sub-step
- Making an architectural or design decision
- Fixing a tricky bug
- Discovering a library / framework gotcha
- User says things like "log this", "记一下", "记到日志里", "记录到 DEVLOG",
  "做个总结", "加到 LESSON"

## First-Run Setup (idempotent)

When the files are missing in the project root:

1. Create both `DEVLOG.md` and `LESSON.md` from their **Templates** below.
2. Make sure both are locally ignored, **without** touching `.gitignore`. Append
   to `.git/info/exclude`:
   - PowerShell:
     ```powershell
     Add-Content .git/info/exclude 'DEVLOG.md'
     Add-Content .git/info/exclude 'LESSON.md'
     ```
   - POSIX:
     ```bash
     printf '%s\n' 'DEVLOG.md' >> .git/info/exclude
     printf '%s\n' 'LESSON.md' >> .git/info/exclude
     ```
3. Verify with:
   ```bash
   git check-ignore -v -- DEVLOG.md LESSON.md
   ```
   Expected: both lines reference `.git/info/exclude`.
4. Tell the user both files are intentionally local-only.

If the files already exist, just read them for context and append.

### Why `.git/info/exclude` and not `.gitignore`?

| Mechanism | Versioned? | Scope | Use when |
|---|---|---|---|
| `.gitignore` | Yes (tracked) | Whole repo, all clones | Team-shared rules (e.g. `node_modules/`) |
| `.git/info/exclude` | **No** (in `.git/`) | This repo, this machine | Personal notes / local-only files |
| `core.excludesFile` | No | Global, all repos | Personal rules everywhere (e.g. `.DS_Store`) |

The user explicitly wants the ignore rules to stay off the remote. The only
correct location is `.git/info/exclude`.

---

# DEVLOG.md

Append-only chronological log.

## Entry Format

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
- When a fix surfaces reusable knowledge, add a pointer:
  `**Lesson:** see LESSON.md → <category> → <slug>`

## Workflow

### On task start

1. Read `DEVLOG.md` (if present) for context and the `## Planned` section.
2. If a `## Planned` item matches the current task, note it in the upcoming entry.

### On task completion / decision

1. Read the current `DEVLOG.md`.
2. Append a new `## [YYYY-MM-DD]` block under the existing content.
3. If a planned item is now done, move it from `## Planned` into a dated entry
   with a `[Done]` prefix in the title (do not delete the original line — strike
   it through or annotate it).
4. Add follow-up items to `## Planned` if any.
5. **Promote** to `LESSON.md` if the learning is reusable (see below).

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

---

# LESSON.md

Aggregated, searchable knowledge base of problems and their solutions. Where
`DEVLOG.md` is a stream, `LESSON.md` is an index — each lesson is a stable
entry that can be referenced, linked, and re-applied.

## When to Promote DEVLOG → LESSON

Promote a `DEVLOG.md` entry into `LESSON.md` when **any** of these is true:

- The same root cause could appear again in this project (or in similar ones).
- The fix took more than ~15 minutes of investigation.
- A library / framework behaved counter to docs or intuition.
- The user asked "why did we do it this way?" — i.e. the rationale is valuable
  out of context.

If the issue was trivial or one-off, keep it only in `DEVLOG.md`.

## Entry Format

Group by **category** (one `##` heading per category). Slugs are stable IDs you
can link to.

```markdown
## <Category, e.g. "Git / Branching">

### <YYYY-MM-DD> short-slug

- **Problem:** One-sentence description of the symptom.
- **Root cause:** Why it happened.
- **Solution:** The fix (commands, code, config).
- **How to avoid:** Checklist, lint rule, or convention to prevent recurrence.
- **Related:**
  - `DEVLOG.md` → `## [YYYY-MM-DD] <title>`
  - upstream issue / docs link
```

Conventions:

- Categories are broad and stable (`Git`, `Build`, `CI`, `Language / Python`,
  `Library / <name>`, `OS / Windows`, `IDE / Trae`, `Performance`, `Security`).
- Slug = lowercase-kebab, ≤ 5 words, action-oriented
  (e.g. `push-fails-on-spaces-in-path`).
- Newest lesson at the **top** of its category, so the freshest knowledge is
  most visible.
- `Problem` is the user-visible symptom. `Root cause` is the underlying reason.
  Keep them separate — symptoms recur even when causes change.

## Workflow

### When a non-trivial bug is fixed

1. Open `LESSON.md` and pick (or create) the right category.
2. Add a new entry at the top of that category with the template above.
3. Cross-link from the matching `DEVLOG.md` entry (`**Lesson:** see LESSON.md → <category> → <slug>`).
4. If this exact lesson already exists, **append** a new dated occurrence under
   it instead of creating a duplicate — frequency matters.

### When starting a task

1. Read the relevant categories in `LESSON.md` before designing the approach.
2. If the user says "have we seen this before?" — search the file first.

### Hygiene

- Never delete a lesson. If advice is wrong or outdated, strike it through and
  add a "Superseded by" note.
- Keep entries terse — one screen each, ideally.
- After ~50 lessons, add a top-of-file **Index** table grouped by category.

## Template (used on first run)

```markdown
# LESSON

> Local-only knowledge base. Aggregates problems → root causes → solutions
> from `DEVLOG.md`. Intentionally **not** tracked by git
> (configured via `.git/info/exclude`, never via `.gitignore`).

Conventions:

- Grouped by category (`## <Category>`), newest lesson at the top of each.
- Entry format: **Problem / Root cause / Solution / How to avoid / Related**.
- Slugs are stable IDs — never rename an old slug, only add "Superseded by".

---

## Index

(to be generated once the file has more than ~10 lessons)

---

## <Category>

### <YYYY-MM-DD> first-slug

- **Problem:**
- **Root cause:**
- **Solution:**
- **How to avoid:**
- **Related:**

---
```

---

## Anti-Patterns

- Do **not** add `DEVLOG.md` or `LESSON.md` to `.gitignore` — that would push
  the ignore rule to the remote, which the user explicitly does not want.
- Do **not** commit either file "just this once" — once tracked, ignore rules
  no longer hide them. If that ever happens, use `git rm --cached <file>` and
  warn the user.
- Do **not** rewrite or delete past `DEVLOG.md` entries.
- Do **not** store secrets, tokens, or credentials in either file.
- Do **not** duplicate information — pick one: chronological (DEVLOG) or
  indexed (LESSON), and cross-link.
