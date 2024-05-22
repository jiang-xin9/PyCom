from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout
from config.read_ini import ConfigReader
from config.handel_config import sys_, command_config


class CreateFastBtn:
    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def create_button_clicked_closure(self, line_edit):
        """实现点击"""

        def button_clicked():
            line_edit_text = line_edit.text()
            self._update_adb_command(line_edit_text)
            self._execute_command(line_edit_text)

        return button_clicked

    def _update_adb_command(self, text):
        """更新写入指令"""

    def _execute_command(self, text):
        """更新接收数据"""

    def create_btn(self):
        """添加指令"""
        # 初始化一个垂直布局，并将其添加到 quick_frame 中
        self.vertical_layout = QVBoxLayout(self.ui.quick_frame)
        self.ui.quick_frame.setLayout(self.vertical_layout)
        try:
            commands = ConfigReader(command_config).get_value()  # 打包时用到路径
        except:
            path = sys_ + "\\" + "fast_btn_config.ini"
            commands = ConfigReader(path).get_value()  # 打包时用到路径

        for command in commands:
            # 为每个命令创建一个水平布局
            row_layout = QHBoxLayout()
            line_edit = QLineEdit(command)
            button1 = QPushButton("发送1")

            line_edit.setFixedHeight(25)  # 设置行高
            button1.setFixedSize(40, 25)  # 设置按钮的长高

            # 注意lambda函数中传递line_edit作为参数来避免late binding问题
            button1.clicked.connect(lambda checked, le=line_edit: self.create_button_clicked_closure(le)())

            row_layout.setContentsMargins(0, 0, 0, 0)  # 设置水平布局的边距
            row_layout.setSpacing(3)  # 设置控件间距
            # 将控件添加到水平布局
            row_layout.addWidget(line_edit)
            row_layout.addWidget(button1)
            self.vertical_layout.setContentsMargins(3, 3, 3, 3)
            self.vertical_layout.setSpacing(3)  # 设置控件间距
            # 将水平布局添加到垂直布局中
            self.vertical_layout.addLayout(row_layout)  # 使用垂直布局
