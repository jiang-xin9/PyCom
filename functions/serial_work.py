import asyncio
import serial_asyncio
from PyQt5.QtCore import QObject, pyqtSignal

class SerialWorker(QObject):
    received_data = pyqtSignal(str)
    data_sent = pyqtSignal(str)
    serial_connection_made = pyqtSignal()
    serial_connection_lost = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, check_enter):
        super().__init__()
        self.transport = None
        self.check_enter = check_enter

    async def open_serial_port(self, port, baudrate):
        try:
            loop = asyncio.get_event_loop()
            self.transport, protocol = await serial_asyncio.create_serial_connection(
                loop, lambda: SerialProtocol(self), port, baudrate)
            self.serial_connection_made.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))

    def close_serial_port(self):
        if self.transport:
            self.transport.close()
            self.transport = None
            self.serial_connection_lost.emit()

    def send_data(self, data):
        if self.transport:
            try:
                if self.check_enter.toggled:
                    self.transport.write((data + '\r\n').encode('utf-8'))  # 确保发送的数据带有结束符
                else:
                    self.transport.write((data).encode('utf-8'))  # 确保发送的数据带有结束符
                self.data_sent.emit(data)  # 发射信号
            except Exception as e:
                self.error_occurred.emit(str(e))

class SerialProtocol(asyncio.Protocol):
    def __init__(self, worker):
        super().__init__()
        self.worker = worker

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        try:
            lines = data.split(b'\r\n')
            for line in lines:
                if line:  # 过滤掉空行
                    message = line.decode('utf-8').strip()
                    self.worker.received_data.emit(message)
        except Exception as e:
            self.worker.error_occurred.emit(str(e))

    def connection_lost(self, exc):
        self.worker.serial_connection_lost.emit()
        self.transport = None
