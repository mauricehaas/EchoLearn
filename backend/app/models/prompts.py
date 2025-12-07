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


evaluate_student_answer = """Bitte vergleiche die folgende Studentenantwort mit der bereitgestellten Musterlösung.
Analysiere dabei:

Inhaltliche Korrektheit
- Welche Schlüsselpunkte der Musterlösung wurden getroffen?
- Welche wichtigen Aspekte fehlen?
- Welche Aussagen sind falsch oder unvollständig?

Gesamtbewertung der inhaltlichen Qualität.
- Tiefe und Präzision der Erklärung
- Wie gut wird das Konzept erklärt?
- Ist die Antwort oberflächlich, ausreichend detailliert oder sehr präzise?

Sprachliche und formale Qualität
- Verwenden von Füllwörtern, unsicheren Formulierungen („äh“, „ähm“, „vielleicht“, „glaube“, „eventuell“ etc.).
- Klarheit, Struktur, Verständlichkeit.
- Professioneller oder unsicherer Sprachstil.

Verbesserungsvorschläge
- Was sollte der Student inhaltlich besser machen?
- Wie könnte die sprachliche Darstellung verbessert werden?

Gib am Ende ein knappes Gesamtrating (z. B. sehr gut / gut / ausreichend / mangelhaft).

Wichtige Regel: Die gesamte Ausgabe muss in deutscher Sprache erfolgen.

Studentenantwort:
{student_answer}

Musterlösung:
{correct_answer}

Wähle bitte die nächste Frage für den Studenten aus dem folgenden Fragenkatalog aus:
{questions}

<Antwortformat>
```json
{{
"feedback_content": "<Hier antwortest du auf die Antwort des Studenten und gibts ihm Feedback entsprechend der Analysepunkte. Die Antwort ist ein Text, es gibt keine JSON-Struktur>",
"question": "<Die nächste ausgewählte Frage wortgenau aus dem Fragenkatalog>",
"statement": "<Hier gehst du kurz auf die Antwort des Studenten ein, anschließend stellst du die nächste Frage, als wärst du im Prüfungsgespräch.>",
"overall_rating": "<Gesamtrating (z. B. sehr gut / gut / ausreichend / mangelhaft)>"
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
