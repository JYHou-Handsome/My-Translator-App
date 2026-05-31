from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QLineEdit, QMessageBox,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
import src.database as db


class WordBookWindow(QWidget):
    def __init__(self):
        super().__init__(None)
        self.setWindowTitle("划词翻译 - 单词本")
        self.setMinimumSize(500, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self._init_ui()
        self._load_words()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        top_row = QHBoxLayout()
        title = QLabel("📖 单词本")
        title.setFont(QFont("", 16, QFont.Weight.Bold))
        top_row.addWidget(title)
        top_row.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索单词或翻译...")
        self.search_input.textChanged.connect(self._on_search)
        self.search_input.setFixedWidth(200)
        top_row.addWidget(self.search_input)
        layout.addLayout(top_row)

        self.word_list = QListWidget()
        self.word_list.setAlternatingRowColors(True)
        self.word_list.setSpacing(2)
        self.word_list.itemDoubleClicked.connect(self._on_delete_word)
        layout.addWidget(self.word_list)

        bottom_row = QHBoxLayout()
        bottom_row.addStretch()
        self.count_label = QLabel("共 0 个单词")
        self.count_label.setStyleSheet("color: #888888;")
        bottom_row.addWidget(self.count_label)

        clear_btn = QPushButton("清空单词本")
        clear_btn.clicked.connect(self._on_clear)
        bottom_row.addWidget(clear_btn)
        layout.addLayout(bottom_row)

    def _load_words(self, keyword: str = ""):
        self.word_list.clear()
        if keyword:
            words = db.search_words(keyword)
        else:
            words = db.get_all_words()
        for w in words:
            text = f"{w['word']}  →  {w['translation']}"
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, w["id"])
            item.setToolTip(f"双击删除 • 收藏于 {w['created_at']}")
            self.word_list.addItem(item)
        self.count_label.setText(f"共 {len(words)} 个单词")

    def _on_search(self, text: str):
        self._load_words(text.strip())

    def _on_delete_word(self, item: QListWidgetItem):
        word_id = item.data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(
            self, "确认删除", f"确定要删除该单词吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            db.delete_word(word_id)
            self._load_words(self.search_input.text().strip())

    def _on_clear(self):
        reply = QMessageBox.question(
            self, "确认清空", "确定要清空所有单词吗？此操作不可恢复。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            db.clear_word_book()
            self._load_words()

    def showEvent(self, event):
        super().showEvent(event)
        self._load_words(self.search_input.text().strip())
