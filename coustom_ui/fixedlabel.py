from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


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
                text-align: center;
            }
        """
        self.current_style = self.default_style  # 增加一个变量来存储当前样式
        self.setStyleSheet(self.default_style)
        self.setFixedSize(60, 30)  # 设置固定高度
        self.adjustSize()

    def setText(self, text):
        super().setText(text)
        self.adjustSize()

    def enterEvent(self, event):
        # 不改变样式
        super().enterEvent(event)

    def leaveEvent(self, event):
        # 不重置样式
        super().leaveEvent(event)

    def set_custom_style(self, style):
        self.current_style = style
        self.setStyleSheet(style)
