# DEVLOG

> Tracked project development log. Shared with the team via git.

Conventions:

- One `## [YYYY-MM-DD] Title` block per logical change.
- Fields: **What**, **Why**, **How**, **Learned**.
- Append-only — never rewrite history.

---

## Planned

- (in-progress or upcoming work goes here)
- [x] Switch devlog to shared (tracked) mode (done 2026-06-19).

---

## [2026-06-19] Add devlog skill and bootstrap DEVLOG.md

**What:** Created `.trae/skills/devlog/SKILL.md` and an initial `DEVLOG.md` in
the project root. Configured `.git/info/exclude` to keep `DEVLOG.md` local
without modifying `.gitignore`.

**Why:** Wanted an append-only, project-local log of changes and plans that
never leaks to the remote. The ignore rule for the log must also stay off the
remote, so the team / public repo is not affected.

**How:**

- Researched similar skills (sourcetms.com "Starter Template: agents.md",
  OpenClaw DevLog Generator, agentskill.sh tutorial) and adopted the
  `What / Why / How / Learned` entry format.
- Used `.git/info/exclude` (per-repo, never tracked) instead of `.gitignore`
  (tracked, shared) to satisfy the local-only-ignore requirement.
- Verified with `git check-ignore -v -- DEVLOG.md` → returns
  `.git/info/exclude:...:DEVLOG.md`.

**Learned:**

- `.gitignore` is the wrong tool for "I want this ignored but I don't want the
  rule visible to teammates". The right tool is `.git/info/exclude`.
- Skills created under `.trae/skills/<name>/SKILL.md` are picked up by the IDE
  for this workspace; committing them to the project shares the convention
  with anyone who clones the repo.

## [2026-06-19] Optimize devlog skill to v1.1.0 (description, examples, scripts, references)

**What:** Restructured the skill per best-practice references:
- Frontmatter now starts with `Use when...` and lists rich trigger keywords.
- Added `license`, `compatibility`, `metadata.version/author`.
- Added `## When NOT to Use` and three worked `## Examples`.
- Split heavy reference into `scripts/` (setup.sh + setup.ps1) and
  `references/` (git-exclude-explained.md + categories.md).
- Re-categorized LESSON.md entries under `## Git` and `## OS / Windows`
  per the new canonical category list.

**Why:** Prior version had a feature-summary description (low CSO score), no
worked examples (template-only), and 6+ steps of manual setup. With scripts +
progressive disclosure the skill is both more discoverable and cheaper to run.

**How:** Cross-referenced mdskills.ai best practices, Anthropic skill spec,
GitHub Copilot skill guide, firecrawl SKILL.md deep-dive, and the
capability-documentation TDD-for-skills pattern. Implemented all six
optimizations the user approved.

**Lesson:** see LESSON.md → Git → ignore-rule-itself-must-not-be-pushed
**Learned:** `description` is the most important field — it determines whether
the agent ever loads the skill. Pattern: "Use when [triggers]. Triggers on
[specific keywords]. Do NOT use for [boundary]."

## [2026-06-19] Inline categories table in SKILL.md Examples

**What:** Added a `### Categories at a glance` subsection inside `## Examples`
in `.trae/skills/devlog/SKILL.md`. It lists the canonical LESSON.md categories
in a compact table so an agent picking a category for a new lesson sees the
full set without having to load `references/categories.md` first.

**Why:** User said the trigger logic for promoting a DEVLOG entry to LESSON
felt indirect — the agent had to remember to open the references file. This
is the same pattern docs sites use for "On this page" summaries: compact
reference data at the decision point, full reference available on demand.

**How:**

- Compact table (≈15 rows) of `Category | Use for` placed at the end of the
  `## Examples` section.
- Each example already names a category inline; the table makes the palette
  visible without a second file load.
- Full table with naming rules stays in `references/categories.md` for
  grep-ability and on-demand loading.

**Lesson:** see LESSON.md → IDE / Trae → co-locate-reference-with-use-site
**Learned:** When designing skills, "where does the agent look first?"
matters as much as "what's available?". A summary at the use site beats a
full reference that requires loading.

## [2026-06-19] Add verify-ignored.{sh,ps1} — self-test for local-only invariant

**What:** Added two cross-platform scripts that assert `DEVLOG.md` and
`LESSON.md` are still ignored by git, are not tracked in the index, and
have never appeared in any commit. Updated `SKILL.md` `## File Layout` to
list them and pointed users at them as a post-setup smoke test.

**Why:** The "local-only" promise is the core invariant of the devlog
skill. Until now it relied on the user running `git check-ignore` manually
after every change — a check that by itself misses two of the three states
a local-only file can be in. A single-command script makes the invariant
testable and fail-loud.

**How:**

- `scripts/verify-ignored.sh` and `scripts/verify-ignored.ps1` run three
  checks per file (all must pass):
  1. `git check-ignore -v -- <f>` → exit 0 (file is in some ignore source)
  2. `git ls-files --error-unmatch -- <f>` → exit non-zero (file is
     not tracked in the index)
  3. `git log --all --oneline -- <f>` → empty (file was never committed)
- Defaults to `DEVLOG.md LESSON.md`; override via positional args.
- Exits 0 on full pass, 1 on any failure.
- Self-tested:
  - Positive: `./verify-ignored.ps1` → 6/6 OK, exit 0.
  - Negative: `./verify-ignored.ps1 random.txt` → 1 FAIL ("not ignored"),
    exit 1 — script correctly fails loud.

**Lesson:** see LESSON.md → Git → how-to-verify-local-only-files-stay-local
**Learned:** "Ignored" is a triplet, not a single property. A file can be
(a) not in any ignore source, (b) ignored but tracked, or (c) tracked-then-
removed but still in history. Any one check (e.g. `git check-ignore` alone)
misses two of the three. The three-check pattern catches all three states
and is short enough to wire into pre-commit / CI.

## [2026-06-19] Switch devlog to shared (tracked) mode

**What:** Reversed the v1.x "local-only" policy. `DEVLOG.md` and
`LESSON.md` are now tracked in git and pushed to remote. The `.git/info/exclude`
entries for them were removed on this machine; both files are `git add`ed.

**Why:** User decided the knowledge base should be shared with the team
on this project, not kept as a per-developer note. New team members can
read past decisions on clone, and a bug fixed by one developer is visible
to the developer fixing the related bug next month.

**How:**

- Bumped `metadata.version` in `SKILL.md` from `1.1.0` → `2.0.0`
  (breaking change to the file-management semantics).
- Rewrote `SKILL.md` description, First-Run Setup, Anti-Patterns, and
  File Layout to reflect the new policy.
- Replaced `references/git-exclude-explained.md` with
  `references/shared-mode.md` (rationale + per-user opt-out instructions).
- Added `Skill Authoring` category to `references/categories.md`.
- `scripts/setup.sh` / `.ps1` no longer add to `.git/info/exclude`; they
  `git add` the files instead and verify with `git ls-files`.
- Removed `scripts/verify-ignored.{sh,ps1}` — their premise (local-only
  invariant) no longer holds.
- Old LESSON entries `ignore-rule-itself-must-not-be-pushed` and
  `how-to-verify-local-only-files-stay-local` are kept as historical
  records, struck through with a "Superseded by" note (per the skill's
  own "never delete" rule).
- This is one atomic commit so the policy change is easy to reason about
  (per the lesson recorded below).

**Lesson:** see LESSON.md → Skill Authoring → policy-reversals-preserve-history
**Learned:** Reversing a documented policy touches description, workflow,
scripts, references, anti-patterns, *and* the audit trail. A single
breaking commit is much easier to review and revert than incremental
drift across multiple commits.
