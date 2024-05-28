from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QApplication, QWidget
from ui.index import Ui_Form
from functions.tool import Tool
from functions.fast_btn_func import CreateFastBtn
from functions.back_expand_func import BackExpand
from functions.serial_config import SerialConfig
from functions.create_instruction_ui import CreateInstructionUi
from coustom_ui.message_prompt import CustomMessageBox


class PyCom(QWidget, Ui_Form):

    def __init__(self):
        super(PyCom, self).__init__()
        self.setupUi(self)

        # 设置无边框窗口
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._isTracking = False
        self._startPos = QPoint(0, 0)

        self.tool = Tool()
        self.init_ui_components()
        self.init_singers()

        self.is_maximized = False  # 用于跟踪窗口是否最大化

        self.serial = SerialConfig(
            serial_config_btn=self.serial_config_btn,
            send_btn=self.send_btn,
            command_line=self.command_line,
            receive_text_edit=self.receive_textEdit,
            show_message_box=CustomMessageBox.show_box,
            check_time=self.check_time
        )

        self.show()

    def init_ui_components(self):
        """初始化UI组件"""
        self.fast_btn = CreateFastBtn(
            quick_frame=self.quick_frame,
            save_config_btn=self.save_config_btn,
            command_line=self.command_line,
            send_btn=self.send_btn
        )
        self.fast_btn.create_btn()
        self.back_expand = BackExpand(self)  # 按钮收缩侧边栏

    def show_instruction(self):
        self.instruction_window = CreateInstructionUi()
        self.instruction_window.show()

    def init_singers(self):
        """初始化信号连接"""
        self.close_btn.clicked.connect(self.close)
        self.min_btn.clicked.connect(self.showMinimized)
        self.max_btn.clicked.connect(self.toggle_maximize_restore)
        self.clear_send_text.clicked.connect(lambda: self.tool.clear_widget(self.command_line))
        self.clear_receive_text.clicked.connect(lambda: self.tool.clear_widget(self.receive_textEdit))
        self.send_instruction_btn.clicked.connect(self.show_instruction)
        self.command_line.installEventFilter(self)  # 文本区域链接键盘回车事件

    def toggle_maximize_restore(self):
        """切换窗口的最大化和恢复"""
        if self.is_maximized:
            self.showNormal()
            self.is_maximized = False
        else:
            self.showMaximized()
            self.is_maximized = True

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = event.pos()

    def mouseMoveEvent(self, event):
        if self._isTracking:
            self._endPos = event.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._isTracking = False

    def eventFilter(self, obj, event):
        if obj == self.command_line and event.type() == QKeyEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                # 将回车键事件转发给发送按钮，实现快速发送数据
                if self.command_line.text():
                    self.send_btn.click()
                return True
        return super().eventFilter(obj, event)


if __name__ == '__main__':
    app = QApplication([])
    window = PyCom()
    app.exec_()
