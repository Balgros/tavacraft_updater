# TavaCraft - Modpack Updater

Dieses Python-Projekt ist ein Modpack-Updater für das Spiel Minecraft. Mit dem Updater können Sie einfach die neueste Version des Modpacks von der TavaCraft-Website herunterladen. 

## Eigenschaften

- Graphische Benutzeroberfläche, die mit Tkinter erstellt wurde.
- Verwendet `requests` und `BeautifulSoup` für das Web-Scraping, um den Download-Link zum neuesten Modpack zu ermitteln.
- Verwendet `requests` zum Herunterladen der Datei.
- Verwendet Threading, um die Benutzeroberfläche reaktionsfähig zu halten, während der Download im Hintergrund stattfindet.
- Zeigt einen Fortschrittsbalken an, der den Fortschritt des Downloads verfolgt.

## Benutzung

Starten Sie die Anwendung und klicken Sie auf die Schaltfläche "Update". Sie werden dann aufgefordert, einen Speicherpfad auszuwählen. Wählen Sie das gewünschte Verzeichnis aus und klicken Sie auf "OK". Der Download des Modpacks beginnt dann und Sie können den Fortschritt im Fortschrittsbalken verfolgen. Nach Abschluss des Downloads wird das Modpack im ausgewählten Verzeichnis gespeichert.

## Anforderungen

- Python 3.7+
- `requests`
- `beautifulsoup4`
- `tkinter`

## Installation

Stellen Sie sicher, dass Sie Python 3.7 oder höher installiert haben. Installieren Sie dann die notwendigen Pakete mit dem folgenden Befehl:

```shell
pip install requests beautifulsoup4
```

Führen Sie das Skript aus:

```shell
python main.py
```

## Lizenz

Dieses Projekt ist unter der GNU General Public License v3.0 lizenziert. Weitere Einzelheiten finden Sie in der Datei LICENSE.

## Mitwirken

Pull-Anfragen sind willkommen. Bei größeren Änderungen bitte zuerst ein Issue eröffnen, um zu diskutieren, was Sie ändern möchten.

## Support

Wenn Sie Unterstützung benötigen oder Fragen haben, eröffnen Sie bitte ein Issue.
