.PHONY: test
SUDO := $(shell [ `uname -s` = "Linux" ] && echo sudo)

DOCKER := $(shell which docker)
DOCKER_COMPOSE_PATH := $(shell if docker compose version > /dev/null 2>&1; then echo "docker compose"; else echo "docker-compose"; fi)
DOCKER_COMPOSE_FILE := docker/docker-compose.yml

DOCKER_COMPOSE := $(DOCKER_COMPOSE_PATH) -f $(DOCKER_COMPOSE_FILE) -p pulse

%:
	@:

up:
	@$(DOCKER_COMPOSE) up -d

down:
	@$(DOCKER_COMPOSE) down

logs:
	@$(DOCKER_COMPOSE) logs -f pulse

bash:
	@$(DOCKER_COMPOSE) exec -it pulse sh