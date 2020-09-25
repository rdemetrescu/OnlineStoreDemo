DOCKER_COMPOSE=docker-compose
SERVER_CONTAINER=server


run:
	@echo "Starting containers"
	-$(DOCKER_COMPOSE) up -d

stop:
	@echo "Stopping containers"
	-$(DOCKER_COMPOSE) stop

down:
	@echo "Stopping containers"
	-$(DOCKER_COMPOSE) down -v

test:
	-$(DOCKER_COMPOSE) exec $(SERVER_CONTAINER) pytest -vv
