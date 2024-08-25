
FLASK = docker-compose exec web flask

.PHONY: migrate

# Start the Docker containers
up:
	docker-compose up -d

# Stop the Docker containers
down:
	docker-compose down

# Run database migrations
migrate:
	@if [ ! -d "migrations" ]; then \
		$(FLASK) db init; \
	else \
		echo "Migration directory already exists."; \
	fi
	$(FLASK) db migrate       # Generate migration scripts
	$(FLASK) db upgrade       # Apply migrations to the database

# Build Docker images
build:
	$(DOCKER_COMPOSE) build

# Rebuild the containers and run migrations
rebuild: down build up migrate
