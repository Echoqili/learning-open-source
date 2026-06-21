#!/usr/bin/env bash
# setup.sh — one-shot initialization for the devlog skill in the current project.
# Creates DEVLOG.md and LESSON.md (if missing) and `git add`s them.
# The files are tracked in git and shared with the team (v2.0+).
#
# Usage:  ./setup.sh
#         (run from the project root; safe to re-run)

set -euo pipefail

# ---------- guards ----------
if [ ! -d .git ]; then
  echo "error: not a git repository (.git/ not found). Run from a project root." >&2
  exit 1
fi

# ---------- helpers ----------
write_devlog_template() {
  cat > DEVLOG.md <<'EOF'
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
EOF
}

write_lesson_template() {
  cat > LESSON.md <<'EOF'
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
EOF
}

# ---------- main ----------
if [ ! -f DEVLOG.md ]; then
  write_devlog_template
  echo "created: DEVLOG.md"
fi

if [ ! -f LESSON.md ]; then
  write_lesson_template
  echo "created: LESSON.md"
fi

# Stage both files (no-op if already tracked). `git add` is safe to re-run.
git add DEVLOG.md LESSON.md 2>/dev/null || true

echo "--- verification ---"
git ls-files -- DEVLOG.md LESSON.md

echo "--- done ---"
echo "DEVLOG.md and LESSON.md are now tracked and will be pushed with the next commit."
echo "Per-user opt-out (e.g. for personal notes): add DEVLOG.md / LESSON.md"
echo "to .git/info/exclude. See .trae/skills/devlog/references/shared-mode.md."
