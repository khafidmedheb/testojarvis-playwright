#!/usr/bin/env python3
"""
================================================================================
Git Repository Initialization Script for TestoJarvis Playwright Assistant
================================================================================

Author: Khalid HAFID-MEDHEB
Created: June 12, 2025
Last Updated: June 12, 2025

Description:
This script automates the initialization of a local Git repository and pushes
it to a remote GitHub repository using SSH authentication. It handles the
complete workflow from git init to the first push, including proper branch
setup and remote configuration.

Features:
- Initializes a new Git repository if none exists
- Stages all files in the current directory
- Creates an initial commit with a descriptive message
- Sets up the main branch as the default branch
- Configures SSH remote origin for GitHub
- Pushes the repository to GitHub with upstream tracking

Requirements:
- Git installed and configured
- SSH key set up for GitHub authentication
- Proper permissions for the target GitHub repository

Usage:
    python init_git_testojarvis.py

Notes:
- The script should be run from the project root directory
- Existing remote origins will be removed and reconfigured
- Failed commits (no changes) are handled gracefully
================================================================================
"""

import os
import subprocess
import sys

# Repository configuration constants
REPO_NAME = "testojarvis-playwright"  # Name of the GitHub repository
USERNAME = "khafidmedheb"             # GitHub username
REMOTE_URL = f"git@github.com:{USERNAME}/{REPO_NAME}.git"  # SSH URL for GitHub remote

def run_cmd(cmd, check=True, capture_output=False):
    """
    Execute a shell command with error handling and optional output capture.
    
    Args:
        cmd (str): The shell command to execute
        check (bool): Whether to raise an exception on command failure
        capture_output (bool): Whether to capture and return stdout
    
    Returns:
        str or None: Command output if capture_output=True, otherwise None
    
    Raises:
        subprocess.CalledProcessError: If command fails and check=True
    """
    result = subprocess.run(cmd, shell=True, check=check, text=True, capture_output=capture_output)
    return result.stdout.strip() if capture_output else None

def get_commit_message():
    """
    Prompt the user to enter a custom commit message or use the default.
    
    Returns:
        str: The commit message to use for the initial commit
    """
    print("\n📝 Commit Message Configuration")
    print("=" * 50)
    
    default_message = "🚀 First commit – Init TestoJarvis Playwright Assistant"
    print(f"Default commit message: {default_message}")
    print("\nOptions:")
    print("1. Press ENTER to use the default message")
    print("2. Type a custom commit message")
    print("-" * 50)
    
    # Prompt user for input
    user_input = input("Enter your commit message (or press ENTER for default): ").strip()
    
    # Return custom message if provided, otherwise return default
    if user_input:
        # Add emoji if the custom message doesn't start with one
        if not user_input.startswith(("🚀", "✨", "🎉", "📝", "🔧", "🐛", "💫")):
            commit_message = f"🚀 {user_input}"
        else:
            commit_message = user_input
        print(f"✅ Using custom commit message: {commit_message}")
        return commit_message
    else:
        print(f"✅ Using default commit message: {default_message}")
        return default_message

def main():
    """
    Main function that orchestrates the Git repository initialization process.
    
    This function performs the following steps:
    1. Changes to the script's directory
    2. Initializes Git repository if needed
    3. Stages all files
    4. Gets commit message from user input
    5. Creates initial commit with the specified message
    6. Sets up main branch
    7. Configures remote origin
    8. Pushes to GitHub
    """
    print("🚀 Initialisation du dépôt Git local...")

    # Change to the directory containing this script
    # This ensures we're working in the correct project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Initialize Git repository if .git directory doesn't exist
    # This check prevents reinitializing an existing repository
    if not os.path.isdir(".git"):
        run_cmd("git init")  # Create new Git repository

    # Stage all files in the current directory for commit
    # The dot (.) represents all files and subdirectories
    run_cmd("git add .")

    # Get the commit message from user input
    # This allows customization of the initial commit message
    commit_message = get_commit_message()

    # Attempt to create the initial commit with the user-specified message
    # Using try-except to handle case where no changes exist to commit
    try:
        # Escape quotes in commit message to prevent shell injection
        escaped_message = commit_message.replace('"', '\\"')
        run_cmd(f'git commit -m "{escaped_message}"')
        print(f"✅ Commit created successfully with message: {commit_message}")
    except subprocess.CalledProcessError:
        # If git commit fails (usually because no changes to commit), 
        # we handle it gracefully and continue
        print("⚠️ Aucun changement à commiter.")

    # Force the current branch to be named 'main'
    # This ensures consistency with GitHub's default branch naming
    run_cmd("git branch -M main")

    # Remove existing 'origin' remote if it exists
    # This prevents conflicts when setting up the new remote
    try:
        run_cmd("git remote remove origin")
    except subprocess.CalledProcessError:
        # If remote 'origin' doesn't exist, the command fails
        # This is expected behavior, so we ignore the error
        pass

    # Add the GitHub repository as the 'origin' remote using SSH
    # This configures where git push will send commits
    run_cmd(f"git remote add origin {REMOTE_URL}")
    print(f"🔗 Remote SSH configuré : {REMOTE_URL}")

    # Push the local 'main' branch to the remote 'origin'
    # The -u flag sets up tracking so future pushes can use just 'git push'
    run_cmd("git push -u origin main")

    # Success message with the remote URL for confirmation
    print(f"✅ Projet poussé via SSH sur GitHub : {REMOTE_URL}")

# Standard Python idiom to run main() only when script is executed directly
# This prevents main() from running if the script is imported as a module
if __name__ == "__main__":
    main()