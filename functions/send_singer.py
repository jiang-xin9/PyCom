from PyQt5.QtCore import QObject, pyqtSignal
from coustom_ui.message_prompt import CustomMessageBox


class SignalEmitter(QObject):
    universal_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    @staticmethod
    def error_signal(message, parent=None):
        """
        发送信号的方法。

        :param message: 要发送的消息
        """
        # self.universal_signal.emit(message)
        if parent:
            CustomMessageBox.show_box(message, "error", parent)
        else:
            CustomMessageBox.show_box(message, "error")

    @staticmethod
    def success_signal(message, parent=None):
        # self.universal_signal.emit(message)
        if parent:
            CustomMessageBox.show_box(message, "success", parent)
        else:
            CustomMessageBox.show_box(message, "success")

    @staticmethod
    def custom_signal(message, parent=None):
        # self.universal_signal.emit(message)
        if parent:
            CustomMessageBox.show_box(message, "custom", parent)
        else:
            CustomMessageBox.show_box(message, "custom")

    @staticmethod
    def warning_signal(message, parent=None):
        # self.universal_signal.emit(message)
        if parent:
            CustomMessageBox.show_box(message, "warning", parent)
        else:
            CustomMessageBox.show_box(message, "warning")
