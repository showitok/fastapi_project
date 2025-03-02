DOCKER_COMPOSE = docker compose -f ./docker/docker-compose.yml -p project

.PHONY: build
build:
	$(DOCKER_COMPOSE) build app

.PHONY: up
up: build
	$(DOCKER_COMPOSE) up --attach app

.PHONY: down
down:
	$(DOCKER_COMPOSE) down --volumes --rmi=local
