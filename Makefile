APP_NAME=docker-api-lab
IMAGE_NAME=$(APP_NAME):latest
CONTAINER_NAME=$(APP_NAME)-container
PORT=5000

.PHONY: build run stop logs shell clean

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):5000 $(IMAGE_NAME)

stop:
	-docker stop $(CONTAINER_NAME) || true
	-docker rm $(CONTAINER_NAME) || true

logs:
	docker logs -f $(CONTAINER_NAME)

shell:
	docker exec -it $(CONTAINER_NAME) /bin/bash

clean: stop
	-docker rmi $(IMAGE_NAME) || true
