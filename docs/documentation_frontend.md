# Dokumentation des Frontends

## Frontend-Überblick

Das EchoLearn-Frontend ist modular aufgebaut und besteht aus **Views, Components und Composables**, die gemeinsam die Benutzeroberfläche und die Interaktivität bereitstellen.

---

## Aktuelle Ordnerstruktur

- `assets`: Globale SCSS-Dateien für das Design
- `components`: Vue 3 Komponenten
- `composables`: Vue 3 Composables
- `router`: Vue Router Setup
- `views`: Hauptseiten der Anwendung

---

## Views und Components

### Views

Views repräsentieren die Hauptseiten des Frontends und sind direkt mit **Routen** verbunden. Jede View kapselt die Logik und das Layout einer gesamten Seite.

- **Home.vue** – Startseite, zeigt Überblick und Einstiegsmöglichkeiten
- **Verwaltung.vue** – Verwaltung von Fragen und deren maximaler Punktzahl
- **Prüfungsbereich.vue** – Interaktive Prüfungsansicht für Studierende, inkl. Spracherkennung, Rückfragen und automatischer Bewertung
- **Statistik.vue** – Darstellung von Prüfungsergebnissen

**Funktionsweise:**

- Jede View wird über den **Vue Router** geladen
- Views enthalten mehrere Components, um die Seite modular aufzubauen

---

### Components

Components sind wiederverwendbare UI- oder Funktionsbausteine, die innerhalb von Views oder anderen Components eingesetzt werden.  
Sie kapseln einzelne Funktionalitäten oder Layout-Elemente und fördern die Wiederverwendbarkeit.

**Beispiele für Components in EchoLearn:**

- **AnswerBox.vue** – Enthält durch Speech-to-Text (STT) erkannten Text und Submit-Button
- **AppFooter.vue** – Footer
- **AppHeader.vue** – Header mit Navigation
- **Exam.vue** – Steuert den Prüfungsablauf im Prüfungsbereich und nutzt mehrere andere Components
- **ExamStats.vue** – Zeigt detaillierte Bewertungen zu jeder Frage im Statistikbereich
- **ExamSummary.vue** – Zeigt das Gesamtergebnis einer Prüfung, im Prüfungsbereich und in der Statistik
- **QuestionNavigation.vue** – Buttons für nächste Frage und Prüfungsabschluss
- **QuestionTable.vue** – Tabelle der Fragen mit CRUD-Funktionen im Verwaltungsbereich

**Vorteile von Components:**

- Wiederverwendbarkeit über mehrere Views hinweg
- Saubere Trennung von Layout und Logik
- Einfaches Testen einzelner Bausteine

---

## Composables

Im Frontend von **EchoLearn** werden zentrale Funktionen der Sprachinteraktion über **Vue 3 Composables** bereitgestellt. Composables sind wiederverwendbare Hooks, die Logik und Zustand kapseln und in mehreren Components genutzt werden können.

### 1. `useSpeechRecognition`

**Zweck:**  
Ermöglicht die Aufnahme und Transkription gesprochener Antworten. Unterstützt kontinuierliche Erkennung und Zwischenstände (interim results).

**Funktionsweise:**

- Initialisiert die Browser SpeechRecognition API (Webkit oder Standard)
- Liefert Refs für den finalen Transkripttext, Zwischenstände und Listening-Status
- Stellt Funktionen bereit:
  - `startListening()` – startet die Spracherkennung
  - `stopListening()` – stoppt die Spracherkennung
  - `restartListening()` – setzt Transkript und Status zurück

**Parameter:**  
Optional können eigene Refs für `transcriptRef`, `interimRef` und `listeningRef` übergeben werden. Sprache (`lang`) kann auf `'de-DE'` oder andere Sprachcodes gesetzt werden.

---

### 2. `speakText`

**Zweck:**  
Wandelt Text in Sprache um und gibt ihn über die Systemausgabe aus.

**Funktionsweise:**

- Nutzt die Browser SpeechSynthesis API
- Unterstützt die Auswahl der Sprache (`lang`) sowie Standardwerte für Geschwindigkeit (`rate`) und Tonhöhe (`pitch`)

**Parameter:**

- `text` – der zu sprechende Text
- `lang` – optional, Standard `'de-DE'`

---

### Vorteile der Composables

- Wiederverwendbarkeit in mehreren Components
- Logik ist vom UI getrennt
- Erleichtert Testbarkeit
- Erweiterbar für zusätzliche Features wie adaptive Filter oder Spracherkennungseinstellungen

---

## Routing

Die Navigation im Frontend von **EchoLearn** wird über **Vue Router** gesteuert. Das Projekt verwendet **`createWebHistory()`** für sauberes URL-Management ohne Hash (#).

### Routenübersicht

| Pfad          | Name            | Beschreibung                                |
| ------------- | --------------- | ------------------------------------------- |
| `/`           | Home            | Startseite                                  |
| `/verwaltung` | Verwaltung      | Verwaltung von Fragen und Daten             |
| `/pruefung`   | Prüfungsbereich | Interaktive Prüfungsansicht für Studierende |
| `/statistik`  | Statistik       | Lern- und Prüfungsergebnisse                |

**Funktionsweise:**

- Die Routen verbinden **Views (Seitenkomponenten)** mit spezifischen Pfaden
- Navigation erfolgt über `<router-link>` oder programmgesteuert (`router.push(...)`)
- Jede Route lädt die zugehörige View-Komponente und kapselt die jeweilige Funktionalität

**Vorteile:**

- Modularität: Jede Seite ist in einer eigenen View gekapselt
- Saubere URLs dank `createWebHistory()`
- Erweiterbar: Neue Seiten/Routen lassen sich leicht hinzufügen
