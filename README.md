
# 🧪 TestoJarvis - Playwright QA Assistant

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/ton-org/testojarvis/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Playwright](https://img.shields.io/badge/tested%20with-Playwright-45ba63.svg)](https://playwright.dev)
[![OpenAI GPT-4](https://img.shields.io/badge/AI-GPT--4-blueviolet)](https://platform.openai.com)

> **TestoJarvis** est ton super assistant IA personnel (façon Jarvis dans Iron Man) pour générer, corriger, stabiliser et automatiser des tests E2E avec **Playwright**. Il s'intègre à ChatGPTs, Next.js, GitHub Actions et plus.

---

## 🚀 Fonctionnalités

✅ Génération de tests Playwright TypeScript (`.spec.ts`)  
✅ Génération de fichiers Page Object Model (`PageObject.ts`)  
✅ Génération de scénarios Gherkin (`.feature`) compatibles Cucumber.js / playwright-bdd  
✅ Analyse et recommandation de sélecteurs robustes (CSS / XPath / Role)  
✅ Stabilisation de tests flaky (timeouts, assertions, CI/CD)  
✅ Génération de scripts de login avancés (storageState, tokens, 2FA)  
✅ Génération de workflows GitHub Actions (`ci.yml`)  
✅ UI Next.js intégrée pour dialoguer avec l’assistant  
✅ Compatible avec OpenAI GPT-4 / GPT-4o  

---

## 📁 Contenu du projet

```

testojarvis-playwright/
├── gpt/
│   └── testojarvis-playwright-gpt.json    # Assistant IA à importer dans ChatGPTs
├── nextjs-ui/
│   ├── pages/
│   │   ├── index.js                        # UI web frontend
│   │   └── api/ask.js                      # API vers OpenAI
├── README.md                               # Ce fichier

````

---

## 🧠 Importer TestoJarvis dans ChatGPTs

1. Ouvre [https://chat.openai.com/gpts/editor](https://chat.openai.com/gpts/editor)
2. Clique sur **Create a GPT**
3. Choisis **Configure manually**
4. Copie-colle le contenu de `testojarvis-playwright-gpt.json`
5. Ajoute une icône de robot et donne-lui le nom `TestoJarvis`

---

## 🖥️ Lancer l’UI locale (Next.js)

```bash
# 1. Va dans ton dossier nextjs-ui
cd nextjs-ui

# 2. Initialise un projet Node (avec default config)
npm init -y

# 3. Installe Next.js, React et les dépendances nécessaires
npm install next react react-dom

# 4. (optionnel mais recommandé) Installe Playwright en plus :
npm install -D @playwright/test
npx playwright install
npm run dev
````

Puis rends-toi sur [http://localhost:3000](http://localhost:3000)

---

## 💬 Exemples de prompts

* "Génère un test Playwright TypeScript pour la fonctionnalité de login."
* "Écris un fichier POM `CheckoutPage.ts` pour le panier."
* "Corrige ce test instable : il échoue en CI."
* "Génère un fichier `.feature` Gherkin pour le flux d'inscription."
* "Crée un script de login avec token et storageState."

---

## ✨ Capacités de TestoJarvis (template de prompt intégré)

```
- test:generateSpec → Fichier `.spec.ts` Playwright
- test:generatePOM → Fichier `PageObject.ts` TypeScript
- test:generateFeature → Fichier `.feature` Gherkin (BDD)
- test:analyzeSelector → Suggestion de sélecteurs robustes
- test:fixFlaky → Debug et stabilisation de tests
- test:generateLogin → Script de login avancé
- test:generateCI → GitHub Actions Workflow
```

---

## 🔐 Intégration OpenAI (API)

1. Crée un fichier `.env.local` dans `nextjs-ui/` :

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

2. Utilise ton propre modèle (`gpt-4`, `gpt-4o`, etc.)

---

## 📅 Suivi des évolutions

| ✅ Fonction                       | Statut      |
| -------------------------------- | ----------- |
| Génération `.spec.ts` Playwright | ✔️ Fait     |
| Génération `.feature` (Gherkin)  | ✔️ Fait     |
| Génération POM `.ts`             | ✔️ Fait     |
| UI Next.js intégrée              | ✔️ Fait     |
| GPT personnalisé importable      | ✔️ Fait     |
| Intégration CI/CD GitHub Actions | 🚧 En cours |
| Export vers Notion/Slack         | 🧠 À venir  |

---

## 📜 Licence

MIT — libre à usage personnel et commercial.
Créé avec ❤️ par un freelance expert QA + IA.

---

## 🤖 Tu veux aller plus loin ?

📦 Génération automatique de tests depuis Linear, Notion, Jira
📩 Export des rapports vers Slack ou Gmail
📈 Visual regression / snapshot testing
🌐 Déploiement Vercel ou serveur privé

