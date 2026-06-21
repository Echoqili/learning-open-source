# Shared Mode: why `DEVLOG.md` and `LESSON.md` are tracked

Starting with **v2.0** of the devlog skill, both files are **tracked in git
and shared with the team** by default. The previous "local-only" design
(v1.x) is deprecated.

## TL;DR

- The files are **committed and pushed** along with code changes.
- They live at the project root and appear in every clone.
- Anyone on the team can read and contribute; the audit trail is shared.
- A single developer can still opt out for *their* machine via
  `.git/info/exclude` — the rule is local, never pushed.

## Why tracked, not local-only

The v1.x design treated these files as personal notes that should never
reach the remote. In practice:

- **Knowledge is project-wide.** A bug a developer fixed on Tuesday
  should be available to the developer fixing a related bug next month.
  Hiding it in a local file defeats the purpose.
- **Onboarding is faster.** New team members reading `LESSON.md` learn
  the project's gotchas before they hit them.
- **The "ignore" is per-machine anyway.** Even when the rule is committed
  to `.gitignore`, individual developers can override with
  `.git/info/exclude` or `core.excludesFile`. The reverse is not true:
  once the files are ignored by `.gitignore`, you can't make them visible
  on a single checkout without editing the rule.

## Quick decision tree

```
Want the rule to apply to the whole team?
├── Yes → commit `.gitignore` to the repo
└── No
    ├── This repo, this machine only?    → .git/info/exclude
    └── Every repo on this machine?      → core.excludesFile (global)
```

The devlog skill's default is **the first option: no rule at all** —
the files are tracked. If a developer wants to keep personal notes out
of their local clone, they add the pattern to `.git/info/exclude`.

## Per-user opt-out (local-only without team-wide rule)

PowerShell:

```powershell
Add-Content .git/info/exclude 'DEVLOG.md'
Add-Content .git/info/exclude 'LESSON.md'
```

POSIX shell:

```bash
printf '%s\n' 'DEVLOG.md' >> .git/info/exclude
printf '%s\n' 'LESSON.md' >> .git/info/exclude
```

This hides the files from `git status` and prevents accidental `git add`
on *your* machine. The file is still tracked in the repo; clone / pull
still brings it down; you just don't see it as a working-tree change.

If you want a stronger opt-out (no file at all on your machine), use
`git update-index --skip-worktree DEVLOG.md LESSON.md` — but note this
is fragile and you may want to revert it later.

## The opposite of the v1.x decision

In v1.x, `.gitignore` was rejected because its rule would be pushed to
the team. v2.0 accepts the inverse: no rule at all is the default, and
**opting out** is a per-user concern. This puts the choice on each
developer instead of forcing it on the team.

The decision trail is preserved in `LESSON.md` →
`Skill Authoring` → `policy-reversals-preserve-history`.
