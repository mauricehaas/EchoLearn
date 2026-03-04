# Dokumentation des Backends

## Backend‑Überblick

Das Backend verwaltet Fragen und Benutzer, nimmt Prüfungsantworten entgegen, bewertet diese mit einem LLM und persistiert sowohl Einzelbewertungen als auch Gesamtauswertungen in der Datenbank.

Architektonisch trennt das System klar zwischen:
- HTTP‑Schnittstelle (`routers/`) für Ein- und Ausgabe,
- fachlicher Orchestrierung (`services/`) für Bewertungslogik und LLM‑Kommunikation,
- Persistenz (`models/`, `core/db.py`) für strukturierte Speicherung der Ergebnisse.

Der Schwerpunkt liegt auf einem prüfungsnahen Ablauf: Jede Antwort wird nicht nur punktuell bewertet, sondern kann abhängig von der Qualität direkt eine passende nächste Interaktion auslösen (Vertiefung, Klärung oder Themenwechsel).

## Ordnerstruktur

Das Backend ist in folgende Hauptverzeichnisse gegliedert:

- `core/`: Hier wird die Datenbankverbindung initialisiert (siehe `app/core/db.py`).
- `models/`: Declarative SQLAlchemy‑Modelle, die die Datenbanktabellen definieren.
- `routers/`: FastAPI‑Router mit den HTTP‑Endpunkten.
- `seed/`: Skripte zum Erstellen der Tabellen und Befüllen mit Beispieldaten.
- `services/`: Logik zur Prüfungssimulation und zur LLM‑Integration.
- `utils/`: Hilfsfunktionen (aktuell leer).

In der Datei _main.py_ wird die FastAPI‑Anwendung initialisiert und als HTTP‑Server bereitgestellt.

## Komponenten

- **Backend:** FastAPI mit asynchronem SQLAlchemy (siehe `app/core/db.py`). Die DB‑Connection nutzt `postgresql+asyncpg`.
- **ORM:** Declarative SQLAlchemy‑Modelle in `app/models/` (z. B. `Question`, `User`, `ExamEvaluationSingleAnswer`, `ExamEvaluationFinal`).
- **Services:** Prüfungssimulation und LLM‑Integration in `app/services/` (`exam_simulator.py`, `llm_handler.py`, `prompts.py`).
- **Router / Endpoints:** REST‑API in `app/routers/` (z. B. `questions.py`, `users.py`, `exam.py`, `exam_evaluation_single_answers.py`).

## Datenbank

- **Connection‑String** (in `app/core/db.py`):

  `postgresql+asyncpg://echolearn:echolearn@db:5432/echolearn`

- Das Seed‑Skript `backend/app/seed/seed_data.py` erstellt die Tabellen und befüllt sie mit Beispieldaten aus `data/processed/questions.csv`.

## Modelle (DB)

- `Question` (`questions`)
  - `id`: `Integer`, `primary_key=True`, `index=True`
  - `question`: `Text`, `nullable=False`
  - `answer`: `Text`, `nullable=False`
  - `max_points`: `Text`, `nullable=False`

- `User` (`users`)
  - `id`: `Integer`, `primary_key=True`, `index=True`
  - `username`: `String(100)`, `unique=True`, `nullable=False`
  - `password_hash`: `String(255)`, `nullable=False`
  - `role`: `String(50)`, `nullable=False`, `default="user"`

- `ExamEvaluationSingleAnswer` (`exam_evaluation_single_answer`)
  - `id`: `Integer`, `primary_key=True`, `index=True`
  - `parent_id`: `Integer`
  - `unique_exam_id`: `Text`, `nullable=False`
  - `question_type`: `Text`, `nullable=False`
  - `question`: `Text`, `nullable=False`
  - `student_answer`: `Text`, `nullable=False`
  - `correct_answer`: `Text`, `nullable=False`
  - `feedback`: `Text`, `nullable=False`
  - `rating`: `Text`, `nullable=False`
  - `max_points`: `Text`, `nullable=False`

- `ExamEvaluationFinal` (`exam_evaluation_final`)
  - `id`: `Integer`, `primary_key=True`, `index=True`
  - `unique_exam_id`: `Text`, `nullable=False`
  - `overall_feedback`: `Text`, `nullable=False`

## LLM‑Integration

Die LLM‑Integration ist als eigener Service gekapselt (`backend/app/services/llm_handler.py`) und dient als technische Schnittstelle zwischen Fachlogik und Modellserver. Dadurch bleibt der Rest des Backends unabhängig von HTTP‑Details, Antwortformaten und Parsing.

**Technischer Ablauf pro LLM‑Aufruf:**
- `ExamSimulator` erstellt aus einem Prompt‑Template plus Laufzeitdaten einen vollständigen Prompt.
- `LLMHandler.call_llm(prompt)` sendet einen `POST` an den Endpoint:

  `http://catalpa-llm.fernuni-hagen.de:11434/api/generate`

- Request‑Payload:
  - `model` (Standard: `phi4:latest`)
  - `prompt` (Template + konkrete Inhalte der aktuellen Prüfungssituation)
- Die Antwort wird in zwei Schritten aufbereitet:
  - JSON‑Lines werden zu einem konsistenten Antworttext zusammengeführt.
  - Aus dem Antworttext wird der JSON‑Block extrahiert und als Python‑`dict` zurückgegeben.

**Rolle der Prompt‑Templates (`backend/app/services/prompts.py`):**
- `evaluate_student_answer`: Punktzahl + Feedback pro Einzelantwort
- `evaluate_exam`: Gesamtfeedback über die gesamte Prüfung
- `rephrase_question`: didaktische Vereinfachung einer Frage
- `next_question`: vertiefende Folgefrage bei hoher Qualität
- `clarify`: minimaler Hinweis bei teilweise korrekter Antwort

## Kernlogik: Prüfungssimulation

Der `ExamSimulator` (`app/services/exam_simulator.py`) bildet die fachliche Kernlogik des Backends. Er steuert den Prüfungsdialog, entscheidet über den nächsten Schritt nach jeder Antwort und sorgt für persistente Nachvollziehbarkeit.

**Ablauf bei der Bewertung einer Einzelantwort (`evaluate_student_answer`):**
1. Die Studentenantwort wird mit `evaluate_student_answer` durch das LLM bewertet.
2. Aus dem Rating wird ein Prozentwert relativ zu `max_points` berechnet.
3. Daraus wird die nächste Aktion abgeleitet:
   - `DEEPEN` bei starker Antwort (>= 80 %) mit neuer Vertiefungsfrage,
   - `CLARIFY` bei teils korrekter Antwort (50-79.99 %) mit kurzem Hinweis,
   - `ADVANCE` bei schwacher Antwort (< 50 %) ohne zusätzliche Klärungsrunde,
   - `EVALUATE_ONLY`, falls explizit nur bewertet werden soll.
4. Die Einzelbewertung wird immer in `exam_evaluation_single_answer` gespeichert.

**Ablauf bei der Gesamtauswertung (`evaluate_the_exam`):**
1. Alle Einzelbewertungen einer `unique_exam_id` werden aus der DB gelesen.
2. Feedback und Ratings werden aggregiert und als Kontext an das LLM gegeben.
3. Das resultierende Gesamtfeedback wird in `exam_evaluation_final` gespeichert.

Ergänzende Funktionen:
- `rephrase_question`: sprachliche Anpassung einer Frage vor oder während der Prüfung.
- `next_question` und `clarify`: dynamische Steuerung der Dialogtiefe innerhalb derselben Prüfungssitzung.

## API‑Referenz & Beispiele

Wichtige Endpunkte (ausführlich):

- <span style="background:#1d4ed8;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">GET</span> ` /questions/`
  - Zweck: Liefert alle gespeicherten Fragen aus der Tabelle `questions`.
  - Eingabeparameter: keine.
  - Request-Body: keiner.
  - Response: Array von `Question`-Objekten (`id`, `question`, `answer`, `max_points`).

- <span style="background:#1d4ed8;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">GET</span> ` /questions/{question_id}`
  - Zweck: Liefert genau eine Frage anhand ihrer ID.
  - Eingabeparameter (Path): `question_id: int`.
  - Request-Body: keiner.
  - Response: ein `Question`-Objekt.
  - Fehlerfälle: `404`, wenn die ID nicht existiert.

- <span style="background:#16a34a;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">POST</span> ` /questions/import`
  - Zweck: Importiert mehrere Fragen aus einer CSV-Datei in die Datenbank.
  - Eingabeparameter: Multipart-Form-Field `file` (UploadFile).
  - Erwartetes CSV-Format: Spalten `question` und `answer` (Header verpflichtend).
  - Request-Body: `multipart/form-data`.
  - Response: `{"imported": <anzahl>}`.
  - Fehlerfälle: `400` bei fehlender Datei oder falschem Dateityp.

- <span style="background:#1d4ed8;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">GET</span> ` /questions/export`
  - Zweck: Exportiert alle Fragen als CSV-Datei.
  - Eingabeparameter: keine.
  - Request-Body: keiner.
  - Response: CSV mit `Content-Disposition: attachment; filename=questions.csv`.

- <span style="background:#1d4ed8;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">GET</span> ` /users/`
  - Zweck: Liefert alle Benutzer.
  - Eingabeparameter: keine.
  - Request-Body: keiner.
  - Response: Array von `User`-Objekten (`id`, `username`, `password_hash`, `role`).

- <span style="background:#1d4ed8;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">GET</span> ` /users/{user_id}`
  - Zweck: Liefert einen Benutzer anhand der ID.
  - Eingabeparameter (Path): `user_id: int`.
  - Request-Body: keiner.
  - Response: ein `User`-Objekt.
  - Fehlerfälle: `404`, wenn kein Benutzer gefunden wurde.

- <span style="background:#16a34a;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">POST</span> ` /exam/rephrase_question`
  - Zweck: Formuliert eine gegebene Frage sprachlich einfacher um, ohne den Inhalt zu ändern.
  - Eingabeparameter: keine Path-/Query-Parameter.
  - Request-Body (JSON):
    ```json
    {
      "question": "Originalfrage"
    }
    ```
  - Response (JSON): LLM-Antwort als Objekt, z. B.
    ```json
    {
      "answer_llm": "Vereinfachte Frage"
    }
    ```

- <span style="background:#16a34a;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">POST</span> ` /exam/evaluate_answer`
  - Zweck: Bewertet eine einzelne Studentenantwort per LLM, speichert die Bewertung in der DB und liefert optional Folgeaktion/-frage.
  - Eingabeparameter: keine Path-/Query-Parameter.
  - Request-Body (JSON):
    ```json
    {
      "unique_exam_id": "exam-123",
      "question": "Fragetext",
      "student_answer": "Antwort des Studierenden",
      "correct_answer": "Musterlösung",
      "max_points": 5,
      "evaluate_only": false,
      "parent_id": 0,
      "question_type": "BASE"
    }
    ```
  - Feldbedeutung:
    - `unique_exam_id`: fachliche Klammer für alle Antworten einer Prüfung.
    - `evaluate_only`: `true` = nur bewerten, keine Folgefrage/-hinweise.
    - `parent_id`: Referenz auf vorherige Antwort (für Folgefragen/Klärungen).
    - `question_type`: Kennzeichnung des Antworttyps (z. B. `BASE`, `CLARIFY`).
  - Response (JSON):
    ```json
    {
      "feedback": "Kurz und prägnant...",
      "rating": 3.5,
      "next_action": "DEEPEN",
      "followup_text": "Vertiefungsfrage oder Hinweis",
      "answer_id": 12,
      "next_max_points": 5,
      "next_answer": "Musterlösung zur Vertiefungsfrage"
    }
    ```
  - Mögliche `next_action`:
    - `EVALUATE_ONLY` (wenn `evaluate_only=true`)
    - `DEEPEN` (bei guter Antwort)
    - `CLARIFY` (bei teilweise korrekter Antwort)
    - `ADVANCE` (bei schwacher Antwort, ohne Folgefrage)

- <span style="background:#16a34a;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">POST</span> ` /exam/evaluate_exam`
  - Zweck: Erstellt aus allen Einzelbewertungen einer Prüfung eine Gesamtevaluation und speichert sie.
  - Eingabeparameter: keine Path-/Query-Parameter.
  - Request-Body (JSON):
    ```json
    {
      "unique_exam_id": "exam-123"
    }
    ```
  - Response (JSON):
    ```json
    {
      "final_feedback": "Gesamtevaluierung der Prüfung"
    }
    ```

- <span style="background:#1d4ed8;color:#ffffff;padding:2px 6px;border-radius:4px;font-weight:700;">GET</span> ` /exam_evaluation_single_answers/exam_scores/{exam_id}`
  - Zweck: Berechnet die Gesamtpunkte und Note einer Prüfung anhand aller gespeicherten Einzelbewertungen.
  - Eingabeparameter (Path): `exam_id: str` (entspricht `unique_exam_id`).
  - Request-Body: keiner.
  - Response (JSON):
    ```json
    {
      "total_points": 18.5,
      "max_points": 25.0,
      "percentage": 74.0,
      "grade": "2,7"
    }
    ```
  - Fehlerfälle: `404`, wenn keine Bewertungen zur `exam_id` vorhanden sind.
