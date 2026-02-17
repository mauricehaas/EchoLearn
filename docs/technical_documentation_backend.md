# Technische Dokumentation

## Inhaltsverzeichnis

- [Projektübersicht](#projektübersicht)
- [Architektur & Komponenten](#architektur--komponenten)
- [Datenbank](#datenbank)
- [Modelle (DB)](#modelle-db)
- [LLM‑Integration](#llm-integration)
- [Kernlogik: Prüfungssimulation](#kernlogik-prüfungssimulation)
- [API‑Referenz & Beispiele](#api-referenz--beispiele)
- [Lokale Entwicklung & Start](#lokale-entwicklung--start)
- [Konfiguration & Umgebungsvariablen](#konfiguration--umgebungsvariablen)
- [Wartung & Troubleshooting](#wartung--troubleshooting)

## Projektübersicht

Dieses Repository enthält die Applikation "EchoLearn" — eine Web‑Applikation zur automatisierten Prüfungsauswertung mit einem FastAPI‑Backend, einem Vite/Vue‑Frontend und einer Postgres‑Datenbank. LLM‑Aufrufe werden zur Bewertung und Rückmeldung verwendet.

Hauptverzeichnisse:
- `backend/`: FastAPI‑Backend (Python, SQLAlchemy, asyncpg)
- `frontend/`: Vite + Vue 3 Frontend
- `data/`: Roh‑ und verarbeitete Frage‑/Antwortdaten
- `docs/`: Projektdokumentation (diese Dateien)

## Architektur & Komponenten

- Backend: FastAPI mit asynchronem SQLAlchemy (siehe `app/core/db.py`). DB‑Connection nutzt `postgresql+asyncpg`.
- ORM: Declarative SQLAlchemy‑Modelle in `app/models/` (z. B. `Question`, `User`, `ExamEvaluationSingleAnswer`, `ExamEvaluationFinal`).
- Services: Prüfungssimulation und LLM‑Integration in `app/services/` (`exam_simulator.py`, `llm_handler.py`, `prompts.py`).
- Router / Endpoints: REST‑API in `app/routers/` (z. B. `questions.py`, `users.py`, `exam.py`, `exam_evaluation_single_answers.py`).

## Datenbank

- Connection‑String (in `app/core/db.py`):

  `postgresql+asyncpg://echolearn:echolearn@db:5432/echolearn`

- Das Seed‑Skript `backend/app/seed/seed_data.py` erstellt Tabellen und befüllt Beispieldaten aus `data/processed/questions.csv`.

## Modelle (DB)

- `Question` (`questions`): `id`, `question`, `answer`, `max_points`.
- `User` (`users`): `id`, `username`, `password_hash`, `role`.
- `ExamEvaluationSingleAnswer` (`exam_evaluation_single_answer`): Felder u.a. `id`, `unique_exam_id`, `question`, `student_answer`, `feedback`, `rating`, `max_points`, `question_type`, `parent_id`.
- `ExamEvaluationFinal` (`exam_evaluation_final`): Felder u.a. `id`, `unique_exam_id`, `overall_feedback`.

## LLM‑Integration

- LLM‑Aufrufe erfolgen via `app/services/llm_handler.py` an folgenden Endpoint:

  `http://catalpa-llm.fernuni-hagen.de:11434/api/generate`

- `LLMHandler.call_llm(prompt)` sendet `model` und `prompt` als JSON und parst die Antwort in ein dict.
- Die Prompt‑Templates befinden sich in `app/services/prompts.py` (z. B. `evaluate_student_answer`, `evaluate_exam`, `rephrase_question`).

## Kernlogik: Prüfungssimulation

- `ExamSimulator` (`app/services/exam_simulator.py`) orchestriert die Interaktion mit dem LLM und die Persistenz:
  - Bewertung einzelner Antworten (`evaluate_student_answer`)
  - Generierung einer Gesamtevaluation (`evaluate_the_exam`)
  - Umformulierung von Fragen (`rephrase_question`)
  - Klärungs‑/Folgefragen (`next_question`, `clarify`)

- Speicherung: Einzelbewertungen → `exam_evaluation_single_answer`; Gesamtevaluation → `exam_evaluation_final`.

## API‑Referenz & Beispiele

Die wichtigsten Endpoints (Kurz):

- `GET /questions/` — alle Fragen
- `GET /questions/{id}` — Frage nach ID
- `POST /questions/import` — CSV Import (`question,answer`)
- `GET /questions/export` — Export als CSV
- `GET /users/`, `GET /users/{id}` — Benutzer abrufen
- `POST /exam/rephrase_question` — Frage umformulieren
- `POST /exam/evaluate_answer` — Einzelantwort bewerten
- `POST /exam/evaluate_exam` — Gesamtevaluation erzeugen
- `GET /exam_evaluation_single_answers/exam_scores/{exam_id}` — Punkte, Maximalpunkte, Prozent, Note

Beispiele — `curl`:

Import CSV:

```bash
curl -X POST "http://localhost:8000/questions/import" -F "file=@questions.csv"
```

Einzelantwort bewerten (vereinfachtes Body‑Schema):

```bash
curl -X POST "http://localhost:8000/exam/evaluate_answer" \
  -H "Content-Type: application/json" \
  -d '{
    "unique_exam_id": "exam-123",
    "question": "Was ist X?",
    "student_answer": "Antwort des Studenten",
    "correct_answer": "Musterlösung",
    "max_points": 5,
    "evaluate_only": true,
    "parent_id": 0,
    "question_type": "BASE"
  }'
```

Beispielantwort (Schema):

```json
{
  "feedback": "Kurz und prägnant...",
  "rating": 3.5,
  "next_action": "NONE",
  "followup_text": "",
  "answer_id": 12,
  "next_max_points": 0,
  "next_answer": ""
}
```

Gesamtevaluation starten:

```bash
curl -X POST "http://localhost:8000/exam/evaluate_exam" -H "Content-Type: application/json" -d '{"unique_exam_id":"exam-123"}'
```

Punkte & Note abrufen:

```bash
curl "http://localhost:8000/exam_evaluation_single_answers/exam_scores/exam-123"
```

## Konfiguration & Umgebungsvariablen

- DB‑URL in `app/core/db.py` (im Deployment in ENV setzen, nicht im Code):

  `DATABASE_URL=postgresql+asyncpg://<user>:<pass>@<host>:5432/<db>`

- LLM‑Endpoint und Modell sollten ebenfalls per ENV konfigurierbar gemacht werden; aktuell ist `app/services/llm_handler.py` die zentrale Stelle.

## Lokale Entwicklung & Start

Voraussetzungen: Python 3.10+, Docker/Docker Compose (optional), Node.js.

Empfohlene Schritte (mit Docker Compose):

```bash
docker-compose up --build
```

Backend ohne Docker (Development):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Wartung & Troubleshooting

- Seed‑Skript verwendet `drop_all` → nur in Development ausführen.
- Logs: SQLAlchemy Engine logging via `create_async_engine(..., echo=True)`.
- Häufige Fehlerquellen:
  - CORS‑Fehler: prüfen in `backend/app/main.py` (Origins)
  - LLM‑Timeouts/Fehler: prüfen `app/services/llm_handler.py` und LLM‑Server
  - DB‑Connection: Credentials und Netzwerk (Docker Service `db`)

---
Für tiefergehende API‑Schemas oder ein OpenAPI‑Beispiel kann diese Datei erweitert werden.
