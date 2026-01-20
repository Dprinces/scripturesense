#!/bin/bash
echo "Building ScriptureSense Controller for macOS..."

# Ensure PyInstaller is installed
pip3 install pyinstaller

# Clean previous builds
rm -rf build dist *.spec

# Run PyInstaller
# Note: macOS uses colon (:) for --add-data separators
pyinstaller --name "ScriptureSenseController" \
--onefile \
--windowed \
--add-data "src/presentation/profiles:src/presentation/profiles" \
--add-data "data/bible.db:data" \
--add-data "data/models:data/models" \
--hidden-import "pyaudio" \
--hidden-import "vosk" \
--hidden-import "keyboard" \
--hidden-import "sqlite3" \
src/main.py

echo ""
echo "Build complete! Check the 'dist' folder for ScriptureSenseController.app"
