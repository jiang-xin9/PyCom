from functions.serial_thread import SerialThread
from functions.create_serial_func import CreateSerialUi


class SerialConfig:
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.ui.serial_config_btn.clicked.connect(self.show_serial_config)
        self.ui.send_btn.clicked.connect(self.send_message)

        self.serial_thread = SerialThread()
        self.serial_thread.worker.received_data.connect(self.display_message)
        self.serial_thread.worker.data_sent.connect(self.display_sent_message)
        self.serial_thread.worker.serial_connection_made.connect(self.on_connection_made)
        self.serial_thread.worker.serial_connection_lost.connect(self.on_connection_lost)
        self.serial_thread.worker.error_occurred.connect(self.display_error)

        self.serial_ui = CreateSerialUi(self.serial_thread)
        self.serial_ui.port_configured.connect(self.update_port_config)

    def show_serial_config(self):
        self.serial_ui.show()
        self.serial_thread.start()

    def update_port_config(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate

    def send_message(self):
        message = self.ui.command_line.text()
        self.serial_thread.send_data(message)

    def display_message(self, message):
        self.ui.receive_textEdit.append(f"收←: {message}")

    def display_sent_message(self, message):
        self.ui.receive_textEdit.append(f"发→: {message}\n")

    def on_connection_made(self):
        self.ui.receive_textEdit.append(f"Opened port {self.port} at {self.baudrate} baud")

    def on_connection_lost(self):
        self.ui.receive_textEdit.append("Closed port")

    def display_error(self, error):
        self.ui.receive_textEdit.append(str(error))

    def closeEvent(self, event):
        self.serial_thread.stop()
        self.serial_thread.wait()
        event.accept()
