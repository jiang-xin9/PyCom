from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QLineEdit, QSizePolicy, QWidget


class NewLineEdit(QLineEdit):
    def __init__(self, text="", parent=None):
        # Handle different types of initializations
        if isinstance(text, QWidget):
            parent = text
            text = ""
        super().__init__(text, parent)

        self.setMouseTracking(True)
        self.default_style = """
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px 10px;
            }
        """
        self.setStyleSheet(self.default_style)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.adjustSizeToText()

        # Set cursor position to the start only on initialization
        self.setCursorPosition(0)

        self.textChanged.connect(self.adjustSizeToText)

    def adjustSizeToText(self):
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.horizontalAdvance(self.text()) + 20
        self.setMinimumWidth(text_width)  # 设置最小宽度而不是固定宽度

    def enterEvent(self, event):
        super().enterEvent(event)

    def leaveEvent(self, event):
        super().leaveEvent(event)
