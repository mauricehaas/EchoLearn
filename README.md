# EchoLearn

EchoLearn ist eine interaktive Lernplattform, die ...

---

## Technologien

- Frontend: Vue 3 (Vite)  
- Backend: FastAPI (Python)  
- Authentifizierung: JWT (JSON Web Tokens)  
- Datenbank: PostgreSQL (Docker)  
- Containerisierung: Docker + Docker Compose  
- State Management: Pinia (optional)  
- Audio Processing / NLP: Whisper + GPT (für spätere Implementierung)  

---

## Local Development (Docker-only)

### Schnellstart

make build-frontend # Frontend wird installiert
make build # Backend wird installiert
make up          # startet alle Services  

make down        # stoppt alle Services  

Backend: http://localhost:8000  
Frontend: http://localhost:5173  

---

## Authentifizierung

- JWT (JSON Web Tokens)  
- Rollen: student / teacher  
- Token wird im Frontend gespeichert (LocalStorage / Pinia)  
- Backend prüft Berechtigungen für API-Endpunkte  

---

## Features (für den Prototyp)

- Benutzerregistrierung / Login  
- Rolle-basiertes Dashboard (Student / Dozent)  
- Flashcards erstellen / verwalten  
- Audioaufnahme der Antworten  
- Feedback nach jeder Karte (inhaltlich + rhetorisch)  
- Lernstatistiken anzeigen  

--- 
