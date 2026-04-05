@echo off
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set LNK_FILE=%STARTUP_FOLDER%\HP_Brightness_Sync.lnk

if exist "%LNK_FILE%" (
    del "%LNK_FILE%"
    echo Removed from startup.
) else (
    echo Startup shortcut not found.
)
pause
