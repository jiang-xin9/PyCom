# - coding:utf-8 -
# author: 清安安
# CSDN: 清安无别事
# file_time: 2024/6/12 14:48
from PyQt5.QtWidgets import QWidget
from ui.parameter_filter import Ui_Filter_Form


class CreateParameterFilterUi(QWidget, Ui_Filter_Form):
    def __init__(self):
        super(CreateParameterFilterUi, self).__init__()
        self.setupUi(self)
