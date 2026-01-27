# Dremio Skill Installation Script (PowerShell)
# Supports Global (Symlink) and Local (Copy) installation modes for Antigravity, Claude Code, and Cursor.

$SKILL_DIR_NAME = "dremio-skill"
$SOURCE_SKILL_PATH = Join-Path -Path (Get-Location) -ChildPath $SKILL_DIR_NAME

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "   Dremio Agent Skill Installer         " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

if (-not (Test-Path $SOURCE_SKILL_PATH)) {
    Write-Host "Error: Cannot find '$SKILL_DIR_NAME' in current directory." -ForegroundColor Yellow
    Write-Host "Please run this script from the root of the 'dremio-agent-skill' repo."
    exit
}

Write-Host ""
Write-Host "Select installation mode:"
Write-Host "1) Global Install (Symlink)"
Write-Host "   - Links repo to ~/.agent/skills & ~/.claude/skills"
Write-Host "   - Best for using this specific repo as the single source of truth."
Write-Host ""
Write-Host "2) Local Project Install (Copy)"
Write-Host "   - Copies 'dremio-skill' to a target project."
Write-Host "   - Sets up .cursorrules."
Write-Host "   - Configures local .agent/.claude folders for project-specific context."
Write-Host ""

$choice = Read-Host "Enter choice [1 or 2]"

if ($choice -eq "1") {
    # --- GLOBAL INSTALL ---
    Write-Host "`n--- Global Installation ---" -ForegroundColor Cyan

    # Antigravity
    $AGENT_SKILLS_DIR = Join-Path -Path $HOME -ChildPath ".agent\skills"
    if (-not (Test-Path $AGENT_SKILLS_DIR)) { New-Item -ItemType Directory -Force -Path $AGENT_SKILLS_DIR | Out-Null }
    
    $AGENT_TARGET = Join-Path -Path $AGENT_SKILLS_DIR -ChildPath $SKILL_DIR_NAME
    if (Test-Path $AGENT_TARGET) {
        Write-Host "Warning: '$AGENT_TARGET' already exists. Skipping Antigravity link." -ForegroundColor Yellow
    } else {
        New-Item -ItemType Junction -Path $AGENT_TARGET -Target $SOURCE_SKILL_PATH | Out-Null
        Write-Host "✔ Linked to Antigravity: $AGENT_TARGET" -ForegroundColor Green
    }

    # Claude Code
    $CLAUDE_SKILLS_DIR = Join-Path -Path $HOME -ChildPath ".claude\skills"
    if (-not (Test-Path $CLAUDE_SKILLS_DIR)) { New-Item -ItemType Directory -Force -Path $CLAUDE_SKILLS_DIR | Out-Null }

    $CLAUDE_TARGET = Join-Path -Path $CLAUDE_SKILLS_DIR -ChildPath $SKILL_DIR_NAME
    if (Test-Path $CLAUDE_TARGET) {
        Write-Host "Warning: '$CLAUDE_TARGET' already exists. Skipping Claude link." -ForegroundColor Yellow
    } else {
        New-Item -ItemType Junction -Path $CLAUDE_TARGET -Target $SOURCE_SKILL_PATH | Out-Null
        Write-Host "✔ Linked to Claude Code: $CLAUDE_TARGET" -ForegroundColor Green
    }

    Write-Host "`nGlobal installation complete!" -ForegroundColor Green

} elseif ($choice -eq "2") {
    # --- LOCAL INSTALL ---
    Write-Host "`n--- Local Project Installation ---" -ForegroundColor Cyan
    $target_input = Read-Host "Enter path to target project (default: current dir)"
    if ([string]::IsNullOrWhiteSpace($target_input)) { $target_input = "." }

    $target_dir = Resolve-Path $target_input
    
    if (-not (Test-Path $target_dir)) {
        Write-Host "Error: Target directory '$target_dir' does not exist." -ForegroundColor Yellow
        exit
    }

    Write-Host "Installing to: $target_dir"

    # Copy Skill Folder
    $DEST_SKILL = Join-Path -Path $target_dir -ChildPath $SKILL_DIR_NAME
    Copy-Item -Recurse -Force -Path $SOURCE_SKILL_PATH -Destination $DEST_SKILL
    Write-Host "✔ Copied 'dremio-skill' folder." -ForegroundColor Green

    # Copy Cursor Rules
    $CURSOR_RULES_SRC = Join-Path -Path $SOURCE_SKILL_PATH -ChildPath "rules\.cursorrules"
    $CURSOR_RULES_DEST = Join-Path -Path $target_dir -ChildPath ".cursorrules"
    if (Test-Path $CURSOR_RULES_SRC) {
        Copy-Item -Force -Path $CURSOR_RULES_SRC -Destination $CURSOR_RULES_DEST
        Write-Host "✔ Installed .cursorrules." -ForegroundColor Green
    }

    # Setup Local .agent symlink (Using Junction for reliability on Windows)
    $LOCAL_AGENT_DIR = Join-Path -Path $target_dir -ChildPath ".agent\skills"
    if (-not (Test-Path $LOCAL_AGENT_DIR)) { New-Item -ItemType Directory -Force -Path $LOCAL_AGENT_DIR | Out-Null }
    
    $LOCAL_AGENT_LINK = Join-Path -Path $LOCAL_AGENT_DIR -ChildPath $SKILL_DIR_NAME
    # Need absolute path for Junction, so we point to the COPIED folder in the project
    New-Item -ItemType Junction -Path $LOCAL_AGENT_LINK -Target $DEST_SKILL | Out-Null
    Write-Host "✔ Configured Antigravity (Local)" -ForegroundColor Green

    # Setup Local .claude symlink
    $LOCAL_CLAUDE_DIR = Join-Path -Path $target_dir -ChildPath ".claude\skills"
    if (-not (Test-Path $LOCAL_CLAUDE_DIR)) { New-Item -ItemType Directory -Force -Path $LOCAL_CLAUDE_DIR | Out-Null }

    $LOCAL_CLAUDE_LINK = Join-Path -Path $LOCAL_CLAUDE_DIR -ChildPath $SKILL_DIR_NAME
    New-Item -ItemType Junction -Path $LOCAL_CLAUDE_LINK -Target $DEST_SKILL | Out-Null
    Write-Host "✔ Configured Claude Code (Local)" -ForegroundColor Green

    Write-Host "`nLocal installation complete!" -ForegroundColor Green
    Write-Host "You can now commit 'dremio-skill' and '.cursorrules' to your project."

} else {
    Write-Host "Invalid choice. Exiting."
    exit
}
