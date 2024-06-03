from PyQt5.QtCore import QObject, QDateTime, QTimer, QPoint, pyqtSignal
from PyQt5.QtGui import QTextCursor
from functions.create_serial_ui import CreateSerialUi
from functions.serial_thread import SerialThread
from functions.log_func import Logger
from config.handel_config import log_folder_path


class SerialConfig(QObject):
    def __init__(self, serial_config_btn, send_btn, command_line,
                 serial_com, receive_text_edit, show_message_box,
                 check_time, check_enter, check_loop_send,
                 line_delayed, check_save_log, line_log):
        super().__init__()
        self.setup_ui_components(serial_config_btn, send_btn, command_line,
                                 serial_com, receive_text_edit, show_message_box,
                                 check_time, check_enter, check_loop_send,
                                 line_delayed, check_save_log, line_log)

        self.setup_signals()
        self.setup_serial_thread()

        self.loop_timer = QTimer(self)
        self.logger = None
        self.log_enabled = False
        self.loop_send_connected = False
        self.serial_ui = None
        self.port_opened = False

    def setup_ui_components(self, serial_config_btn, send_btn, command_line,
                            serial_com, receive_text_edit, show_message_box,
                            check_time, check_enter, check_loop_send,
                            line_delayed, check_save_log, line_log):
        """初始化UI组件"""
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

    def setup_signals(self):
        """绑定信号与槽"""
        self.serial_config_btn.clicked.connect(self.show_serial_config)
        self.send_btn.clicked.connect(self.send_message)
        self.check_loop_send.toggled_signal.connect(self.toggle_loop_send)
        self.check_save_log.toggled_signal.connect(self.toggle_save_log)

    def setup_serial_thread(self):
        """设置串口线程"""
        self.serial_thread = SerialThread(self.check_enter)
        self.serial_thread.worker.received_data.connect(self.display_message)
        self.serial_thread.worker.data_sent.connect(self.display_sent_message)
        self.serial_thread.worker.serial_connection_made.connect(self.on_connection_made)
        self.serial_thread.worker.serial_connection_lost.connect(self.on_connection_lost)
        self.serial_thread.worker.error_occurred.connect(self.display_error)
        self.serial_thread.start()

    def show_serial_config(self):
        """显示串口配置界面"""
        if self.serial_ui is None:
            self.serial_ui = CreateSerialUi(self.serial_thread)
            self.serial_ui.port_configured.connect(self.update_port_config)

        if not self.serial_ui.isVisible():
            self.serial_ui.show()
        else:
            self.serial_ui.raise_()
            self.serial_ui.activateWindow()

    def update_port_config(self, port, baudrate):
        """更新串口配置"""
        self.port = port
        self.baudrate = baudrate

    def send_message(self, command=None):
        """发送消息"""
        if not command:
            message = self.command_line.text()
            self.serial_thread.send_data(message)
        else:
            self.serial_thread.send_data(command)

    def display_message(self, message):
        """显示接收到的消息"""
        timestamp = self.get_timestamp() if self.check_time.toggled else ""
        formatted_message = f"[{timestamp}] 收←: {message}" if timestamp else f"收<: {message}"
        self.append_to_receive_text_edit(formatted_message)
        self.log_message(formatted_message)

    def display_sent_message(self, message):
        """显示已发送的消息"""
        timestamp = self.get_timestamp() if self.check_time.toggled else ""
        formatted_message = f"[{timestamp}] 发→: {message}" if timestamp else f"发>: {message}"
        self.append_to_receive_text_edit(formatted_message)
        self.limit_text_edit_size()
        self.log_message(formatted_message)

    def on_connection_made(self):
        """串口连接建立时的处理"""
        self.port_opened = True  # 标记串口已打开
        timestamp = self.get_timestamp() if self.check_time.toggled else ""
        message = f"[{timestamp}] Opened port {self.port} at {self.baudrate} baud\n" \
            if timestamp else f"Opened port {self.port} at {self.baudrate} baud\n"
        self.append_to_receive_text_edit(message)
        self.show_message_box(f"{self.port} Success", "success")
        if self.port:
            self.serial_com.setText(self.port)

    def on_connection_lost(self):
        """串口连接丢失时的处理"""
        self.port_opened = False  # 标记串口已关闭
        timestamp = self.get_timestamp() if self.check_time.toggled else ""
        message = f"[{timestamp}] Closed port" if timestamp else "Closed port"
        self.append_to_receive_text_edit(message)
        self.show_message_box(f"{self.port} Disconnect", "success")
        self.stop_saving_log()

    def display_error(self, error):
        """显示错误消息"""
        timestamp = self.get_timestamp() if self.check_time.toggled else ""
        error_message = f"[{timestamp}] {error}" if timestamp else error
        self.append_to_receive_text_edit(error_message)
        self.show_message_box(f"{self.port} Disconnect", "error")

    def toggle_loop_send(self, toggled):
        """切换循环发送"""
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
        """切换日志存储"""
        self.start_saving_log() if toggled else self.stop_saving_log()

    def stop_saving_log(self):
        """停止日志存储"""
        if self.logger:
            self.logger.stop_logging()
            self.logger = None

    def start_saving_log(self):
        """开始日志存储"""
        max_size_kb = self.line_log.text()
        self.logger = Logger(log_folder_path, max_size_kb) if max_size_kb else Logger(log_folder_path)
        self.logger.start()

    def closeEvent(self, event):
        """窗口关闭事件"""
        self.serial_thread.stop()
        self.serial_thread.wait()
        self.stop_saving_log()
        event.accept()

    def limit_text_edit_size(self):
        """限制接收文本编辑框的大小"""
        max_block_count = 2860
        document = self.receive_text_edit.document()
        if document.blockCount() > max_block_count:
            cursor = self.receive_text_edit.textCursor()
            cursor.movePosition(QTextCursor.Start)
            for _ in range(document.blockCount() - max_block_count):
                cursor.select(QTextCursor.BlockUnderCursor)
                cursor.removeSelectedText()
                cursor.deleteChar()
                if document.blockCount() <= max_block_count:
                    break

    def get_timestamp(self):
        """获取当前时间戳"""
        return QDateTime.currentDateTime().toString("HH:mm:ss.zzz")

    def append_to_receive_text_edit(self, message):
        """将消息追加到接收文本编辑框"""
        self.receive_text_edit.append(f"{message}")

    def log_message(self, message):
        """记录消息到日志"""
        if self.logger:
            self.logger.log_signal.emit(message)

    def is_port_open(self):
        """检查串口是否已打开"""
        return self.port_opened
