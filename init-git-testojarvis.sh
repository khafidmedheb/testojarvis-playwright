#!/bin/bash

################################################################################
# Git Repository Initialization Script for TestoJarvis Playwright Assistant
################################################################################
#
# Author: Khalid HAFID-MEDHEB
# Created: June 12, 2025
# Last Updated: June 12, 2025
#
# Description:
# This shell script automates the initialization of a local Git repository and
# pushes it to a remote GitHub repository using SSH authentication. It handles
# the complete workflow from git init to the first push, including proper branch
# setup and remote configuration.
#
# Features:
# - Initializes a new Git repository if none exists
# - Stages all files in the current directory
# - Creates an initial commit with a descriptive message
# - Sets up the main branch as the default branch
# - Configures SSH remote origin for GitHub
# - Pushes the repository to GitHub with upstream tracking
#
# Requirements:
# - Git installed and configured
# - SSH key set up for GitHub authentication
# - Proper permissions for the target GitHub repository
# - Bash shell environment
#
# Usage:
#     chmod +x init_git_testojarvis.sh
#     ./init_git_testojarvis.sh
#
# Notes:
# - The script should be run from the project root directory
# - Existing remote origins will be removed and reconfigured
# - Failed commits (no changes) are handled gracefully
# - Script will exit on any critical error
#
################################################################################

# Enable strict error handling
set -e  # Exit immediately if a command exits with a non-zero status
set -u  # Treat unset variables as an error

# Repository configuration constants
readonly REPO_NAME="testojarvis-playwright"  # Name of the GitHub repository
readonly USERNAME="khafidmedheb"             # GitHub username
readonly REMOTE_URL="git@github.com:${USERNAME}/${REPO_NAME}.git"  # SSH URL for GitHub remote

# Global variable for commit message
COMMIT_MESSAGE=""  # Will be set by get_commit_message function

# Color codes for better output formatting
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

################################################################################
# Function: print_message
# Description: Print colored messages to stdout
# Arguments:
#   $1 - Color code
#   $2 - Message to print
################################################################################
print_message() {
    local color="$1"
    local message="$2"
    echo -e "${color}${message}${NC}"
}

################################################################################
# Function: run_cmd
# Description: Execute a command with error handling and logging
# Arguments:
#   $1 - Command to execute
#   $2 - Optional: "ignore_error" to continue on failure
# Returns:
#   0 on success, 1 on failure (unless ignore_error is set)
################################################################################
run_cmd() {
    local cmd="$1"
    local ignore_error="${2:-}"
    
    print_message "$BLUE" "Executing: $cmd"
    
    if [[ "$ignore_error" == "ignore_error" ]]; then
        # Execute command and capture exit code without stopping script
        if ! eval "$cmd" 2>/dev/null; then
            print_message "$YELLOW" "Command failed (ignored): $cmd"
            return 1
        fi
    else
        # Execute command and stop script on failure
        if ! eval "$cmd"; then
            print_message "$RED" "Command failed: $cmd"
            exit 1
        fi
    fi
    
    return 0
}

################################################################################
# Function: check_git_installed
# Description: Verify that Git is installed and accessible
################################################################################
check_git_installed() {
    if ! command -v git &> /dev/null; then
        print_message "$RED" "Error: Git is not installed or not in PATH"
        exit 1
    fi
    
    print_message "$GREEN" "Git is installed: $(git --version)"
}

################################################################################
# Function: init_git_repo
# Description: Initialize Git repository if it doesn't exist
################################################################################
init_git_repo() {
    # Check if .git directory exists (indicates existing Git repository)
    if [[ ! -d ".git" ]]; then
        print_message "$BLUE" "Initializing new Git repository..."
        run_cmd "git init"
        print_message "$GREEN" "Git repository initialized successfully"
    else
        print_message "$YELLOW" "Git repository already exists, skipping initialization"
    fi
}

################################################################################
# Function: stage_files
# Description: Add all files to Git staging area
################################################################################
stage_files() {
    print_message "$BLUE" "Staging all files for commit..."
    # Add all files and directories to staging area
    # The dot (.) represents all files in current directory and subdirectories
    run_cmd "git add ."
    print_message "$GREEN" "All files staged successfully"
}

################################################################################
# Function: get_commit_message
# Description: Prompt the user to enter a custom commit message or use the default
# Returns:
#   Sets the global variable COMMIT_MESSAGE with the chosen message
################################################################################
get_commit_message() {
    local default_message="🚀 First commit – Init TestoJarvis Playwright Assistant"
    
    echo
    print_message "$BLUE" "📝 Commit Message Configuration"
    echo "=================================================="
    print_message "$YELLOW" "Default commit message: $default_message"
    echo
    echo "Options:"
    echo "1. Press ENTER to use the default message"
    echo "2. Type a custom commit message"
    echo "--------------------------------------------------"
    
    # Prompt user for input
    read -p "Enter your commit message (or press ENTER for default): " user_input
    
    # Process the input
    if [[ -n "$user_input" ]]; then
        # Check if custom message starts with an emoji
        if [[ ! "$user_input" =~ ^[🚀✨🎉📝🔧🐛💫] ]]; then
            COMMIT_MESSAGE="🚀 $user_input"
        else
            COMMIT_MESSAGE="$user_input"
        fi
        print_message "$GREEN" "✅ Using custom commit message: $COMMIT_MESSAGE"
    else
        COMMIT_MESSAGE="$default_message"
        print_message "$GREEN" "✅ Using default commit message: $COMMIT_MESSAGE"
    fi
    
    echo
}

################################################################################
# Function: create_initial_commit
# Description: Create the first commit with the user-specified message
################################################################################
create_initial_commit() {
    print_message "$BLUE" "Creating initial commit..."
    
    # Get the commit message from user input
    # This allows customization of the initial commit message
    get_commit_message
    
    # Attempt to create commit with the user-specified message
    # Use ignore_error to prevent script from stopping if commit fails
    if run_cmd "git commit -m \"$COMMIT_MESSAGE\"" "ignore_error"; then
        print_message "$GREEN" "Initial commit created successfully with message: $COMMIT_MESSAGE"
    else
        print_message "$YELLOW" "No changes to commit, continuing..."
    fi
}

################################################################################
# Function: setup_main_branch
# Description: Ensure the default branch is named 'main'
################################################################################
setup_main_branch() {
    print_message "$BLUE" "Setting up main branch..."
    
    # Force the current branch to be renamed to 'main'
    # This ensures consistency with GitHub's default branch naming convention
    run_cmd "git branch -M main"
    print_message "$GREEN" "Main branch configured successfully"
}

################################################################################
# Function: configure_remote
# Description: Set up the GitHub remote repository connection
################################################################################
configure_remote() {
    print_message "$BLUE" "Configuring remote repository..."
    
    # Remove existing 'origin' remote if it exists to avoid conflicts
    # Use ignore_error because it's normal for origin to not exist initially
    run_cmd "git remote remove origin" "ignore_error"
    
    # Add the GitHub repository as the 'origin' remote using SSH
    # This configures the destination for git push operations
    run_cmd "git remote add origin ${REMOTE_URL}"
    
    print_message "$GREEN" "Remote SSH configured: ${REMOTE_URL}"
}

################################################################################
# Function: push_to_github
# Description: Push the local repository to GitHub with upstream tracking
################################################################################
push_to_github() {
    print_message "$BLUE" "Pushing repository to GitHub..."
    
    # Push the local 'main' branch to remote 'origin'
    # The -u flag sets up upstream tracking for future pushes
    # This allows using just 'git push' without specifying remote and branch
    run_cmd "git push -u origin main"
    
    print_message "$GREEN" "Repository pushed successfully to GitHub: ${REMOTE_URL}"
}

################################################################################
# Function: main
# Description: Main function that orchestrates the entire Git setup process
################################################################################
main() {
    print_message "$BLUE" "🚀 Starting Git repository initialization process..."
    echo
    
    # Change to the directory containing this script
    # This ensures we're working in the correct project directory
    # ${BASH_SOURCE[0]} gets the path of the current script
    cd "$(dirname "${BASH_SOURCE[0]}")"
    print_message "$BLUE" "Working directory: $(pwd)"
    echo
    
    # Execute the Git setup workflow step by step
    check_git_installed      # Verify Git is available
    init_git_repo           # Initialize repository if needed
    stage_files             # Add all files to staging area
    create_initial_commit   # Get commit message from user and create first commit
    setup_main_branch       # Configure main branch
    configure_remote        # Set up GitHub remote
    push_to_github          # Push to GitHub
    
    echo
    print_message "$GREEN" "✅ Git repository initialization completed successfully!"
    print_message "$GREEN" "Repository URL: ${REMOTE_URL}"
}

################################################################################
# Script execution entry point
# Only run main function if script is executed directly (not sourced)
################################################################################
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi