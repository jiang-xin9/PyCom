import asyncio
import serial_asyncio
from PyQt5.QtCore import QObject, pyqtSignal

class SerialWorker(QObject):
    received_data = pyqtSignal(str)
    data_sent = pyqtSignal(str)
    serial_connection_made = pyqtSignal()
    serial_connection_lost = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, check_enter, check_hex_receive, check_hex_send):
        super().__init__()
        self.transport = None
        self.check_enter = check_enter
        self.check_hex_receive = check_hex_receive
        self.check_hex_send = check_hex_send

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
                if self.check_hex_send.toggled:
                    message = bytes.fromhex(data)
                else:
                    message = f"{data}\r\n".encode('utf-8') if self.check_enter.toggled else data.encode('utf-8')
                self.transport.write(message)
                self.data_sent.emit(data)
            except Exception as e:
                self.error_occurred.emit(str(e))

class SerialProtocol(asyncio.Protocol):
    def __init__(self, worker):
        super().__init__()
        self.worker = worker
        self.buffer = bytearray()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.buffer.extend(data)
        if self.worker.check_hex_receive.toggled:
            message = self.buffer.hex()
            self.worker.received_data.emit(message)
            self.buffer.clear()
        else:
            while True:
                if b'\r\n' not in self.buffer:
                    break
                line, self.buffer = self.buffer.split(b'\r\n', 1)
                if line:
                    message = line.decode('utf-8').strip()
                    self.worker.received_data.emit(message)

    def connection_lost(self, exc):
        self.worker.serial_connection_lost.emit()
        self.transport = None
