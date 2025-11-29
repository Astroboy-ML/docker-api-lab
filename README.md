# 🚀 docker-api-lab – API Flask Dockerisée + CI/CD GitHub Actions + GHCR

[![CI/CD - Docker API](https://github.com/Astroboy-ML/docker-api-lab/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Astroboy-ML/docker-api-lab/actions/workflows/ci-cd.yml)
![GHCR Registry](https://img.shields.io/badge/GHCR-astroboy--ml%2Fdocker--api--lab-blue)
![Python Version](https://img.shields.io/badge/python-3.12-blue)
![Flask](https://img.shields.io/badge/flask-API-lightgrey)
![Gunicorn](https://img.shields.io/badge/gunicorn-production-green)

> API Flask conteneurisée avec Docker + exécution en production sous **Gunicorn**, pipeline **CI/CD GitHub Actions**, **tests**, **linting**, **build Docker**, **push vers GHCR**, Makefile et bonnes pratiques de containerisation.

---

## 🎯 Objectifs du projet

- Développer et containeriser une API Flask simple mais propre  
- Utiliser un **Dockerfile multi-stage** optimisé  
- Exécuter l’app en production avec **Gunicorn**  
- Appliquer les bonnes pratiques :  
  - image slim  
  - utilisateur non-root  
  - healthcheck  
  - séparation builder/runtime  
- Mettre en place une **CI/CD complète** :
  - Lint (flake8)
  - Tests (pytest)
  - Build & push Docker
  - Tags automatiques (`latest`, `main`, `sha`)
- Publier l’image dans **GitHub Container Registry (GHCR)**  
- Fournir un workflow dev avec **Makefile**

---

## 🧱 Stack Technique

| Composant | Rôle |
|----------|------|
| Python 3.12 | Langage backend |
| Flask | API minimaliste |
| Gunicorn | Serveur WSGI de production |
| Docker (multi-stage) | Conteneurisation optimisée |
| GHCR | Registry privé/public |
| GitHub Actions | CI/CD |
| flake8 | Linter |
| pytest | Tests |
| Makefile | Automatisation |

---

## 📁 Structure du Projet

```text
docker-api-lab/
├── app/
│   ├── app.py           # API Flask : /health + /info
│   └── __init__.py
├── tests/
│   └── test_example.py  # Tests pytest
├── Dockerfile           # Dockerfile multi-stage (prod-ready)
├── Makefile             # build/run/shell/logs
├── requirements.txt     # Dépendances
├── .dockerignore
├── .gitignore
└── .github/
    └── workflows/
        └── ci-cd.yml    # Pipeline CI/CD GitHub Actions
```

---

## 🌐 Endpoints de l’API

### 🔵 GET `/health`
```json
{"status": "ok"}
```

### 🔵 GET `/info`
Retourne un message + le hostname du conteneur.
```json
{
  "message": "Hello from Dockerized API 🔥",
  "hostname": "<container-hostname>"
}
```

---

## 🐳 Utilisation avec Docker (image GHCR)

Image publiée automatiquement :

```
ghcr.io/astroboy-ml/docker-api-lab:latest
```

### 1️⃣ Pull de l’image

```bash
docker pull ghcr.io/astroboy-ml/docker-api-lab:latest
```

### 2️⃣ Exécution du conteneur

```bash
docker run -p 5000:5000 ghcr.io/astroboy-ml/docker-api-lab:latest
```

### 3️⃣ Tests

```bash
curl http://localhost:5000/health
curl http://localhost:5000/info
```

---

## ⚙️ CI/CD GitHub Actions

Pipeline : `.github/workflows/ci-cd.yml`

Déclencheurs :

- push sur `main`
- PR vers `main`
- tags `v*.*.*`

### Étapes du pipeline

#### 1️⃣ Lint & Tests
- flake8  
- pytest  

#### 2️⃣ Build & Push Docker
- login GHCR  
- génération tags  
- build Docker  
- push GHCR  

Tags générés :

- `latest`
- `main`
- `sha-xxxxxx`
- `vX.Y.Z` (si tag)

---

## 🧪 Tests & Lint en local

```bash
pip install -r requirements.txt
pip install pytest flake8

flake8 .
pytest
```

---

## 🛠️ Makefile

```bash
make build     # Build image
make run       # Run container
make logs      # Logs temps réel
make shell     # Shell dans le container
make stop      # Stop container
make clean     # Supprime image + container
```

---

## 🔄 Workflow global

```text
Dev → git push main
        ↓
GitHub Actions CI
        ↓ Lint + Tests (flake8/pytest)
        ↓ Build Docker
        ↓ Push GHCR
User → docker pull + docker run
```

---

## 🚀 Améliorations futures

- Test coverage  
- Analyse statique (bandit)  
- Scan vulnérabilités (Trivy)  
- Multi-architecture build  
- Déploiement auto (Fly.io / Render / Railway)  
- Semantic Release (versioning auto)

