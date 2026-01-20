# Licensing & White-Label Guide

**ScriptureSense** is designed not just as a standalone tool, but as a platform that can be adapted, rebranded, and deployed by partners. This guide outlines the technical and commercial possibilities for licensing.

## 🏢 Why White-Label?

Church networks, software resellers, and large ministries often want to provide technology under their own trusted brand. ScriptureSense supports this through a modular architecture that allows for easy "reskinning" and configuration.

### Supported Customizations

| Component | Customization Options | Difficulty |
| :--- | :--- | :--- |
| **Product Name** | Rename app (e.g., "VictoryConnect Controller") | Easy (Config) |
| **Logo/Icon** | Replace `assets/logo.svg` and `.ico` | Easy (Asset Swap) |
| **UI Colors** | Change primary accent colors in `src/ui/app.py` | Easy (Code Edit) |
| **Profiles** | Pre-load specific settings for your denomination | Medium (JSON) |
| **Installer** | Branded MSI/EXE installer with EULA | Medium (Build) |

## 💼 Licensing Models

### 1. The "Reseller" License
*   **Target**: AV Integrators, Church Software Shops.
*   **Model**: You sell "ScriptureSense" as an add-on to your installation services.
*   **Rights**: Distribution rights, Priority Support.
*   **Tech**: Standard Binary.

### 2. The "Network" License (White-Label)
*   **Target**: Denominations (e.g., "Assembly of God Tech Suite").
*   **Model**: You distribute a branded version to 500+ member churches.
*   **Rights**: Rebranding, Custom Default Configs.
*   **Tech**: Custom Build.

### 3. The "Source" License (Enterprise)
*   **Target**: Major Church Tech Companies (e.g., Planning Center, Logos).
*   **Model**: Full acquisition of source code to integrate into existing platforms.
*   **Rights**: Full IP usage, Modification rights.
*   **Tech**: Git Repository Access.

## 🛠 Technical Rebranding Steps

To create a white-label build:

1.  **Replace Assets**:
    *   Overwrite `assets/logo.svg` with your vector logo.
    *   Create a valid `.ico` file for Windows.

2.  **Update Branding Config**:
    *   In `src/ui/app.py`, change the window title and header text.
    *   Update `ABOUT` dialog text.

3.  **Rebuild**:
    *   Run `build_windows.bat` with the `--icon=assets/your_icon.ico` flag.

## 📞 Contact

For licensing inquiries, please contact the developer directly.
*   **Email**: [Insert Email]
*   **Version**: 1.0.0 (Enterprise Ready)
