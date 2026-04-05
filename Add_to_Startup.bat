@echo off
set SCRIPT_PATH=%~dp0brightness_app.py
set VENV_PYTHON=%~dp0venv\Scripts\pythonw.exe
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set SHORTCUT_NAME=HP_Brightness_Sync.vbs

echo Creating startup shortcut...

:: Use a small VBScript to create the shortcut to the pythonw command
echo set WshShell = WScript.CreateObject("WScript.Shell") > "%TEMP%\shortcut.vbs"
echo set oShellLink = WshShell.CreateShortcut("%STARTUP_FOLDER%\HP_Brightness_Sync.lnk") >> "%TEMP%\shortcut.vbs"
echo oShellLink.TargetPath = "%VENV_PYTHON%" >> "%TEMP%\shortcut.vbs"
echo oShellLink.Arguments = "%SCRIPT_PATH%" >> "%TEMP%\shortcut.vbs"
echo oShellLink.WorkingDirectory = "%~dp0" >> "%TEMP%\shortcut.vbs"
echo oShellLink.WindowStyle = 1 >> "%TEMP%\shortcut.vbs"
echo oShellLink.Save >> "%TEMP%\shortcut.vbs"

cscript //nologo "%TEMP%\shortcut.vbs"
del "%TEMP%\shortcut.vbs"

echo.
echo Success! The app will now start automatically when you log in.
echo You can see it in your system tray (bottom right).
pause
