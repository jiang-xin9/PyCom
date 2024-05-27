import asyncio
import serial_asyncio
from PyQt5.QtCore import QObject, pyqtSignal


class SerialWorker(QObject):
    data_received = pyqtSignal(str)
    data_sent = pyqtSignal(str)
    connection_made = pyqtSignal()
    connection_lost = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.transport = None

    async def open_serial_port(self, port, baudrate):
        try:
            loop = asyncio.get_event_loop()
            self.transport, protocol = await serial_asyncio.create_serial_connection(
                loop, lambda: SerialProtocol(self), port, baudrate)
            self.connection_made.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))

    def close_serial_port(self):
        if self.transport:
            self.transport.close()
            self.transport = None
            self.connection_lost.emit()

    def send_data(self, data):
        if self.transport:
            try:
                print(f"Sending: {data}")  # 调试信息
                self.transport.write((data + '\r\n').encode('utf-8'))  # 确保发送的数据带有结束符
                self.data_sent.emit(data)  # 发射信号
            except Exception as e:
                self.error_occurred.emit(str(e))


class SerialProtocol(asyncio.Protocol):
    def __init__(self, worker):
        super().__init__()
        self.worker = worker

    def connection_made(self, transport):
        self.transport = transport
        print("Connection made")  # 调试信息

    def data_received(self, data):
        try:
            print(f"Raw data received: {data}")  # 调试信息
            lines = data.split(b'\r\n')
            for line in lines:
                if line:  # 过滤掉空行
                    message = line.decode('utf-8').strip()
                    print(f"Received: {message}")  # 调试信息
                    self.worker.data_received.emit(message)
        except Exception as e:
            self.worker.error_occurred.emit(str(e))

    def connection_lost(self, exc):
        print("Connection lost")  # 调试信息
        self.worker.connection_lost.emit()
        self.transport = None
