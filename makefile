DJANGO_WEB_PY := ./main_project/manage.py
DJANGO_WEB := runserver
DEPLOYMENT_PATH := ./deployment_tcei/
DOCKER_COMPOSE_FILE := $(DEPLOYMENT_PATH)docker-compose-prod.yml
DOCKER_COMPOSE_FILE_DEV := $(DEPLOYMENT_PATH)docker-compose-dev.yml
DOCKER_SERVICE_NAME := web

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make run-dev                      - Run the Django application in development mode"
	@echo "  make run-dev-docker               - Run the Django application in development mode with Docker Compose"
	@echo "  make run-dev-docker-ngrok         - Run the 「HTTPS」 Django application in development mode with Docker Compose"
	@echo "  make run-prod                     - Run the Django application in production mode with Docker Compose"

.PHONY: run-dev
run-dev:
	DEBUG=True python3 ./main_project/manage.py runserver

.PHONY: run-dev-docker
run-dev-docker:
	@echo "========== Starting Docker Compose Process =========="
	@echo "========== 1. Stopping and removing containers, and cleaning up unused images =========="
	docker-compose -f $(DOCKER_COMPOSE_FILE_DEV) down
	docker image prune -f
	@echo "========== 2. Building and starting the Docker service ($(DOCKER_SERVICE_NAME)) =========="
	docker-compose -f $(DOCKER_COMPOSE_FILE_DEV) up --build -d $(DOCKER_SERVICE_NAME)
	docker-compose -f $(DOCKER_COMPOSE_FILE_DEV) logs -f $(DOCKER_SERVICE_NAME)
	@echo "========== 3. Checking the status of the Docker service ($(DOCKER_SERVICE_NAME)) =========="
	docker-compose -f $(DOCKER_COMPOSE_FILE) ps
	docker image prune -f
	@echo "========== Docker Compose Process Complete =========="

.PHONY: run-dev-docker-ngrok
run-dev-docker-ngrok:
	@echo "========== Starting Docker Compose Process =========="
	@echo "========== 1. Stopping and removing containers, and cleaning up unused images =========="
	docker-compose -f $(DOCKER_COMPOSE_FILE_DEV) down
	docker image prune -f
	@echo "========== 2. Building and starting the Docker service ($(DOCKER_SERVICE_NAME)) =========="
	docker-compose -f $(DOCKER_COMPOSE_FILE_DEV) up --build -d
	docker-compose -f $(DOCKER_COMPOSE_FILE_DEV) logs -f $(DOCKER_SERVICE_NAME) &
	docker-compose -f $(DOCKER_COMPOSE_FILE_DEV) logs -f ngrok
	@echo "========== 3. Checking the status of the Docker service ($(DOCKER_SERVICE_NAME)) =========="
	docker-compose -f $(DOCKER_COMPOSE_FILE) ps
	@echo "========== Docker Compose Process Complete =========="

.PHONY: run-prod
run-prod:
	@echo "========== Starting Docker Compose Process (Production) =========="
	@echo "========== 1. Stopping and removing containers, and cleaning up unused images =========="
	docker-compose -f $(DOCKER_COMPOSE_FILE) down
	docker image prune -f
	@echo "========== 2. Building and starting the Docker service ($(DOCKER_SERVICE_NAME)) =========="
	docker-compose -f $(DOCKER_COMPOSE_FILE) up --build -d $(DOCKER_SERVICE_NAME)
	@echo "========== 3. Checking the status of the Docker service ($(DOCKER_SERVICE_NAME)) =========="
	docker-compose -f $(DOCKER_COMPOSE_FILE) ps
	docker image prune -f
	@echo "========== Docker Compose Production Process Complete =========="

