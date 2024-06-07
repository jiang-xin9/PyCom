import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from ui.resources import *


class CustomMessageBox(QWidget):
    message_box_positions = []
    default_parent = None  # 添加一个类变量来存储默认父窗口

    def __init__(self, message, message_type, parent=None):
        if parent is None:
            parent = CustomMessageBox.default_parent
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        styles = {
            "success": """
                background-color: rgb(240,249,235);
                color: rgb(119,200,79);
                border: 1px solid rgb(225,243,216);
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                font-family: 'Microsoft YaHei';
            """,
            "warning": """
                background-color: rgb(253,246,236);
                color: rgb(230,162,60);
                border: 1px solid rgb(250,236,216);
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                font-family: 'Microsoft YaHei';
            """,
            "error": """
                background-color: rgb(254,240,240);
                color: rgb(247,141,141);
                border: 1px solid rgb(253,226,226);
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                font-family: 'Microsoft YaHei';
            """,
            "custom": """
                background-color: rgb(244,244,245);
                color: rgb(144,147,153);
                border: 1px solid rgb(233,233,235);
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                font-family: 'Microsoft YaHei';
            """
        }

        icons = {
            "success": ":icons/icon/success.png",  # Replace with your success icon path
            "warning": ":icons/icon/warning.png",  # Replace with your warning icon path
            "error": ":icons/icon/error.png",  # Replace with your error icon path
            "custom": "::icons/icon/info.png"  # Replace with your custom icon path
        }

        frame = QFrame(self)
        frame.setStyleSheet(styles[message_type])
        frame.setContentsMargins(3, 3, 3, 3)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        icon_label = QLabel(frame)
        icon_path = icons[message_type]
        pixmap = QPixmap(icon_path).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("padding-right: 5px;border: none;")

        text_label = QLabel(message, frame)
        text_label.setStyleSheet("padding-left: 0px;border: none;")
        text_label.adjustSize()

        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        frame.setLayout(layout)

        frame.adjustSize()
        frame.setFixedWidth(frame.sizeHint().width())

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

        QTimer.singleShot(1500, self.close)

    @staticmethod
    def show_box(message, message_type, parent=None):
        if parent is None:
            parent = CustomMessageBox.default_parent
        custom_message_box = CustomMessageBox(message, message_type, parent)

        custom_message_box.adjustSize()
        custom_message_box.setFixedWidth(custom_message_box.sizeHint().width())

        parent_geometry = parent.geometry()
        x = parent_geometry.center().x() - custom_message_box.width() // 2
        y = parent_geometry.top() + 20

        if CustomMessageBox.message_box_positions:
            y = CustomMessageBox.message_box_positions[-1] + 40

        custom_message_box.setGeometry(x, y, custom_message_box.width(), 65)
        custom_message_box.show()
        custom_message_box.raise_()
        custom_message_box.activateWindow()  # 确保消息框在前台显示

        CustomMessageBox.message_box_positions.append(y)

    def closeEvent(self, event):
        CustomMessageBox.message_box_positions.remove(self.geometry().y())
        event.accept()
