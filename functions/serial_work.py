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
        self.protocol = None  # 保存 SerialProtocol 的引用
        self.check_enter = check_enter
        self.check_hex_receive = check_hex_receive
        self.check_hex_send = check_hex_send
        self.port_opened = False
        self.closing = False
        self.expected_length = 16  # 默认值，可以通过UI进行修改

    async def open_serial_port(self, port, baudrate):
        if self.port_opened:
            await self.close_serial_port()
        try:
            loop = asyncio.get_event_loop()
            self.transport, self.protocol = await serial_asyncio.create_serial_connection(
                loop, lambda: SerialProtocol(self, self.expected_length), port, baudrate)
            self.port_opened = True
            self.serial_connection_made.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))

    async def close_serial_port(self):
        if self.transport and self.port_opened and not self.closing:
            self.closing = True
            self.transport.close()
            self.transport = None
            self.protocol = None  # 清空 protocol 引用
            self.port_opened = False
            await asyncio.sleep(0.1)  # 等待资源完全释放
            self.serial_connection_lost.emit()
            self.closing = False

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

    def is_port_open(self):
        return self.port_opened

    def set_expected_length(self, length):
        self.expected_length = length
        if self.protocol:
            self.protocol.set_expected_length(length)


class SerialProtocol(asyncio.Protocol):
    def __init__(self, worker, expected_length):
        super().__init__()
        self.worker = worker
        self.buffer = bytearray()
        self.expected_length = expected_length  # hex字节数

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        try:
            self.buffer.extend(data)
            if self.worker.check_hex_receive.toggled:
                while len(self.buffer) >= self.expected_length:
                    message = ' '.join(f"{byte:02X}" for byte in self.buffer[:self.expected_length])
                    self.worker.received_data.emit(message)
                    self.buffer = self.buffer[self.expected_length:]
            else:
                while b'\r\n' in self.buffer:
                    line, self.buffer = self.buffer.split(b'\r\n', 1)
                    if line:
                        message = line.decode('utf-8').strip()
                        self.worker.received_data.emit(message)
        except UnicodeDecodeError:
            pass

    def connection_lost(self, exc):
        if not self.worker.closing:
            self.worker.serial_connection_lost.emit()
        self.transport = None

    def set_expected_length(self, length):
        self.expected_length = length
