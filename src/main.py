import time
import logging
import sys
import os
import threading
import tkinter as tk

from audio.capture import AudioCapture
from stt.google_stt import GoogleSTT
from stt.vosk_stt import VoskSTT
from detection.detector import ScriptureDetector
from bible.provider import BibleProvider
from presentation.controller import PresentationController
from ui.app import ScriptureSenseUI

# Configure logging to buffer or stdout
# The UI will grab the root logger, so basicConfig is fine.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ScriptureSenseApp:
    def __init__(self):
        self.detector = ScriptureDetector()
        self.bible = BibleProvider()
        self.presenter = PresentationController()
        
        self.audio_source = None
        self.stt_engine = None
        self.is_listening = False
        
        # Duplicate Prevention State
        self.last_sent_verse = None
        self.last_sent_time = 0
        self.DUPLICATE_TIMEOUT = 5.0 # Seconds to ignore duplicates

        # Initialize Audio/STT components lazily
        self._init_audio_components()

    def _init_audio_components(self):
        try:
            self.audio_source = AudioCapture()
            if os.path.exists("data/models/vosk-model-small-en-us-0.15"):
                logging.info("Using Offline STT (Vosk).")
                self.stt_engine = VoskSTT()
            else:
                logging.info("Using Online STT (Google).")
                self.stt_engine = GoogleSTT()
        except Exception as e:
            logging.error(f"Audio Init Failed: {e}")

    def start_listening_thread(self):
        """Called by UI Start button"""
        if not self.audio_source:
            self._init_audio_components()
            if not self.audio_source:
                logging.error("Cannot start: Audio source unavailable.")
                return

        self.is_listening = True
        try:
            self.audio_source.start_listening()
            # Start processing loop in a separate thread
            threading.Thread(target=self._processing_loop, daemon=True).start()
        except Exception as e:
            logging.error(f"Start Failed: {e}")
            self.is_listening = False

    def stop_listening(self):
        """Called by UI Stop button"""
        self.is_listening = False
        if self.audio_source:
            self.audio_source.stop_listening()
        logging.info("Stopped listening.")

    def change_profile(self, profile_name):
        """Called by UI Profile Selector"""
        self.presenter.set_profile(profile_name)

    def _processing_loop(self):
        logging.info("Listening for scripture...")
        
        while self.is_listening:
            try:
                # Get audio chunks generator (non-blocking usually, but here we iterate)
                # Since get_audio yields, we need to be careful about stopping.
                # We'll just manually pull from queue if possible or use the generator
                # The generator in capture.py has a timeout, so it yields periodically.
                
                # NOTE: AudioCapture.get_audio is a generator that runs while is_listening is True.
                # If we stop_listening, the generator breaks.
                for audio_chunk in self.audio_source.get_audio():
                    if not self.is_listening: break
                    
                    text = self.stt_engine.transcribe(audio_chunk)
                    if text:
                        # Update UI Transcript
                        if self.ui:
                            self.ui.root.after(0, self.ui.update_transcript, text)
                        
                        self._handle_text(text)
                        
            except Exception as e:
                logging.error(f"Loop Error: {e}")
                time.sleep(1)

    def _handle_text(self, text):
        references = self.detector.detect(text)
        if not references: return

        for ref in references:
            book = ref['book']
            chapter = ref['chapter']
            verse = ref['verse']
            confidence = ref.get('confidence', 0.0)
            
            # 1. Fetch Text
            verse_text = self.bible.get_verse(book, chapter, verse)
            if not verse_text:
                logging.warning(f"Verse not found: {book} {chapter}:{verse}")
                continue

            ref_str = f"{book} {chapter}:{verse}"

            # 2. Update UI (Main Display)
            if self.ui:
                # Define callback for the SEND NOW button
                send_action = lambda b=book, c=chapter, v=verse: self.presenter.display_verse(b, c, v)
                
                self.ui.root.after(0, lambda r=ref_str, t=verse_text, conf=confidence, cb=send_action: 
                                   self.ui.update_detected(r, t, conf, cb))

            # 3. Safety Checks
            # Rule A: Confidence >= 85% (0.85)
            if confidence < 0.85:
                logging.info(f"Skipped {ref_str}: Low confidence ({confidence:.2f})")
                continue

            # Rule B: Duplicate Check
            now = time.time()
            if self.last_sent_verse == ref_str and (now - self.last_sent_time) < self.DUPLICATE_TIMEOUT:
                logging.info(f"Skipped {ref_str}: Duplicate (sent {int(now - self.last_sent_time)}s ago)")
                continue

            # Rule C: Auto Mode
            # UI handles countdown and trigger now via update_detected logic if auto mode is on
            # We just update state here if needed, but UI drives the "Send" event
            pass

    def test_profile_send(self):
        """Sends John 3:16 to test integration"""
        logging.info("Testing Profile Integration...")
        self.presenter.display_verse("John", 3, 16)

    def run(self):
        root = tk.Tk()
        self.ui = ScriptureSenseUI(
            root, 
            start_callback=self.start_listening_thread, 
            stop_callback=self.stop_listening,
            profile_callback=self.change_profile,
            test_profile_callback=self.test_profile_send
        )
        root.mainloop()

if __name__ == "__main__":
    app = ScriptureSenseApp()
    app.run()
