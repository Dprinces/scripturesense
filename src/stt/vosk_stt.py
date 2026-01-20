import json
import logging
import os
import vosk
from .engine import STTEngine

class VoskSTT(STTEngine):
    def __init__(self, model_path="data/models/vosk-model-small-en-us-0.15"):
        self.model_path = model_path
        if not os.path.exists(self.model_path):
            logging.error(f"Vosk model not found at {self.model_path}")
            logging.error("Please run 'python scripts/setup_vosk.py' to download it.")
            raise FileNotFoundError(f"Vosk model missing: {self.model_path}")
            
        logging.info(f"Loading Vosk model from {self.model_path}...")
        self.model = vosk.Model(self.model_path)
        logging.info("Vosk model loaded.")

    def transcribe(self, audio_data):
        """
        Transcribes audio data using Vosk.
        Note: Vosk expects raw audio bytes (PCM 16-bit mono), but speech_recognition 
        AudioData provides wav/raw.
        """
        try:
            # Create a recognizer for this specific audio chunk
            rec = vosk.KaldiRecognizer(self.model, audio_data.sample_rate)
            
            # Get raw bytes
            data = audio_data.get_raw_data()
            
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
            else:
                # Partial result
                result = json.loads(rec.PartialResult())
                text = result.get("partial", "")
            
            if text:
                logging.info(f"Vosk Output: {text}")
                return text
            return None
            
        except Exception as e:
            logging.error(f"Vosk STT Error: {e}")
            return None
