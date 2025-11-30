# 🚀 docker-api-lab

[![CI/CD - Docker API](https://github.com/Astroboy-ML/docker-api-lab/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Astroboy-ML/docker-api-lab/actions/workflows/ci-cd.yml)

> Projet complet DevOps / Platform Engineering : API Flask + Redis, Docker multi-stage, Makefile, Docker Compose, CI/CD GitHub Actions, scans de sécurité Trivy & pip-audit.  
> Conçu comme un **projet portfolio** démontrant les compétences essentielles d’un Platform Engineer moderne.

---

# 🎯 Objectifs du projet

## 🔹 Objectifs techniques
- Développer et containeriser une **API Flask simple mais propre**  
- Utiliser un **Dockerfile multi-stage** optimisé  
- Exécuter l'app en mode production avec **Gunicorn**  
- Mettre en place les bonnes pratiques Docker :  
  - image minimaliste (`python:slim`)  
  - utilisateur **non-root**  
  - `HEALTHCHECK` intégré  
  - séparation complète **builder / runtime**  
- Ajouter un service Redis pour manipuler un compteur via `/counter`  
- Créer un environnement multi-services avec **Docker Compose**

## 🔹 Objectifs DevOps / Platform Engineer
- Mettre en place une **CI/CD complète** avec GitHub Actions :  
  - Lint (flake8)  
  - Tests (pytest + coverage)  
  - Analyse de sécurité (Bandit)  
  - Scan dépendances Python (pip-audit)  
  - Scan filesystem (Trivy FS)  
  - Build & push Docker  
  - Tags automatiques : `latest`, `main`, `sha`  
- Publier automatiquement l’image Docker dans **GitHub Container Registry (GHCR)**  
- Fournir un workflow de développement ergonomique via un **Makefile**

---

# 🧭 Schéma global du workflow CI/CD

```
                     ┌────────────────────────┐
                     │        Git Push        │
                     └────────────┬───────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │ 1. Lint & Tests           │
                    │ - flake8                  │
                    │ - pytest + coverage       │
                    │ - bandit                  │
                    └────────────┬──────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │ 2. Sécurité dépendances      │
                  │ - pip-audit                  │
                  │ - trivy fs                   │
                  └─────────────┬────────────────┘
                                │
                                ▼
                ┌──────────────────────────────────┐
                │ 3. Build & Push Docker           │
                │ - docker/metadata-action         │
                │ - build-push-action              │
                │ => ghcr.io/astroboy-ml/docker-api│
                └──────────────┬───────────────────┘
                               │
                               ▼
              ┌──────────────────────────────────────┐
              │ 4. Scan Trivy de l'image Docker      │
              │ - trivy image                        │
              │ - vuln OS + libs Python              │
              └──────────────────────────────────────┘
```

---

# 🧱 Stack technique

| Composant      | Version / Info |
|----------------|----------------|
| **Python**     | 3.11 |
| **Flask**      | API minimaliste |
| **Gunicorn**   | Serveur WSGI (prod) |
| **Redis**      | Cache / compteur |
| **Docker**     | Multi-stage |
| **Docker Compose** | Multi-services |
| **GitHub Actions** | CI/CD |
| **Trivy** | Sécurité |
| **pip-audit** | Analyse dépendances |

---

# 📂 Structure du projet

```text
docker-api-lab/
├── app/
│   ├── app.py               # Code Flask + Redis
│   └── __init__.py
├── tests/
│   └── test_app.py          # Tests unitaires pytest
├── Dockerfile               # Multi-stage optimisé
├── docker-compose.yml       # API + Redis
├── requirements.txt         # Dépendances Python
├── Makefile                 # Commandes outils
├── .dockerignore
├── .gitignore
└── .github/workflows/
    └── ci-cd.yml            # Pipeline CI/CD complet
```

---

# 🌐 Endpoints API

| Méthode | URL | Description |
|--------|-----|-------------|
| GET | `/health` | Healthcheck |
| GET | `/info` | Message + hostname du container |
| GET | `/counter` | Incrémente un compteur Redis |

---

# 🐳 Docker : Build & Run

### 🔧 Build

```bash
make build
```

### ▶️ Run

```bash
make run
```

### Test

```bash
curl http://localhost:5000/health
curl http://localhost:5000/info
curl http://localhost:5000/counter
```

---

# 🧪 Docker Compose (API + Redis)

```bash
docker compose up -d
```

---

# ⚙️ Pipeline CI/CD

### ✔️ Lint & Sécurité
- flake8  
- Bandit  
- pip-audit  

### ✔️ Tests
- pytest + coverage

### ✔️ Build & Publish
- Docker multi-stage  
- Tags multiples (`sha`, `latest`, `main`)  
- GHCR registry  

### ✔️ Scans
- trivy fs  
- trivy image  

---

# 🛠️ Makefile

```bash
make build
make run
make stop
make logs
make shell
make clean
```

---

# 🚀 Déploiement (coming soon)

Prochaine étape : déploiement automatique sur VM / Cloud.

---

# 📌 Idées d'amélioration

- Reverse proxy : Traefik / Nginx  
- Monitoring Prometheus + Grafana  
- GitOps (ArgoCD)  
- Système de logs avancé  
- Intégration TDD / tests e2e  

---

# 👨‍💻 Auteur

Projet développé dans une démarche d’apprentissage DevOps & Platform Engineering.
