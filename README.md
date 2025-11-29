# 🚀 docker-api-lab

> Projet de démonstration DevOps : une API Flask dockerisée proprement avec un Dockerfile multi-stage, un utilisateur non-root, un Makefile et un healthcheck.  
> Objectif : apprendre, documenter et présenter des bonnes pratiques Docker / Platform Engineering.

---

## 🎯 Objectifs du projet

Ce projet a été réalisé pour :

- Comprendre la **containerisation** d’une application web.
- Concevoir un **Dockerfile propre et optimisé** (multi-stage build).
- Utiliser **Gunicorn** comme serveur WSGI de production.
- Suivre les bonnes pratiques Docker :
  - user non-root
  - image minimale
  - healthcheck
  - variables d’environnement
- Automatiser le workflow avec un **Makefile**.

---

## 🧱 Stack technique

| Composant      | Version / Info |
|----------------|----------------|
| **Python**     | 3.12 |
| **Flask**      | API minimale |
| **Gunicorn**   | Serveur WSGI de production |
| **Docker**     | Multi-stage + best practices |
| **Makefile**   | Automatisation des commandes |
| **OS**         | Ubuntu (VM VirtualBox + VS Code Remote SSH) |

---

## 📂 Structure du projet

```text
docker-api-lab/
├── app/
│   ├── app.py           # API Flask (2 endpoints)
│   └── __init__.py      # Module Python
├── Dockerfile           # Dockerfile multi-stage avec healthcheck
├── Makefile             # Automatisation build/run/logs/clean
├── requirements.txt     # Dépendances Python
├── .dockerignore        # Optimisation du contexte Docker
└── .gitignore           # Fichiers à ignorer pour Git
```

---

## 🌐 Endpoints

| Méthode | URL        | Description |
|---------|------------|-------------|
| GET | `/health` | Vérifie que l’API fonctionne |
| GET | `/info`   | Donne un message + hostname du container |

---

## 🐳 Docker : build & run

### 🔧 Build de l’image

```bash
make build
```

### ▶️ Lancer le container

```bash
make run
```

Le container écoute sur **port 5000** (configurable via `${APP_PORT}`).

### 🧪 Tester l’API

```bash
curl http://localhost:5000/health
curl http://localhost:5000/info
```

---

## ⚙️ Détails sur le Dockerfile

Le Dockerfile utilise un **multi-stage build** :

### 🏗️ **Stage 1 — Builder**
- Installe les dépendances de build (compilation).
- Génère des *wheels* Python (install plus rapide).
- Cette image ne sera **pas** utilisée au runtime.

### 📦 **Stage 2 — Runtime**
- Image minimale (`python:3.12-slim`).
- Installation uniquement du strict nécessaire.
- User non-root : `appuser`.
- Endpoints exposés.
- **Healthcheck intégré** :
  ```Dockerfile
  HEALTHCHECK CMD curl -f http://localhost:${APP_PORT}/health || exit 1
  ```

### ⚡ Résultats
- Image **plus légère**  
- Surface d’attaque **réduite**  
- Déploiement **plus rapide**  
- Standards production **respectés**

---

## 🛠️ Makefile : commandes disponibles

```bash
make build     # Build de l'image Docker
make run       # Lance le container en detach
make logs      # Affiche les logs en temps réel
make shell     # Ouvre un bash dans le container
make stop      # Stop + supprime le container
make clean     # Supprime container + image
```

---

## 🧪 Exécuter l’app sans Docker (mode dev)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/app.py
```

---

## 🧠 Mémo : comment refaire ce projet de zéro

1. Installer Docker sur une VM Ubuntu  
2. Cloner ce repo :
   ```bash
   git clone git@github.com:<ton-username>/docker-api-lab.git
   ```
3. Build et run :
   ```bash
   make build
   make run
   ```
4. Tester avec :
   ```bash
   curl http://localhost:5000/health
   ```

---

## 📌 Pistes d'amélioration

- Ajouter des tests unitaires (pytest)
- Ajouter un Docker Compose
- Ajouter un pipeline CI/CD (GitHub Actions)
- Pousser l'image dans un registre (Docker Hub ou GHCR)

---
