from PyQt5.QtCore import QObject, pyqtSignal
from coustom_ui.message_prompt import CustomMessageBox


class SignalEmitter(QObject):
    universal_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def error_signal(self, message):
        """
        发送信号的方法。

        :param message: 要发送的消息
        """
        # self.universal_signal.emit(message)
        CustomMessageBox.show_box(message, "error")

    def success_signal(self, message):
        # self.universal_signal.emit(message)
        CustomMessageBox.show_box(message, "success")

    def custom_signal(self, message):
        # self.universal_signal.emit(message)
        CustomMessageBox.show_box(message, "custom")

    def warning_signal(self, message):
        # self.universal_signal.emit(message)
        CustomMessageBox.show_box(message, "warning")
