# TavaCraft - Modpack Updater

Dieses Python-Projekt ist ein Modpack-Updater für das Spiel Minecraft. Mit dem Updater können Sie einfach die neueste Version des Modpacks von der TavaCraft-Website herunterladen. 

## Eigenschaften

- Graphische Benutzeroberfläche, die mit Tkinter erstellt wurde.
- Verwendet `requests` und `BeautifulSoup` für das Web-Scraping, um den Download-Link zum neuesten Modpack zu ermitteln.
- Verwendet `requests` zum Herunterladen der Datei.
- Verwendet Threading, um die Benutzeroberfläche reaktionsfähig zu halten, während der Download im Hintergrund stattfindet.
- Zeigt einen Fortschrittsbalken an, der den Fortschritt des Downloads verfolgt.

## Benutzung

Anleitung zur Benutzung des TavaCraft Modpack-Updaters

    Vorbereitung:
        Stellen Sie sicher, dass Minecraft auf Ihrem Computer installiert ist.
        Vergewissern Sie sich, dass Sie über eine aktive Internetverbindung verfügen.

    Starten des Updaters:
        Navigieren Sie zu dem Verzeichnis, in dem sich der Updater befindet.
        Doppelklicken Sie auf die Datei main.py oder führen Sie sie von der Kommandozeile mit python main.py aus.

    Hauptfenster:
        Nach dem Start des Updaters sollte das Hauptfenster des TavaCraft-Updaters angezeigt werden.
        In der Mitte des Fensters sehen Sie einen grünen Button mit der Beschriftung "Update Modpack".

    Update-Prozess:
        Klicken Sie auf die Schaltfläche "Update Modpack".
        Der Updater sucht nun automatisch nach der neuesten Version des Modpacks.
        Wenn bereits die neueste Version installiert ist, wird eine Benachrichtigung angezeigt. Andernfalls beginnt der Download.
        Ein Fortschrittsbalken am unteren Rand des Fensters zeigt den aktuellen Downloadfortschritt an.

    Nach dem Download:
        Ist der Download abgeschlossen, wird das Modpack automatisch im .minecraft/mods-Ordner installiert.
        Eine Bestätigungsnachricht wird angezeigt, um Sie über den erfolgreichen Abschluss des Updates zu informieren.

    Forge Update (Optional):
        Falls Sie auch Forge aktualisieren möchten, klicken Sie auf den Button "Get Forge" unten links im Fenster. Befolgen Sie die Anweisungen, um die neueste Forge-Version zu installieren.

    Schließen des Updaters:
        Schließen Sie das Hauptfenster des Updaters, indem Sie auf das "X"-Symbol in der oberen rechten Ecke klicken oder das Nachrichtenfenster bestätigen.

    Spielen:
        Starten Sie Minecraft und genießen Sie das aktualisierte TavaCraft-Modpack!

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
