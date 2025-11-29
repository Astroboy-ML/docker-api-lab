# Nom logique du projet (utilisé pour nommer l'image et le container)
APP_NAME=docker-api-lab

# Nom complet de l'image Docker finale (docker-api-lab:latest)
IMAGE_NAME=$(APP_NAME):latest

# Nom du container Docker à lancer
CONTAINER_NAME=$(APP_NAME)-container

# Port sur lequel l'API écoutera depuis la machine hôte
PORT=5000

# Liste des commandes qui ne correspondent pas à de vrais fichiers
.PHONY: build run stop logs shell clean


# === Build de l'image Docker ===
# Construit l'image avec le tag défini dans IMAGE_NAME
build:
	docker build -t $(IMAGE_NAME) .


# === Lancement du container ===
# -d : mode détaché
# --name : donne un nom fixe au container
# -p : mappe PORT (host) -> 5000 (container)
run:
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):5000 $(IMAGE_NAME)


# === Stop + suppression du container ===
# Le "-" devant les commandes évite que Make s'arrête si la commande échoue
# (ex : si le container n'existe pas encore)
stop:
	-docker stop $(CONTAINER_NAME) || true
	-docker rm $(CONTAINER_NAME) || true


# === Afficher les logs du container en live ===
logs:
	docker logs -f $(CONTAINER_NAME)


# === Ouvrir un shell dans le container ===
# Très utile pour debug à l'intérieur du container
shell:
	docker exec -it $(CONTAINER_NAME) /bin/bash


# === Nettoyage : stop + suppression de l'image ===
# Supprime l'image Docker après avoir stoppé le container
clean: stop
	-docker rmi $(IMAGE_NAME) || true
