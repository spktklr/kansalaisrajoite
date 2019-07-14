ifeq ($(filter $(ENV),dev prod),)
$(error Set ENV to "dev" or "prod".)
endif

COMPOSE_FILES := -f docker-compose.yml -f docker-compose.$(ENV).yml

build:
	docker-compose $(COMPOSE_FILES) build $(SERVICE)

start:
	docker-compose $(COMPOSE_FILES) up -d $(SERVICE)

stop:
	docker-compose $(COMPOSE_FILES) stop $(SERVICE)

down:
	docker-compose $(COMPOSE_FILES) down -v $(SERVICE)

restart:
	@make -s stop
	@make -s start

logs:
	docker-compose $(COMPOSE_FILES) logs -f $(SERVICE)

config:
	docker-compose $(COMPOSE_FILES) config
