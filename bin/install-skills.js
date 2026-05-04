#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

const SKILLS_DIR = path.join(__dirname, '..', 'all-skills');
const TARGET_SKILLS_DIRS = {
    claude: path.join(os.homedir(), '.claude', 'skills'),
    cursor: path.join(os.homedir(), '.cursor', 'skills'),
    windsurf: path.join(os.homedir(), '.windsurf', 'skills'),
    kiro: path.join(os.homedir(), '.kiro', 'skills'),
    opencode: path.join(os.homedir(), '.config', 'opencode', 'skills'),
    codex: path.join(os.homedir(), '.codex', 'skills'),
    continue: path.join(os.homedir(), '.continue', 'skills'),
};

function log(message, type = 'info') {
    const colors = {
        info: '\x1b[34m',
        success: '\x1b[32m',
        error: '\x1b[31m',
        warning: '\x1b[33m',
    };
    console.log(`${colors[type]}[${type.toUpperCase()}]${'\x1b[0m'} ${message}`);
}

function mkdirp(dir) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
}

function copySkill(source, dest) {
    if (fs.existsSync(dest)) {
        fs.rmSync(dest, { recursive: true, force: true });
    }
    fs.cpSync(source, dest, { recursive: true });
}

function installToIDE(ideName, targetDir) {
    try {
        mkdirp(targetDir);

        const skillDirs = fs.readdirSync(SKILLS_DIR, { withFileTypes: true })
            .filter(dir => dir.isDirectory())
            .map(dir => dir.name);

        log(`Installing ${skillDirs.length} skills to ${ideName}...`, 'info');

        let installed = 0;
        for (const skillDir of skillDirs) {
            const sourcePath = path.join(SKILLS_DIR, skillDir);
            const destPath = path.join(targetDir, skillDir);

            try {
                copySkill(sourcePath, destPath);
                installed++;
            } catch (err) {
                log(`Failed to install ${skillDir}: ${err.message}`, 'warning');
            }
        }

        log(`Successfully installed ${installed} skills to ${ideName}`, 'success');
        return true;
    } catch (err) {
        log(`Failed to install to ${ideName}: ${err.message}`, 'error');
        return false;
    }
}

function installToAll() {
    log('Installing skills to all supported IDEs...', 'info');
    let successCount = 0;
    let totalCount = 0;

    for (const [ideName, targetDir] of Object.entries(TARGET_SKILLS_DIRS)) {
        totalCount++;
        if (installToIDE(ideName, targetDir)) {
            successCount++;
        }
    }

    log(`\nInstallation complete: ${successCount}/${totalCount} IDEs configured`, 'success');
}

function listSkills() {
    const skillDirs = fs.readdirSync(SKILLS_DIR, { withFileTypes: true })
        .filter(dir => dir.isDirectory())
        .map(dir => dir.name);

    log(`Available skills (${skillDirs.length}):`, 'info');
    console.log('');
    skillDirs.forEach(skill => {
        console.log(`  - ${skill}`);
    });
    console.log('');
}

function createSymlinkToAll() {
    log('Creating symlinks to all supported IDEs...', 'info');

    const sourceSkills = path.resolve(SKILLS_DIR);
    let successCount = 0;
    let totalCount = 0;

    for (const [ideName, targetDir] of Object.entries(TARGET_SKILLS_DIRS)) {
        totalCount++;
        try {
            mkdirp(targetDir);

            const destLink = path.join(targetDir, 'learning-open-source');
            if (fs.existsSync(destLink)) {
                fs.unlinkSync(destLink);
            }

            if (os.platform() === 'win32') {
                execSync(`mklink /D "${destLink}" "${sourceSkills}"`);
            } else {
                fs.symlinkSync(sourceSkills, destLink);
            }

            log(`Created symlink for ${ideName}`, 'success');
            successCount++;
        } catch (err) {
            log(`Failed to create symlink for ${ideName}: ${err.message}`, 'warning');
        }
    }

    log(`\nSymlinks created: ${successCount}/${totalCount} IDEs`, 'success');
}

function showHelp() {
    console.log(`
Usage: install-skills.js [options]

Options:
  --all           Install skills to all supported IDEs
  --claude        Install to Claude Code
  --cursor        Install to Cursor
  --windsurf      Install to Windsurf
  --kiro          Install to Kiro
  --opencode      Install to OpenCode
  --codex         Install to Codex
  --continue      Install to Continue
  --link          Create symlinks instead of copying
  --list          List available skills
  --help          Show this help message

Examples:
  node bin/install-skills.js --all          # Install to all IDEs
  node bin/install-skills.js --claude       # Install only to Claude Code
  node bin/install-skills.js --cursor --claude  # Install to multiple IDEs
  node bin/install-skills.js --link --all   # Create symlinks for all IDEs
`);
}

function main() {
    const args = process.argv.slice(2);

    if (args.length === 0 || args.includes('--help')) {
        showHelp();
        return;
    }

    if (args.includes('--list')) {
        listSkills();
        return;
    }

    const useSymlink = args.includes('--link');

    const targets = [];
    if (args.includes('--all')) {
        targets.push(...Object.keys(TARGET_SKILLS_DIRS));
    } else {
        for (const [ideName] of Object.entries(TARGET_SKILLS_DIRS)) {
            if (args.includes(`--${ideName}`)) {
                targets.push(ideName);
            }
        }
    }

    if (targets.length === 0) {
        log('No target IDE specified. Use --all or specific IDE flags.', 'error');
        showHelp();
        return;
    }

    if (useSymlink) {
        log('Using symlink mode (recommended for development)', 'info');
        createSymlinkToAll();
    } else {
        log('Using copy mode', 'info');
        for (const ideName of targets) {
            installToIDE(ideName, TARGET_SKILLS_DIRS[ideName]);
        }
    }
}

main();
