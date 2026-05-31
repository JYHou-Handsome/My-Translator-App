import sys
from PyQt6.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QWidget, QMessageBox,
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor, QFont, QBrush

import src.database as db
from src.translator import YoudaoTranslator
from src.ocr_engine import OCREngine
from src.tts_engine import TTSEngine
from src.floating_window import FloatingWindow
from src.settings_window import SettingsWindow
from src.word_book_window import WordBookWindow
from src.history_window import HistoryWindow
from src.screen_capture import ScreenCaptureOverlay
from src.hotkey_listener import HotkeyListener


def create_tray_icon_pixmap() -> QPixmap:
    px = QPixmap(64, 64)
    px.fill(Qt.GlobalColor.transparent)
    painter = QPainter(px)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QBrush(QColor("#1a73e8")))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(4, 4, 56, 56, 12, 12)
    painter.setPen(QColor("#ffffff"))
    font = QFont("Segoe UI", 28, QFont.Weight.Bold)
    painter.setFont(font)
    painter.drawText(px.rect(), Qt.AlignmentFlag.AlignCenter, "T")
    painter.end()
    return px


class TranslatorApp(QWidget):
    trans_hotkey_triggered = pyqtSignal()
    ocr_hotkey_triggered = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("划词翻译")
        self.setWindowIcon(QIcon(create_tray_icon_pixmap()))

        db.init_db()
        self._translator = YoudaoTranslator()
        self._ocr_engine = OCREngine()
        self._tts_engine = TTSEngine()
        self._hotkey_listener = HotkeyListener()
        self._settings = SettingsWindow.get_settings()
        self._last_clipboard = ""

        self.trans_hotkey_triggered.connect(self._on_translate_hotkey)
        self.ocr_hotkey_triggered.connect(self._on_ocr_hotkey)

        self._floating_window = FloatingWindow()
        self._screen_capture = ScreenCaptureOverlay()
        self._screen_capture.region_selected.connect(self._on_region_captured)

        self._word_book_window = None
        self._history_window = None
        self._settings_window = None

        self._clipboard_timer = QTimer()
        self._clipboard_timer.timeout.connect(self._check_clipboard)

        self._setup_tray()
        self._setup_hotkeys()
        self._start_clipboard_monitor()

    def _setup_tray(self):
        self._tray = QSystemTrayIcon(self)
        self._tray.setIcon(QIcon(create_tray_icon_pixmap()))
        self._tray.setToolTip("划词翻译 - 运行中")

        menu = QMenu()
        trans_action = QAction("🔍 划词翻译 (Ctrl+Shift+T)", self)
        trans_action.triggered.connect(self._on_translate_hotkey)
        menu.addAction(trans_action)

        ocr_action = QAction("📷 OCR 截图翻译 (Ctrl+Shift+O)", self)
        ocr_action.triggered.connect(self._on_ocr_hotkey)
        menu.addAction(ocr_action)

        menu.addSeparator()

        wordbook_action = QAction("📖 单词本", self)
        wordbook_action.triggered.connect(self._show_word_book)
        menu.addAction(wordbook_action)

        history_action = QAction("📜 历史记录", self)
        history_action.triggered.connect(self._show_history)
        menu.addAction(history_action)

        menu.addSeparator()

        settings_action = QAction("⚙ 设置", self)
        settings_action.triggered.connect(self._show_settings)
        menu.addAction(settings_action)

        menu.addSeparator()

        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self._on_quit)
        menu.addAction(quit_action)

        self._tray.setContextMenu(menu)
        self._tray.activated.connect(self._on_tray_activated)
        self._tray.show()

    def _setup_hotkeys(self):
        self._hotkey_listener.register(
            self._settings.get("trans_hotkey", "ctrl+shift+t"),
            self.trans_hotkey_triggered.emit,
        )
        self._hotkey_listener.register(
            self._settings.get("ocr_hotkey", "ctrl+shift+o"),
            self.ocr_hotkey_triggered.emit,
        )
        self._hotkey_listener.start()

    def _start_clipboard_monitor(self):
        if self._settings.get("auto_translate", "开启") == "开启":
            self._clipboard_timer.start(1000)
        else:
            self._clipboard_timer.stop()

    def _check_clipboard(self):
        text = HotkeyListener.get_clipboard_text()
        if text and text != self._last_clipboard:
            self._last_clipboard = text

    def _on_translate_hotkey(self):
        text = HotkeyListener.get_clipboard_text()
        if not text:
            self._floating_window.show_translation(
                "提示", "请先复制要翻译的文本到剪贴板",
                tts_callback=None,
            )
            return
        self._do_translate(text)

    def _on_ocr_hotkey(self):
        self._screen_capture.showFullScreen()
        self._screen_capture.raise_()
        self._screen_capture.activateWindow()

    def _on_region_captured(self, pixmap):
        import tempfile, os
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp_path = tmp.name
        tmp.close()
        pixmap.save(tmp_path, "PNG")
        from PIL import Image
        image = Image.open(tmp_path)
        lang = "eng"
        target_lang = self._settings.get("target_lang", "zh")
        if target_lang == "zh":
            lang = "chi_sim+eng"

        text = self._ocr_engine.recognize_from_image(image, lang=lang)
        os.unlink(tmp_path)

        if not text or text.startswith("[OCR"):
            self._floating_window.show_translation(
                "OCR 识别结果", text or "[未能识别到文字]",
                tts_callback=None,
            )
            return

        self._do_translate(text, is_ocr=True)

    def _do_translate(self, text: str, is_ocr: bool = False):
        self._translator.app_key = self._settings.get("youdao_app_key", "")
        self._translator.app_secret = self._settings.get("youdao_app_secret", "")

        source_lang = self._settings.get("source_lang", "auto")
        target_lang = self._settings.get("target_lang", "zh")

        success, result = self._translator.translate(text, source=source_lang, target=target_lang)

        if success:
            db.add_history(text, result, source_lang, target_lang)
            source_display = f"[OCR 识别] {text}" if is_ocr else text
            tts_lang = self._detect_lang(source_lang, text)
            self._floating_window.show_translation(
                source_display, result,
                tts_callback=lambda t, lang=tts_lang: self._tts_engine.speak(t, lang=lang),
            )
        else:
            self._floating_window.show_translation(
                text, result,
                tts_callback=None,
            )

    def _detect_lang(self, lang: str, text: str) -> str:
        if lang and lang != "auto":
            return "zh" if lang == "zh" else "en"
        if any('\u4e00' <= c <= '\u9fff' for c in text):
            return "zh"
        return "en"

    def _show_word_book(self):
        if not self._word_book_window or not self._word_book_window.isVisible():
            self._word_book_window = WordBookWindow()
        self._word_book_window.show()
        self._word_book_window.raise_()
        self._word_book_window.activateWindow()

    def _show_history(self):
        if not self._history_window or not self._history_window.isVisible():
            self._history_window = HistoryWindow()
        self._history_window.show()
        self._history_window.raise_()
        self._history_window.activateWindow()

    def _show_settings(self):
        if not self._settings_window or not self._settings_window.isVisible():
            self._settings_window = SettingsWindow()
            self._settings_window.finished.connect(self._on_settings_closed)
        self._settings_window.show()
        self._settings_window.raise_()
        self._settings_window.activateWindow()

    def _on_settings_closed(self, result):
        if result == SettingsWindow.DialogCode.Accepted.value:
            self._settings = SettingsWindow.get_settings()
            self._hotkey_listener.stop()
            self._ocr_engine.set_tesseract_path(
                self._settings.get("tesseract_path", "")
            )
            self._setup_hotkeys()
            self._clipboard_timer.stop()
            self._start_clipboard_monitor()

    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self._on_translate_hotkey()

    def _on_quit(self):
        self._hotkey_listener.stop()
        QApplication.quit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
