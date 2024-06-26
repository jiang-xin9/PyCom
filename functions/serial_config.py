import asyncio, re
from PyQt5.QtCore import QObject, QDateTime, QTimer
from PyQt5.QtGui import QTextCursor
from qasync import asyncSlot
from functions.create_serial_ui import CreateSerialUi
from functions.log_func import Logger
from config.handel_config import log_folder_path
from functions.serial_work import SerialWorker
from functions.create_parameter_filter_ui import CreateParameterFilterUi


class SerialConfig(QObject):
    def __init__(self, serial_config_btn, send_btn, command_line, serial_com, receive_text_edit, show_message_box,
                 check_time, check_enter, check_loop_send, line_delayed, check_save_log, line_log, check_hex_receive,
                 check_hex_send, parameter_filter_btn):
        super().__init__()
        self.setup_ui_components(serial_config_btn, send_btn, command_line, serial_com, receive_text_edit,
                                 show_message_box, check_time, check_enter, check_loop_send, line_delayed,
                                 check_save_log, line_log, check_hex_receive, check_hex_send, parameter_filter_btn)

        self.setup_signals()
        self.loop_timer = QTimer(self)
        self.logger = None
        self.log_enabled = False
        self.loop_send_connected = False
        self.serial_ui = None
        self.filter_condition = None
        self.capture_condition = None
        self.filter_ui = None

    def setup_ui_components(self, serial_config_btn, send_btn, command_line, serial_com, receive_text_edit,
                            show_message_box, check_time, check_enter, check_loop_send, line_delayed, check_save_log,
                            line_log, check_hex_receive, check_hex_send, parameter_filter_btn):
        self.serial_config_btn = serial_config_btn
        self.send_btn = send_btn
        self.command_line = command_line
        self.serial_com = serial_com
        self.receive_text_edit = receive_text_edit
        self.show_message_box = show_message_box
        self.check_time = check_time
        self.check_enter = check_enter
        self.check_loop_send = check_loop_send
        self.line_delayed = line_delayed
        self.check_save_log = check_save_log
        self.line_log = line_log
        self.check_hex_receive = check_hex_receive
        self.check_hex_send = check_hex_send
        self.parameter_filter_btn = parameter_filter_btn

    def setup_signals(self):
        self.serial_worker = SerialWorker(self.check_enter, self.check_hex_receive, self.check_hex_send)
        self.serial_config_btn.clicked.connect(self.show_serial_config)
        self.send_btn.clicked.connect(self.send_message)
        self.check_loop_send.toggled_signal.connect(self.toggle_loop_send)
        self.check_save_log.toggled_signal.connect(self.toggle_save_log)

        self.serial_worker.received_data.connect(self.display_message)
        self.serial_worker.data_sent.connect(self.display_sent_message)
        self.serial_worker.serial_connection_made.connect(self.on_connection_made)
        self.serial_worker.serial_connection_lost.connect(self.on_connection_lost)
        self.serial_worker.error_occurred.connect(self.display_error)

        self.parameter_filter_btn.clicked.connect(self.show_parameter_filter_config)

    def show_parameter_filter_config(self):
        if self.filter_ui is None:
            self.filter_ui = CreateParameterFilterUi(self.apply_filter, self.cancel_filter,
                                                     self.apply_capture, self.cancel_capture)
        self.filter_ui.show()

    def cancel_filter(self):
        self.filter_condition = None

    def apply_filter(self, filter_condition):
        self.filter_condition = filter_condition

    def apply_capture(self, capture_condition):
        self.capture_condition = capture_condition

    def cancel_capture(self):
        self.capture_condition = None

    def show_serial_config(self):
        if self.serial_ui is None:
            self.serial_ui = CreateSerialUi(self.serial_worker)
            self.serial_ui.port_configured.connect(self.update_port_config)
            self.serial_ui.close_requested.connect(self.close_serial_port)
        self.serial_ui.show()

    def update_port_config(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate

    @asyncSlot()
    async def send_message(self, command=None):
        if not command:
            message = self.command_line.text()
            self.serial_worker.send_data(message)
        else:
            self.serial_worker.send_data(command)

    def display_message(self, message):
        if self.filter_message(message):
            timestamp = self.get_timestamp() if self.check_time.toggled else ""
            formatted_message = f"[{timestamp}] 收←: {message}" if timestamp else f"收<: {message}"
            self.append_to_receive_text_edit(formatted_message)
            self.log_message(formatted_message)

    def filter_message(self, message):
        if not self.filter_condition and not self.capture_condition:
            return True

        if self.filter_condition:
            if isinstance(self.filter_condition, tuple) and len(self.filter_condition) == 2:
                re_text_1, re_text_2 = self.filter_condition
                pattern = re.compile(re.escape(re_text_1) + r".*?" + re.escape(re_text_2))
                if not pattern.search(message):
                    return False

        if self.capture_condition:
            if self.filter_ui.check_Inversion.toggled:
                if self.capture_condition in message:
                    return False
            else:
                if self.capture_condition not in message:
                    return False

        return True

    def display_sent_message(self, message):
        timestamp = self.get_timestamp() if self.check_time.toggled else ""
        formatted_message = f"[{timestamp}] 发→: {message}" if timestamp else f"发>: {message}"
        self.append_to_receive_text_edit(formatted_message)
        self.log_message(formatted_message)

    def on_connection_made(self):
        timestamp = self.get_timestamp() if self.check_time.toggled else ""
        message = f"[{timestamp}] Opened port {self.port} at {self.baudrate} baud\n" \
            if timestamp else f"Opened port {self.port} at {self.baudrate} baud\n"
        self.append_to_receive_text_edit(message)
        self.show_message_box(f"{self.port} Success", "success")
        if self.port:
            self.serial_com.setText(self.port)

    def on_connection_lost(self):
        timestamp = self.get_timestamp() if self.check_time.toggled else ""
        message = f"[{timestamp}] Closed port" if timestamp else "Closed port"
        self.append_to_receive_text_edit(message)
        self.show_message_box(f"{self.port} Disconnect", "success", self.serial_ui)
        self.stop_saving_log()

    def display_error(self, error):
        timestamp = self.get_timestamp() if self.check_time.toggled else ""
        error_message = f"[{timestamp}] {error}" if timestamp else error
        self.append_to_receive_text_edit(error_message)
        self.show_message_box(f"{self.port} Disconnect", "error", self.serial_ui)

    def toggle_loop_send(self, toggled):
        self.start_loop_send() if toggled else self.stop_loop_send()

    def start_loop_send(self):
        try:
            interval = float(self.line_delayed.text()) * 1000
        except ValueError:
            self.show_message_box("请先填写延迟时间", "error")
            return

        if self.loop_send_connected:
            self.loop_timer.timeout.disconnect(self.send_message)
        self.loop_timer.timeout.connect(self.send_message)
        self.loop_send_connected = True
        self.loop_timer.start(int(interval))

    def stop_loop_send(self):
        self.loop_timer.stop()
        if self.loop_send_connected:
            self.loop_timer.timeout.disconnect(self.send_message)
            self.loop_send_connected = False

    def toggle_save_log(self, toggled):
        self.start_saving_log() if toggled else self.stop_saving_log()

    def stop_saving_log(self):
        if self.logger:
            self.logger.stop_logging()
            self.logger = None

    def start_saving_log(self):
        max_size_kb = self.line_log.text()
        self.logger = Logger(log_folder_path, max_size_kb) if max_size_kb else Logger(log_folder_path)
        self.logger.start()

    def close_serial_port(self):
        asyncio.create_task(self.serial_worker.close_serial_port())

    def closeEvent(self, event):
        asyncio.create_task(self.serial_worker.close_serial_port())
        self.stop_saving_log()
        event.accept()

    def limit_text_edit_size(self):
        max_block_count = 512
        document = self.receive_text_edit.document()

        if document.blockCount() > max_block_count:
            cursor = QTextCursor(document)
            cursor.beginEditBlock()

            while document.blockCount() > max_block_count:
                cursor.setPosition(document.findBlockByNumber(0).position())
                cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
                cursor.removeSelectedText()
                cursor.deleteChar()

            cursor.endEditBlock()

    def get_timestamp(self):
        return QDateTime.currentDateTime().toString("HH:mm:ss.zzz")

    def append_to_receive_text_edit(self, message):
        self.limit_text_edit_size()
        self.receive_text_edit.append(f"{message}")

    def log_message(self, message):
        if self.logger:
            self.logger.log_signal.emit(message)
