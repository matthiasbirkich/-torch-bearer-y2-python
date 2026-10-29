@echo off
setlocal
cd /d "%~dp0"
title Torch Bearer Y2 - Python-Einrichtung
if not exist ".venv\Scripts\python.exe" (
  py -3.13 --version
  if errorlevel 1 (
    echo Python 3.13 wurde nicht gefunden.
    echo Bitte zuerst Python wie in docs\INSTALLATION_WINDOWS_DE.md beschrieben installieren.
    pause
    exit /b 1
  )
  py -3.13 -m venv .venv
  if errorlevel 1 goto fail
)
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto fail
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto fail
".venv\Scripts\python.exe" -m pip check
if errorlevel 1 goto fail
echo.
echo Fertig. Jetzt COM-Port in start.bat pruefen und start.bat starten.
pause
exit /b 0
:fail
echo.
echo Einrichtung fehlgeschlagen. Fehlermeldung oben pruefen.
pause
exit /b 1
