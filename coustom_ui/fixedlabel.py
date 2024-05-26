from PyQt5.QtWidgets import QLabel


class FixedLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setMouseTracking(True)

        self.default_style = """
            QLabel {
                background-color: #F56C6C;
                border-radius: 4px;
                color: rgb(255, 255, 255);
                padding: 5px 10px;
                font-size: 12px;
                font-family: 'Microsoft YaHei';
            }
        """
        self.setStyleSheet(self.default_style)
        self.setFixedSize(60, 30)  # 设置固定高度
        self.adjustSize()

    def setText(self, text):
        super().setText(text)
        self.adjustSize()

    def enterEvent(self, event):
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self.default_style)
        super().leaveEvent(event)
