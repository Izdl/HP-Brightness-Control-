@echo off
echo Starting HP Brightness Sync in background...
cd /d "%~dp0"
start "" ".\venv\Scripts\pythonw.exe" brightness_app.py
echo.
echo The app is now running in your system tray (bottom right icons).
timeout /t 3
