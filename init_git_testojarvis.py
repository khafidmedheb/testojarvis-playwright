from dotenv import load_dotenv
import os
import subprocess
import random
import re
from datetime import datetime
from collections import defaultdict

load_dotenv()

# === CONFIG ===
REPO_NAME = "testojarvis-playwright"
USERNAME = "khafidmedheb"
REMOTE_URL = f"git@github.com:{USERNAME}/{REPO_NAME}.git"

# === UTILS ===

def run(cmd):
    """Exécute une commande shell et retourne le résultat"""
    return subprocess.run(
        cmd,
        shell=True,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

def get_git_status():
    """Récupère le statut détaillé des fichiers modifiés"""
    result = run("git diff --cached --name-status")
    return result.stdout.strip()

def get_file_extensions(files_status):
    """Analyse les extensions de fichiers pour déterminer le type de changements"""
    extensions = defaultdict(int)
    files = []
    
    for line in files_status.split('\n'):
        if line.strip():
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                status = parts[0]
                filename = parts[1]
                files.append((status, filename))
                
                # Extraire l'extension
                if '.' in filename:
                    ext = filename.split('.')[-1].lower()
                    extensions[ext] += 1
    
    return files, dict(extensions)

def get_project_type(extensions):
    """Détermine le type de projet basé sur les extensions"""
    if any(ext in extensions for ext in ['py', 'pyx', 'pyi']):
        return 'python'
    elif any(ext in extensions for ext in ['js', 'ts', 'jsx', 'tsx']):
        return 'javascript'
    elif any(ext in extensions for ext in ['html', 'css', 'scss']):
        return 'web'
    elif any(ext in extensions for ext in ['java', 'kt', 'scala']):
        return 'jvm'
    elif any(ext in extensions for ext in ['cpp', 'c', 'h', 'hpp']):
        return 'cpp'
    elif any(ext in extensions for ext in ['rs']):
        return 'rust'
    elif any(ext in extensions for ext in ['go']):
        return 'go'
    elif any(ext in extensions for ext in ['md', 'txt', 'rst']):
        return 'docs'
    elif any(ext in extensions for ext in ['json', 'yml', 'yaml', 'toml']):
        return 'config'
    else:
        return 'general'

def analyze_changes(files):
    """Analyse les types de changements (ajout, modification, suppression)"""
    added = sum(1 for status, _ in files if status == 'A')
    modified = sum(1 for status, _ in files if status == 'M')
    deleted = sum(1 for status, _ in files if status == 'D')
    renamed = sum(1 for status, _ in files if status.startswith('R'))
    
    return {
        'added': added,
        'modified': modified,
        'deleted': deleted,
        'renamed': renamed,
        'total': len(files)
    }

def get_smart_emoji(project_type, changes, extensions):
    """Sélectionne un emoji approprié basé sur le contexte"""
    emoji_map = {
        'python': ['🐍', '🔧', '⚡', '🚀'],
        'javascript': ['⚡', '🚀', '✨', '🔧'],
        'web': ['🎨', '💄', '✨', '🌐'],
        'docs': ['📝', '📚', '📖', '✏️'],
        'config': ['⚙️', '🔧', '🛠️', '📦'],
        'rust': ['🦀', '⚡', '🔧', '🚀'],
        'go': ['🐹', '⚡', '🚀', '🔧'],
        'general': ['✨', '🔧', '📦', '🚀']
    }
    
    # Choix spécial basé sur les types de changements
    if changes['added'] > changes['modified']:
        return random.choice(['✨', '🎉', '🚀', '💫'])
    elif changes['deleted'] > 0:
        return random.choice(['🗑️', '🧹', '🔥', '✂️'])
    elif 'test' in str(extensions) or any('test' in f[1] for f in changes if isinstance(changes, list)):
        return random.choice(['🧪', '✅', '🔬', '🎯'])
    
    return random.choice(emoji_map.get(project_type, emoji_map['general']))

def generate_commit_templates():
    """Génère des templates de messages de commit variés"""
    templates = {
        'feature': [
            "{emoji} Add {description}",
            "{emoji} Implement {description}",
            "{emoji} Introduce {description}",
            "{emoji} Create {description}",
        ],
        'fix': [
            "{emoji} Fix {description}",
            "{emoji} Resolve {description}",
            "{emoji} Patch {description}",
            "{emoji} Correct {description}",
        ],
        'update': [
            "{emoji} Update {description}",
            "{emoji} Improve {description}",
            "{emoji} Enhance {description}",
            "{emoji} Refactor {description}",
        ],
        'docs': [
            "{emoji} Update documentation",
            "{emoji} Add documentation for {description}",
            "{emoji} Improve docs",
            "{emoji} Document {description}",
        ],
        'config': [
            "{emoji} Update configuration",
            "{emoji} Adjust settings",
            "{emoji} Configure {description}",
            "{emoji} Setup {description}",
        ],
        'initial': [
            "{emoji} Initial commit",
            "{emoji} Project setup",
            "{emoji} Bootstrap project",
            "{emoji} Initial implementation",
        ]
    }
    return templates

def get_file_description(files, extensions):
    """Génère une description basée sur les fichiers modifiés"""
    if len(files) == 1:
        filename = files[0][1]
        if '/' in filename:
            return filename.split('/')[-1]
        return filename
    
    # Descriptions basées sur les extensions
    if 'py' in extensions:
        return "Python modules"
    elif any(ext in extensions for ext in ['js', 'ts']):
        return "JavaScript components"
    elif 'html' in extensions:
        return "HTML templates"
    elif 'css' in extensions:
        return "stylesheets"
    elif 'md' in extensions:
        return "documentation"
    elif any(ext in extensions for ext in ['json', 'yml', 'yaml']):
        return "configuration files"
    elif len(files) <= 3:
        return f"{len(files)} files"
    else:
        return f"multiple files ({len(files)} total)"

def generate_smart_commit_message(files_status):
    """Génère un message de commit intelligent sans IA externe"""
    if not files_status:
        return "📦 Update project files"
    
    files, extensions = get_file_extensions(files_status)
    if not files:
        return "📦 Update project files"
    
    project_type = get_project_type(extensions)
    changes = analyze_changes(files)
    emoji = get_smart_emoji(project_type, changes, extensions)
    templates = generate_commit_templates()
    
    # Déterminer le type de commit
    if changes['total'] == changes['added'] and changes['total'] > 5:
        commit_type = 'initial'
    elif any('readme' in f[1].lower() or 'doc' in f[1].lower() for f in files):
        commit_type = 'docs'
    elif any(ext in ['json', 'yml', 'yaml', 'toml', 'ini'] for ext in extensions):
        commit_type = 'config'
    elif changes['added'] > changes['modified']:
        commit_type = 'feature'
    elif changes['deleted'] > 0:
        commit_type = 'fix'
    else:
        commit_type = 'update'
    
    # Sélectionner un template
    template = random.choice(templates[commit_type])
    description = get_file_description(files, extensions)
    
    # Générer le message final
    message = template.format(emoji=emoji, description=description)
    
    # Ajouter des détails si pertinents
    details = []
    if changes['added'] > 0:
        details.append(f"+ {changes['added']} files")
    if changes['modified'] > 0:
        details.append(f"~ {changes['modified']} files")
    if changes['deleted'] > 0:
        details.append(f"- {changes['deleted']} files")
    
    if details and len(details) > 1:
        message += f" ({', '.join(details)})"
    
    return message

def add_timestamp_variant():
    """Ajoute une variation basée sur l'heure pour éviter les doublons"""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        return " (morning update)"
    elif 12 <= hour < 18:
        return " (afternoon changes)"
    elif 18 <= hour < 22:
        return " (evening work)"
    else:
        return " (late night coding)"

# === SCRIPT PRINCIPAL ===

def create_gitignore():
    """Crée ou met à jour le fichier .gitignore avec les patterns essentiels"""
    gitignore_content = """# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
dist/
build/
*.tsbuildinfo

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv/

# Large files and binaries
*.node
*.dll
*.exe
*.bin
*.so
*.dylib

# Logs
*.log
logs/

# Cache directories
.cache/
.parcel-cache/
.next/
.nuxt/
"""
    
    if not os.path.exists('.gitignore'):
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print("📝 Created .gitignore file")
        return True
    else:
        # Vérifier si .gitignore contient node_modules
        with open('.gitignore', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'node_modules' not in content:
            with open('.gitignore', 'a', encoding='utf-8') as f:
                f.write('\n# Auto-added by git script\nnode_modules/\n*.node\n')
            print("📝 Updated .gitignore file")
            return True
    
    return False

def check_large_files():
    """Vérifie la présence de fichiers volumineux avant le commit"""
    result = run("find . -type f -size +50M 2>/dev/null || find . -type f -exec ls -l {} \\; | awk '$5 > 52428800'")
    large_files = []
    
    if result.stdout:
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                # Extraire le nom du fichier
                if 'find:' not in line and line.strip():
                    large_files.append(line.strip())
    
    return large_files

def clean_repository():
    """Nettoie le repository des fichiers problématiques"""
    print("🧹 Cleaning repository...")
    
    # Supprimer récursivement tous les node_modules
    result = run("find . -name 'node_modules' -type d")
    if result.stdout:
        print("🗑️ Removing all node_modules directories...")
        run("find . -name 'node_modules' -type d -exec rm -rf {} + 2>/dev/null || true")
    
    # Supprimer d'autres dossiers problématiques
    problematic_dirs = ['.next', 'dist', 'build', '__pycache__', '.cache', '.parcel-cache']
    for dir_name in problematic_dirs:
        result = run(f"find . -name '{dir_name}' -type d")
        if result.stdout:
            print(f"🗑️ Removing all {dir_name} directories...")
            run(f"find . -name '{dir_name}' -type d -exec rm -rf {{}} + 2>/dev/null || true")
    
    # Supprimer tous les fichiers .node
    result = run("find . -name '*.node' -type f")
    if result.stdout:
        print("🗑️ Removing all .node files...")
        run("find . -name '*.node' -type f -delete 2>/dev/null || true")
    
    # Supprimer autres fichiers volumineux courants
    large_patterns = ['*.exe', '*.dll', '*.bin', '*.so', '*.dylib']
    for pattern in large_patterns:
        result = run(f"find . -name '{pattern}' -size +10M")
        if result.stdout:
            print(f"🗑️ Removing large {pattern} files...")
            run(f"find . -name '{pattern}' -size +10M -delete 2>/dev/null || true")

def reset_git_history():
    """Remet à zéro l'historique Git pour éliminer les gros fichiers"""
    print("🔄 Resetting Git history...")
    
    # Sauvegarder les fichiers de config Git
    run("cp .git/config .git/config.backup 2>/dev/null || true")
    
    # Supprimer complètement .git et recommencer
    run("rm -rf .git")
    run("git init")
    
    # Restaurer la config si elle existait
    if os.path.exists('.git/config.backup'):
        run("cp .git/config.backup .git/config")
        run("rm .git/config.backup")
    
    print("✅ Git history reset successfully")

def main():
    print("🚀 Initializing advanced Git automation...")
    
    # Nettoyer le repository en premier
    clean_repository()
    
    # Créer/mettre à jour .gitignore
    gitignore_updated = create_gitignore()
    
    # Reset Git si .git existe déjà (pour nettoyer l'historique)
    if os.path.isdir(".git"):
        print("⚠️ Existing Git repository detected with potential large files")
        print("🔄 Performing complete reset to clean history...")
        reset_git_history()
    else:
        print("📁 Initializing new Git repository...")
        run("git init")
    
    # Vérifier les fichiers volumineux après nettoyage
    large_files = check_large_files()
    if large_files:
        print(f"⚠️ Warning: Still found {len(large_files)} potentially large files")
        for file in large_files[:5]:
            print(f"   📁 {file}")
        if len(large_files) > 5:
            print(f"   ... and {len(large_files) - 5} more")
        
        # Demander confirmation pour continuer
        response = input("⚠️ Continue anyway? (y/N): ").lower()
        if response != 'y':
            print("❌ Aborted by user")
            return
    
    # Ajouter tous les fichiers
    print("📦 Staging all changes...")
    run("git add .")
    
    # Analyser les changements
    files_status = get_git_status()
    if not files_status:
        print("❌ No staged changes detected after cleaning.")
        return
    
    # Générer le message de commit
    commit_msg = generate_smart_commit_message(files_status)
    
    # Ajouter une variante temporelle occasionnellement
    if random.random() < 0.3:  # 30% de chance
        commit_msg += add_timestamp_variant()
    
    print(f"💬 Generated commit message: {commit_msg}")
    
    # Effectuer le commit
    print("✍️ Committing changes...")
    result = run(f'git commit -m "{commit_msg}"')
    if result.returncode != 0:
        print(f"❌ Commit failed: {result.stderr}")
        return
    
    # Configurer la branche principale
    print("🌿 Setting up main branch...")
    run("git branch -M main")
    
    # Configurer le remote
    print("🔗 Configuring remote...")
    run("git remote remove origin 2>/dev/null || true")  # Supprimer s'il existe
    run(f"git remote add origin {REMOTE_URL}")
    
    # Pousser vers GitHub avec force (puisqu'on a reset l'historique)
    print("🚀 Pushing to GitHub...")
    result = run("git push -f -u origin main")
    if result.returncode == 0:
        print("✅ Successfully pushed to GitHub!")
        print(f"🌐 Repository: https://github.com/{USERNAME}/{REPO_NAME}")
    else:
        print(f"❌ Push failed: {result.stderr}")
        if "Large files detected" in result.stderr or "exceeds GitHub's file size limit" in result.stderr:
            print("\n🚨 Large files still detected!")
            print("📋 Files that might be causing issues:")
            
            # Lister les fichiers par taille
            result = run("find . -type f -exec ls -lh {} \\; | sort -k5 -hr | head -10")
            if result.stdout:
                for line in result.stdout.strip().split('\n')[:5]:
                    if line.strip():
                        print(f"   {line}")
            
            print("\n💡 Solutions:")
            print("   1. Add problematic files to .gitignore")
            print("   2. Use Git LFS: git lfs track '*.node'")
            print("   3. Remove files manually and re-run script")
        else:
            print("💡 Make sure your SSH key is configured and you have access to the repository")

if __name__ == "__main__":
    main()