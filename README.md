# 🚀 docker-api-lab — DevOps & Cloud-Native Playground

[![CI/CD - Docker API](https://github.com/Astroboy-ML/docker-api-lab/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Astroboy-ML/docker-api-lab/actions/workflows/ci-cd.yml)
![AWS ECS](https://img.shields.io/badge/AWS-ECS%20Fargate-orange)
![Docker](https://img.shields.io/badge/Docker-Multi--Stage-blue)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-lightgrey)
![Python Version](https://img.shields.io/badge/python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-API-lightgrey)
![Gunicorn](https://img.shields.io/badge/Gunicorn-production-green)

> Projet showcase pour démontrer un workflow complet **Dev + Sec + Ops** : API Flask, Redis, Docker multi-stage, docker-compose local, CI/CD GitHub Actions, sécurité automatisée, déploiement AWS ECS Fargate et observabilité CloudWatch.

---

## 🧭 Sommaire

- [Highlights rapides](#-highlights-rapides)
- [Architecture & flux](#-architecture--flux)
- [Stack & structure](#-stack--structure)
- [Démarrer en local](#-démarrer-en-local)
- [Qualité & sécurité](#-qualité--sécurité)
- [Conteneurisation](#-conteneurisation)
- [Pipeline CI/CD](#-pipeline-cicd)
- [Déploiement AWS ECS](#-déploiement-aws-ecs)
- [Opérations & troubleshooting](#-opérations--troubleshooting)
- [API](#-api)
- [Roadmap](#-roadmap)
- [Auteur](#-auteur)

---

## ⚡ Highlights rapides

| Thème | Description |
|-------|-------------|
| API & Cache | Flask 3.0 + Gunicorn, Redis pour cache et rate limiting |
| Local | docker-compose (API + Redis + RedisInsight), Makefile pour builder/run |
| Qualité | flake8, pytest + coverage, Bandit, pip-audit, Trivy (FS & image) |
| CI/CD | Workflow GitHub Actions multi-jobs → build/push GHCR + ECR → déploiement ECS |
| Cloud | Task Fargate `awsvpc`, logs CloudWatch, IAM `ecsTaskExecutionRole` |
| Observabilité | CloudWatch Logs + endpoints santé/info |

---

## 🏗 Architecture & flux

```
                          ┌───────────────────────────────┐
                          │     Dev machine / VS Code     │
                          │  Makefile • docker compose    │
                          └───────────────┬───────────────┘
                                          │
                                docker compose up
                                          ▼
                 ┌────────────────────────────────────────────────┐
                 │                Local Environment               │
                 │                                                │
                 │   ┌──────────────┐     ┌──────────────┐        │
                 │   │ Flask API    │<--->│     Redis    │        │
                 │   │  Gunicorn    │     └──────────────┘        │
                 │   └──────────────┘             ▲               │
                 │            │                   │               │
                 │   ┌────────▼─────────┐         │               │
                 │   │ RedisInsight GUI │─────────┘               │
                 │   └──────────────────┘                         │
                 └────────────────────────────────────────────────┘

                                      git push
                                          │
                                          ▼
                        ┌───────────────────────────────┐
                        │        GitHub Actions         │
                        │ lint → tests → scans → build  │
                        │ push GHCR+ECR → deploy ECS    │
                        └───────────────┬───────────────┘
                                        │
                                        ▼
                      ┌────────────────────────────────────┐
                      │             AWS Cloud              │
                      │                                    │
                      │  ┌──────────────┐   ┌───────────┐  │
                      │  │  Amazon ECR  │   │ CloudWatch│  │
                      │  └──────┬───────┘   └─────┬─────┘  │
                      │         │    image        │ logs   │
                      │  ┌──────▼─────────┐       │        │
                      │  │ ECS Fargate    │◄──────┘        │
                      │  │  Service/Task  │                │
                      │  └────────────────┘                │
                      └────────────────────────────────────┘
```

---

## 🧱 Stack & structure

| Domaine | Choix |
|---------|-------|
| Langage | Python 3.12 |
| Framework | Flask |
| Webserver prod | Gunicorn |
| Cache | Redis 7 |
| Orchestration local | docker-compose |
| Build | Docker multi-stage |
| CI/CD | GitHub Actions |
| Sécurité | flake8, pytest, bandit, pip-audit, Trivy |
| Cloud | AWS ECS Fargate, Amazon ECR, CloudWatch Logs |

```
docker-api-lab/
├── app/                # Code Flask + routes Redis
├── tests/              # pytest
├── Dockerfile          # multi-stage builder → runtime
├── docker-compose.yml  # API + Redis + RedisInsight
├── Makefile            # helpers build/run/logs
├── requirements.txt
└── .github/workflows/ci-cd.yml
```

---

## 🛠 Démarrer en local

### Prérequis

- Docker / Docker Compose v2
- Python 3.12 (optionnel si exécution via Docker uniquement)

### Setup rapide (compose)

```bash
# Build + run API + Redis + RedisInsight
docker compose up --build -d

# Logs API
docker compose logs -f api

# Arrêt et nettoyage
docker compose down -v
```

### Utilisation du Makefile (mode container seul)

```bash
make build          # docker build -t docker-api-lab:latest .
make run            # start container (port 5000)
make logs           # tail logs
make shell          # bash dans le container
make clean          # stop + remove image
```

### Exécution pure Python (debug rapide)

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
FLASK_DEBUG=true flask --app app.app run
```

---

## ✅ Qualité & sécurité

```bash
flake8 .
pytest --cov=app --cov-report=term-missing
bandit -r app -ll
pip-audit           # vulnérabilités Python
trivy fs .          # scan filesystem (ignores unfixed)
```

Ces commandes sont orchestrées automatiquement dans le workflow `CI/CD - Docker API`.

---

## 🐳 Conteneurisation

- **Image multi-stage** (builder → runtime slim) définie dans `Dockerfile`.
- Variables clés :
  - `REDIS_HOST` (defaut `redis`)
  - `REDIS_PORT` (defaut `6379`)
  - `FLASK_DEBUG` (uniquement local)
- Docker Compose ajoute Redis et RedisInsight (GUI sur `http://localhost:5540`).

Builder l'image à la main :

```bash
docker build -t ghcr.io/astroboy-ml/docker-api-lab:dev .
docker run -p 5000:5000 ghcr.io/astroboy-ml/docker-api-lab:dev
```

---

## 🔁 Pipeline CI/CD

Workflow multi-jobs (`.github/workflows/ci-cd.yml`) :

1. **Lint & Tests** – flake8, pytest, Bandit, pip-audit.
2. **Security Scan (FS)** – Trivy filesystem scan.
3. **Build & Push** – docker/build-push-action :
   - Login GHCR.
   - Génère tags (`latest`, `sha`, etc.).
   - Push vers GHCR.
   - Configure AWS creds → login ECR → retag/push (latest + sha).
4. **Trivy Image Scan** – scan de l’image publiée.
5. **Deploy to ECS** – render task definition avec nouvelle image ECR puis `amazon-ecs-deploy`.

### Secrets GitHub requis

| Secret | Exemple | Description |
|--------|---------|-------------|
| `AWS_ACCOUNT_ID` | `424051098783` | 12 chiffres |
| `AWS_REGION` | `eu-west-3` | Région ECS/ECR |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` | — | User/role avec droits ECR/ECS |
| `ECR_REPOSITORY` | `docker-api-lab` | Nom du repo dans Amazon ECR |

> Le rôle `ecsTaskExecutionRole` doit posséder `AmazonECSTaskExecutionRolePolicy`.

---

## ☁️ Déploiement AWS ECS

Composants utilisés :

- Cluster : `docker-api-cluster`
- Service Fargate : `docker-api-container-service-729agg55`
- Task definition family : `docker-api-task`
- Réseau : mode `awsvpc` (subnets privés + SG orienté ALB/NAT selon ton infra)
- Logs : CloudWatch group `/ecs/docker-api-task`, prefix `ecs`

### Checklist avant déploiement

1. **ECR** : repo `${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/docker-api-lab`.
2. **IAM** :
   - `ecsTaskExecutionRole` + policy `AmazonECSTaskExecutionRolePolicy`.
   - Optionnel : `taskRoleArn` si l’app appelle d’autres services AWS.
3. **CloudWatch Logs** :

```bash
aws logs create-log-group \
  --log-group-name /ecs/docker-api-task \
  --region eu-west-3
```

4. **Secrets GitHub** validés (voir tableau).
5. **Service ECS** déjà créé (une fois) et attaché à un load balancer ou IP publique.

Chaque push sur `main` déclenche le workflow et force un nouveau déploiement avec l’image taggée par le SHA courant.

---

## 🩺 Opérations & troubleshooting

| Symptôme | Cause probable | Correctif |
|----------|----------------|-----------|
| `InvalidParameterException: registryIds` | `AWS_ACCOUNT_ID` invalide | Vérifier le secret (12 chiffres) |
| `ResourceInitializationError: CreateLogStream ... log group does not exist` | `/ecs/docker-api-task` absent | Créer le log group (commande ci-dessus) |
| 429 sur `/limited` | Rate limit 5 req/min par IP | Attendre expiration ou flush Redis |
| Redis indisponible | Container down ou variable env incorrecte | Vérifier `docker compose ps`, logs `redis` |

Logs CloudWatch disponibles dans le groupe `/ecs/docker-api-task` (region `eu-west-3`).

---

## 🔥 API

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/health` | Healthcheck |
| GET | `/info` | Message + hostname du container |
| GET | `/cache-test` | Round-trip Redis basique |
| GET | `/counter` | Compteur Redis persistant |
| GET | `/limited` | Rate limiting (5 req / 60s par IP) |
| GET | `/slow` | Simule un traitement lent (2s) |
| GET | `/slow/cached` | Version cache Redis (TTL 10s) |

---

## 🧭 Roadmap

- Reverse proxy (Traefik / Nginx) + HTTPS via ALB.
- Environnements multiples (staging/prod) + stratégies GitOps.
- Observabilité avancée (Prometheus/Grafana, traces).
- Tests end-to-end + performance.
- Terraformisation complète (ECS, ECR, IAM, CloudWatch).

---

## 👨‍💻 Auteur

Projet construit dans le cadre d’un parcours **DevOps & Platform Engineering**. N’hésite pas à ouvrir des issues / PRs pour échanger ou proposer des améliorations 🙌
