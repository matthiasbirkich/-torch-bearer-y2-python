# Torch Bearer Y2 - Python am Windows-PC

Eigenständige USB-Erfassung und Auswertung für das **Torch Bearer Y2**.
Dieses Projekt benötigt **Python313**

Grundlage ist das serielle Protokoll aus
[ZoidTechnology/Torch-Bearer-Tools](https://github.com/ZoidTechnology/Torch-Bearer-Tools).
Die hier zusammengestellte PC-Variante verwendet `main_export.py` **1.2.2**
und die dazugehörigen Kennwertmodule. Projektpaket: **1.0.0**, Stand 29.10.2026.

## Neuinstallation unter Windows 11

1. Das Projekt vollständig herunterladen und in einen eigenen beschreibbaren
   Benutzerordner entpacken, z. B. `Dokumente\TorchBearer_Y2`.
2. Den offiziellen [Python Install Manager](https://www.python.org/downloads/windows/)
   installieren. Im neuen PowerShell-Fenster ausführen:

   ```powershell
   py install 3.13
   py -3.13 --version
   ```

3. `install_dependencies.bat` doppelklicken. Sie erstellt bei Bedarf `.venv`
   im Projektordner und installiert die Pakete aus `requirements.txt`.
4. Y2 per USB-Datenkabel anschließen. Die COM-Nummer im Geräte-Manager prüfen.
5. `start.bat` im Editor öffnen und `set "TB_PORT=COM5"` anpassen, falls nötig.
6. `start.bat` doppelklicken und auf die erste **NORMAL**-Messung warten.

Die vollständige [Windows-Anleitung](docs/INSTALLATION_WINDOWS_DE.md) erklärt
Benutzerrechte, Prüfungen und Fehlerbehebung. Für Python-Benutzerinstallation,
Pakete in `.venv` und den normalen Betrieb sind üblicherweise keine
Administratorrechte erforderlich.

## Welche Funtionen sind enthalten?

Die Grafikfunktionen von **main_export.py 1.2.2** ist vollständig enthalten:

- schematische Spektralfarben **unter der Messkurve**;
- dunkles Violett für UV und zum rechten Rand dunkler werdendes Rot für NIR;
- deutsche Achsentitel und Hinweis, dass UV und IR unsichtbar sind;
- beschriftete 100-nm-Hauptmarken, Teilstriche alle 10 nm, Hilfslinien alle 50 nm;
- Ausgabe der Grafik als `spectrum.png` und Anzeige eines Grafikfensters.

Messwerte werden für die Grafik nicht normiert. Die Farben und Achsenteilung
ändern weder die Messwerte noch die optische Auflösung. Die vier Python-Module
wurden unverändert aus dem geprüften PC-Stand übernommen.

## Kennwerte und Export

Das Gerät wird direkt über USB Serial ausgelesen. Eine Aufnahme erzeugt einen
neuen Unterordner unter `Messungen` mit:

- `spectrum.csv` und `spectrum.png`;
- `metrics.txt`, `metrics.csv`, `metrics.json`;
- `bands.csv`, `ratios.csv`, `cri_samples.csv`;
- `measurement.json`, Messblöcken und protokollierter Rohkommunikation.

Die Auswertung umfasst unter anderem Lux, PPFD 400-700 nm, energetisches PAR,
ePAR 400-750 nm, xPAR nach dokumentierter Definition, CRI Ra und R1-R14,
CCT/Duv sowie Bandintegrale und -verhältnisse. Absolute Werte setzen
spektrale Bestrahlungsstärke in **W/m²/nm** voraus.

## Nachberechnung vorhandener PC-CSV

Eine von diesem Programm erzeugte `spectrum.csv` auf `auswertung.bat` ziehen.
Die Kennwerte werden im CSV-Ordner neu geschrieben. **Dabei wird weiterhin
keine neue Grafik erzeugt und measurement.json nicht aktualisiert.**


## Datenweg
**Y2 → USB Serial → Python-Protokoll → Kennwertberechnung und Grafik → CSV/PNG/JSON.**
`pip` installiert die Python-Pakete;
Die Windows-Batchdateien sind Start- und Einrichtungshilfen

## Nachvollziehbarkeit und Sicherheit

Der Anwendungscode liegt als Python-Quelltext vor. Bibliotheken wie NumPy,
SciPy und Matplotlib enthalten allerdings auch kompilierte Bestandteile.
Eine `.venv` trennt Paketstände, ist keine Sicherheits-Sandbox. Dieses Projekt
ist funktionell geprüft, aber nicht als vollständiges Sicherheitsaudit zertifiziert.

[Herkunft, Versionen und Prüfstand](docs/HERKUNFT_UND_PRUEFUNG.md)

## Lizenz

Programmcode: **GPL-3.0-or-later**, siehe [LICENSE](LICENSE).
Urheberrechte der ursprünglichen Autoren bleiben erhalten. Kein offizielles
Produkt von Torch Bearer oder ZoidTechnology. Die offizielle Hersteller-App
wird nicht mitgeliefert. Erweiterungen und Dokumentation: Matthias Birkicht,
mit Unterstützung von ChatGPT/Codex.
