# LESSON

> Tracked project knowledge base. Aggregates problems → root causes →
> solutions from `DEVLOG.md`. Shared with the team via git.

Conventions:

- Grouped by category (`## <Category>`), newest lesson at the top of each.
- Entry format: **Problem / Root cause / Solution / How to avoid / Related**.
- Slugs are stable IDs — never rename an old slug, only add "Superseded by".
- Past lessons are **never deleted**; outdated ones are struck through and
  annotated with "Superseded by".

See `.trae/skills/devlog/references/categories.md` for the canonical category list.

---

## Index

- **Skill Authoring** — `policy-reversals-preserve-history`
- **Git** — `ignore-rule-itself-must-not-be-pushed` (~~deprecated~~),
  `how-to-verify-local-only-files-stay-local` (~~deprecated~~)
- **IDE / Trae** — `co-locate-reference-with-use-site`
- **OS / Windows** — `power-shell-no-and-or-pipe-pipe`

(to be expanded once the file has more than ~10 lessons)

---

## Skill Authoring

### 2026-06-19 policy-reversals-preserve-history

- **Problem:** A skill has a documented policy (e.g. "local-only") that
  the user later reverses. Changing only the forward behavior leaves
  the description, scripts, and references in a contradictory state.
- **Root cause:** Documentation tends to lag implementation, and
  dependent scripts / references are easy to forget. The audit trail
  (past entries) is especially at risk of being silently "cleaned
  up" along with the policy change.
- **Solution:** When reversing a documented policy:
  1. Update `SKILL.md` — description, First-Run Setup, Anti-Patterns,
     File Layout. Bump `metadata.version` (major for breaking changes).
  2. Update or remove dependent scripts / references so they don't
     tell the new user to do the old thing.
  3. Add a new `DEVLOG.md` entry explaining the reversal.
  4. Add a new `LESSON.md` entry under a `Skill Authoring` category
     (or whichever category fits) describing the workflow.
  5. **Do not delete old entries.** Strike them through and add a
     "Superseded by" note. Past entries are the audit trail.
- **How to avoid:** At the moment of any policy change, run a checklist
  of every artifact that referenced the old policy and update them in
  one atomic commit. A single breaking commit is easier to reason
  about than incremental drift.
- **Related:**
  - DEVLOG.md → ## [2026-06-19] Switch devlog to shared (tracked) mode
  - `.trae/skills/devlog/SKILL.md` (v2.0.0)
  - `.trae/skills/devlog/references/shared-mode.md`

---

## Git

### ~~2026-06-19 ignore-rule-itself-must-not-be-pushed~~ (deprecated)

> **Superseded by** `Skill Authoring` → `policy-reversals-preserve-history`
> (2026-06-19). The local-only policy this lesson justified was reversed
> the same day. Kept as a historical record of the v1.x design decision.

- **Problem:** User wants `DEVLOG.md` (and `LESSON.md`) ignored, but does
  **not** want the ignore rule itself visible to the team / on the remote.
- **Root cause:** `.gitignore` is versioned — any rule added to it is committed
  and shared. There is no way to add to `.gitignore` "just locally".
- **Solution (v1.x, no longer recommended):** Use `.git/info/exclude` for
  per-repo, local-only ignore rules. (v2.0+ tracks the files instead —
  see `references/shared-mode.md`.)
- **Related:**
  - DEVLOG.md → ## [2026-06-19] Add devlog skill and bootstrap DEVLOG.md,
    ## [2026-06-19] Extend devlog skill with LESSON.md
  - `.trae/skills/devlog/references/shared-mode.md` (replacement rationale)

### ~~2026-06-19 how-to-verify-local-only-files-stay-local~~ (deprecated)

> **Superseded by** `Skill Authoring` → `policy-reversals-preserve-history`
> (2026-06-19). The `verify-ignored` scripts were removed the same day.
> Kept as a historical record; the three-check pattern is still valid
> for any *future* local-only file you may need to assert.

- **Problem:** A file is "ignored" by git, but the property can be
  violated in three different ways: (a) not in any ignore source, (b)
  ignored but already tracked in the index, (c) tracked-then-removed but
  still in commit history. Any single check (e.g. `git check-ignore`)
  misses two of the three states.
- **Root cause:** "Ignored" is a snapshot of the working tree, not a
  permanent state. Once a file is committed and then `git rm --cached`,
  it becomes untracked *and* historical. A future `git add` will
  resurrect it, breaking the local-only promise silently.
- **Solution (still useful if you re-introduce a local-only file):** Run
  all three checks per file:
  1. `git check-ignore -v -- <f>` → exit 0
  2. `git ls-files --error-unmatch -- <f>` → exit non-zero
  3. `git log --all --oneline -- <f>` → empty output
- **Related:**
  - DEVLOG.md → ## [2026-06-19] Add verify-ignored.{sh,ps1} — self-test for local-only invariant

---

## IDE / Trae

### 2026-06-19 co-locate-reference-with-use-site

- **Problem:** When an agent followed the SKILL.md workflow, it had to
  remember to load `references/categories.md` before it could pick the
  right `## <Category>` heading for a new LESSON.md entry. The decision
  point (in the Examples section) and the data needed to make the
  decision (in `references/`) were in different places.
- **Root cause:** Reference data was treated as separate from the
  workflow that used it. Agents don't proactively load files they
  weren't told to load, so the data effectively didn't exist for them.
- **Solution:** Add a compact `### Categories at a glance` subsection
  inside `## Examples`. The full table stays in `references/categories.md`
  for grep-ability and on-demand loading, but the table that matters at
  decision time is visible inline.
- **How to avoid:** When designing a skill, ask: "at the moment of
  decision, is the data the agent needs visible without loading
  another file?" If not, inline a compact summary at the use site
  and keep the full version behind a reference link.
- **Related:**
  - DEVLOG.md → ## [2026-06-19] Inline categories table in SKILL.md Examples
  - `.trae/skills/devlog/SKILL.md` → ## Examples → Categories at a glance

---

## OS / Windows

### 2026-06-19 power-shell-no-and-or-pipe-pipe

- **Problem:** `git status && git log` (and `||`) errors with
  `标记“&&”不是此版本中的有效语句分隔符` in Windows PowerShell.
- **Root cause:** PowerShell's parser rejects `&&` and `||` as statement
  separators; those are `cmd.exe` / POSIX-shell syntax. PowerShell 7+ adds
  `&&` / `||`, but Trae's default shell is `powershell5` (Windows PowerShell
  5.1), which does not.
- **Solution:** Use `;` for sequential commands and avoid `||` / `&&`.
  - Sequential: `git status; git log --oneline -5`
  - Conditional fallback: use `if ($LASTEXITCODE -ne 0) { ... }` or
    `try { cmd1 } catch { cmd2 }`.
- **How to avoid:** In this workspace prefer semicolons; for long pipelines
  use a `.ps1` script. Reserve `&&` / `||` for POSIX scripts only.
- **Related:**
  - DEVLOG.md → ## [2026-06-19] Add devlog skill and bootstrap DEVLOG.md
