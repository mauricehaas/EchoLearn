begin_exam = """
Du bist ein Data-Science-Prüfungsgenerator.
Begrüße den Studenten freundlich und erkläre kurz den Ablauf sowie die Bedingungen der Prüfung.

Wähle anschließend genau eine Frage aus dem folgenden Fragenkatalog aus und stelle sie dem Studenten wortgleich:

<Fragenkatalog>
{questions}
</Fragenkatalog>

Wichtige Regeln:
- Stelle die Frage ausschließlich so, wie sie im Fragenkatalog steht (keine Umformulierungen).
- Die gesamte Ausgabe muss in deutscher Sprache erfolgen.
- Beende deine Ausgabe mit der ausgewählten Frage.

<Antwortformat>
```json
{{
"question": "<Die ausgewählte Frage wortgenau aus dem Fragenkatalog>",
"statement": "<Die gesamte Ausgabe inklusive Begrüßung, Erklärung und der ausgewählten Frage>"
}}
```
"""


evaluate_student_answer = """Bitte vergebe bis zu 5 Punkte für die folgende Studentenantwort auf die gegebene Frage. Für die Orientierung bekommst du eine bereitgestellte Musterlösung.
Vergebe die Punkte folgendermaßen:

Inhaltliche Korrektheit
- Wurden die Antwort komplett richtig und vollständig beantwortet, vergebe 5 Punkte
- Wenn nicht, dann vergebe die erreichten Punkte prozentual 

Gebe zusätzlich Verbesserungsvorschläge
- Was sollte der Student inhaltlich besser machen?
- Welche Schlüsselpunkte der Musterlösung wurden getroffen?
- Welche Aussagen sind falsch oder unvollständig?

Gib am Ende ein knappes Gesamtrating (0-5 Punkte). Gerundet auf eine Nachkommastelle

Wichtige Regel: Die gesamte Ausgabe muss in deutscher Sprache erfolgen.

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
"overall_rating": "<Gesamtrating (0-5 Punkte)>"
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
