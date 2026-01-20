# ScriptureSense Controller - User Manual

## Introduction
ScriptureSense Controller acts as a "smart assistant" for your media team. Instead of manually typing scripture references, it listens to the audio feed and types them for you.

## System Requirements
*   **OS**: Windows 10/11 or macOS 12+
*   **Microphone**: A clean audio feed from the pulpit (USB interface recommended) or a laptop microphone for testing.
*   **Presentation Software**: EasyWorship, ProPresenter, PowerPoint, or similar.

## Interface Overview

### 1. Live Speech Panel
*   Shows a running transcript of what the AI hears.
*   **Tip**: Use this to verify that the microphone is picking up clear audio.

### 2. Detected Scripture Panel
*   Displays the most recently identified verse (e.g., "John 3:16").
*   **Confidence**: A percentage score indicating how sure the AI is.
    *   The system ignores detections below 85% confidence to avoid errors.

### 3. Controls
*   **START / STOP LISTENING**: Toggles the AI engine.
*   **AUTO MODE**:
    *   **Checked**: Detected verses are sent automatically after a 1.5-second safety delay.
    *   **Unchecked**: Verses wait in the "Detected" box until you click **SEND NOW**.
*   **SEND NOW**: Manually triggers the displayed verse.
*   **CANCEL**: Appears during the auto-send countdown. Click to stop a verse from going live.

## Integration Setup

### EasyWorship
1.  Ensure EasyWorship is running.
2.  Verify that `Ctrl+B` opens the Scripture Search tab (this is the default).
3.  In ScriptureSense, select **EasyWorship** from the dropdown.

### ProPresenter
1.  Ensure ProPresenter is running.
2.  Verify that `Cmd+F` (Mac) or `Ctrl+F` (Windows) opens the Library Search.
3.  In ScriptureSense, select **ProPresenter** from the dropdown.

## Troubleshooting

### "It's not hearing anything"
*   Check your default microphone in Windows Settings > Sound.
*   Restart ScriptureSense.

### "It detects the wrong verse"
*   The AI relies on clear pronunciation. Background noise or mumbling can affect accuracy.
*   Switch **Auto Mode** OFF to manually approve verses before they go live.

### "It types into the wrong window"
*   ScriptureSense tries to bring your presentation app to the front.
*   If it fails, manually click on your presentation app window to ensure it has focus.
