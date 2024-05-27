# - coding:utf-8 -
# author: 清安安
# CSDN: 清安无别事
# file_time: 2024/5/26 11:11
import serial.tools.list_ports
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from ui.serial_config import Serial_Form


class CreateSerialUi(QWidget, Serial_Form):
    port_configured = pyqtSignal(str, int)

    def __init__(self, serial_thread, parent=None):
        super(CreateSerialUi, self).__init__(parent)
        self.setupUi(self)
        self.init_singers()
        self.serial_thread = serial_thread

    def init_singers(self):
        self.ok_btn.clicked.connect(self.ok)
        self.Com_Refresh_Button.clicked.connect(self.refresh_ports)
        self.Com_Open_Button.clicked.connect(self.open_port)
        self.Com_Close_Button.clicked.connect(self.close_port)

    def ok(self):
        # self.sava_config()
        self.close()

    def sava_config(self):
        """保存串口配置"""
        config = {"Com": self.Com_Name_Combo.currentText(), "Baud": self.Com_Baud_Combo.currentText(),
                  "Open": self.Com_Open_Button.isEnabled(), "Close": self.Com_Close_Button.isEnabled()}
        return config

    def refresh_ports(self):
        """刷新串口"""
        self.Com_Name_Combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.Com_Name_Combo.addItem(port.device)

    def open_port(self):
        """打开串口"""
        port = self.Com_Name_Combo.currentText()  # 串口
        baud = int(self.Com_Baud_Combo.currentText())  # 波特率
        if port:
            self.serial_thread.open_serial_port(port, baud)
            self.port_configured.emit(port, baud)

    def close_port(self):
        """关闭串口"""
        self.serial_thread.close_serial_port()
