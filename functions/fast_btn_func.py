from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout
from config.read_ini import ConfigReader
from config.handel_config import command_config
from coustom_ui.message_prompt import CustomMessageBox


class CreateFastBtn:
    def __init__(self, quick_frame, save_config_btn, command_line, send_btn):
        self.quick_frame = quick_frame
        self.save_config_btn = save_config_btn
        self.command_line = command_line
        self.send_btn = send_btn

        # 初始化一个垂直布局，并将其添加到 quick_frame 中
        self.vertical_layout = QVBoxLayout(self.quick_frame)
        self.quick_frame.setLayout(self.vertical_layout)
        self.save_config_btn.clicked.connect(self.get_ini_config)

    def create_button_clicked_closure(self, line_edit):
        """实现点击"""

        def button_clicked():
            line_edit_text = line_edit.text()
            self._update_command(line_edit_text)

        return button_clicked

    def _update_command(self, text):
        """更新写入指令"""
        if self.command_line.text():
            self.command_line.clear()
        self.command_line.setText(text)
        self.send_btn.click()  # 点击按钮下发指令

    def create_btn(self):
        """添加指令"""
        try:
            self.commands = ConfigReader(command_config)
        except Exception:
            # path = sys_ + "\\" + "fast_btn_config.ini"
            # self.commands = ConfigReader(path)
            return None
        finally:
            commands = self.commands.get_value()  # 打包时用到路径

        def create_command_row(command):
            row_layout = QHBoxLayout()
            line_edit = QLineEdit(command)
            button1 = QPushButton("发送1")

            line_edit.setFixedHeight(25)
            button1.setFixedSize(40, 25)
            button1.clicked.connect(self.create_button_clicked_closure(line_edit))

            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(3)
            row_layout.addWidget(line_edit)
            row_layout.addWidget(button1)

            return row_layout

        self.vertical_layout.setContentsMargins(3, 3, 3, 3)
        self.vertical_layout.setSpacing(3)

        for command in commands:
            row_layout = create_command_row(command)
            self.vertical_layout.addLayout(row_layout)

    def get_ini_config(self):
        """保存更新后的ini配置信息"""
        line_edits = self.quick_frame.findChildren(QLineEdit)
        texts = [line_edit.text() for line_edit in line_edits]
        self.commands.save_data("Commands", texts)
        CustomMessageBox.show_box("Save Success", "success")
