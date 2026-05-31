import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from src.app import TranslatorApp


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("划词翻译")
    app.setQuitOnLastWindowClosed(False)

    window = TranslatorApp()
    window.hide()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
