# === STAGE 1 : build des dépendances ===
# Image de base légère pour la compilation des dépendances Python
FROM python:3.12-slim AS builder

# Empêche la création des .pyc et désactive le buffering (logs instantanés)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Répertoire de travail du container
WORKDIR /app

# Installe les outils nécessaires pour compiler les dépendances
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*   # Nettoyage du cache APT pour réduire la taille

# Copie le fichier des dépendances Python
COPY requirements.txt .

# Met à jour pip et génère des "wheels" pour toutes les dépendances
# Les wheels permettent une installation plus rapide dans l'image finale
RUN pip install --upgrade pip \
 && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels



# === STAGE 2 : image finale minimale ===
# Nouvelle image propre, sans outils de compilation
FROM python:3.12-slim

# Même configuration pour un comportement de Python cohérent
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Répertoire de travail de l'image finale
WORKDIR /app

# Création d'un utilisateur non-root (bonne pratique sécurité)
RUN useradd -m appuser

# Installe uniquement les dépendances système nécessaires au runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*   

# On garde l'image très légère
# Copie les wheels générés dans le builder (1er stage)
COPY --from=builder /wheels /wheels

# Installe les dépendances Python depuis les wheels, sans pip install "classique"
RUN pip install --no-cache-dir /wheels/* \
 && rm -rf /wheels   # Supprime les wheels après installation : image plus légère

# Copie uniquement le code source de l'application
COPY app ./app

# Donne la propriété du dossier à l'utilisateur non-root
RUN chown -R appuser:appuser /app

# Exécution en tant qu'utilisateur non-root
USER appuser

# Expose le port utilisé par l'application
EXPOSE 5000

# Commande de lancement en production : Gunicorn sert l'app Flask
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.app:app"]
