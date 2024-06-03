from PyQt5.QtCore import QObject, QTimer, Qt
from PyQt5.QtWidgets import QHBoxLayout
from config.handel_config import instruction_config
from functions.send_singer import SignalEmitter
from coustom_ui.fixedlabel import FixedLabel
from coustom_ui.lineEdit import NewLineEdit


class InstructionConfig(QObject):
    def __init__(self, file_path_line, tool, frame_2, serial_config):
        super().__init__()
        self.tool = tool
        self.file_path_line = file_path_line
        self.serial_config = serial_config
        self.frame_2 = frame_2
        self.commands = []  # 用于存储命令
        self.current_index = 0  # 当前执行命令的索引
        self.timer = QTimer(self)  # 用于执行命令的定时器
        self.timer.timeout.connect(self.execute_command)  # 连接到执行命令的方法

    def handle_file_path(self):
        """处理获取到的路径"""
        path = self.file_path_line.text()
        if '/' in path:
            csv = path.split('/')
        elif '//' in path:
            csv = path.split("//")
        else:
            csv = path.split("\\")
        self.csv_message(path, csv)

    def default_command(self):
        try:
            self.commands = self.tool.read_csv_by_command(instruction_config)
            self.create_widget(self.commands)
        except Exception as e:
            print(f"Error reading commands: {e}")
            return None

    def start_sequence(self):
        """开始依次执行命令"""
        if not self.serial_config.is_port_open():
            SignalEmitter.error_signal("串口未打开，无法发送指令")
            return
        if self.commands:
            self.current_index = 0
            self.update_all_labels_to_waiting()
            self.execute_command()  # 开始执行第一个命令

    def update_all_labels_to_waiting(self):
        """将所有 label_send_ 的样式替换为橘黄色背景，文本修改为 '等待发送'"""
        for index in range(len(self.commands)):
            command_text = f"label_send_{index + 1}"
            label_send = self.frame_2.findChild(FixedLabel, command_text)
            if label_send:
                label_send.set_custom_style("background-color: orange; color: rgb(255, 255, 255);")
                label_send.setText("待执行")
                label_send.setAlignment(Qt.AlignCenter)

    def execute_command(self):
        """执行当前命令"""
        if self.current_index < len(self.commands):
            command = self.commands[self.current_index]
            command_text = command[0]   # 获取当前命令文本
            interval = int(command[1])  # 获取当前命令的延时时间
            self.serial_config.send_message(command_text)
            self.update_command(self.current_index)  # 更新当前命令
            self.current_index += 1
            if self.current_index < len(self.commands):
                self.timer.start(interval)  # 设置下一个命令的定时器
            else:
                self.timer.stop()  # 如果是最后一个命令，停止定时器
        else:
            self.timer.stop()  # 所有命令执行完后，停止定时器

    def stop_sequence(self):
        self.timer.stop()

    def update_command(self, index):
        """更新指令"""
        command_text = f"label_send_{index + 1}"
        label_send = self.frame_2.findChild(FixedLabel, command_text)
        if label_send:
            label_send.setText("已执行")
            label_send.set_custom_style("background-color: rgb(149,212,117); text-align: center; color: rgb(255, 255, 255);")

    def csv_message(self, path, text):
        if ".csv" not in text[-1]:
            SignalEmitter.warning_signal("非csv文件，无法加载")
        else:
            self.commands = self.tool.read_csv_by_command(path)

    def create_widget(self, commands):
        """添加指令"""
        if commands:
            for index, command in enumerate(commands):
                row_layout = QHBoxLayout()
                line_edit = NewLineEdit(command[0])
                line_edit.setObjectName(f"line_edit_{index + 1}")
                line_edit.setFixedHeight(30)

                label_timer = NewLineEdit(command[1])
                label_timer.setObjectName(f"label_timer_{index + 1}")
                label_timer.setFixedSize(80, 30)

                label_send = FixedLabel("待执行")
                label_send.setObjectName(f"label_send_{index + 1}")

                row_layout.addWidget(line_edit)
                row_layout.addWidget(label_timer)
                row_layout.addWidget(label_send)
                self.frame_2.layout().addLayout(row_layout)
