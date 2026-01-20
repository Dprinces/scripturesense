import speech_recognition as sr
import threading
import queue
import logging

class AudioCapture:
    def __init__(self, device_index=None, energy_threshold=300):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.microphone = sr.Microphone(device_index=device_index)
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.stop_listening_func = None

    def start_listening(self):
        """
        Starts listening in a background thread.
        Audio chunks (or processed audio objects) are put into the queue.
        """
        logging.info("Starting audio capture...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            logging.info("Microphone calibrated.")
        
        # listen_in_background spawns a thread and calls callback when audio is captured
        self.stop_listening_func = self.recognizer.listen_in_background(
            self.microphone, 
            self._audio_callback
        )
        self.is_listening = True

    def _audio_callback(self, recognizer, audio):
        """
        Callback called by speech_recognition when a phrase is recorded.
        """
        try:
            self.audio_queue.put(audio)
        except Exception as e:
            logging.error(f"Error in audio callback: {e}")

    def stop_listening(self):
        if self.stop_listening_func:
            self.stop_listening_func(wait_for_stop=False)
            self.stop_listening_func = None
        self.is_listening = False
        logging.info("Audio capture stopped.")

    def get_audio(self):
        """
        Generator to yield audio objects from the queue.
        """
        while self.is_listening or not self.audio_queue.empty():
            try:
                yield self.audio_queue.get(timeout=1)
            except queue.Empty:
                continue
