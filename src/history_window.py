from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
import src.database as db


class HistoryWindow(QWidget):
    def __init__(self):
        super().__init__(None)
        self.setWindowTitle("划词翻译 - 历史记录")
        self.setMinimumSize(500, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self._init_ui()
        self._load_history()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        top_row = QHBoxLayout()
        title = QLabel("📜 历史记录")
        title.setFont(QFont("", 16, QFont.Weight.Bold))
        top_row.addWidget(title)
        top_row.addStretch()
        layout.addLayout(top_row)

        self.history_list = QListWidget()
        self.history_list.setAlternatingRowColors(True)
        self.history_list.setSpacing(2)
        self.history_list.setWordWrap(True)
        layout.addWidget(self.history_list)

        bottom_row = QHBoxLayout()
        bottom_row.addStretch()
        self.count_label = QLabel("共 0 条记录")
        self.count_label.setStyleSheet("color: #888888;")
        bottom_row.addWidget(self.count_label)

        clear_btn = QPushButton("清空历史")
        clear_btn.clicked.connect(self._on_clear)
        bottom_row.addWidget(clear_btn)
        layout.addLayout(bottom_row)

    def _load_history(self):
        self.history_list.clear()
        records = db.get_history(limit=200)
        for r in records:
            text = f"{r['source_text']}\n    →  {r['translation']}    [{r['created_at']}]"
            item = QListWidgetItem(text)
            self.history_list.addItem(item)
        self.count_label.setText(f"共 {len(records)} 条记录")

    def _on_clear(self):
        db.clear_history()
        self._load_history()

    def showEvent(self, event):
        super().showEvent(event)
        self._load_history()
