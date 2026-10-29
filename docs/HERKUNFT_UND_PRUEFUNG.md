## Inhalt des Pythonpaketes zur Auswertung der Spektraldaten vom Y2 von Torch Bearer

- main_export.py (USB-Erfassung, Export, Farbgrafik)
- protocol.py (ursprüngliches serielles Protokoll von ZoidTechnology)
- spectral_metrics.py (Lux, Photonenintegrale, CRI usw.)
- photobiology_metrics.py (Bänder und Verhältnisse)
- requirements.txt (bisherige Paketvorgaben)

Der Paketinstaller kann die `.venv` bei Bedarf selbst anlegen und verwendet
`requirements.txt`. 
Die Startvorgabe bleibt COM5.

## Bereits im kombinierten Projekt geprüfte Eigenschaften

Die unveränderten vier Module bestanden die dort dokumentierten Tests mit
simulierter USB-Kommunikation, fragmentierten Antworten, 661 Spektralwerten,
CSV/JSON/PNG-Export und Kennwertberechnung. Die Darstellung wurde mit realem
Spektrum und Null-/negativen Werten geprüft. Eine Prüfung derselben Daten
bestätigt Rechenkonsistenz, nicht die absolute Kalibration des Messgeräts.

## Prüfung dieser eigenständigen Zusammenstellung

Drei automatisierte Tests bestanden am 29.10.2026 unter Linux mit Python 3.12:
STOP-Nachricht, vollständige und fragmentierte simulierte Messung, Grafikfarben
und Achsenteilung. Verwendet wurden die Paketanforderungen dieses Projekts.
Die dokumentierte Python-3.13-Installation unter Windows wurde hier nicht ausgeführt.


- Python-Syntax und bytegleiche Übernahme der vier Python-Module.
- Lokale Dokumentationslinks und Vollständigkeit der Paketstruktur.
- Protokoll-/Kommunikationstests gemäß beigefügtem Test.
- Grafikfunktion der mitgelieferten main_export.py.

Tests nach Installation der Anforderungen:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
