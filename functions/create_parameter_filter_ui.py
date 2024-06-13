# - coding:utf-8 -
# author: 清安安
# CSDN: 清安无别事
# file_time: 2024/6/12 14:48
from PyQt5.QtWidgets import QWidget
from ui.parameter_filter import Ui_Filter_Form


class CreateParameterFilterUi(QWidget, Ui_Filter_Form):
    def __init__(self, apply_filter_callback=None, cancel_filter_callback=None,
                 apply_capture_callback=None, cancel_capture_callback=None):
        super(CreateParameterFilterUi, self).__init__()
        self.setupUi(self)
        self.apply_filter_callback = apply_filter_callback
        self.cancel_filter_callback = cancel_filter_callback
        self.apply_capture_callback = apply_capture_callback
        self.cancel_capture_callback = cancel_capture_callback
        self.filter_active = False
        self.capture_active = False
        self.init_signals()

    def init_signals(self):
        self.start_capture_btn.clicked.connect(self.toggle_capture)
        self.filter_btn.clicked.connect(self.toggle_filter)

    def toggle_capture(self):
        if self.capture_active:
            self.cancel_capture()
            self.start_capture_btn.setText("开始捕获")
            self.capture_active = False
        else:
            self.start_capture()
            self.start_capture_btn.setText("取消捕获")
            self.capture_active = True

    def toggle_filter(self):
        if self.filter_active:
            self.cancel_filter()
            self.filter_btn.setText("应用过滤")
            self.filter_active = False
        else:
            self.start_filter()
            self.filter_btn.setText("取消过滤")
            self.filter_active = True

    def start_capture(self):
        # 启动捕获逻辑
        if self.apply_capture_callback:
            self.apply_capture_callback(self.capture_line.text())

    def cancel_capture(self):
        # 取消捕获逻辑
        if self.cancel_capture_callback:
            self.cancel_capture_callback()

    def start_filter(self):
        # 获取过滤条件并应用过滤逻辑
        re_text_1 = self.re1_line.text()
        re_text_2 = self.re2_line.text()

        filter_condition = (re_text_1, re_text_2) if re_text_1 and re_text_2 else None

        if self.apply_filter_callback:  # 将数据回调回去
            self.apply_filter_callback(filter_condition)

    def cancel_filter(self):
        # 取消过滤逻辑
        if self.cancel_filter_callback:
            self.cancel_filter_callback()
