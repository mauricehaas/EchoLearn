EchoLearn ist ein interaktiver Prototyp zur Simulation mündlicher Prüfungssituationen.  
Das System stellt Fragen, verarbeitet gesprochene Antworten, bewertet diese automatisiert und generiert adaptive Rückfragen, um einen prüfungsähnlichen Dialog zu erzeugen.

Das Projekt wurde im universitären Kontext als experimentelle Lernplattform entwickelt und dient der konzeptionellen Untersuchung KI-gestützter Bewertung freier mündlicher Antworten.

---

## Installation & Nutzung

### Voraussetzungen

Für die lokale Ausführung werden benötigt:

- Docker
- Docker Compose
- make

---

### Lokale Ausführung

Repository klonen:

```
git clone https://github.com/mauricehaas/EchoLearn
cd EchoLearn
```

Services bauen und starten:

```
make build-frontend
make build
make up
```

Datenbank aufbauen:

```
make seed
```

---

### Zugriff auf Services

Frontend  
http://localhost:5173

Backend API  
http://localhost:8000

API Dokumentation  
http://localhost:8000/docs

### Services stoppen

```
make down
```

## Projektstatus

Lokaler Forschungs- und Entwicklungsprototyp.

- ausschließlich für lokale Ausführung vorgesehen
- kein Produktionssystem
- kein Deployment-Setup
- keine Sicherheits- oder Skalierungsoptimierung
- Fokus auf Konzeptvalidierung

---

## Funktionsumfang

- Erstellung und Verwaltung von Prüfungsfragen
- Vorlesen von Fragen (Text-to-Speech)
- Aufnahme gesprochener Antworten (Speech-to-Text)
- Automatisierte Bewertung durch ein Sprachmodell
- Generierung kontextabhängiger Rückfragen
- Anzeige von Lernstatistiken

## Technologieauswahl

Frontend: Vue 3 (Vite)  
Backend: FastAPI (Python)  
Datenbank: PostgreSQL  
Containerisierung: Docker + Docker Compose  
CI: Github Actions

---

## Weitere Dokumentation

Weitere konzeptionelle Details befinden sich hier:

- [Allgemeine Projektdokumentation](docs/documentation_allgemein.md)
- [Frontend Dokumentation](docs/documentation_frontend.md)
- [Backend Dokumentation](docs/documentation_backend.md)
- [Architektur Dokumentation](docs/documentation_architecture.md)
- [Evaluation Dokumentation](docs/evaluation.md)

## Verantwortungsbereiche

**Sandra Fischer**
Dokumentation, Testen, Daten

**Aleksandar Trifonov**
Backend (funktionale und inhaltliche Anbindung der LLMs in die App, Bereitstellung der Daten für die LLMs, Testen der
Funktionalitäten)

**Maurice Haas**
Projektarchitektur (Docker, CI Pipelines, Linter, Formatter, Make-Befehle), Frontend, Backend (CRUD Routen, CSV-Export/Import Routen), Datenbankverbindung, Skript für automatische Datenbankerstellung und Löschung
