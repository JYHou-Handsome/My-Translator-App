from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QRect, QPoint, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QScreen, QPixmap


class ScreenCaptureOverlay(QWidget):
    region_selected = pyqtSignal(object)

    def __init__(self):
        super().__init__(None)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(Qt.CursorShape.CrossCursor)
        self._start_point = None
        self._end_point = None
        self._is_selecting = False

    def showEvent(self, event):
        screen = QApplication.primaryScreen()
        if screen:
            self.setGeometry(screen.virtualGeometry())
        self.raise_()
        self.activateWindow()
        super().showEvent(event)

    def mousePressEvent(self, event):
        self._start_point = event.position().toPoint()
        self._end_point = self._start_point
        self._is_selecting = True
        self.update()

    def mouseMoveEvent(self, event):
        if self._is_selecting:
            self._end_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        self._is_selecting = False
        self.update()

        if self._start_point and self._end_point:
            x1 = min(self._start_point.x(), self._end_point.x())
            y1 = min(self._start_point.y(), self._end_point.y())
            x2 = max(self._start_point.x(), self._end_point.x())
            y2 = max(self._start_point.y(), self._end_point.y())
            rect = QRect(x1, y1, x2 - x1, y2 - y1)

            if rect.width() > 10 and rect.height() > 10:
                self.hide()
                QTimer.singleShot(200, lambda: self._capture_region(rect))
            else:
                self._start_point = None
                self._end_point = None
                self.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self._start_point = None
            self._end_point = None
            self.hide()

    def _capture_region(self, rect: QRect):
        screen = QApplication.primaryScreen()
        if screen:
            pixmap = screen.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())
            self.region_selected.emit(pixmap)
        self._start_point = None
        self._end_point = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        overlay_color = QColor(0, 0, 0, 100)
        painter.fillRect(self.rect(), overlay_color)

        if self._start_point and self._end_point:
            x1 = min(self._start_point.x(), self._end_point.x())
            y1 = min(self._start_point.y(), self._end_point.y())
            x2 = max(self._start_point.x(), self._end_point.x())
            y2 = max(self._start_point.y(), self._end_point.y())
            rect = QRect(x1, y1, x2 - x1, y2 - y1)

            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(rect, QColor(0, 0, 0, 0))
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)

            pen = QPen(QColor("#1a73e8"), 2)
            painter.setPen(pen)
            painter.drawRect(rect)

            dim_w, dim_h = 60, 24
            dim_x = rect.right() - dim_w - 4
            dim_y = rect.top() - dim_h - 4
            if dim_y < 0:
                dim_y = rect.bottom() + 4
            painter.fillRect(QRect(int(dim_x), int(dim_y), dim_w, dim_h), QColor("#1a73e8"))
            painter.setPen(QColor("#ffffff"))
            painter.drawText(
                QRect(int(dim_x), int(dim_y), dim_w, dim_h),
                Qt.AlignmentFlag.AlignCenter,
                f"{rect.width()}×{rect.height()}",
            )

        painter.end()
