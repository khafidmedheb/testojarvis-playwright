import os
import subprocess
import sys

REPO_NAME = "testojarvis-playwright"
USERNAME = "khafidmedheb"
REMOTE_URL = f"git@github.com:{USERNAME}/{REPO_NAME}.git"

def run_cmd(cmd, check=True, capture_output=False):
    result = subprocess.run(cmd, shell=True, check=check, text=True, capture_output=capture_output)
    return result.stdout.strip() if capture_output else None

def main():
    print("🚀 Initialisation du dépôt Git local...")

    # Se placer dans le répertoire du script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Initialiser git si non déjà fait
    if not os.path.isdir(".git"):
        run_cmd("git init")

    # Ajouter tous les fichiers
    run_cmd("git add .")

    # Premier commit
    try:
        run_cmd('git commit -m "🚀 First commit – Init TestoJarvis Playwright Assistant"')
    except subprocess.CalledProcessError:
        # Si pas de modification à commit, git commit échoue, on ignore
        print("⚠️ Aucun changement à commiter.")

    # Forcer la branche main
    run_cmd("git branch -M main")

    # Supprimer le remote origin s'il existe déjà
    try:
        run_cmd("git remote remove origin")
    except subprocess.CalledProcessError:
        # Pas grave si le remote n'existait pas
        pass

    # Ajouter le remote SSH
    run_cmd(f"git remote add origin {REMOTE_URL}")
    print(f"🔗 Remote SSH configuré : {REMOTE_URL}")

    # Pousser le projet sur la branche main
    run_cmd("git push -u origin main")

    print(f"✅ Projet poussé via SSH sur GitHub : {REMOTE_URL}")

if __name__ == "__main__":
    main()
