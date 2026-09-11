# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1
DOCKER_COMPOSE ?= docker compose

all: down build up test

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down --remove-orphans

test: up
	$(DOCKER_COMPOSE) run --rm --no-deps --entrypoint=pytest api /tests/unit /tests/integration /tests/e2e

unit-tests:
	$(DOCKER_COMPOSE) run --rm --no-deps --entrypoint=pytest api /tests/unit

integration-tests: up
	$(DOCKER_COMPOSE) run --rm --no-deps --entrypoint=pytest api /tests/integration

e2e-tests: up
	$(DOCKER_COMPOSE) run --rm --no-deps --entrypoint=pytest api /tests/e2e

logs:
	$(DOCKER_COMPOSE) logs --tail=25 api redis_pubsub

black:
	black -l 86 $$(find * -name '*.py')
