import asyncio
from PyQt5.QtCore import QThread
from functions.serial_work import SerialWorker


class SerialThread(QThread):
    def __init__(self):
        super().__init__()
        self.worker = SerialWorker()
        self.loop = None

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def stop(self):
        if self.loop is not None:
            self.loop.call_soon_threadsafe(self.loop.stop)

    def open_serial_port(self, port, baudrate):
        if self.loop is not None:
            asyncio.run_coroutine_threadsafe(self.worker.open_serial_port(port, baudrate), self.loop)

    def close_serial_port(self):
        if self.loop is not None:
            self.loop.call_soon_threadsafe(self.worker.close_serial_port)

    def send_data(self, data):
        if self.loop is not None:
            self.loop.call_soon_threadsafe(self.worker.send_data, data)
