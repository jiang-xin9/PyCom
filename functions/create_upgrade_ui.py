# - coding:utf-8 -
# author: 清安安
# CSDN: 清安无别事
# file_time: 2024/5/26 11:11
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from ui.upgrade import Upgrade_Form
from functions.tool import Tool
from functions.send_singer import SignalEmitter


class CreateUpgradeUi(QWidget, Upgrade_Form):
    upgrade_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(CreateUpgradeUi, self).__init__(parent)
        self.setupUi(self)
        self.tool = Tool()
        self.init_singers()

    def init_singers(self):
        """初始化信号槽"""
        self.get_bin_file.clicked.connect(self.get_bin_path_clicked)
        self.file_bin_path.textChanged.connect(self.handle_bin_path)
        self.start_upgrade_btn.clicked.connect(self.start_upgrade)

    def get_bin_path_clicked(self):
        """获取文件路径"""
        self.tool.get_file_path(self.file_bin_path)

    def handle_bin_path(self):
        """处理文件路径, 判断bin文件"""
        path, text = self.tool.handle_file_path(self.file_bin_path)
        if ".bin" not in text[-1]:
            SignalEmitter.warning_signal("非bin文件，无法加载")
        else:
            self.upgrade_signal.emit(path)

    def start_upgrade(self):
        """开始升级"""
        bin_path = self.file_bin_path.text()
        if bin_path and ".bin" in bin_path:
            self.upgrade_signal.emit(bin_path)
        else:
            SignalEmitter.warning_signal("请先选择正确的bin文件")
