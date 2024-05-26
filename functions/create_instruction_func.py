from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QHBoxLayout, QWidget
from functions.tool import Tool
from config.handel_config import sys_, instruction_config
from coustom_ui.fixedlabel import FixedLabel
from coustom_ui.lineEdit import NewLineEdit
from ui.instruction import Instruction_Form
from coustom_ui.message_prompt import CustomMessageBox


class CreateInstructionUi(QWidget, Instruction_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tool = Tool()
        self.init_singers()

        # 初始化定时器
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_labels_background)
        # self.timer.start(500)  # 每500毫秒触发一次

    def init_singers(self):
        """初始化信号槽"""
        self.file_path_line.setCursorPosition(0)  # 设置光标位置为最左边
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.update_style)
        # 获取文件路径
        self.get_file_path.clicked.connect(lambda line:self.tool.get_file_path(self.file_path_line))
        self.file_path_line.textChanged.connect(self.handle_file_path)

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

    def csv_message(self,path, text):
        if ".csv" not in text[-1]:
            CustomMessageBox.show_box("非csv文件，无法加载", "warning", self)
        else:
            self.start_btn.setEnabled(True)
            self.create_widget(self.tool.read_csv_by_command(path))

    def update_style(self):
        # 67C23A
        pass

    def create_instruction_closure(self, line_edit):
        """添加实现点击"""

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

    def create_widget(self, commands):
        """添加指令"""
        if commands:
            for command in commands:
                # 为每个命令创建一个水平布局
                row_layout = QHBoxLayout()
                line_edit = NewLineEdit(command[0])
                line_edit.setFixedHeight(30)
                label_timer = NewLineEdit(command[1])
                label_timer.setFixedSize(80, 30)
                label_send = FixedLabel("待发送")
                # label_timer.setFixedSize(40, 30)

                # 将控件添加到水平布局
                row_layout.addWidget(line_edit)
                row_layout.addWidget(label_timer)
                row_layout.addWidget(label_send)

                # 将水平布局添加到已存在的 frame 的垂直布局中
                self.frame_2.layout().addLayout(row_layout)  # 使用 layout() 方法获取现有布局并添加内容
