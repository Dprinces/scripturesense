import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import logging
import os
import time
from .state import AppState

class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.configure(state='disabled')
            self.text_widget.yview(tk.END)
        self.text_widget.after(0, append)

class ScriptureSenseUI:
    def __init__(self, root, start_callback, stop_callback, profile_callback, test_profile_callback):
        self.root = root
        self.root.title("ScriptureSense Controller")
        self.root.geometry("500x800")
        
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.profile_callback = profile_callback
        self.test_profile_callback = test_profile_callback
        
        self.is_running = False
        self.auto_mode = tk.BooleanVar(value=True)
        self.delay_timer = None
        self.countdown_active = False

        self._setup_ui()
        self.set_state(AppState.IDLE)

    def _setup_ui(self):
        # Styles
        style = ttk.Style()
        style.configure("Big.TLabel", font=("Helvetica", 18, "bold"))
        style.configure("Status.TLabel", font=("Helvetica", 12, "bold"))
        style.configure("Verse.TLabel", font=("Helvetica", 14))

        # 1. Header & Status
        header_frame = ttk.Frame(self.root, padding="15")
        header_frame.pack(fill=tk.X)
        
        ttk.Label(header_frame, text="ScriptureSense Controller", font=("Helvetica", 16, "bold")).pack(side=tk.LEFT)
        self.lbl_status = ttk.Label(header_frame, text="IDLE", style="Status.TLabel", foreground="gray")
        self.lbl_status.pack(side=tk.RIGHT)

        # 2. Live Speech Transcript
        transcript_frame = ttk.LabelFrame(self.root, text="🎙 Live Speech", padding="10")
        transcript_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.lbl_transcript = ttk.Label(transcript_frame, text="Waiting for speech...", font=("Courier", 12), wraplength=450, foreground="#555")
        self.lbl_transcript.pack(fill=tk.X)

        # 3. Detected Scripture
        detected_frame = ttk.LabelFrame(self.root, text="📖 Detected Scripture", padding="15")
        detected_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.lbl_reference = ttk.Label(detected_frame, text="---", style="Big.TLabel", foreground="#007AFF")
        self.lbl_reference.pack()
        
        self.lbl_confidence = ttk.Label(detected_frame, text="Confidence: -", font=("Helvetica", 9), foreground="gray")
        self.lbl_confidence.pack(pady=(2, 10))
        
        self.lbl_verse_text = ttk.Label(detected_frame, text="...", style="Verse.TLabel", wraplength=450, justify="center")
        self.lbl_verse_text.pack()
        
        # Soft Confirm Countdown Label
        self.lbl_countdown = ttk.Label(detected_frame, text="", font=("Helvetica", 10, "bold"), foreground="orange")
        self.lbl_countdown.pack(pady=5)

        # 4. Action Controls
        action_frame = ttk.Frame(self.root, padding="10")
        action_frame.pack(fill=tk.X, padx=10)
        
        # Auto Mode Toggle
        self.chk_auto = ttk.Checkbutton(action_frame, text="AUTO MODE", variable=self.auto_mode, command=self.on_auto_toggle)
        self.chk_auto.pack(side=tk.LEFT, padx=5)
        
        # Manual Send Button
        self.btn_send = ttk.Button(action_frame, text="SEND NOW", command=self.manual_send, state="disabled")
        self.btn_send.pack(side=tk.RIGHT, padx=5)
        
        # Cancel Button (Hidden by default)
        self.btn_cancel = ttk.Button(action_frame, text="CANCEL", command=self.cancel_auto_send, state="disabled")
        self.btn_cancel.pack(side=tk.RIGHT, padx=5)

        # Main Toggle (Start/Stop)
        self.btn_toggle = ttk.Button(self.root, text="START LISTENING", command=self.toggle_listening)
        self.btn_toggle.pack(fill=tk.X, padx=20, pady=10)

        # 5. Settings
        settings_frame = ttk.LabelFrame(self.root, text="⚙ Settings", padding="10")
        settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(settings_frame, text="Target App:").pack(side=tk.LEFT)
        
        profiles = [f.replace(".json", "") for f in os.listdir("src/presentation/profiles") if f.endswith(".json")]
        if not profiles: profiles = ["EasyWorship"]
        
        self.combo_profile = ttk.Combobox(settings_frame, values=profiles, state="readonly", width=15)
        if "EasyWorship" in profiles:
            self.combo_profile.set("EasyWorship")
        else:
            self.combo_profile.current(0)
            
        self.combo_profile.pack(side=tk.LEFT, padx=10)
        self.combo_profile.bind("<<ComboboxSelected>>", self.on_profile_change)
        
        # Test Profile Button
        self.btn_test_profile = ttk.Button(settings_frame, text="TEST SEND", command=self.on_test_profile)
        self.btn_test_profile.pack(side=tk.RIGHT)

        # 6. Logs
        log_frame = ttk.LabelFrame(self.root, text="System Logs", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.txt_log = scrolledtext.ScrolledText(log_frame, height=8, state='disabled', font=("Courier", 9))
        self.txt_log.pack(fill=tk.BOTH, expand=True)

        # Hook up logging
        text_handler = TextHandler(self.txt_log)
        logging.getLogger().addHandler(text_handler)

    def set_state(self, state):
        self.current_state = state
        self.lbl_status.config(text=state.value)
        
        if state == AppState.IDLE:
            self.lbl_status.config(foreground="gray")
        elif state == AppState.LISTENING:
            self.lbl_status.config(foreground="green")
        elif state == AppState.DETECTED:
            self.lbl_status.config(foreground="blue")
        elif state == AppState.SENDING:
            self.lbl_status.config(foreground="orange")
        elif state == AppState.ERROR:
            self.lbl_status.config(foreground="red")

    def toggle_listening(self):
        if self.is_running:
            self.stop_callback()
            self.is_running = False
            self.set_state(AppState.IDLE)
            self.btn_toggle.config(text="START LISTENING")
        else:
            threading.Thread(target=self.start_callback, daemon=True).start()
            self.is_running = True
            self.set_state(AppState.LISTENING)
            self.btn_toggle.config(text="STOP LISTENING")

    def on_auto_toggle(self):
        mode = "ON" if self.auto_mode.get() else "OFF"
        logging.info(f"Auto Mode: {mode}")

    def on_profile_change(self, event):
        profile = self.combo_profile.get()
        self.profile_callback(profile)
        logging.info(f"Switched profile to: {profile}")

    def on_test_profile(self):
        self.test_profile_callback()

    def update_transcript(self, text):
        self.lbl_transcript.config(text=f'"{text}"')

    def update_detected(self, reference, text, confidence, send_callback=None):
        self.lbl_reference.config(text=reference)
        self.lbl_verse_text.config(text=text)
        self.lbl_confidence.config(text=f"Confidence: {int(confidence * 100)}%")
        
        self.set_state(AppState.DETECTED)
        self.last_detected = (reference, text)
        self.send_callback = send_callback
        
        self.btn_send.config(state="normal")
        
        # Soft Confirm Logic
        if self.auto_mode.get():
            self.start_auto_send_countdown()

    def start_auto_send_countdown(self):
        if self.countdown_active:
            # Reset existing timer
            if self.delay_timer: self.root.after_cancel(self.delay_timer)
        
        self.countdown_active = True
        self.btn_cancel.config(state="normal")
        self._countdown_step(1.5) # 1.5s delay

    def _countdown_step(self, remaining):
        if not self.countdown_active: return
        
        if remaining <= 0:
            self.lbl_countdown.config(text="")
            self.btn_cancel.config(state="disabled")
            self.countdown_active = False
            self.perform_send()
        else:
            self.lbl_countdown.config(text=f"Sending in {remaining:.1f}s...")
            self.delay_timer = self.root.after(100, lambda: self._countdown_step(remaining - 0.1))

    def cancel_auto_send(self):
        self.countdown_active = False
        if self.delay_timer: self.root.after_cancel(self.delay_timer)
        self.lbl_countdown.config(text="Auto-Send Cancelled", foreground="red")
        self.btn_cancel.config(state="disabled")
        logging.info("Auto-send cancelled by user.")

    def perform_send(self):
        if self.send_callback:
            self.set_state(AppState.SENDING)
            self.send_callback()
            # Revert to listening after a moment
            self.root.after(1000, lambda: self.set_state(AppState.LISTENING))

    def manual_send(self):
        self.cancel_auto_send() # Cancel any pending auto timer to avoid double send
        self.perform_send()
