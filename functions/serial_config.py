import time

from functions.serial_thread import SerialThread
from functions.create_serial_ui import CreateSerialUi
from PyQt5.QtCore import QObject, QDateTime


class SerialConfig(QObject):
    def __init__(self, serial_config_btn, send_btn, command_line, receive_text_edit,
                 show_message_box,
                 check_time,
                 check_enter,
                 check_loop_send,
                 line_delayed):
        super().__init__()
        # 初始化需要的组件
        self.serial_config_btn = serial_config_btn
        self.send_btn = send_btn
        self.command_line = command_line
        self.receive_text_edit = receive_text_edit
        self.show_message_box = show_message_box
        self.check_time = check_time
        self.check_enter = check_enter
        self.check_loop_send = check_loop_send
        # 绑定信号
        self.serial_config_btn.clicked.connect(self.show_serial_config)
        self.send_btn.clicked.connect(self.send_message)
        # 实例化串口线程
        self.serial_thread = SerialThread(self.check_enter)  # 传递 check_enter
        self.serial_thread.worker.received_data.connect(self.display_message)
        self.serial_thread.worker.data_sent.connect(self.display_sent_message)
        self.serial_thread.worker.serial_connection_made.connect(self.on_connection_made)
        self.serial_thread.worker.serial_connection_lost.connect(self.on_connection_lost)
        self.serial_thread.worker.error_occurred.connect(self.display_error)
        # 初始获取串口
        self.serial_ui = CreateSerialUi(self.serial_thread)
        self.serial_ui.port_configured.connect(self.update_port_config)

    def show_serial_config(self):
        """显示串口配置界面启动线程"""
        self.serial_ui.show()
        self.serial_thread.start()

    def update_port_config(self, port, baudrate):
        """更新串口配置"""
        self.port = port
        self.baudrate = baudrate

    def send_message(self):
        """获取发送指令"""
        message = self.command_line.text()
        self.serial_thread.send_data(message)

    def display_message(self, message):
        """写入接收数据"""
        if self.check_time.toggled:
            timestamp = QDateTime.currentDateTime().toString("HH:mm:ss.zzz")
            message = f"[{timestamp}] 收←: {message}"
        else:
            message = f"收←: {message}"
        self.receive_text_edit.append(f"{message}\n")

    def display_sent_message(self, message):
        """写入发送数据"""
        if self.check_time.toggled:
            timestamp = QDateTime.currentDateTime().toString("HH:mm:ss.zzz")
            message = f"[{timestamp}] 发→: {message}"
        else:
            message = f" 发→: {message}"
        self.receive_text_edit.append(f"{message}\n")

    def on_connection_made(self):
        """打开串口"""
        if self.check_time.toggled:
            timestamp = QDateTime.currentDateTime().toString("HH:mm:ss.zzz")
            message = f"[{timestamp}] Opened port {self.port} at {self.baudrate} baud\n"
        else:
            message = f"Opened port {self.port} at {self.baudrate} baud\n"
        self.receive_text_edit.append(message)
        self.show_message_box(f"{self.port} Success", "success")

    def on_connection_lost(self):
        """关闭串口"""
        if self.check_time.toggled:
            timestamp = QDateTime.currentDateTime().toString("HH:mm:ss.zzz")
            message = f"[{timestamp}] Closed port"
        else:
            message = "Closed port"
        self.receive_text_edit.append(message)
        self.show_message_box(f"{self.port} Disconnect", "success")

    def display_error(self, error):
        """显示错误"""
        if self.check_time.toggled:
            timestamp = QDateTime.currentDateTime().toString("HH:mm:ss.zzz")
            error = f"[{timestamp}] {error}"
        self.receive_text_edit.append(error)
        self.show_message_box(f"{self.port} Disconnect", "error")

    def closeEvent(self, event):
        self.serial_thread.stop()
        self.serial_thread.wait()
        event.accept()
