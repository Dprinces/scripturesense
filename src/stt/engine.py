from abc import ABC, abstractmethod

class STTEngine(ABC):
    @abstractmethod
    def transcribe(self, audio_data):
        """
        Transcribes audio data to text.
        :param audio_data: Audio data object (e.g., speech_recognition.AudioData)
        :return: Transcribed text (str) or None if failed
        """
        pass
