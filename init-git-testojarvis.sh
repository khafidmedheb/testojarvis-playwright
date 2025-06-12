#!/bin/bash

REPO_NAME="testojarvis-playwright"
USERNAME="khafidmedheb"
REMOTE_URL="git@github.com:$USERNAME/$REPO_NAME.git"

echo "🚀 Initialisation du dépôt Git local..."

cd "$(dirname "$0")"

# Initialiser Git si non déjà fait
if [ ! -d ".git" ]; then
  git init
fi

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "🚀 First commit – Init TestoJarvis Playwright Assistant"

# Forcer la branche main
git branch -M main

# Supprimer le remote origin s'il existe déjà
git remote remove origin 2>/dev/null

# Ajouter le remote SSH
git remote add origin "$REMOTE_URL"
echo "🔗 Remote SSH configuré : $REMOTE_URL"

# Pousser le projet sur la branche main
git push -u origin main

echo "✅ Projet poussé via SSH sur GitHub : $REMOTE_URL"
