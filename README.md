EchoLearn ist ein interaktiver Prototyp zur Simulation mündlicher Prüfungssituationen.  
Das System stellt Fragen, verarbeitet gesprochene Antworten, bewertet diese automatisiert und generiert adaptive Rückfragen und Vertiefungsfragen, um einen prüfungsähnlichen Dialog zu erzeugen.

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

### Tabellen zurücksetzen

```
make clear-tables
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
- Vorlesen von Fragen durch Text-to-Speech (TTS)
- Aufnahme gesprochener Antworten durch Speech-to-Text (STT)
- Automatisierte Bewertung durch ein Sprachmodell
- Generierung kontextabhängiger Rückfragen und Vertiefungsfragen
- Anzeige von Lernstatistiken

## Technologieauswahl

Frontend: Vue 3 (Vite)  
Backend: FastAPI (Python)  
Datenbank: PostgreSQL  
Containerisierung: Docker + Docker Compose  
CI: Github Actions

---

## Dokumentation

Weitere konzeptionelle Details befinden sich hier:

- [Projektdokumentation](docs/documentation.md)
