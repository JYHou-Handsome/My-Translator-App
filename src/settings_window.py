from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QWidget, QFormLayout,
    QComboBox, QMessageBox,
)
from PyQt6.QtCore import Qt
import src.database as db


LANGUAGES = {
    "auto": "自动检测",
    "zh": "中文",
    "en": "英语",
    "ja": "日语",
    "ko": "韩语",
    "fr": "法语",
    "de": "德语",
    "es": "西班牙语",
    "pt": "葡萄牙语",
    "ru": "俄语",
}


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("划词翻译 - 设置")
        self.setMinimumSize(480, 380)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self._init_ui()
        self._load_settings()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        tabs = QTabWidget()
        layout.addWidget(tabs)

        general_tab = QWidget()
        tabs.addTab(general_tab, "基本设置")
        self._init_general_tab(general_tab)

        shortcut_tab = QWidget()
        tabs.addTab(shortcut_tab, "快捷键")
        self._init_shortcut_tab(shortcut_tab)

        about_tab = QWidget()
        tabs.addTab(about_tab, "关于")
        self._init_about_tab(about_tab)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        save_btn = QPushButton("保存")
        save_btn.clicked.connect(self._on_save)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

    def _init_general_tab(self, tab):
        form = QFormLayout(tab)
        form.setContentsMargins(20, 20, 20, 20)
        form.setSpacing(12)

        self.youdao_app_key = QLineEdit()
        self.youdao_app_key.setPlaceholderText("有道翻译应用 ID")
        form.addRow("有道 App Key:", self.youdao_app_key)

        self.youdao_app_secret = QLineEdit()
        self.youdao_app_secret.setPlaceholderText("有道翻译应用密钥")
        self.youdao_app_secret.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("有道 App Secret:", self.youdao_app_secret)

        key_hint = QLabel(
            '<a href="https://ai.youdao.com" style="color:#1a73e8;">去有道 AI 开放平台创建应用 →</a>'
        )
        key_hint.setOpenExternalLinks(True)
        form.addRow("", key_hint)

        test_btn = QPushButton("测试连接")
        test_btn.clicked.connect(self._test_connection)
        form.addRow("", test_btn)

        self.source_lang = QComboBox()
        for code, name in LANGUAGES.items():
            self.source_lang.addItem(f"{name} ({code})", code)
        form.addRow("源语言:", self.source_lang)

        self.target_lang = QComboBox()
        for code, name in LANGUAGES.items():
            if code != "auto":
                self.target_lang.addItem(f"{name} ({code})", code)
        form.addRow("目标语言:", self.target_lang)

        self.tesseract_path = QLineEdit()
        self.tesseract_path.setPlaceholderText("留空则使用系统 PATH（不装Tesseract则OCR不可用）")
        form.addRow("Tesseract 路径:", self.tesseract_path)

    def _init_shortcut_tab(self, tab):
        form = QFormLayout(tab)
        form.setContentsMargins(20, 20, 20, 20)
        form.setSpacing(12)

        self.trans_hotkey = QLineEdit()
        self.trans_hotkey.setPlaceholderText("例如: ctrl+shift+t")
        form.addRow("划词翻译快捷键:", self.trans_hotkey)

        self.ocr_hotkey = QLineEdit()
        self.ocr_hotkey.setPlaceholderText("例如: ctrl+shift+o")
        form.addRow("OCR 翻译快捷键:", self.ocr_hotkey)

        self.auto_translate = QComboBox()
        self.auto_translate.addItems(["开启", "关闭"])
        form.addRow("自动检测剪贴板翻译:", self.auto_translate)

    def _init_about_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        info = QLabel(
            "划词翻译工具 v1.0\n\n"
            "技术栈: Python + PyQt6\n"
            "翻译引擎: 有道翻译 API\n"
            "OCR: Tesseract\n"
            "TTS: pyttsx3\n\n"
            "使用说明:\n"
            "1. 先设置有道翻译 App Key 和 App Secret\n"
            "2. 选中文本后按快捷键调出翻译\n"
            "3. 支持 OCR 截图识别翻译\n"
            "4. 可收藏单词/短语到单词本\n"
            "5. 支持朗读原文发音"
        )
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(info)

    def _test_connection(self):
        key = self.youdao_app_key.text().strip()
        secret = self.youdao_app_secret.text().strip()
        if not key or not secret:
            QMessageBox.warning(self, "提示", "请先填写 App Key 和 App Secret")
            return
        from src.translator import YoudaoTranslator
        t = YoudaoTranslator(key, secret)
        success, result = t.test_connection()
        if success:
            QMessageBox.information(self, "连接成功", f"有道翻译 API 连接正常！\n翻译测试: hello → {result}")
        else:
            QMessageBox.warning(self, "连接失败", result)

    def _load_settings(self):
        self.youdao_app_key.setText(db.get_setting("youdao_app_key", ""))
        self.youdao_app_secret.setText(db.get_setting("youdao_app_secret", ""))
        self.trans_hotkey.setText(db.get_setting("trans_hotkey", "ctrl+shift+t"))
        self.ocr_hotkey.setText(db.get_setting("ocr_hotkey", "ctrl+shift+o"))

        src = db.get_setting("source_lang", "auto")
        idx = self.source_lang.findData(src)
        if idx >= 0:
            self.source_lang.setCurrentIndex(idx)

        tgt = db.get_setting("target_lang", "zh")
        idx = self.target_lang.findData(tgt)
        if idx >= 0:
            self.target_lang.setCurrentIndex(idx)

        auto = db.get_setting("auto_translate", "开启")
        self.auto_translate.setCurrentText(auto)
        self.tesseract_path.setText(db.get_setting("tesseract_path", ""))

    def _on_save(self):
        db.set_setting("youdao_app_key", self.youdao_app_key.text().strip())
        db.set_setting("youdao_app_secret", self.youdao_app_secret.text().strip())
        db.set_setting("trans_hotkey", self.trans_hotkey.text().strip() or "ctrl+shift+t")
        db.set_setting("ocr_hotkey", self.ocr_hotkey.text().strip() or "ctrl+shift+o")
        db.set_setting("source_lang", self.source_lang.currentData())
        db.set_setting("target_lang", self.target_lang.currentData())
        db.set_setting("auto_translate", self.auto_translate.currentText())
        db.set_setting("tesseract_path", self.tesseract_path.text().strip())
        QMessageBox.information(self, "已保存", "设置已保存，部分设置重启后生效")
        self.accept()

    @staticmethod
    def get_settings() -> dict:
        return {
            "youdao_app_key": db.get_setting("youdao_app_key", ""),
            "youdao_app_secret": db.get_setting("youdao_app_secret", ""),
            "trans_hotkey": db.get_setting("trans_hotkey", "ctrl+shift+t"),
            "ocr_hotkey": db.get_setting("ocr_hotkey", "ctrl+shift+o"),
            "source_lang": db.get_setting("source_lang", "auto"),
            "target_lang": db.get_setting("target_lang", "zh"),
            "auto_translate": db.get_setting("auto_translate", "开启"),
            "tesseract_path": db.get_setting("tesseract_path", ""),
        }
