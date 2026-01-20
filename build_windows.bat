@echo off
echo Building ScriptureSense Controller for Windows...

:: Ensure PyInstaller is installed
pip install pyinstaller

:: Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

:: Run PyInstaller
:: Note: Windows uses semicolon (;) for --add-data separators
pyinstaller --name "ScriptureSenseController" ^
--onefile ^
--windowed ^
--icon=NONE ^
--add-data "src/presentation/profiles;src/presentation/profiles" ^
--add-data "data/bible.db;data" ^
--add-data "data/models;data/models" ^
--hidden-import "pyaudio" ^
--hidden-import "vosk" ^
--hidden-import "keyboard" ^
--hidden-import "sqlite3" ^
src/main.py

echo.
echo Build complete! Check the 'dist' folder for ScriptureSenseController.exe
pause
