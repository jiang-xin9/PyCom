# - coding:utf-8 -
# author: 清安安
# CSDN: 清安无别事
# file_time: 2024/5/26 11:11
from PyQt5.QtWidgets import QWidget
from ui.serial_config import Serial_Form


class CreateSerialUi(QWidget, Serial_Form):
    def __init__(self, parent=None):
        super(CreateSerialUi, self).__init__(parent)
        self.setupUi(self)
        self.init_singers()

    def init_singers(self):
        self.ok_btn.clicked.connect(self.ok)

    def ok(self):
        self.close()

    def sava_config(self):
        """保存串口配置"""
        config = {"Com": self.Com_Name_Combo.currentText(), "Baud": self.Com_Baud_Combo.currentText(),
                  "Open": self.Com_Open_Button.isEnabled(), "Close": self.Com_Close_Button.isEnabled()}
        return config