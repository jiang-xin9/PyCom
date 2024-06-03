from PyQt5.QtWidgets import QWidget
from functions.tool import Tool
from ui.instruction import Instruction_Form
from functions.instruction_config import InstructionConfig


class CreateInstructionUi(QWidget, Instruction_Form):
    def __init__(self, serial_config):
        super().__init__()
        self.setupUi(self)
        self.tool = Tool()
        self.init_singers()
        self.instruction_config = InstructionConfig(self.file_path_line, self.tool,
                                                    self.frame_2, self.start_btn,
                                                    serial_config)
        self.default_command()

    def init_singers(self):
        """初始化信号槽"""
        self.file_path_line.setCursorPosition(0)
        self.get_file_path.clicked.connect(self.get_file_path_clicked)
        self.file_path_line.textChanged.connect(self.handle_file_path)
        self.start_btn.clicked.connect(self.start_clock_csv)

    def get_file_path_clicked(self):
        """获取文件路径"""
        self.tool.get_file_path(self.file_path_line)

    def handle_file_path(self):
        """处理文件路径"""
        self.instruction_config.handle_file_path()

    def default_command(self):
        """设置默认指令"""
        self.instruction_config.default_command()

    def create_instruction_closure(self, line_edit):
        """添加实现点击"""

        def button_clicked():
            line_edit_text = line_edit.text()
            self._update_command(line_edit_text)

        return button_clicked

    def _update_command(self, text):
        """更新写入指令"""
        self.command_line.clear()
        self.command_line.setText(text)
        self.send_btn.click()

    def start_clock_csv(self):
        """启动定时"""
        if self.start_btn.text() == "暂停执行":
            self.start_btn.setText("开始执行")
            self.instruction_config.stop_sequence()
        elif self.file_path_line.text():
            self.start_btn.setText("暂停执行")
            self.instruction_config.commands = self.tool.read_csv_by_command(self.file_path_line.text())
            self.instruction_config.start_sequence()
