import threading
import pyttsx3


class TTSEngine:
    def __init__(self):
        self._rate = 150
        self._volume = 1.0

    def speak(self, text: str, lang: str = "en"):
        thread = threading.Thread(target=self._speak_thread, args=(text, lang), daemon=True)
        thread.start()

    def _speak_thread(self, text: str, lang: str):
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", self._rate)
            engine.setProperty("volume", self._volume)
            voices = engine.getProperty("voices")
            for v in voices:
                if lang == "zh" and ("chinese" in v.name.lower() or "zh" in v.id.lower()):
                    engine.setProperty("voice", v.id)
                    break
                elif lang == "en" and ("english" in v.name.lower() or "en" in v.id.lower()):
                    engine.setProperty("voice", v.id)
                    break
            engine.say(text)
            engine.runAndWait()
            del engine
        except Exception:
            pass

    def set_rate(self, rate: int):
        self._rate = rate

    def set_volume(self, volume: float):
        self._volume = max(0.0, min(1.0, volume))

    @property
    def rate(self):
        return self._rate

    @property
    def volume(self):
        return self._volume
