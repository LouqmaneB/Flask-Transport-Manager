
---

# Transport Management System

## Inhaltsverzeichnis

1. [Projektbeschreibung](#1-projektbeschreibung)
2. [Ziel des Projekts](#2-ziel-des-projekts)
3. [Anwendungsbereich](#3-anwendungsbereich)
4. [Technische Grundlagen](#4-technische-grundlagen)
5. [Systemarchitektur](#5-systemarchitektur)
6. [Installation und Inbetriebnahme](#6-installation-und-inbetriebnahme)
7. [Verwendung der Anwendung](#7-verwendung-der-anwendung)
8. [Projektstruktur](#8-projektstruktur)
9. [Funktionaler Umfang](#9-funktionaler-umfang)
10. [Bekannte Einschränkungen](#10-bekannte-einschränkungen)

## 1. Projektbeschreibung

Dieses Projekt ist eine webbasierte Transport-Management-Anwendung auf Basis von Flask.  
Sie ermöglicht die Verwaltung von Transportdaten und deren Darstellung in einer interaktiven Kartenansicht.

## 2. Ziel des Projekts

- Ziel dieses Projekts ist die Erstellung eines modularen Grundsystems, das als Ausgangspunkt für ein umfassendes [Bus-Management-System](#) ( Noch in Entwicklung ) fungiert.
- Der Fokus liegt auf der Implementierung zentraler Basisfunktionen, die in späteren Entwicklungsphasen erweitert werden können.

## 3. Projektabgrenzung

- Dieses Projekt bildet ein Grundsystem und ist bewusst auf zentrale Funktionen beschränkt.
- Erweiterte Funktionen wie Benutzerverwaltung oder Echtzeit-Tracking sind nicht Bestandteil der aktuellen Version.

## 4. Technische Grundlagen

<p align="center"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python" width="45" height="45"/> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/flask/flask-original.svg" alt="Flask" width="45" height="45"/> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mongodb/mongodb-original.svg" alt="MongoDB" width="45" height="45"/> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original.svg" alt="HTML5" width="45" height="45"/> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original.svg" alt="CSS3" width="45" height="45"/> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="JavaScript" width="45" height="45"/> <img src="https://cdn.freebiesupply.com/logos/thumbs/2x/leaflet-1-logo.png" alt="Leaflet" width="90"/> </p>

- Python
- Flask (ein Web-Framework für Python)
- MongoDB
- HTML5 & CSS3
- JavaScript (Clientseitige Logik)
- Leaflet.js (Karten- und Routenvisualisierung)

## 5. Systemarchitektur
<p align="center">
  <img src="static\images\Systemarchitektur.png" alt="Systemarchitektur">
</p>
## 6. Installation und Inbetriebnahme

Zur lokalen Inbetriebnahme der Anwendung sind folgende Schritte erforderlich:

1. Klonen des Repositories:

   ```bash
   git clone https://github.com/LouqmaneB/Flask-Transport-Manager.git
   ```

2. Wechsel in das Projektverzeichnis:

   ```bash
   cd Flask-Transport-Manager
   ```

3. Erstellen und Aktivieren einer virtuellen Python-Umgebung:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate      # Windows
   ```

4. Installation der benötigten Abhängigkeiten:

   ```bash
   pip install -r requirements.txt
   ```

5. Starten der MongoDB-Datenbank.

6. Start der Anwendung:

   ```bash
   flask run
   ```

7. Zugriff auf die Anwendung über:
   `http://127.0.0.1:5000`

## 7. Verwendung der Anwendung

Nach dem Start der Anwendung erhält der Benutzer Zugriff auf die Hauptoberfläche.  
Die Anwendung bietet zwei Hauptseiten (Routen):  
- `/` – Anzeige und Verwaltung der Transportlinien und Routen auf der interaktiven Karte  
- `/stops` – Verwaltung von Haltestellen: hinzufügen, bearbeiten oder entfernen


## 8. Projektstruktur

Die grundlegende Projektstruktur ist wie folgt aufgebaut:

```
transport-management-system/
│
├── app.py                 # Einstiegspunkt der Anwendung
├── requirements.txt       # Projektabhängigkeiten
│
├── templates/             # HTML-Templates
│   ├── index.html
│   └── routes.html
│
├── static/
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript-Dateien
│   └── images/            # Statische Ressourcen
│
├── models/                # Datenbankmodelle
├── routes/                # Flask-Routen und Controller
└── README.md              # Projektdokumentation
```

## 9. Funktionaler Umfang

Die Anwendung bietet unter anderem folgende Funktionen, die eine intuitive Verwaltung von Transportdaten ermöglichen:

- **Kartenbasierte Darstellung** der Transportwege, um Routen und Haltestellen auf einen Blick zu erfassen
- **Erstellung, Bearbeitung und Löschung von Routen**, direkt über die interaktive Karte
- **Interaktive Marker** mit Drag-and-Drop-Funktion zur einfachen Anpassung von Haltepunkten
- **Persistente Speicherung** aller Daten in MongoDB, sodass Änderungen jederzeit erhalten bleiben
- **Responsives Layout**, das die Anwendung auf verschiedenen Geräten nutzbar macht

## 10. Bekannte Einschränkungen

Der aktuelle Stand der Anwendung weist noch folgende Einschränkungen auf:

- **Benutzer-Authentifizierung**: nicht implementiert
- **Echtzeit-Tracking**: nicht verfügbar

