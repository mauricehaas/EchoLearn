# Build aller Docker-Images
build:
	docker compose build

build-frontend:
	docker compose run --rm frontend sh -c "npm install && npm install axios"

# Startet alle Services (Container hochfahren)
up:
	docker compose up -d

# Stoppt alle Services
down:
	docker compose down

# Backend-Logs anzeigen
logs-backend:
	docker compose logs -f backend

# Frontend-Logs anzeigen
logs-frontend:
	docker compose logs -f frontend

# Entfernt alle gestoppten Container (Volumes bleiben erhalten)
clean:
	docker compose rm -f

seed:
	docker compose exec backend python -m app.seed.seed_data
