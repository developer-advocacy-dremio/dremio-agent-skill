#!/bin/bash

# Dremio Skill Installation Script
# Supports Global (Symlink) and Local (Copy) installation modes for Antigravity, Claude Code, and Cursor.

set -e

SKILL_DIR="dremio-skill"
SOURCE_SKILL_PATH="$(pwd)/$SKILL_DIR"

# ANSI Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}   Dremio Agent Skill Installer         ${NC}"
echo -e "${BLUE}=========================================${NC}"

if [ ! -d "$SOURCE_SKILL_PATH" ]; then
    echo -e "${YELLOW}Error: Cannot find '$SKILL_DIR' in current directory.${NC}"
    echo "Please run this script from the root of the 'dremio-agent-skill' repo."
    exit 1
fi

echo ""
echo "Select installation mode:"
echo "1) Global Install (Symlink)"
echo "   - Links repo to ~/.agent/skills & ~/.claude/skills"
echo "   - Best for using this specific repo as the single source of truth."
echo ""
echo "2) Local Project Install (Copy)"
echo "   - Copies 'dremio-skill' to a target project."
echo "   - Sets up .cursorrules."
echo "   - Configures local .agent/.claude folders for project-specific context."
echo ""

read -p "Enter choice [1 or 2]: " choice

if [ "$choice" == "1" ]; then
    # --- GLOBAL INSTALL ---
    echo -e "\n${BLUE}--- Global Installation ---${NC}"

    # Antigravity
    AGENT_SKILLS_DIR="$HOME/.agent/skills"
    mkdir -p "$AGENT_SKILLS_DIR"
    
    if [ -L "$AGENT_SKILLS_DIR/$SKILL_DIR" ] || [ -d "$AGENT_SKILLS_DIR/$SKILL_DIR" ]; then
        echo -e "${YELLOW}Warning: '$AGENT_SKILLS_DIR/$SKILL_DIR' already exists. Skipping Antigravity link.${NC}"
    else
        ln -s "$SOURCE_SKILL_PATH" "$AGENT_SKILLS_DIR/$SKILL_DIR"
        echo -e "${GREEN}✔ Linked to Antigravity: $AGENT_SKILLS_DIR/$SKILL_DIR${NC}"
    fi

    # Claude Code
    CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
    mkdir -p "$CLAUDE_SKILLS_DIR"

    if [ -L "$CLAUDE_SKILLS_DIR/$SKILL_DIR" ] || [ -d "$CLAUDE_SKILLS_DIR/$SKILL_DIR" ]; then
        echo -e "${YELLOW}Warning: '$CLAUDE_SKILLS_DIR/$SKILL_DIR' already exists. Skipping Claude link.${NC}"
    else
        ln -s "$SOURCE_SKILL_PATH" "$CLAUDE_SKILLS_DIR/$SKILL_DIR"
        echo -e "${GREEN}✔ Linked to Claude Code: $CLAUDE_SKILLS_DIR/$SKILL_DIR${NC}"
    fi

    echo -e "\n${GREEN}Global installation complete!${NC}"

elif [ "$choice" == "2" ]; then
    # --- LOCAL INSTALL ---
    echo -e "\n${BLUE}--- Local Project Installation ---${NC}"
    read -p "Enter path to target project (default: current dir): " target_dir
    target_dir=${target_dir:-.}

    # Expand absolute path
    target_dir=$(realpath "$target_dir")
    
    if [ ! -d "$target_dir" ]; then
        echo -e "${YELLOW}Error: Target directory '$target_dir' does not exist.${NC}"
        exit 1
    fi

    echo "Installing to: $target_dir"

    # Copy Skill Folder
    cp -r "$SOURCE_SKILL_PATH" "$target_dir/"
    echo -e "${GREEN}✔ Copied 'dremio-skill' folder.${NC}"

    # Copy Cursor Rules
    if [ -f "$SOURCE_SKILL_PATH/rules/.cursorrules" ]; then
        cp "$SOURCE_SKILL_PATH/rules/.cursorrules" "$target_dir/.cursorrules"
        echo -e "${GREEN}✔ Installed .cursorrules.${NC}"
    fi

    # Setup Local .agent symlink
    mkdir -p "$target_dir/.agent/skills"
    # We link the relative copied folder, not the original repo
    ln -sf "../../$SKILL_DIR" "$target_dir/.agent/skills/$SKILL_DIR"
    echo -e "${GREEN}✔ Configured Antigravity (Local)${NC}"

    # Setup Local .claude symlink
    mkdir -p "$target_dir/.claude/skills"
    ln -sf "../../$SKILL_DIR" "$target_dir/.claude/skills/$SKILL_DIR"
    echo -e "${GREEN}✔ Configured Claude Code (Local)${NC}"

    echo -e "\n${GREEN}Local installation complete!${NC}"
    echo "You can now commit 'dremio-skill' and '.cursorrules' to your project."

else
    echo "Invalid choice. Exiting."
    exit 1
fi
