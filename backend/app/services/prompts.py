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
- Die gesamte Ausgabe muss in deutscher Sprache erfolgen.

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
Bitte erstelle auf Basis der folgenden zwei Informationsquellen eine umfassende Gesamtevaluierung der gesamten Prüfung:

Feedback-String: enthält alle inhaltlichen und sprachlichen Feedbacks zu den einzelnen Antworten

Bewertungs-String: enthält die jeweiligen Einzelbewertungen (z. B. Punkte, Noten oder qualitative Einstufungen)

<Aufgaben>
Gesamtzusammenfassung der Prüfung
- Welche Stärken zeigen sich über alle Antworten hinweg?
- Welche Schwächen treten wiederholt auf?

Inhaltliche Gesamtbewertung
- Wie gut beherrscht der Student die zentralen fachlichen Konzepte insgesamt?

- Welche Themenbereiche sind besonders stark bzw. schwach?

Sprachliche & kommunikative Gesamtbewertung
- Wie klar und präzise sind die Antworten insgesamt formuliert?
- Tritt Unsicherheit häufig auf (z. B. durch Füllwörter wie „äh“, „ähm“, „vielleicht“, „glaube“ etc.)?
- Wie gut ist der strukturelle Aufbau?

Verbesserungsvorschläge
- Fachlich
- Sprachlich
- Strukturell

Gesamtbewertung
- Fasse die Bewertung der gesamten Prüfung in einer abschließenden Note oder Qualitätsstufe zusammen (z. B. sehr gut / gut / ausreichend / mangelhaft oder vergleichbare Skala).
- Begründe diese Gesamtnote verständlich anhand der Inhalte aus Feedback- und Bewertungs-String.

Wichtige Hinweise:
- Verwende ausschließlich die Informationen aus beiden Strings.
- Formuliere die Gesamtevaluierung klar, strukturiert und in deutscher Sprache.
</Aufgaben>

Feedback-String:
{overall_feedback}

Bewertungs-String:
{overall_rating}

<Antwortformat>
```json
{{
  "final_feedback": "<string: Hier gibst du die gesamte Evaluierung der Prüfung wieder, inklusive Zusammenfassung, Stärken, Schwächen, Verbesserungsvorschläge und Gesamtbewertung.>",
  "final_rating": "<string: Hier gibst du die abschließende Note oder Qualitätsstufe der gesamten Prüfung wieder.>"
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

**Interne Schritte (nicht ausgeben):**
- Berücksichtige die ursprüngliche Frage und die Musterlösung.
- Wähle eine sinnvolle nächste Prüfungsfrage, die das fachliche Verständnis weiter überprüft.
- Bestimme eine angemessene Punktzahl für diese Frage, **maximal 5 Punkte**.

**Wichtige Regeln:**
1. Gib nur die JSON-Antwort zurück, **keine zusätzlichen Kommentare oder Erklärungen**.
2. Verwende das exakte JSON-Format unten.
3. Die gesamte Ausgabe muss in deutscher Sprache erfolgen.
4. `max_points` muss als String angegeben werden.

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
  "question": "<Generierte Vertiefungsfrage>",
  "correct_answer": "<Musterlösung zur generierten Vertiefungsfrage>",
  "max_points": "<Punkte als String, maximal '5'>"
}}
```
"""
