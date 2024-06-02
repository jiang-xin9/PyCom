# coding:utf-8
# author: 清安安
# CSDN: 清安无别事
# file_time: 2024/6/2 11:18
from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtWidgets import QHBoxLayout

from config.handel_config import instruction_config
from coustom_ui.message_prompt import CustomMessageBox
from coustom_ui.fixedlabel import FixedLabel
from coustom_ui.lineEdit import NewLineEdit


class InstructionConfig(QObject):
    def __init__(self, file_path_line, tool,frame_2):
        super().__init__()
        self.tool = tool
        self.file_path_line = file_path_line
        self.frame_2 = frame_2

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
            commands = self.tool.read_csv_by_command(instruction_config)  # 打包时用到路径
            self.create_widget(commands)
        except Exception as e:
            print(f"Error reading commands: {e}")
            return None

    def csv_message(self, path, text):
        if ".csv" not in text[-1]:
            CustomMessageBox.show_box("非csv文件，无法加载", "warning", self)
        else:
            self.create_widget(self.tool.read_csv_by_command(path))

    def create_widget(self, commands):
        """添加指令"""
        if commands:
            for command in commands:
                row_layout = QHBoxLayout()
                line_edit = NewLineEdit(command[0])
                line_edit.setFixedHeight(30)
                label_timer = NewLineEdit(command[1])
                label_timer.setFixedSize(80, 30)
                label_send = FixedLabel("待发送")

                row_layout.addWidget(line_edit)
                row_layout.addWidget(label_timer)
                row_layout.addWidget(label_send)
                self.frame_2.layout().addLayout(row_layout)
