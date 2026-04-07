#!/usr/bin/env bats
# common-setup.bash — Shared test setup/teardown helpers.

export PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$BATS_TEST_DIRNAME")/.." && pwd)}"
export TESTS_DIR="$PROJECT_ROOT/tests"
export FIXTURES_DIR="$TESTS_DIR/fixtures"
export TEMP_DIR=""

setup_temp_dir() {
    TEMP_DIR="$(mktemp -d -t skills-tests.XXXXXX)"
    export TEMP_DIR
}

teardown_temp_dir() {
    if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
}
