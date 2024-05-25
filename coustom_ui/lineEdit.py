from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QLineEdit, QSizePolicy

class NewLineEdit(QLineEdit):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setMouseTracking(True)
        self.default_style = """
            QLineEdit {
                border: 0.5px solid rgb(64, 158, 255);
                background-color: rgb(255, 255, 255);
                border-radius: 4px;
                color: rgb(64, 158, 255);
                padding: 5px 10px;
                font-size: 10px;
                font-family: 'Microsoft YaHei';
            }
        """
        self.setStyleSheet(self.default_style)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.adjustSizeToText()

        self.textChanged.connect(self.adjustSizeToText)

    def adjustSizeToText(self):
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text()) + 20
        self.setMinimumWidth(text_width)  # 设置最小宽度而不是固定宽度

    def enterEvent(self, event):
        super().enterEvent(event)

    def leaveEvent(self, event):
        super().leaveEvent(event)
