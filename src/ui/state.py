from enum import Enum

class AppState(Enum):
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    DETECTED = "DETECTED"
    SENDING = "SENDING"
    ERROR = "ERROR"
