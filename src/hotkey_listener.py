import threading
import keyboard
import pyperclip


class HotkeyListener:
    def __init__(self):
        self._hotkeys = {}
        self._registered_hooks = []
        self._thread = None
        self._running = False

    def register(self, hotkey: str, callback):
        self._hotkeys[hotkey] = callback

    def unregister(self, hotkey: str):
        if hotkey in self._hotkeys:
            del self._hotkeys[hotkey]

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._listen, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        for hook in self._registered_hooks:
            try:
                keyboard.remove_hotkey(hook)
            except Exception:
                pass
        self._registered_hooks.clear()

    def _listen(self):
        for hotkey, callback in self._hotkeys.items():
            try:
                hook = keyboard.add_hotkey(hotkey, callback)
                self._registered_hooks.append(hook)
            except Exception:
                pass
        try:
            keyboard.wait()
        except Exception:
            pass

    def reload(self):
        self.stop()
        self.start()

    @staticmethod
    def get_clipboard_text() -> str:
        try:
            return pyperclip.paste().strip()
        except Exception:
            return ""
