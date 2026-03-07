# Dokumentation des Backends

## Backend-Überblick

Das EchoLearn-Backend ist der Teil des Systems, der den Prüfungsablauf im Hintergrund steuert.  
Es verwaltet Fragen, nimmt Antworten entgegen, lässt diese vom LLM bewerten und speichert sowohl Einzelbewertungen als auch das Gesamtfeedback einer Sitzung.

Grob ist der Code in drei Bereiche aufgeteilt:
- `routers/`: Hier kommen HTTP-Anfragen an und werden an die passende Logik weitergegeben.
- `services/`: Hier liegt die eigentliche Fachlogik (z. B. Bewertung und nächste Aktion).
- `models/` + `core/db.py`: Hier ist definiert, wie Daten gespeichert werden.

## Aktuelle Ordnerstruktur

- `backend/app/main.py`: Startpunkt der FastAPI-Anwendung, inklusive CORS und Router-Einbindung
- `backend/app/core/`: Basis-Setup wie die Datenbankverbindung (`db.py`)
- `backend/app/models/`: SQLAlchemy-Modelle für die Tabellen
- `backend/app/routers/`: API-Endpunkte
- `backend/app/services/`: LLM-Integration und Prüfungslogik
- `backend/app/seed/`: Seed-Skript zum Neuaufsetzen der Tabellen und Befüllen mit Startdaten
- `backend/app/utils/`: vorhanden, derzeit ohne aktive Nutzung

## Aktive Router in `main.py`

Aktuell sind folgende Router aktiv eingebunden:
- `questions.router`
- `exam.router`
- `exam_evaluation_single_answers.router`

## Datenbank

- Verbindungs-URL in `backend/app/core/db.py`:
  - `postgresql+asyncpg://echolearn:echolearn@db:5432/echolearn`

- `backend/app/seed/seed_data.py`:
  - setzt die Tabellen neu auf (`drop_all` + `create_all`)
  - lädt Fragen aus `data/processed/questions.csv` in die Datenbank

## Modelle

- `Question` (`questions`)
  - `id` (`Integer`, PK)
  - `question` (`Text`, Pflicht)
  - `answer` (`Text`, Pflicht)
  - `max_points` (`Text`, Pflicht)

- `ExamEvaluationSingleAnswer` (`exam_evaluation_single_answer`)
  - `id` (`Integer`, PK)
  - `parent_id` (`Integer`)
  - `unique_exam_id` (`Text`, Pflicht)
  - `question_type` (`Text`, Pflicht)
  - `question` (`Text`, Pflicht)
  - `student_answer` (`Text`, Pflicht)
  - `correct_answer` (`Text`, Pflicht)
  - `feedback` (`Text`, Pflicht)
  - `rating` (`Text`, Pflicht)
  - `max_points` (`Text`, Pflicht)

- `ExamEvaluationFinal` (`exam_evaluation_final`)
  - `id` (`Integer`, PK)
  - `unique_exam_id` (`Text`, Pflicht)
  - `overall_feedback` (`Text`, Pflicht)

## LLM-Integration

Die Kommunikation mit dem Modellserver ist zentral in `backend/app/services/llm_handler.py` gekapselt.  
So bleibt die Fachlogik unabhängig von den technischen Details des LLM-Aufrufs.

- Modellserver:
  - `http://catalpa-llm.fernuni-hagen.de:11434/api/generate`

- Standardmodell:
  - `phi4:latest`

- Prompt-Quellen:
  - `backend/app/services/prompts.py`

- Fachliche Orchestrierung:
  - `backend/app/services/exam_simulator.py`

## API-Referenz

### Questions (`/questions`)

- <span style="background:#1d4ed8;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">GET</span> ` /questions/`
  - gibt alle gespeicherten Fragen zurück
  - Eingabeparameter: keine
  - Request-Body: keiner
  - Response (JSON):
    ```json
    [
      {
        "id": 1,
        "question": "Was ist ...?",
        "answer": "Die Antwort ist ...",
        "max_points": "5"
      }
    ]
    ```

- <span style="background:#1d4ed8;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">GET</span> ` /questions/random`
  - liefert bis zu 7 zufällige Fragen für eine Session
  - Eingabeparameter: keine
  - Request-Body: keiner
  - Response (JSON):
    ```json
    [
      {
        "id": 3,
        "question": "Erkläre ...",
        "answer": "Dabei gilt ...",
        "max_points": "5"
      }
    ]
    ```

- <span style="background:#1d4ed8;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">GET</span> ` /questions/{question_id}`
  - liefert eine einzelne Frage anhand der ID
  - Eingabeparameter (Path): `question_id: int`
  - Request-Body: keiner
  - Response (JSON):
    ```json
    {
      "id": 1,
      "question": "Was ist ...?",
      "answer": "Die Antwort ist ...",
      "max_points": "5"
    }
    ```
  - `404`, wenn nicht vorhanden

- <span style="background:#16a34a;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">POST</span> ` /questions/`
  - legt eine neue Frage an
  - Eingabeparameter: keine
  - Body:
    ```json
    {
      "question": "Frage",
      "answer": "Antwort",
      "max_points": "5"
    }
    ```
  - Response (JSON):
    ```json
    {
      "id": 42,
      "question": "Frage",
      "answer": "Antwort",
      "max_points": "5"
    }
    ```

- <span style="background:#d97706;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">PATCH</span> ` /questions/{question_id}`
  - aktualisiert einzelne Felder einer Frage (`question`, `answer`, `max_points`)
  - Eingabeparameter (Path): `question_id: int`
  - Body (alle Felder optional):
    ```json
    {
      "question": "Neue Frage",
      "answer": "Neue Antwort",
      "max_points": "6"
    }
    ```
  - Response (JSON):
    ```json
    {
      "id": 42,
      "question": "Neue Frage",
      "answer": "Neue Antwort",
      "max_points": "6"
    }
    ```
  - `404`, wenn nicht vorhanden

- <span style="background:#dc2626;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">DELETE</span> ` /questions/{question_id}`
  - löscht eine Frage
  - Eingabeparameter (Path): `question_id: int`
  - Request-Body: keiner
  - Response (JSON):
    ```json
    {
      "message": "Question deleted successfully"
    }
    ```
  - `404`, wenn nicht vorhanden

- <span style="background:#16a34a;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">POST</span> ` /questions/import`
  - importiert Fragen aus einer CSV-Datei (Multipart, Feld `file`)
  - Eingabeparameter: keine
  - erwartet Spalten: `question`, `answer`, `max_points`
  - Antwort: `{"imported": <anzahl>}`
  - Response (JSON):
    ```json
    {
      "imported": 25
    }
    ```
  - `400` bei fehlender Datei/falschem Dateityp

- <span style="background:#1d4ed8;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">GET</span> ` /questions/export`
  - exportiert alle Fragen als CSV (`questions.csv`)
  - Eingabeparameter: keine
  - Request-Body: keiner
  - Response:
    - kein JSON
    - `text/csv; charset=utf-8`
    - Header: `Content-Disposition: attachment; filename=questions.csv`

### Exam (`/exam`)

- <span style="background:#16a34a;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">POST</span> ` /exam/rephrase_question`
  - formuliert eine Frage verständlicher um (inhaltlich gleich)
  - Eingabeparameter: keine
  - Body:
    ```json
    { "question": "Originalfrage" }
    ```
  - Response (JSON):
    ```json
    {
      "answer_llm": "Vereinfachte Version der Frage"
    }
    ```

- <span style="background:#16a34a;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">POST</span> ` /exam/evaluate_answer`
  - bewertet eine einzelne Antwort
  - kann abhängig vom Ergebnis eine Folgeaktion/Folgefrage auslösen
  - Eingabeparameter: keine
  - Body:
    ```json
    {
      "unique_exam_id": "exam-123",
      "question": "Fragetext",
      "student_answer": "Antwort",
      "correct_answer": "Musterlösung",
      "max_points": 5,
      "evaluate_only": false,
      "parent_id": 0,
      "question_type": "BASE"
    }
    ```
  - Response (JSON):
    ```json
    {
      "feedback": "Fachlich solide, ein Aspekt fehlt noch.",
      "rating": 3.5,
      "next_action": "CLARIFY",
      "followup_text": "Gehe noch auf ... ein.",
      "answer_id": 12,
      "next_max_points": 0,
      "next_answer": ""
    }
    ```

- <span style="background:#16a34a;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">POST</span> ` /exam/evaluate_exam`
  - erstellt das Gesamtfeedback für eine komplette Prüfung
  - Eingabeparameter: keine
  - Body:
    ```json
    { "unique_exam_id": "exam-123" }
    ```
  - Response (JSON):
    ```json
    {
      "final_feedback": "Insgesamt zeigst du ein gutes Verständnis ..."
    }
    ```

### Exam-Einzelbewertungen (`/exam_evaluation_single_answers`)

- <span style="background:#1d4ed8;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">GET</span> ` /exam_evaluation_single_answers/`
  - liefert alle gespeicherten Einzelbewertungen
  - Eingabeparameter: keine
  - Request-Body: keiner
  - Response (JSON):
    ```json
    [
      {
        "id": 12,
        "parent_id": 0,
        "unique_exam_id": "exam-123",
        "question_type": "BASE",
        "question": "Fragetext",
        "student_answer": "Antwort",
        "correct_answer": "Musterlösung",
        "feedback": "Feedback",
        "rating": "3.5",
        "max_points": "5.0"
      }
    ]
    ```

- <span style="background:#1d4ed8;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">GET</span> ` /exam_evaluation_single_answers/exam/{exam_id}`
  - liefert die Einzelbewertungen zu einer bestimmten `exam_id`
  - Eingabeparameter (Path): `exam_id: str`
  - Request-Body: keiner
  - Response (JSON):
    ```json
    [
      {
        "id": 12,
        "parent_id": 0,
        "unique_exam_id": "exam-123",
        "question_type": "BASE",
        "question": "Fragetext",
        "student_answer": "Antwort",
        "correct_answer": "Musterlösung",
        "feedback": "Feedback",
        "rating": "3.5",
        "max_points": "5.0"
      }
    ]
    ```
  - `404`, wenn keine Daten vorhanden

- <span style="background:#1d4ed8;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">GET</span> ` /exam_evaluation_single_answers/exam_scores/{exam_id}`
  - berechnet Gesamtpunkte, Prozentwert und Note für eine Prüfung
  - Eingabeparameter (Path): `exam_id: str`
  - Request-Body: keiner
  - Response (JSON):
    ```json
    {
      "total_points": 18.5,
      "max_points": 25.0,
      "percentage": 74.0,
      "grade": "2,7"
    }
    ```
  - `404`, wenn keine Daten vorhanden

## Fachlogik

`ExamSimulator` steuert den Ablauf nach jeder Antwort:
- gute Antwort: `DEEPEN`
- teilweise korrekt: `CLARIFY`
- schwach: `ADVANCE`
- nur Bewertung angefordert: `EVALUATE_ONLY`

Einzelbewertungen landen in `exam_evaluation_single_answer`, das finale Gesamtfeedback in `exam_evaluation_final`.
