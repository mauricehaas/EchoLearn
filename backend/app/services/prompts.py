evaluate_student_answer = """Bitte vergebe bis zu {max_points} Punkte für die folgende Studentenantwort auf die gegebene Frage. Für die Orientierung bekommst du eine bereitgestellte Musterlösung.
Vergebe die Punkte folgendermaßen:

Inhaltliche Korrektheit
- Wurden die Antwort komplett richtig und vollständig beantwortet, vergebe {max_points} Punkte
- Wenn nicht, dann vergebe die erreichten Punkte prozentual 
- Gib ein kurzes, sachliches Feedback zur Antwort des Studenten.
- Hebe Stärken hervor (z. B. fachliche Korrektheit, Struktur, Vollständigkeit).
- Maximal 2–3 Sätze.

Gib am Ende ein knappes Gesamtrating (0-{max_points} Punkte). Gerundet auf eine Nachkommastelle

Wichtige Regeln: 
- Gib keine Meta-Kommentare über dein Vorgehen aus.
- Die gesamte Ausgabe muss ausschließlich im unten definierten JSON-Format erfolgen.
- Deutsch, Du-Form

Frage:
{question}

Studentenantwort:
{student_answer}

Musterlösung:
{correct_answer}

<Antwortformat>
```json
{{
"feedback_content": "<Hier antwortest du auf die Antwort des Studenten und gibts ihm Feedback entsprechend der Analysepunkte. Die Antwort ist ein Text, es gibt keine JSON-Struktur>",
"statement": "<Hier gehst du kurz auf die Antwort des Studenten ein.>",
"overall_rating": "<Gesamtrating (0-{max_points} Punkte)>"
}}```
"""

evaluate_exam = """
Bitte erstelle ausschließlich auf Basis der beiden folgenden Informationsquellen eine prägnante Gesamtevaluierung der gesamten Prüfung.

Du darfst keinerlei Informationen ergänzen, interpretieren oder erfinden, die nicht explizit in den beiden Strings enthalten sind.

<Aufgabenreihenfolge strikt einhalten>
1. Gesamtzusammenfassung der Prüfung (Stärken & wiederkehrende Schwächen)
2. Inhaltliche Gesamtbewertung (fachliche Beherrschung, starke & schwache Themen)
3. Konkrete Verbesserungsvorschläge (fachlich und strukturell)

<Wichtige Regeln>
- Verwende nur Informationen aus Feedback-String und Bewertungs-String
- Keine Beispiele erfinden
- Keine neuen Argumente hinzufügen
- Deutsch, Du-Form
- Maximal 5 kurze, informationsdichte Sätze
- Bewertungs-String muss in die Gesamtbewertung erkennbar einfließen

Feedback-String:
{overall_feedback}

Bewertungs-String:
{overall_rating}

<Antwortformat>
```json
{{
  "final_feedback": "<Gesamtevaluierung hier>",
}}```
"""

rephrase_question = """
Deine einzige Aufgabe ist es, den folgenden Text sprachlich umzuschreiben.

- Beantworte die Frage NICHT.
- Füge keine neuen Informationen hinzu.
- Entferne keine inhaltlichen Informationen.
- Ändere nur den Sprachstil: 
  von akademisch/kompliziert → zu klar, einfach, allgemeinverständlich.
- Vermeide Fachjargon, lange Schachtelsätze und abstrakte Formulierungen.
- Verwende jedoch keine Slang-Ausdrücke, keine Jugendsprache und keine lockeren Redewendungen.
- Die Bedeutung muss exakt gleich bleiben (bedeutungsinvariant).

Gib ausschließlich die umformulierte Frage aus, ohne Erklärung und ohne sie zu beantworten.

Text:
{question}

Antwortformat:
```json
{{
  "answer_llm": "<Die vereinfachte, allgemeinverständliche Version der Frage>"
}}
```
"""

next_question = """
Die Antwort des Studenten ist inhaltlich korrekt und vollständig.

Deine Aufgabe ist es, im Stil eines echten Prüfungsgesprächs zu reagieren und anschließend genau **eine neue Prüfungsfrage** zu stellen. Dabei darfst du entscheiden, ob:
- eine vertiefende Frage zum gleichen Themengebiet gestellt wird, oder
- eine weiterführende Frage zu einem neuen, aber fachlich angrenzenden Themengebiet gestellt wird.
- eine **Musterlösung zu der neuen Frage** in maximal 3 Sätzen anzugeben.

**Interne Schritte (nicht ausgeben):**
- Berücksichtige die ursprüngliche Frage und die Musterlösung.
- Wähle eine sinnvolle nächste Prüfungsfrage, die das fachliche Verständnis weiter überprüft, für die du genau 5 Punkte vergeben würdest.
- Gebe eine Musterlösung zu dieser neuen Prüfungsfrage an, welche maximal 3 Sätze lang sein darf.

**Wichtige Regeln:**
1. Gib nur die JSON-Antwort zurück, **keine zusätzlichen Kommentare oder Erklärungen**.
2. Verwende das exakte JSON-Format unten.
3. Die gesamte Ausgabe muss in deutscher Sprache erfolgen.

---

Frage:
{question}

Studentenantwort:
{student_answer}

Musterlösung:
{correct_answer}

---

Antwortformat:
```json
{{
  "question": "<string: Generierte Vertiefungsfrage>",
  "answer": "<string: Musterlösung zur generierten Vertiefungsfrage>"
}}
```
"""

clarify = """
Die Antwort des Studenten ist teilweise korrekt (ca. 50-80%).

Deine Aufgabe ist es, im Stil eines echten Prüfungsgesprächs zu reagieren und **nur einen minimalen Hinweis** zu geben, **welche Aspekte in der Antwort noch fehlen**, sodass der Student die Chance hat, den fehlenden Teil selbst zu ergänzen. Gib keine Musterlösungen, keine vollständigen Erklärungen und keine neuen Fragen.

**Interne Schritte (nicht ausgeben):**
- Analysiere die Studentenantwort im Hinblick auf die ursprüngliche Frage und Musterlösung.
- Gib **nur einen kurzen Hinweis**, der den Studenten auf die fehlenden oder unvollständigen Punkte aufmerksam macht.
- Ignoriere alles, was korrekt ist, außer um zu betonen, dass es korrekt ist.
- Gib keine Musterlösungen oder weiterführende Fragen.

**Wichtige Regeln:**
1. Gib nur die JSON-Antwort zurück, **keine zusätzlichen Kommentare oder Erklärungen**.
2. Verwende das exakte JSON-Format unten.
3. Die gesamte Ausgabe muss in deutscher Sprache erfolgen.

---

Frage:
{question}

Studentenantwort:
{student_answer}

Musterlösung:
{correct_answer}

---

Antwortformat:
```json
{{
  "hint": "<string: Minimaler Hinweis, welcher Teil der Antwort noch fehlt>"
}}
```
"""
