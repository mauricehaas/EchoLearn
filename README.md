# EchoLearn

EchoLearn ist eine interaktive Lernplattform, die eine mündliche Prüfung simuliert, diese bewertet und an erwarteten Stellen Rückfragen stellt.

---

## Inhaltsverzeichnis

- [Projektübersicht](#echolearn)
- [Technologien](#technologien)
- [Local Development (Docker-only)](#local-development-docker-only)
- [Schnellstart](#schnellstart)
- [Features (für den Prototyp)](#features-für-den-prototyp)
- [Technische Dokumentation Backend](docs/technical_documentation.md)
- [Benutzerdokumentation Backend](docs/user_documentation.md)
- [Backend](backend/)
- [Frontend](frontend/)
- [Evaluation](docs/evaluation.md)


## Technologien

- Frontend: Vue 3 (Vite)
- Backend: FastAPI (Python)
- Datenbank: PostgreSQL (Docker)
- Containerisierung: Docker + Docker Compose

---

## Local Development (Docker-only)

### Schnellstart

- make build-frontend # Frontend wird installiert
- make build # Backend wird installiert
- make up # startet alle Services

- make down # stoppt alle Services

- Backend: http://localhost:8000
- Frontend: http://localhost:5173

---

## Features (für den Prototyp)

- Flashcards erstellen / verwalten
- Text to Speech um Fragen vorzulesen
- Speech to text um Antworten aufzunehmen
- Bewertung der Antworten durch LLM
- Stellen von Rückfragen an erwarteten Stellen
- Lernstatistiken anzeigen

---
