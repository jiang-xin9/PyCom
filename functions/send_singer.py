from PyQt5.QtCore import QObject, pyqtSignal


class SignalEmitter(QObject):
    universal_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def send_signal(self, message):
        """
        发送信号的方法。

        :param message: 要发送的消息
        """
        self.universal_signal.emit(message)
