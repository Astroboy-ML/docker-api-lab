# 🚀 docker-api-lab — Professional DevOps & Cloud-Native Project

[![CI/CD - Docker API](https://github.com/Astroboy-ML/docker-api-lab/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Astroboy-ML/docker-api-lab/actions/workflows/ci-cd.yml)
![AWS ECS](https://img.shields.io/badge/AWS-ECS%20Fargate-orange)
![Docker](https://img.shields.io/badge/Docker-Multi--Stage-blue)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-lightgrey)
![Python Version](https://img.shields.io/badge/python-3.12-blue)
![Flask](https://img.shields.io/badge/flask-API-lightgrey)
![Gunicorn](https://img.shields.io/badge/gunicorn-production-green)

> This project demonstrates a **full Cloud-Native & Platform Engineering workflow**, including:
> - Flask API + Redis  
> - Docker multi-stage build  
> - Local multi-service orchestration (docker-compose)  
> - CI/CD GitHub Actions  
> - Security scanning (Bandit, pip-audit, Trivy)  
> - Automatic container build & push  
> - Automated **AWS ECS Fargate deployment**  
> - CloudWatch logging + IAM roles  
>  
> The goal: **demonstrate end‑to‑end DevOps & Cloud platform skills** with production‑grade patterns.

---

# 🧭 Global Overview

This project covers **ALL core skills** of a modern Platform Engineer:

- API engineering  
- Containerization & orchestration  
- CI/CD automation  
- Cloud deployment (AWS ECS Fargate)  
- Security & best practices  
- Documentation & reproducible workflows  

---

# 🏗️ Architecture — Global View (Cloud + Local)

```
                              ┌───────────────────────────────┐
                              │           Developer           │
                              │      VS Code / Makefile       │
                              └───────────────┬───────────────┘
                                              │
                                Local testing │ docker compose
                                              ▼
                   ┌────────────────────────────────────────────────┐
                   │                Local Environment               │
                   │                                                │
                   │   ┌──────────────┐     ┌──────────────┐        │
                   │   │ Flask API    │<--->│    Redis      │       │
                   │   │  Gunicorn    │     └──────────────┘        │
                   │   └──────────────┘            ▲                │
                   │            │                   │               │
                   │   ┌────────▼─────────┐         │               │
                   │   │ RedisInsight GUI │─────────┘               │
                   │   └──────────────────┘                         │
                   └────────────────────────────────────────────────┘

                                      Git Push
                                         │
                                         ▼

                          ┌─────────────────────────────────────┐
                          │          GitHub Actions             │
                          │   CI/CD: test → scan → build → push │
                          └───────────────┬─────────────────────┘
                                          │
                                  Docker Image pushed
                                          │
                                          ▼

                       ┌──────────────────────────────────────────┐
                       │                 AWS Cloud                │
                       │                                          │
                       │  ┌──────────────┐   ┌────────────────┐   │
                       │  │ AWS ECR      │   │ CloudWatch Logs│   │
                       │  │ image store  │   └────────────────┘   │
                       │  └──────┬───────┘            ▲           │
                       │         │                    │           │
                       │  ┌──────▼─────────┐   logs   │           │
                       │  │ ECS Fargate     │─────────┘           │
                       │  │ Container Task  │                     │
                       │  └─────────────────┘                     │
                       └──────────────────────────────────────────┘
```

---

# 🚦 CI/CD Pipeline — Professional Diagram

```
                    ┌─────────────────────────┐
                    │         Developer       │
                    │        git push         │
                    └─────────────┬───────────┘
                                  │
                                  ▼
                 ┌────────────────────────────────┐
                 │    GitHub Actions Pipeline     │
                 └────────────────┬───────────────┘
                                  │
     ┌────────────────────────────▼───────────────────────────────┐
     │                         CI Phase                           │
     │────────────────────────────────────────────────────────────│
     │ Lint      → flake8                                         │
     │ Tests     → pytest + coverage                              │
     │ Security  → bandit, pip‑audit, trivy filesystem            │
     └────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
             ┌─────────────────────────────────────────────┐
             │               Docker Build                  │
             │        Multi-stage Dockerfile build         │
             └───────────────────┬─────────────────────────┘
                                 │
                                 ▼
             ┌─────────────────────────────────────────────┐
             │         Push to GHCR (Container Registry)   │
             └───────────────────┬─────────────────────────┘
                                 │
                                 ▼
             ┌─────────────────────────────────────────────┐
             │            CD Phase — AWS Deployment        │
             │  - Update ECS Task Definition               │
             │  - Force new deployment                     │
             └───────────────────┬─────────────────────────┘
                                 │
                                 ▼
                        ┌────────────────┐
                        │ ECS Fargate    │
                        │ Running API    │
                        └────────────────┘
```

---

# 🧱 Stack Technique

| Domain | Component |
|--------|-----------|
| Language | Python 3.12 |
| Framework | Flask |
| Webserver | Gunicorn |
| Cache | Redis |
| Local Orchestration | Docker Compose |
| Container Build | Docker multi-stage |
| CI/CD | GitHub Actions |
| Cloud | AWS ECS Fargate + ECR |
| Logging | AWS CloudWatch |
| Security | Bandit, pip-audit, Trivy |

---

# 📁 Project Structure

```
docker-api-lab/
├── app/
│   ├── app.py
│   ├── __init__.py
│   └── config.py
├── tests/
│   └── test_app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── Makefile
├── .dockerignore
├── .gitignore
└── .github/workflows/
    └── ci-cd.yml
```

---

# 🧪 Local Usage

### Launch full stack (API + Redis + RedisInsight)

```
docker compose up -d
```

### API:
http://localhost:5000

### RedisInsight:
http://localhost:5540

---

# ☁️ Cloud Deployment — AWS ECS Fargate

Pipeline steps:

1️⃣ Build Docker image  
2️⃣ Push GHCR  
3️⃣ Update ECS Task Definition  
4️⃣ Deploy new Fargate task  
5️⃣ Logs streamed into CloudWatch  

```
ECR → ECS Fargate → Public IP → Internet
```

---

# 🔥 API Endpoints

| Method | Route | Description |
|--------|--------|-------------|
| GET | `/health` | Container health |
| GET | `/info` | Hostname + version |
| GET | `/counter` | Redis‑powered counter |

---

# 🚀 Future Improvements

- Reverse proxy (Traefik / Nginx)
- HTTPS + ALB
- Staging environment + multi-env pipeline
- Prometheus + Grafana
- GitOps (ArgoCD)
- End-to-end testing

---

# 👨‍💻 Author

Project built as part of a professional DevOps & Platform Engineering learning journey.

