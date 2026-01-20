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

# Datenbank erstellen
seed:
	docker compose exec backend python -m app.seed.seed_data

# Datenbank leeren
clear-tables:
	docker compose exec db psql -U echolearn -d echolearn -c "TRUNCATE TABLE users RESTART IDENTITY CASCADE;"
	docker compose exec db psql -U echolearn -d echolearn -c "TRUNCATE TABLE questions RESTART IDENTITY CASCADE;"
	docker compose exec db psql -U echolearn -d echolearn -c "TRUNCATE TABLE exam_evaluation_single_answer RESTART IDENTITY CASCADE;"

data-questions:
	docker compose run --rm backend python app/data_processing/questions.py
