# Delaring Docker Compose
DOCKER_COMPOSE = docker-compose

# Default target
all: build run

# Build Docker images
build:
	$(DOCKER_COMPOSE) build

# Run Docker containers
run:
	$(DOCKER_COMPOSE) --env-file .env up

# Stop and remove Docker containers
stop:
	$(DOCKER_COMPOSE) down

# Clean up Docker resources
clean:
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans

# Rebuild and restart containers
restart: stop build run

# Enter backend container shell
backend-shell:
	$(DOCKER_COMPOSE) exec backend /bin/bash

# Enter frontend container shell
frontend-shell:
	$(DOCKER_COMPOSE) exec frontend /bin/sh