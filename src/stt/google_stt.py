import speech_recognition as sr
import logging
from .engine import STTEngine

class GoogleSTT(STTEngine):
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio_data):
        try:
            # recognize_google uses the Google Web Speech API
            text = self.recognizer.recognize_google(audio_data)
            logging.info(f"STT Output: {text}")
            return text
        except sr.UnknownValueError:
            logging.debug("STT: Could not understand audio")
            return None
        except sr.RequestError as e:
            logging.error(f"STT: Could not request results from Google Speech Recognition service; {e}")
            return None
