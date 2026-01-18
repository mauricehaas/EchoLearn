begin_exam = """
Du bist ein Data-Science-Prüfungsgenerator.
Begrüße den Studenten freundlich und erkläre kurz den Ablauf sowie die Bedingungen der Prüfung.

Baue anschließend folgende Frage in deine Begrüßung ein. Am besten befindet sich die Frage am Ende deiner Aussage:
<Frage>
{question}
</Frage>

Wichtige Regeln:
- Stelle die Frage ausschließlich so, wie sie im Fragenkatalog steht (keine Umformulierungen).
- Die gesamte Ausgabe muss in deutscher Sprache erfolgen.

<Antwortformat>
```json
{{
"llm_answer": "<Die gesamte Ausgabe inklusive Begrüßung, Erklärung und der ausgewählten Frage>"
}}
```
"""

evaluate_student_answer = """
Analysiere die folgende Studentenantwort auf die gegebene Frage mithilfe der Musterlösung und entscheide, um welchen der folgenden Fälle es sich handelt:

Fall 1: Die Antwort des Studenten ist inhaltlich korrekt und vollständig.
Fall 2: Die Antwort des Studenten ist teilweise korrekt oder inkorrekt.

Wichtige Regeln:
- Wähle **genau einen** der drei Fälle.
- Gib **keine Begründung**, **keine Bewertung**, **keine Rückfragen** und **keinen zusätzlichen Text** aus.
- Die gesamte Ausgabe muss **ausschließlich** aus dem unten definierten JSON bestehen.
- Die gesamte Ausgabe muss in **deutscher Sprache** erfolgen.

Frage:
{question}

Studentenantwort:
{student_answer}

Musterlösung:
{correct_answer}

<Antwortformat>
```json
{{
  "case": "Fall 1 | Fall 2"
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

prompt_case_one_answer_correct_next_specific_question = """
Die Antwort des Studenten ist inhaltlich korrekt und vollständig.

Deine Aufgabe ist es, im Stil eines echten Prüfungsgesprächs zu reagieren und anschließend eine neue Prüfungsfrage zu stellen. Dabei darfst du frei entscheiden, ob:
- eine vertiefende Frage zum gleichen Themengebiet gestellt wird, oder
- eine weiterführende Frage zu einem neuen, aber fachlich angrenzenden Themengebiet gestellt wird.

Gehe dabei intern wie folgt vor (ohne dies auszugeben):
- Berücksichtige die ursprüngliche Frage und die Musterlösung.
- Beurteile die Qualität der Studentenantwort.
- Wähle eine sinnvolle nächste Prüfungsfrage, die das fachliche Verständnis weiter überprüft.

Erstelle anschließend fünf Ausgaben:

1) **answer_llm**  
   - Antworte dialogisch wie in einer mündlichen Prüfung.
   - Gehe kurz positiv auf die korrekte Antwort des Studenten ein.
   - Leite fließend zur neuen Prüfungsfrage über.
   - Keine detaillierte Bewertung oder Punktevergabe in diesem Feld.

2) **llm_feedback**  
   - Gib ein kurzes, sachliches Feedback zur Antwort des Studenten.
   - Hebe Stärken hervor (z. B. fachliche Korrektheit, Struktur, Vollständigkeit).
   - Maximal 2–3 Sätze.

3) **llm_rating**  
   - Vergib eine Gesamtbewertung zwischen **0 und 5 Punkten**.
   - Da es sich um Fall 1 handelt, muss die Bewertung **hoch ausfallen** (z. B. 4,0–5,0).
   - Gib nur die Zahl aus (z. B. `4.5`).

Wichtige Regeln:
- Stelle genau **eine** neue Frage.
- Gib keine Meta-Kommentare über dein Vorgehen aus.
- Die gesamte Ausgabe muss ausschließlich im unten definierten JSON-Format erfolgen.
- Die gesamte Ausgabe muss in deutscher Sprache erfolgen.

---

Frage:
{question}

Studentenantwort:
{student_answer}

Musterlösung:
{correct_answer}

---

<Antwortformat>
```json
{{
  "answer_llm": "<Dialogische Antwort im Prüfungskontext mit Überleitung zur neuen Frage>",
  "llm_feedback": "<Kurzes inhaltliches Feedback zur Antwort des Studenten>",
  "llm_rating": "<Gesamtbewertung (0–5 Punkte)>"
}}```
"""

prompt_case_two_answer_partially_correct_question_to_examine_knowledge_gaps = """
Die Antwort des Studenten ist teilweise korrekt oder inkorrekt.

Deine Aufgabe ist es, die Studentenantwort im Kontext der ursprünglichen Frage und der Musterlösung zu analysieren und darauf dialogisch zu reagieren.

Gehe dabei intern wie folgt vor (ohne dies auszugeben):
- Prüfe, ob die Studentenantwort zur ursprünglichen Frage passt.
- Vergleiche die Studentenantwort mit der Musterlösung.
- Identifiziere inhaltliche Lücken, unklare Stellen oder falsche Aussagen.
- Wähle die **wichtigste inhaltliche Lücke**, die für das Verständnis zentral ist.

Erstelle anschließend fünf Ausgaben:

1) **answer_llm**  
   - Antworte wie in einem Gespräch oder Prüfungskontext.
   - Gehe kurz auf richtige Aspekte der Studentenantwort ein.
   - Weise vorsichtig auf die zentrale inhaltliche Lücke hin.
   - Integriere fließend die neue Folgefrage.

2) **llm_feedback**  
   - Gib ein kurzes, sachliches Feedback zur Studentenantwort.
   - Benenne sowohl korrekte Aspekte als auch die wichtigste Schwäche.
   - Maximal 2–3 Sätze.

3) **llm_rating**  
   - Vergib eine Gesamtbewertung zwischen **0 und 5 Punkten**.
   - Die Bewertung soll dem inhaltlichen Stand der Antwort entsprechen (typischerweise **1,0–3,9 Punkte**).
   - Gib nur die Zahl aus (z. B. `2.5`).

4) **next_question**  
   - Formuliere **eine** gezielte Folgefrage, die auf die identifizierte Lücke abzielt.

5) **correct_answer**  
   - Gib die fachlich korrekte und vollständige Musterantwort auf diese Folgefrage an.

Wichtige Regeln:
- Stelle genau **eine** Folgefrage.
- Gib keine Meta-Erklärungen oder Hinweise auf dein Vorgehen aus.
- Die gesamte Ausgabe muss ausschließlich im unten definierten JSON-Format erfolgen.
- Die gesamte Ausgabe muss in deutscher Sprache erfolgen.

---

Frage:
{question}

Studentenantwort:
{student_answer}

Musterlösung:
{correct_answer}

---

<Antwortformat>
```json
{{
  "answer_llm": "<Dialogische Antwort mit Überleitung zur Folgefrage>",
  "llm_feedback": "<Kurzes Feedback zur Studentenantwort>",
  "llm_rating": "<Gesamtbewertung (0–5 Punkte)>",
  "next_question": "<Gezielte Folgefrage zur identifizierten Lücke>",
  "correct_answer": "<Fachlich korrekte Musterantwort auf die Folgefrage>"
}}```
"""

prompt_case_three_student_does_not_understand_question = """
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
