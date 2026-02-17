# Benutzer‑Dokumentation

## Inhaltsverzeichnis

- [Schnellstart (Frontend)](#schnellstart-frontend)
- [Fragen importieren (CSV)](#fragen-importieren-csv)
- [Fragen exportieren](#fragen-exportieren)
- [Einzelantwort bewerten (API)](#einzelantwort-bewerten-api)
- [Gesamtevaluation einer Prüfung](#gesamtevaluation-einer-prüfung)
- [Noten / Punkte abrufen](#noten--punkte-abrufen)
- [Praktische Beispiele (curl)](#praktische-beispiele-curl)
- [Fehler & Support](#fehler--support)

Diese Anleitung richtet sich an Anwender:innen, die das Frontend benutzen oder einfache API‑Aufrufe durchführen wollen.

## Schnellstart (Frontend)

1. Frontend starten (Development):

```bash
cd frontend
npm install
npm run dev
```

Der Vite‑Devserver läuft standardmäßig auf `http://localhost:5173`.

2. Backend starten (lokal):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

3. Im Browser `http://localhost:5173` öffnen.

Im Frontend kannst du Fragen durchgehen, Prüfungen durchführen und generiertes Feedback lesen oder abspielen.

## Fragen importieren (CSV)

Bereite eine CSV mit Kopfzeile `question,answer` vor. Beispielzeile:

```csv
question,answer
Was ist maschinelles Lernen?,Ein Bereich der KI, bei dem Modelle aus Daten lernen.
```

API (Backend): `POST /questions/import` mit Multipart‑Formfile.

Beispiel:

```bash
curl -X POST "http://localhost:8000/questions/import" -F "file=@questions.csv"
```

Antwort:

```json
{"imported": 42}
```

## Fragen exportieren

Endpoint: `GET /questions/export` — liefert CSV mit `question,answer`.

```bash
curl -o questions_export.csv "http://localhost:8000/questions/export"
```

## Einzelantwort bewerten (API)

Endpoint: `POST /exam/evaluate_answer`

Wichtigste Felder (aus `AnswerEvaluationBody`):
- `unique_exam_id` (string)
- `question` (string)
- `student_answer` (string)
- `correct_answer` (string)
- `max_points` (int)
- `evaluate_only` (bool) — wenn true: keine Folgefrage
- `parent_id` (int) — für Folgefragen/Clarify
- `question_type` (string) — z. B. `BASE` oder `CLARIFY`

Beispiel:

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

Beispielantwort:

```json
{
  "feedback": "Gute Struktur, aber einige Punkte fehlen...",
  "rating": 3.0,
  "next_action": "NONE",
  "followup_text": "",
  "answer_id": 17,
  "next_max_points": 0,
  "next_answer": ""
}
```

## Gesamtevaluation einer Prüfung

- Endpoint: `POST /exam/evaluate_exam` mit Body `{ "unique_exam_id": "exam-123" }`.
- Die API aggregiert gespeicherte Einzelbewertungen und erzeugt ein finales Feedback (in `exam_evaluation_final`).

```bash
curl -X POST "http://localhost:8000/exam/evaluate_exam" -H "Content-Type: application/json" -d '{"unique_exam_id":"exam-123"}'
```

Antwort (Beispiel):

```json
{
  "final_feedback": "Stärken: ... Schwächen: ... Konkrete Verbesserungen: ..."
}
```

## Noten / Punkte abrufen

- Endpoint: `GET /exam_evaluation_single_answers/exam_scores/{exam_id}`
- Antwort enthält: `total_points`, `max_points`, `percentage`, `grade`.

```bash
curl "http://localhost:8000/exam_evaluation_single_answers/exam_scores/exam-123"
```

## Praktische Tipps

- Nutze `evaluate_only=true` beim API‑Call, wenn du keine Folgefragen willst.
- Verwende eindeutige `unique_exam_id` pro Prüfungssession, damit Bewertungen korrekt aggregiert werden.

## Fehler & Support

- CORS‑Probleme: `backend/app/main.py` prüfen (Origins).
- Backend‑Fehler: Server‑Logs / Uvicorn Konsole anschauen.
- LLM‑Probleme: `app/services/llm_handler.py` und LLM‑Server prüfen.

Bei Fragen oder Erweiterungswünschen erstelle bitte ein Issue oder kontaktiere das Entwicklerteam.
