#!/usr/bin/env bash
# skill-validate.sh — Skill quality validation hook
# Validates skill format, structure, and content before committing.
# Reads skill metadata from SKILL.md files.
# Exit code 0 = pass, 1 = fail (with warnings to stderr)

set -euo pipefail

HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
INDEX_FILE="${SKILLS_ROOT}/skills-index.json"
CATALOG_FILE="${SKILLS_ROOT}/skills-catalog.md"

WARN_COUNT=0
ERROR_COUNT=0

warn() {
    echo "[skill-validate] WARNING: $1" >&2
    WARN_COUNT=$((WARN_COUNT + 1))
}

error() {
    echo "[skill-validate] ERROR: $1" >&2
    ERROR_COUNT=$((ERROR_COUNT + 1))
}

info() {
    echo "[skill-validate] INFO: $1" >&2
}

validate_yaml_frontmatter() {
    local file="$1"

    if [ ! -f "$file" ]; then
        error "File not found: $file"
        return 1
    fi

    local has_start=false
    local has_end=false
    local frontmatter=""

    while IFS= read -r line || [ -n "$line" ]; do
        if [ "$line" = "---" ]; then
            if [ "$has_start" = false ]; then
                has_start=true
            else
                has_end=true
                break
            fi
        elif [ "$has_start" = true ] && [ "$has_end" = false ]; then
            frontmatter="${frontmatter}${line}"$'\n'
        elif [ "$has_end" = true ]; then
            break
        fi
    done < "$file"

    if [ "$has_start" = false ] || [ "$has_end" = false ]; then
        error "Missing YAML frontmatter in $file (need --- delimiters)"
        return 1
    fi

    if [ -z "$frontmatter" ]; then
        error "Empty frontmatter in $file"
        return 1
    fi

    if ! echo "$frontmatter" | head -1 | grep -qE "^name:|^description:"; then
        error "Frontmatter must start with 'name:' or 'description:'"
        return 1
    fi

    return 0
}

validate_skill_structure() {
    local skill_dir="$1"
    local skill_name
    skill_name="$(basename "$skill_dir")"

    if [ ! -d "$skill_dir" ]; then
        error "Skill directory not found: $skill_dir"
        return 1
    fi

    local skill_md="${skill_dir}/SKILL.md"
    if [ ! -f "$skill_md" ]; then
        error "Missing SKILL.md in $skill_dir"
        return 1
    fi

    validate_yaml_frontmatter "$skill_md"
}

validate_required_sections() {
    local file="$1"
    local required_sections=("Purpose" "Instructions" "Examples")
    local missing=""

    for section in "${required_sections[@]}"; do
        if ! grep -qE "^#{1,3} ${section}" "$file" 2>/dev/null; then
            missing="${missing}${missing:+, }$section"
        fi
    done

    if [ -n "$missing" ]; then
        warn "Missing recommended sections: $missing"
        return 1
    fi

    return 0
}

validate_description_length() {
    local file="$1"
    local desc_line

    desc_line="$(grep -m1 "^description:" "$file" 2>/dev/null | cut -d: -f2- | sed 's/^[[:space:]]*//')"

    if [ ${#desc_line} -lt 10 ]; then
        warn "Description too short (min 10 chars): $desc_line"
        return 1
    fi

    if [ ${#desc_line} -gt 200 ]; then
        warn "Description too long (max 200 chars): ${desc_line:0:50}..."
        return 1
    fi

    return 0
}

validate_index_consistency() {
    if [ ! -f "$INDEX_FILE" ]; then
        warn "skills-index.json not found (run build_skills_index.py)"
        return 1
    fi

    if ! command -v jq >/dev/null 2>&1; then
        warn "jq not available, skipping index validation"
        return 0
    fi

    local total_count
    total_count="$(jq -r '.total_count // 0' "$INDEX_FILE" 2>/dev/null)"

    if [ "$total_count" -eq 0 ]; then
        warn "skills-index.json has zero skills"
        return 1
    fi

    info "Index contains $total_count skills"
    return 0
}

main() {
    local changed_files
    local skill_dirs=()

    info "Starting skill validation..."

    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        info "Not a git repo, skipping hook validation"
        exit 0
    fi

    changed_files="$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null)"
    if [ -z "$changed_files" ]; then
        changed_files="$(git diff --name-only --diff-filter=ACM 2>/dev/null)"
    fi

    if [ -z "$changed_files" ]; then
        info "No files changed, skipping validation"
        exit 0
    fi

    while IFS= read -r file; do
        [ -z "$file" ] && continue

        if [[ "$file" == *.md ]] && [[ "$file" == */SKILL.md ]]; then
            local skill_dir
            skill_dir="$(dirname "$file")"

            if [[ ! " ${skill_dirs[*]} " =~ " ${skill_dir} " ]]; then
                skill_dirs+=("$skill_dir")
            fi
        fi
    done <<< "$changed_files"

    if [ ${#skill_dirs[@]} -eq 0 ]; then
        info "No SKILL.md files changed, skipping validation"
        exit 0
    fi

    info "Validating ${#skill_dirs[@]} skill(s)..."

    for skill_dir in "${skill_dirs[@]}"; do
        local skill_md="${skill_dir}/SKILL.md"

        if ! validate_skill_structure "$skill_dir"; then
            continue
        fi

        validate_required_sections "$skill_md"
        validate_description_length "$skill_md"
    done

    validate_index_consistency

    echo ""
    if [ "$ERROR_COUNT" -gt 0 ]; then
        error "Validation failed with $ERROR_COUNT error(s)"
        exit 1
    elif [ "$WARN_COUNT" -gt 0 ]; then
        warn "Validation passed with $WARN_COUNT warning(s)"
        exit 0
    else
        info "All validations passed"
        exit 0
    fi
}

main "$@"
