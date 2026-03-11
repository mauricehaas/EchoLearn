# Allgemeine Dokumentation

## Motivation

Die Vorbereitung auf mündliche Prüfungen ist oft eingeschränkt, da sie typischerweise eine zweite Person erfordert und reale Prüfungssituationen nur schwer reproduzierbar sind.

Digitale Lernsysteme bieten häufig nur:

- Multiple-Choice-Tests
- statische Übungsfragen
- nicht-interaktive Lernmaterialien

EchoLearn verfolgt den Ansatz, einen adaptiven Prüfungsdialog zu simulieren, der auf Antworten reagiert und gezielte Rückfragen stellt.

---

## Projektziel

Ziel von EchoLearn ist die Entwicklung eines Systems zur Unterstützung der Vorbereitung auf mündliche Prüfungen durch automatisierte Dialogsimulation.

Der Fokus liegt auf:

- Simulation prüfungsähnlicher Dialoge
- automatisierter Bewertung offener Antworten
- adaptiver Gesprächsführung durch Rückfragen
- Analyse individueller Lernverläufe
- sprachbasierter Mensch-Maschine-Interaktion

Das Projekt untersucht insbesondere, inwieweit große Sprachmodelle zur formativen Bewertung und dialogischen Lernunterstützung eingesetzt werden können.

---

## Ursprüngliche Pitch Beschreibung

Die Idee ist eine KI-gestützte Lernplattform zur ganzheitlichen Vorbereitung auf mündliche Prüfungen. Ziel ist es, nicht nur Wissen aufzubauen, sondern die tatsächliche Prüfungssituation realitätsnah zu trainieren.

Im Zentrum steht eine intelligente Prüfungssimulation, wobei die KI die Rolle der prüfenden Person übernimmt, fachliche Fragen stellt, dynamisch auf Antworten reagiert und durch gezielte Rückfragen zu präziserem Denken und Argumentieren herausfordert, ähnlich wie in einer echten mündlichen Prüfung. Im Anschluss erfolgt eine differenzierte Bewertung der Leistung mit individuellem Feedback zu Inhalt, Argumentationsstruktur, sprachlicher Klarheit und Prüfungskompetenz.

Ergänzend dazu umfasst das Konzept einen Trainingsbereich, der auf lernpsychologischen Prinzipien wie Active Recall und Spaced Repetition basiert. Inhalte werden aktiv abgefragt, wiederholt und langfristig gefestigt. Dabei erfolgt die Interaktion sowohl schriftlich als auch mündlich: Lernende erklären Inhalte laut, beantworten Fragen verbal und trainieren so neben Fachwissen auch ihre Ausdrucksfähigkeit und spontane Reaktionskompetenz.

Die Vision: Eine Plattform, die Wissensaufbau, Anwendung und Performanztraining verbindet – damit Lernende nicht nur wissen, was richtig ist, sondern es auch souverän und strukturiert ausdrücken können.

---

## Methodischer Ansatz

Die Bewertung freier Antworten erfolgt über semantische Analyse mithilfe eines großen Sprachmodells.  
Antworten werden mit erwarteten Konzepten verglichen, um Verständnis zu bewerten und gezielte Rückfragen zu erzeugen.

Das System bildet damit eine dialogische Prüfungsinteraktion nach.

---

## Limitationen

- Bewertung basiert auf probabilistischen Sprachmodellen
- keine pädagogische Validierung der Bewertungsqualität
- keine Benutzerstudie zur Wirksamkeit
- Speech-to-Text abhängig von Audioqualität
- eingeschränkte inhaltliche Domänen

---

## Mögliche Weiterentwicklungen

- empirische Evaluation mit Studierenden
- adaptive Schwierigkeitsmodelle
- personalisierte Lernpfade
- Benutzerkonten und Langzeittracking
- Lernmodus (Active Recall und Spaced Repetition) implementieren
