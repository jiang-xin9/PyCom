import asyncio, re
from PyQt5.QtCore import QObject, QDateTime, QTimer
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor
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
        """显示参数过滤配置界面"""
        if self.filter_ui is None:
            self.filter_ui = CreateParameterFilterUi(self.apply_filter, self.cancel_filter,
                                                     self.apply_capture, self.cancel_capture)
        self.filter_ui.show()

    def cancel_filter(self):
        """取消过滤条件"""
        self.filter_condition = None

    def apply_filter(self, filter_condition):
        """应用过滤条件"""
        self.filter_condition = filter_condition

    def apply_capture(self, capture_condition):
        """应用捕获条件"""
        self.capture_condition = capture_condition

    def cancel_capture(self):
        """取消捕获条件"""
        self.capture_condition = None

    def show_serial_config(self):
        """显示串口配置界面"""
        if self.serial_ui is None:
            self.serial_ui = CreateSerialUi(self.serial_worker)
            self.serial_ui.port_configured.connect(self.update_port_config)
            self.serial_ui.close_requested.connect(self.close_serial_port)
        self.serial_ui.show()

    def update_port_config(self, port, baudrate):
        """更新串口配置"""
        self.port = port
        self.baudrate = baudrate

    @asyncSlot()
    async def send_message(self, command=None):
        """发送消息到串口"""
        if not command:
            message = self.command_line.text()
            self.serial_worker.send_data(message)
        else:
            self.serial_worker.send_data(command)

    def display_message(self, message):
        """显示接收到的消息"""
        filtered_message, highlighted = self._filter_message(message)
        if filtered_message:
            timestamp = self.get_timestamp() if self.check_time.toggled else ""
            formatted_message = f"[{timestamp}] 收←: {filtered_message}" if timestamp else f"收<: {filtered_message}"
            self._append_to_receive_text_edit(formatted_message, highlighted)
            self.log_message(formatted_message)

    def _filter_message(self, message):
        """根据过滤和捕获条件过滤消息并高亮显示特定字符"""
        if not self.filter_condition and not self.capture_condition:
            return message, False

        if self.filter_condition and not self._check_filter_condition(message):
            return None, False

        highlighted = False
        if self.capture_condition:
            message, highlighted = self._apply_highlighting(message, self.capture_condition,
                                                            invert=self.filter_ui.check_Inversion.toggled if self.filter_ui else False)

        if self.filter_condition:
            message, highlighted = self._apply_highlighting(message, self.filter_condition, is_filter=True)

        return message, highlighted

    def _check_filter_condition(self, message):
        """检查消息是否符合过滤条件"""
        if isinstance(self.filter_condition, tuple) and len(self.filter_condition) == 2:
            re_text_1, re_text_2 = self.filter_condition
            pattern = re.compile(re.escape(re_text_1) + r".*?" + re.escape(re_text_2))
            return bool(pattern.search(message))
        return True

    def _apply_highlighting(self, message, condition, is_filter=False, invert=False):
        """应用过滤条件、捕获条件并高亮显示特定字符"""
        highlighted_message = ""
        highlighted = False
        start = 0

        if isinstance(condition, tuple) and len(condition) == 2:
            re_text_1, re_text_2 = condition
            pattern = re.compile(re.escape(re_text_1) + r"(.*?)" + re.escape(re_text_2))
        else:
            pattern = re.compile(re.escape(condition))

        for match in pattern.finditer(message):
            highlighted_message += message[start:match.start()]
            highlighted_message += f"<highlight>{match.group()}</highlight>"
            start = match.end()
            highlighted = True

        highlighted_message += message[start:]

        if invert:
            return self._apply_inversion_highlighting(message, condition), True

        return highlighted_message, highlighted

    def _apply_inversion_highlighting(self, message, condition):
        """应用反转捕获条件并高亮显示非捕获部分"""
        inverted_highlight_message = ""
        start = 0
        for match in re.finditer(re.escape(condition), message):
            inverted_highlight_message += f"<highlight>{message[start:match.start()]}</highlight>"
            inverted_highlight_message += match.group()
            start = match.end()
        inverted_highlight_message += f"<highlight>{message[start:]}</highlight>"
        return inverted_highlight_message

    def display_sent_message(self, message):
        """显示发送的消息"""
        timestamp = self.get_timestamp() if self.check_time.toggled else ""
        formatted_message = f"[{timestamp}] 发→: {message}" if timestamp else f"发>: {message}"
        self._append_to_receive_text_edit(formatted_message)
        self.log_message(formatted_message)

    def on_connection_made(self):
        """串口连接建立时的处理"""
        self.show_message_box(f"{self.port} Success", "success")
        if self.port:
            self.serial_com.setText(self.port)

    def on_connection_lost(self):
        """串口关闭连接"""
        self.show_message_box(f"{self.port} Disconnect", "success", self.serial_ui)
        self.stop_saving_log()

    def display_error(self, error):
        """显示错误信息"""
        self.show_message_box(f"{self.port} Disconnect", "error", self.serial_ui)

    def toggle_loop_send(self, toggled):
        """切换循环发送功能"""
        self.start_loop_send() if toggled else self.stop_loop_send()

    def start_loop_send(self):
        """开始循环发送"""
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
        """停止循环发送"""
        self.loop_timer.stop()
        if self.loop_send_connected:
            self.loop_timer.timeout.disconnect(self.send_message)
            self.loop_send_connected = False

    def toggle_save_log(self, toggled):
        """切换保存日志功能"""
        self.start_saving_log() if toggled else self.stop_saving_log()

    def stop_saving_log(self):
        """停止保存日志"""
        if self.logger:
            self.logger.stop_logging()
            self.logger = None

    def start_saving_log(self):
        """开始保存日志"""
        max_size_kb = self.line_log.text()
        self.logger = Logger(log_folder_path, max_size_kb) if max_size_kb else Logger(log_folder_path)
        self.logger.start()

    def close_serial_port(self):
        """关闭串口端口"""
        asyncio.create_task(self.serial_worker.close_serial_port())

    def closeEvent(self, event):
        """处理窗口关闭事件"""
        asyncio.create_task(self.serial_worker.close_serial_port())
        self.stop_saving_log()
        event.accept()

    def _limit_text_edit_size(self):
        """限制接收文本编辑框的大小"""
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
        """获取当前时间戳"""
        return QDateTime.currentDateTime().toString("HH:mm:ss.zzz")

    def _append_to_receive_text_edit(self, message, highlighted=False):
        """写入ui文本"""
        if highlighted:
            self._append_highlighted_text(message)
        else:
            self._append_plain_text(message)

    def _append_plain_text(self, message):
        """显示数据并保持滚动条处于最下面"""
        self._limit_text_edit_size()
        cursor = self.receive_text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(message + "\n")
        self.receive_text_edit.setTextCursor(cursor)

    def _append_highlighted_text(self, message):
        """显示指定字符的高光颜色"""
        self._limit_text_edit_size()
        cursor = self.receive_text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)

        default_format = QTextCharFormat()
        red_format = QTextCharFormat()
        red_format.setForeground(QColor('red'))

        cursor.beginEditBlock()
        start = 0
        pattern = re.compile(r'<highlight>(.*?)</highlight>')
        for match in pattern.finditer(message):
            cursor.insertText(message[start:match.start()], default_format)
            cursor.insertText(match.group(1), red_format)
            start = match.end()
        cursor.insertText(message[start:], default_format)
        cursor.insertText("\n")
        cursor.endEditBlock()

        self.receive_text_edit.setTextCursor(cursor)

    def log_message(self, message):
        """记录消息日志"""
        if self.logger:
            self.logger.log_signal.emit(message)
