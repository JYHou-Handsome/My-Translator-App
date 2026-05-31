from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QApplication
from PyQt6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont
import src.database as db


STYLE_SHEET = """
QWidget#floatingWindow {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 12px;
}
QLabel#titleLabel {
    color: #888888;
    font-size: 11px;
}
QLabel#sourceText {
    color: #333333;
    font-size: 14px;
    font-weight: bold;
}
QLabel#translationText {
    color: #1a73e8;
    font-size: 15px;
}
QPushButton#actionBtn {
    background-color: #f0f0f0;
    border: none;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    color: #555555;
}
QPushButton#actionBtn:hover {
    background-color: #e0e0e0;
}
QPushButton#actionBtn:pressed {
    background-color: #d0d0d0;
}
QPushButton#closeBtn {
    background: transparent;
    border: none;
    font-size: 16px;
    color: #999999;
}
QPushButton#closeBtn:hover {
    color: #333333;
}
"""


class FloatingWindow(QWidget):
    def __init__(self):
        super().__init__(None)
        self._opacity = 1.0
        self._source_text = ""
        self._translation = ""
        self._tts_callback = None
        self._init_ui()
        self._setup_animation()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setObjectName("floatingWindow")
        self.setStyleSheet(STYLE_SHEET)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)

        top_row = QHBoxLayout()
        self.title_label = QLabel("划词翻译")
        self.title_label.setObjectName("titleLabel")
        top_row.addWidget(self.title_label)
        top_row.addStretch()
        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.clicked.connect(self.hide)
        top_row.addWidget(self.close_btn)
        layout.addLayout(top_row)

        self.source_label = QLabel()
        self.source_label.setObjectName("sourceText")
        self.source_label.setWordWrap(True)
        self.source_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.source_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(separator)

        self.trans_label = QLabel()
        self.trans_label.setObjectName("translationText")
        self.trans_label.setWordWrap(True)
        self.trans_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.trans_label)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        self.tts_btn = QPushButton("🔊 朗读")
        self.tts_btn.setObjectName("actionBtn")
        self.tts_btn.clicked.connect(self._on_tts)
        btn_row.addWidget(self.tts_btn)

        self.save_btn = QPushButton("📖 收藏")
        self.save_btn.setObjectName("actionBtn")
        self.save_btn.clicked.connect(self._on_save)
        btn_row.addWidget(self.save_btn)

        btn_row.addStretch()
        layout.addLayout(btn_row)

        self.adjustSize()

    def _setup_animation(self):
        self._anim = QPropertyAnimation(self, b"opacity")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_opacity(self):
        return self._opacity

    def set_opacity(self, opacity):
        self._opacity = opacity
        self.setWindowOpacity(opacity)
        self.update()

    opacity = pyqtProperty(float, get_opacity, set_opacity)

    def show_translation(self, source: str, translation: str, tts_callback=None):
        self._source_text = source
        self._translation = translation
        self._tts_callback = tts_callback

        self.save_btn.setText("📖 收藏")
        self.save_btn.setEnabled(True)

        self._anim.stop()

        self.source_label.setText(source)
        self.trans_label.setText(translation)
        self.adjustSize()

        pos = self._calculate_position()
        self.move(pos)
        self.setWindowOpacity(1.0)
        self._opacity = 1.0
        self.show()
        self.raise_()
        self.activateWindow()

    def _calculate_position(self) -> QPoint:
        cursor_pos = self.cursor().pos()
        screen = QApplication.screenAt(cursor_pos)
        if screen:
            screen_geo = screen.availableGeometry()
        else:
            screen_geo = QApplication.primaryScreen().availableGeometry()

        w = self.width()
        h = self.height()

        x = cursor_pos.x() + 10
        y = cursor_pos.y() + 10

        if x + w > screen_geo.right():
            x = cursor_pos.x() - w - 10
        if y + h > screen_geo.bottom():
            y = cursor_pos.y() - h - 10
        if x < screen_geo.left():
            x = screen_geo.left() + 5
        if y < screen_geo.top():
            y = screen_geo.top() + 5

        return QPoint(int(x), int(y))

    def _on_tts(self):
        if self._tts_callback:
            self._tts_callback(self._translation)

    def _on_save(self):
        db.save_to_word_book(self._source_text, self._translation)
        self.save_btn.setText("✓ 已收藏")
        self.save_btn.setEnabled(False)

    def mousePressEvent(self, event):
        self._drag_pos = event.globalPosition().toPoint()
        self._dragging = True
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if hasattr(self, "_dragging") and self._dragging:
            self.move(self.pos() + event.globalPosition().toPoint() - self._drag_pos)
            self._drag_pos = event.globalPosition().toPoint()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._dragging = False
        super().mouseReleaseEvent(event)
