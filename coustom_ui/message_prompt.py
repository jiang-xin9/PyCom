# - coding:utf-8 -
# author: 清安安
# CSDN: 清安无别事
# file_time: 2024/5/26 13:40
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
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        icon_label = QLabel(frame)
        icon_path = icons[message_type]
        pixmap = QPixmap(icon_path).scaled(25, 25, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(pixmap)

        text_label = QLabel(message, frame)
        text_label.adjustSize()

        # Calculate width based on text and icon size
        width = text_label.sizeHint().width() + icon_label.width()
        frame.setFixedWidth(width)

        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.setAlignment(Qt.AlignLeft)
        frame.setLayout(layout)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

        QTimer.singleShot(1000, self.close)  # Message box will disappear after 3 seconds

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom Message Box Example")

        self.success_button = QPushButton("Success", self)
        self.success_button.clicked.connect(
            lambda: CustomMessageBox.show_box("Success Message", "success", self))

        self.warning_button = QPushButton("Warning", self)
        self.warning_button.clicked.connect(
            lambda: CustomMessageBox.show_box("Warning Message", "warning", self))

        self.error_button = QPushButton("Error", self)
        self.error_button.clicked.connect(
            lambda: CustomMessageBox.show_box("Error Message", "error", self))

        self.custom_button = QPushButton("Custom", self)
        self.custom_button.clicked.connect(
            lambda: CustomMessageBox.show_box("Custom Message", "custom", self))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.success_button)
        self.layout.addWidget(self.warning_button)
        self.layout.addWidget(self.error_button)
        self.layout.addWidget(self.custom_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
