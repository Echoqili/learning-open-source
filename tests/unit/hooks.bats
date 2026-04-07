#!/usr/bin/env bats
# hooks.bats — Tests for skill validation hooks.

load '../test_helper/common-setup'

setup() {
    setup_temp_dir
    cd "$TEMP_DIR"
}

teardown() {
    teardown_temp_dir
}

@test "skill-validate.sh exits 0 for valid skill structure" {
    mkdir -p "skills/test-skill"
    cat > "skills/test-skill/SKILL.md" <<'EOF'
---
name: "test-skill"
description: "A test skill for validation"
---
# Test Skill

## Purpose
This is a test skill.

## Instructions
Run the test.

## Examples
Example usage here.
EOF

    run bash "$PROJECT_ROOT/hooks/skill-validate.sh"
    [ "$status" -eq 0 ]
}

@test "skill-validate.sh exits 1 for missing YAML frontmatter" {
    mkdir -p "skills/bad-skill"
    cat > "skills/bad-skill/SKILL.md" <<'EOF'
# Bad Skill

No frontmatter here.
EOF

    run bash "$PROJECT_ROOT/hooks/skill-validate.sh"
    [ "$status" -eq 1 ]
    [[ "$output" == *"ERROR: Missing YAML frontmatter"* ]]
}

@test "skill-validate.sh exits 1 for missing SKILL.md" {
    mkdir -p "skills/missing-md"

    run bash "$PROJECT_ROOT/hooks/skill-validate.sh"
    [ "$status" -eq 1 ]
    [[ "$output" == *"ERROR: Missing SKILL.md"* ]]
}

@test "skill-validate.sh warns on missing recommended sections" {
    mkdir -p "skills/incomplete-skill"
    cat > "skills/incomplete-skill/SKILL.md" <<'EOF'
---
name: "incomplete-skill"
description: "Missing sections"
---
# Incomplete Skill

Only Purpose section.
EOF

    run bash "$PROJECT_ROOT/hooks/skill-validate.sh"
    [[ "$output" == *"WARNING"* ]]
}

@test "skill-validate.sh skips validation when no SKILL.md files changed" {
    mkdir -p "docs"
    touch "docs/README.md"

    run bash "$PROJECT_ROOT/hooks/skill-validate.sh"
    [ "$status" -eq 0 ]
    [[ "$output" == *"No SKILL.md files changed"* ]]
}
