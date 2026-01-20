import logging
import keyboard
import time
import platform
import json
import os

# Platform specific imports
if platform.system() == "Windows":
    try:
        import win32gui
        import win32con
        import win32com.client
    except ImportError:
        logging.warning("pywin32 not found. Window focus will not work on Windows.")
elif platform.system() == "Darwin":
    try:
        import Quartz
        from AppKit import NSWorkspace
    except ImportError:
        logging.warning("pyobjc not found. Window focus might be limited on Mac.")

class PresentationController:
    def __init__(self, profile_name="EasyWorship"):
        self.system = platform.system()
        self.profile = self._load_profile(profile_name)
        
    def _load_profile(self, name):
        path = f"src/presentation/profiles/{name}.json"
        if not os.path.exists(path):
            logging.warning(f"Profile {name} not found. Using default.")
            return {
                "window_titles": [],
                "actions": {"search": [], "confirm": ["enter"]},
                "delays": {"post_focus": 0.1}
            }
        
        with open(path, 'r') as f:
            return json.load(f)

    def set_profile(self, profile_name):
        logging.info(f"Loading profile: {profile_name}")
        self.profile = self._load_profile(profile_name)

    def focus_window(self):
        """Attempts to bring the presentation app to foreground."""
        titles = self.profile.get("window_titles", [])
        if not titles:
            return False

        if self.system == "Windows":
            return self._focus_windows(titles)
        elif self.system == "Darwin": # macOS
            return self._focus_mac(titles)
        return False

    def _focus_windows(self, titles):
        try:
            import win32gui
            
            def callback(hwnd, found_windows):
                window_text = win32gui.GetWindowText(hwnd)
                for title in titles:
                    if title.lower() in window_text.lower():
                        found_windows.append(hwnd)
            
            hwnds = []
            win32gui.EnumWindows(callback, hwnds)
            
            if hwnds:
                # Bring to front
                hwnd = hwnds[0]
                # win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
                return True
        except Exception as e:
            logging.error(f"Windows Focus Error: {e}")
        return False

    def _focus_mac(self, titles):
        # On Mac, focusing via script is tricky without permissions.
        # This is a placeholder for Applescript or PyObjC implementation.
        # For now, we rely on the user keeping the window open/nearby or using standard Alt-Tab.
        logging.info(f"Please ensure {titles[0]} is focused.")
        return True

    def display_verse(self, book, chapter, verse):
        reference = f"{book} {chapter}:{verse}"
        logging.info(f"Presentation Trigger: Sending '{reference}'...")
        
        # 1. Focus App
        if not self.focus_window():
            logging.warning("Could not focus target window. Check if app is running.")
            # We proceed anyway as user might have focused it manually
        
        time.sleep(self.profile.get("delays", {}).get("post_focus", 0.2))
        
        # 2. Trigger Search
        search_keys = self.profile["actions"].get("search", [])
        if search_keys:
            try:
                keyboard.send(*search_keys)
                time.sleep(self.profile["delays"].get("post_search", 0.1))
            except Exception as e:
                logging.error(f"Error sending hotkeys: {e}")
            
        # 3. Type Reference
        try:
            keyboard.write(reference)
            time.sleep(self.profile["delays"].get("post_type", 0.2))
        except Exception as e:
            logging.error(f"Error typing text: {e}")
        
        # 4. Confirm/Enter
        confirm_keys = self.profile["actions"].get("confirm", ["enter"])
        for key in confirm_keys:
            try:
                keyboard.press_and_release(key)
            except Exception as e:
                logging.error(f"Error pressing confirm key: {e}")
            
        logging.info("Keystrokes sent.")
