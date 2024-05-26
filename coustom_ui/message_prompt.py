import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from ui.resources import *


class CustomMessageBox(QWidget):
    message_box_positions = []

    def __init__(self, message, message_type, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        styles = {
            "success": """
                background-color: #d4edda;
                color: #155724;
                border-radius: 5px;
                padding: 5px;
                font-size: 18px;
            """,
            "warning": """
                background-color: #fff3cd;
                color: #856404;
                border-radius: 5px;
                padding: 5px;
                font-size: 18px;
            """,
            "error": """
                background-color: #f8d7da;
                color: #721c24;
                border-radius: 5px;
                padding: 5px;
                font-size: 18px;
            """,
            "custom": """
                background-color: #d1ecf1;
                color: #0c5460;
                border-radius: 5px;
                padding: 5px;
                font-size: 18px;
            """
        }

        icons = {
            "success": ":icons/icon/success.png",  # Replace with your success icon path
            "warning": ":icons/icon/warning.png",  # Replace with your warning icon path
            "error": ":icons/icon/error.png",  # Replace with your error icon path
            "custom": ":icons/icon/info.png"  # Replace with your custom icon path
        }

        frame = QFrame(self)
        frame.setStyleSheet(styles[message_type])
        frame.setContentsMargins(3, 3, 3, 3)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        icon_label = QLabel(frame)
        icon_path = icons[message_type]
        pixmap = QPixmap(icon_path).scaled(25, 25, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("padding-right: 5px;")  # 调整图标右侧的间距

        text_label = QLabel(message, frame)
        text_label.setStyleSheet("padding-left: 0px;")  # 调整文本左侧的间距
        text_label.adjustSize()

        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        frame.setLayout(layout)

        # Ensure the width is enough to display the text and icon properly
        frame.adjustSize()
        frame.setFixedWidth(frame.sizeHint().width())

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

        QTimer.singleShot(1500, self.close)  # Message box will disappear after 3 seconds

    @staticmethod
    def show_box(message, message_type, parent):
        screen_geometry = QApplication.desktop().availableGeometry(parent)
        x = screen_geometry.center().x() - 200  # Center horizontally, 200 is half the width of the message box
        y = screen_geometry.top() + 20  # Display near the top of the screen

        # Adjust y position based on previous message boxes
        if CustomMessageBox.message_box_positions:
            y = CustomMessageBox.message_box_positions[-1] + 60  # 60 is the height of the message box plus some margin

        custom_message_box = CustomMessageBox(message, message_type, parent)
        custom_message_box.setGeometry(x, y, custom_message_box.width(), 50)
        custom_message_box.show()
        custom_message_box.raise_()

        # Save the y position of the current message box
        CustomMessageBox.message_box_positions.append(y)

    def closeEvent(self, event):
        # Remove the current message box from the position list
        CustomMessageBox.message_box_positions.remove(self.geometry().y())
        event.accept()