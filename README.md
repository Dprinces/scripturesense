# ScriptureSense Controller

**ScriptureSense Controller** is an offline, AI-powered automation tool designed for churches. It listens to the pastor's voice in real-time, detects scripture references (e.g., "John 3:16"), and automatically displays them in your presentation software (EasyWorship, ProPresenter, PowerPoint, etc.).

## 🚀 Key Features

*   **Offline AI**: Uses Vosk Speech Recognition (no internet required).
*   **Real-Time Detection**: Instantly identifies books, chapters, and verses.
*   **Virtual Keyboard Bridge**: Simulates keystrokes to control *any* presentation software.
*   **Safety First**: Confidence scoring and "Soft Confirm" delay to prevent mistakes.
*   **Platform Agnostic**: Works with EasyWorship, ProPresenter, PowerPoint, OpenLP, etc.

## 📦 Installation

### Windows (Recommended)
1.  Download the latest `ScriptureSenseController.exe` release.
2.  Run the executable. No installation required.

### From Source (Developers)
1.  Clone the repository.
2.  Install Python 3.10+.
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Download the Offline Model:
    ```bash
    python scripts/setup_vosk.py
    ```
5.  Run the application:
    ```bash
    python src/main.py
    ```

## 🛠 Usage

1.  **Launch the App**: Open `ScriptureSenseController.exe`.
2.  **Select Profile**: Choose your presentation software (e.g., EasyWorship) from the dropdown.
3.  **Start Listening**: Click the **START LISTENING** button.
4.  **Speak**: Say a scripture reference clearly (e.g., "Matthew chapter five verse nine").
5.  **Auto-Send**:
    *   If **Auto Mode** is ON: The app will count down (1.5s) and then trigger the verse.
    *   If **Auto Mode** is OFF: The verse will appear in the "Detected" box. Click **SEND NOW** to display it.

## ⚙️ Configuration

### Presentation Profiles
Profiles define how ScriptureSense talks to your software. They are located in `src/presentation/profiles/`.
*   **EasyWorship**: `Ctrl+B` (Search) → Type Reference → `Enter`
*   **ProPresenter**: `Cmd+F` (Search) → Type Reference → `Enter`

### Building the Executable
To package the app for distribution:
*   **Windows**: Run `build_windows.bat`
*   **macOS**: Run `./build_mac.sh`

## 📄 Documentation
*   [User Manual](docs/USER_MANUAL.md) - Detailed guide for media teams.
*   [Demo Script](docs/DEMO_SCRIPT.md) - How to demonstrate the system to leadership.

## 📜 License
Private & Confidential.
