# Dokumentation der Architektur

## Docker-Architektur

Die Anwendung wird lokal über **Docker Compose** ausgeführt und besteht aus drei zentralen Services:

- Backend (API)
- Datenbank
- Frontend

Durch die Containerisierung werden alle benötigten Komponenten in isolierten Umgebungen gestartet und automatisch miteinander verbunden.

---

## Backend Service

Der Backend-Service stellt die zentrale API der Anwendung bereit.
Er wird aus dem lokalen `backend` Verzeichnis gebaut und läuft in einem eigenen Container.

Das Backend übernimmt unter anderem:

- Verarbeitung von API-Anfragen
- Zugriff auf die Datenbank
- Integration der Sprachmodelle zur Bewertung von Antworten
- Bereitstellung der Daten für das Frontend

Der Service ist über folgenden Port erreichbar:

```
http://localhost:8000
```

Die API-Dokumentation wird automatisch von FastAPI generiert und ist unter folgender Adresse verfügbar:

```
http://localhost:8000/docs
```

Die Verbindung zur Datenbank erfolgt über die Umgebungsvariable `DATABASE_URL`.

---

## Datenbank Service

Für die Persistenz der Daten wird eine **PostgreSQL-Datenbank** verwendet.

Der Datenbankcontainer basiert auf dem offiziellen PostgreSQL-Image und wird mit folgenden Parametern initialisiert:

- Datenbankname: `echolearn`
- Benutzer: `echolearn`
- Passwort: `echolearn`

Die Daten werden in einem **Docker-Volume** gespeichert, sodass sie auch nach einem Neustart der Container erhalten bleiben.

```
Volume: db-data
```

Die Datenbank ist lokal über Port `5432` erreichbar.

---

## Frontend Service

Das Frontend basiert auf **Vue 3** und wird innerhalb eines Node.js-Containers ausgeführt.

Beim Start des Containers werden automatisch:

1. die benötigten npm-Abhängigkeiten installiert
2. die Entwicklungsumgebung gestartet

Der Dev-Server wird anschließend auf Port `5173` bereitgestellt.

```
http://localhost:5173
```

Das Frontend kommuniziert mit der Backend-API, um:

- Prüfungsfragen abzurufen
- Antworten zu übermitteln
- Bewertungen und Rückfragen zu erhalten
- Lernstatistiken darzustellen

---

## Service-Abhängigkeiten

Die Services werden in einer definierten Reihenfolge gestartet:

1. Datenbank (`db`)
2. Backend (`backend`)
3. Frontend (`frontend`)

Das Backend benötigt eine aktive Datenbankverbindung, während das Frontend auf das Backend zugreift.

Docker Compose stellt sicher, dass diese Abhängigkeiten berücksichtigt werden.

---

## Persistente Daten

Die Datenbank speichert ihre Daten in einem benannten Docker-Volume:

```
db-data
```

Dieses Volume sorgt dafür, dass Daten auch dann erhalten bleiben, wenn die Container neu gestartet oder neu gebaut werden.

---

## Lokales Entwicklungssetup

Die gesamte Anwendung kann lokal mit Docker Compose gestartet werden.
Alle Services sind anschließend über die jeweiligen Ports erreichbar und bilden gemeinsam die vollständige Entwicklungsumgebung.
