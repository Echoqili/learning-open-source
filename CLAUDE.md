# CLAUDE.md — Learning Open Source

> Auto-loaded by AI agents on startup. Single source for project rules, conventions, and learned knowledge.

---

## Project Overview

**Purpose:** Learn open-source projects + host custom Trae skills for structured, low-cost code changes.

**Key files:**
- `.trae/skills/superpowers-openspec-pipeline/SKILL.md` — Main orchestration skill (v3.6.0)
- `DEVLOG.md` — Append-only development log (`## [YYYY-MM-DD] Title` with What/Why/How/Learned)
- `LESSON.md` — Knowledge base grouped by category (Problem/Root cause/Solution/How to avoid/Related)
- `candidates.json` — 148 GitHub repo candidates for learning
- `superpowers-openspec-manual/` — Visual HTML manual

---

## Superpowers + OpenSpec Pipeline Essentials

### Three Operating Modes

| Mode | Default? | Explore | Proposal | TDD | Redline | Archive |
|------|----------|---------|----------|-----|---------|---------|
| **Think** | No | If fuzzy | proposal+design+tasks+features+specs | Mandatory | Full scan | Merge to spec baseline |
| **Plan-First** | No | If fuzzy | plan+tasks only | Mandatory | lint+test+type+secret | META only, spec optional |
| **Fast** | **YES** | Skip | proposal+tasks+minimal design | Mandatory | Only lint+test | META only, spec optional |

### Risk Classification

| Level | Criteria | Gate |
|-------|----------|------|
| **low** | Pure new feature, no sensitive data/API/perf | Skip ①, light redline |
| **medium** | Normal business, involves user data/internal API | Normal gate ① + standard redline |
| **high** | Permissions/payment/security/API migration/cross-service | Gate ① + security review + full redline |

### Pipeline Steps

```
explore → propose(risk grade) → gate① → apply(TDD) → compile/test gate② → redline-check③ → acceptance④ → archive
```

### Hard Constraints (Violations = Bugs)

1. **Never modify** `openspec/changes/{change_name}/` docs during coding — only `propose` can touch them
2. **Never implement** features not in `proposal.md`/`plan.md` acceptance criteria
3. **TDD is mandatory** — every task: Red (write failing test) → Green (make pass) → Refactor
4. **Gate ①** for medium/high risk: wait for explicit user approval ("通过/approve/ok") before entering apply
5. **Blocking redline** items must be fixed before moving to acceptance
6. **Archive always** — update `META.md` with `status: archived`, never skip

### Common Anti-Patterns

| Anti-Pattern | Correct |
|---|---|
| `/opsx:explore` writes files | Keep in memory only |
| `/opsx:propose` writes code | Write only spec docs |
| Auto-enter apply without gate① approval (medium/high) | Must wait for explicit pass |
| Modify spec docs during coding | Forbidden; requirement changes → re-propose |
| Skip redline on blocking items | Fix then re-run `/redline-check` |
| Archive before acceptance | Wait for gate④ pass |
| Add undeclared features during implementation | Strip out or re-propose |

---

## Lessons Learned (from LESSON.md)

### Policy Reversals Need Full Checklist

When reversing a documented policy, in ONE atomic commit:
1. Update `SKILL.md` description, setup, anti-patterns, file layout
2. Update/remove dependent scripts and references
3. Log the reversal in `DEVLOG.md`
4. Record the lesson in `LESSON.md`
5. Strike through old entries — **never delete them**

### Co-locate Reference with Use Site

At decision time, the data the agent needs must be visible without loading another file. Inline a compact summary; keep the full version behind a reference link.

### PowerShell 5.1 (this workspace)

- `&&` / `||` are NOT supported — use `;` for sequential, `if ($LASTEXITCODE)` for conditional
- Prefer semicolons; for long pipelines use `.ps1` scripts
- Reserve `&&` / `||` for POSIX scripts only

### Git Ignore Is a Triplet

"Ignored" = 3 checks:
1. `git check-ignore -v -- <f>` → exit 0 (in some ignore source)
2. `git ls-files --error-unmatch -- <f>` → exit non-zero (not tracked in index)
3. `git log --all --oneline -- <f>` → empty (never committed)

### Skill Discovery

Skills under `.trae/skills/<name>/SKILL.md` are auto-discovered by the IDE. The `description` field in frontmatter is the most important — it determines whether the agent loads the skill.

---

## Coding Conventions

- **Japanese/Chinese comments OK** — project is bilingual
- **TDD first** — write test before implementation
- **Never commit secrets** — `.env` is in `.gitignore`
- **CLAUDE.md is append-only** — add new rules, never remove old ones (strike through if outdated)

## AI Agent Rules

- Read CLAUDE.md on every startup (auto-loaded)
- Before editing a file, read it first
- When reversing any documented policy, follow the atomic-commit checklist above
- DEVLOG entries: `## [YYYY-MM-DD] Title` with What/Why/How/Learned
- LESSON entries: Problem / Root cause / Solution / How to avoid / Related
- Past entries are never deleted — strike through and annotate "Superseded by"

## Directory Structure

```
learning-open-source/
├── .trae/skills/                    # Trae Skill definitions (auto-discovered)
│   └── superpowers-openspec-pipeline/SKILL.md
├── .skills/                         # Empty (reserved)
├── .state/                          # Empty (reserved)
├── openspec/                        # Generated by pipeline (git-ignored if local)
│   ├── config/redline.yml
│   ├── specs/<domain>.md
│   └── changes/{change_name}/
│       ├── META.md
│       ├── proposal.md | plan.md
│       ├── design.md (think/fast)
│       ├── tasks.md
│       ├── specs/
│       └── features/
├── CLAUDE.md                        # ← You are here
├── DEVLOG.md                        # Tracked dev log
├── LESSON.md                        # Tracked knowledge base
└── candidates.json                  # 148 learning repo candidates
```