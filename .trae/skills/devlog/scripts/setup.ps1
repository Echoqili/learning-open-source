# setup.ps1 — one-shot initialization for the devlog skill in the current project.
# Creates DEVLOG.md and LESSON.md (if missing) and `git add`s them.
# The files are tracked in git and shared with the team (v2.0+).
#
# Usage:  .\setup.ps1
#         (run from the project root; safe to re-run)

$ErrorActionPreference = 'Stop'

# ---------- guards ----------
if (-not (Test-Path .git)) {
  Write-Error "not a git repository (.git/ not found). Run from a project root."
}

# ---------- templates ----------
$devlogTemplate = @'
# DEVLOG

> Tracked project development log. Shared with the team via git.

Conventions:

- One `## [YYYY-MM-DD] Title` block per logical change.
- Fields: **What**, **Why**, **How**, **Learned**.
- Append-only — never rewrite history.

---

## Planned

- (in-progress or upcoming work goes here)

---
'@

$lessonTemplate = @'
# LESSON

> Tracked project knowledge base. Aggregates problems → root causes →
> solutions from `DEVLOG.md`. Shared with the team via git.

Conventions:

- Grouped by category (`## <Category>`), newest lesson at the top of each.
- Entry format: **Problem / Root cause / Solution / How to avoid / Related**.
- Slugs are stable IDs — never rename an old slug, only add "Superseded by".

See `.trae/skills/devlog/references/categories.md` for the canonical category list.

---

## Index

(to be generated once the file has more than ~10 lessons)

---
'@

# ---------- main ----------
if (-not (Test-Path DEVLOG.md)) {
  Set-Content -Path DEVLOG.md -Value $devlogTemplate -Encoding UTF8
  Write-Host "created: DEVLOG.md"
}

if (-not (Test-Path LESSON.md)) {
  Set-Content -Path LESSON.md -Value $lessonTemplate -Encoding UTF8
  Write-Host "created: LESSON.md"
}

# Stage both files. `git add` is safe to re-run; no-op if already tracked.
$null = git add DEVLOG.md LESSON.md 2>&1

Write-Host '--- verification ---'
git ls-files -- DEVLOG.md LESSON.md

Write-Host '--- done ---'
Write-Host 'DEVLOG.md and LESSON.md are now tracked and will be pushed with the next commit.'
Write-Host 'Per-user opt-out (e.g. for personal notes): add DEVLOG.md / LESSON.md'
Write-Host 'to .git/info/exclude. See .trae/skills/devlog/references/shared-mode.md.'
