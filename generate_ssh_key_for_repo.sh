#!/bin/bash

################################################################################
# Author      : Khalid HAFID-MEDHEB
# Created on  : 2025-06-04
# Last update : 2025-06-04
# Description : This script generates a new SSH key, copies it to clipboard,
#               adds it to the local SSH agent, and uploads it to your GitHub
#               account using the API. It also tests SSH access to GitHub.
################################################################################

# ANSI color codes for styled terminal output
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ------------------------------------------------------------------------------
#                           INPUTS FROM THE USER
# ------------------------------------------------------------------------------

# Ask for the GitHub repository name (e.g., user/repo)
read -p "GitHub repository name (format: user/repo): " REPO_NAME

# Ask for GitHub token (PAT with 'admin:public_key' scope)
read -p "Your GitHub Personal Access Token (PAT with 'admin:public_key' scope): " GITHUB_TOKEN

# Ask for the title to be associated with the SSH key in GitHub
read -p "Title for the SSH key (e.g., work-laptop-key): " KEY_TITLE

# Extract GitHub username from the repository name
GITHUB_USER=$(echo "$REPO_NAME" | cut -d'/' -f1)

# Define SSH key filenames
KEY_NAME="id_rsa_${GITHUB_USER}"
SSH_DIR="$HOME/.ssh"
KEY_PATH="$SSH_DIR/$KEY_NAME"
PUB_KEY="${KEY_PATH}.pub"

# ------------------------------------------------------------------------------
#                        GENERATE SSH KEY PAIR
# ------------------------------------------------------------------------------

# Ensure the .ssh directory exists and is secured
mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"

# Generate a new RSA 4096 SSH key pair
ssh-keygen -t rsa -b 4096 -f "$KEY_PATH" -C "$REPO_NAME" -N ""

# ------------------------------------------------------------------------------
#                          COPY PUBLIC KEY TO CLIPBOARD
# ------------------------------------------------------------------------------

# Try to copy the public key to clipboard using available tools
if command -v pbcopy &> /dev/null; then
    cat "$PUB_KEY" | pbcopy
    echo -e "${GREEN}[INFO] Public key copied to clipboard (pbcopy).${NC}"
elif command -v xclip &> /dev/null; then
    cat "$PUB_KEY" | xclip -selection clipboard
    echo -e "${GREEN}[INFO] Public key copied to clipboard (xclip).${NC}"
elif command -v wl-copy &> /dev/null; then
    cat "$PUB_KEY" | wl-copy
    echo -e "${GREEN}[INFO] Public key copied to clipboard (wl-copy).${NC}"
else
    echo -e "${YELLOW}[WARNING] No clipboard tool found. Here's your public key:${NC}"
    cat "$PUB_KEY"
fi

# ------------------------------------------------------------------------------
#                           ADD KEY TO SSH AGENT
# ------------------------------------------------------------------------------

# Start the SSH agent and add the newly created key
eval "$(ssh-agent -s)"
ssh-add "$KEY_PATH"

# ------------------------------------------------------------------------------
#                         UPLOAD SSH KEY TO GITHUB
# ------------------------------------------------------------------------------

# Read public key content
PUB_KEY_CONTENT=$(cat "$PUB_KEY")

echo -e "\n[INFO] Attempting to add the SSH key to your GitHub account..."

# Make a POST request to GitHub API to upload the SSH key
RESPONSE=$(curl -s -o /tmp/github_add_key_response.json -w "%{http_code}" \
  -X POST https://api.github.com/user/keys \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d "{\"title\":\"$KEY_TITLE\",\"key\":\"$PUB_KEY_CONTENT\"}"
)

# Handle GitHub API response
if [ "$RESPONSE" == "201" ]; then
    echo -e "${GREEN}[SUCCESS] SSH key successfully added to your GitHub account.${NC}"
else
    echo -e "${RED}[ERROR] Failed to add SSH key to GitHub (HTTP $RESPONSE).${NC}"
    cat /tmp/github_add_key_response.json
fi

# ------------------------------------------------------------------------------
#                       TEST SSH CONNECTION TO GITHUB
# ------------------------------------------------------------------------------

echo -e "\n[INFO] Testing SSH connection to GitHub..."

# Attempt SSH connection and save output
ssh -T git@github.com &> /tmp/ssh_test_output

# Check for success message
if grep -q "successfully authenticated" /tmp/ssh_test_output || grep -q "Hi " /tmp/ssh_test_output; then
    echo -e "${GREEN}[SUCCESS] SSH connection to GitHub successful!${NC}"
else
    echo -e "${RED}[ERROR] SSH connection to GitHub failed. Make sure the key is added and active.${NC}"
    cat /tmp/ssh_test_output
fi

# ------------------------------------------------------------------------------
#                                CLEANUP
# ------------------------------------------------------------------------------

# Remove temporary files
rm -f /tmp/ssh_test_output /tmp/github_add_key_response.json
