from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QLabel, QWidget
from functions.tool import Tool
from config.handel_config import sys_, instruction_config
from coustom_ui.fixedlabel import FixedLabel
from coustom_ui.lineEdit import NewLineEdit
from ui.instruction import Instruction_Form


class CreateInstruction(QWidget, Instruction_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tool = Tool()

    def create_instruction_closure(self, line_edit):
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

    def create_widget(self):
        """添加指令"""
        try:
            self.commands = self.tool.read_csv_by_command(instruction_config)
        except Exception:
            path = sys_ + "\\" + "instruction_config.csv"
            self.commands = self.tool.read_csv_by_command(path)  # 打包时用到路径

        for command in self.commands:
            # 为每个命令创建一个水平布局
            row_layout = QHBoxLayout()
            line_edit = NewLineEdit(command[0])
            line_edit.setFixedHeight(30)
            label_timer = NewLineEdit(command[1])
            label_timer.setFixedSize(80, 30)
            label_send = FixedLabel("待发送")
            # label_timer.setFixedSize(40, 30)

            # 注意lambda函数中传递line_edit作为参数来避免late binding问题
            # label.clicked.connect(lambda checked, le=line_edit: self.create_instruction_closure(le)())

            # 将控件添加到水平布局
            row_layout.addWidget(line_edit)
            row_layout.addWidget(label_timer)
            row_layout.addWidget(label_send)

            # 将水平布局添加到已存在的 frame 的垂直布局中
            self.frame_2.layout().addLayout(row_layout)  # 使用 layout() 方法获取现有布局并添加内容
