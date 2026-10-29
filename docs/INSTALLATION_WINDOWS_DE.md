# Windows 11: Python-Installation für das Y2

Stand 29.10.2026. Für einen neuen üblichen Intel-/AMD-Windows-11-PC ohne Python.

## 1. Rechte und Voraussetzungen

Benötigt wird das USB-Datenkabel von TorchBearer, Internet während der Einrichtung von Python sowie ein
beschreibbarer Ordner im eigenen Benutzerkonto. Python und Projektumgebung
können normalerweise ohne Administratorrechte für den eigenen Benutzer
installiert werden.

PowerShell und Batchdateien normal öffnen.

## 2. Python installieren

Den offiziellen Python Install Manager von
<https://www.python.org/downloads/windows/> oder aus dem Microsoft Store
(Herausgeber Python Software Foundation) installieren.

Ein neues PowerShell-Fenster öffnen:

```powershell
py install 3.13
py -3.13 --version
```

Erwartet wird `Python 3.13.x`. Keinen experimentellen free-threaded oder
embeddable Build auswählen. Der Manager ist nur die Python-Installationshilfe.

Falls `py` nicht gefunden wird, das Terminal neu öffnen und die
App-Ausführungsaliase des Managers prüfen. Bei einem Namenskonflikt kann
`pymanager install 3.13` den Manager ausdrücklich aufrufen.

## 3. Projekt einrichten

Das Projekt-ZIP vollständig in einen eigenen Ordner entpacken. Die Python-
und Batchdateien liegen **direkt im Projektordner**, ohne zusätzlichen
`interface`-Unterordner. Keine alte `.venv` von einem anderen PC hineinkopieren.

`install_dependencies.bat` doppelklicken. Sie legt `.venv` an und installiert
die Anforderungen. Alternativ im Projektordner (Explorer: Alt+D, powershell,
Enter) die folgenden Befehle einzeln ausführen:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

Eine Aktivierung mit Activate.ps1 und eine Änderung der Execution Policy sind
nicht nötig. Das Paket heißt `colour-science` mit „u“, der Import heißt `colour`.

## 4. Ohne Gerät prüfen

```powershell
.\.venv\Scripts\python.exe -c "import colour, scipy, matplotlib, serial"
.\.venv\Scripts\python.exe -m tkinter
```

Der erste Befehl soll ohne Fehler enden; der zweite öffnet ein Tk-Testfenster.
Dieses wieder schließen. Tcl/Tk ist Teil der vollständigen Python-Laufzeit,
kein zusätzliches mit pip zu installierendes Paket.

## 5. Anschließen und messen

Y2 per USB anschließen. Im Geräte-Manager unter „Anschlüsse (COM & LPT)“ die
COM-Nummer ermitteln.

Andere Messprogramme schließen. In `start.bat` die Zeile
`set "TB_PORT=COM5"` gegebenenfalls ändern, dann die Datei doppelklicken.
Alternativer Direktstart für COM5:

```powershell
.\.venv\Scripts\python.exe main_export.py COM5 --show
```

Auf NORMAL-Messung, neuen Ordner unter `Messungen` und Grafikfenster warten.
Eine JSON-Datei allein belegt noch keine erfolgreiche Erfassung; Fehlermeldungen
in der Konsole prüfen. Für eine weitere Messung das Grafikfenster schließen
und erneut starten.

## 6. Nachberechnung und Tageslichtintegral

Eine PC-`spectrum.csv` auf `auswertung.bat` ziehen. Keine neue Grafik bei dieser
Nachberechnung. Android-Originalexporte werden noch nicht automatisch erkannt.
Für eine DLI-Schätzung `TB_PHOTOPERIOD_HOURS` in der jeweiligen Batchdatei auf
z. B. `16` setzen. Das setzt konstantes Licht über 16 Stunden voraus und ist
keine Messung einer tatsächlichen Tageszeitreihe.

## 7. Fehlerbehebung

- Fehlendes Modul: Pakete mit genau dem `.venv`-Interpreter erneut installieren.
- Falscher Port / Access denied: COM-Nummer und andere geöffnete Programme prüfen.
- Datei nicht gefunden: Im Projektordner arbeiten, Dateiendungen kontrollieren.
- Tcl/Tk-Fehler: Tk-Test prüfen, vollständige Python-Laufzeit reparieren.
- Proxy-/Zertifikatsfehler: IT fragen, Zertifikatsprüfung nicht abschalten.
- COM-Nummer nach USB-Wechsel geändert: Nur `start.bat` anpassen.

## Quellen

- Python unter Windows: <https://docs.python.org/3/using/windows.html>
- Virtuelle Umgebung und Aufruf ohne Aktivierung: <https://docs.python.org/3.13/library/venv.html>
- Ursprung des Protokolls: <https://github.com/ZoidTechnology/Torch-Bearer-Tools>
