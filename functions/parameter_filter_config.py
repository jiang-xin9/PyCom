# - coding:utf-8 -
# author: 清安安
# CSDN: 清安无别事
# file_time: 2024/6/12 14:53
from PyQt5.QtCore import QObject
from functions.create_parameter_filter_ui import CreateParameterFilterUi


class CreateParameterFilterConfig(QObject):
    def __init__(self):
        super().__init__()
        self.parameterFilter_window = None

    def show_parameter_filter_config(self):
        if self.parameterFilter_window is None:
            self.parameterFilter_window = CreateParameterFilterUi()  # 实例化 CreateInstructionUi
        self.parameterFilter_window.show()
