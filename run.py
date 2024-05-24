from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit
from ui.index import Ui_Form
from functions.fast_btn_func import CreateFastBtn
from functions.back_expand_func import BackExpand
from ui.serial_config import Serial_Form
from ui.instruction import Instruction_Form
from functions.instruction_func import CreateInstruction


class PyCom(QWidget, Ui_Form):

    def __init__(self):
        super(PyCom, self).__init__()
        self.setupUi(self)

        # 设置无边框窗口
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._isTracking = False
        self._startPos = QPoint(0, 0)

        self.init_ui_components()
        self.init_singers()

        self.show()

    def init_ui_components(self):
        """初始化UI组件"""
        self.fast_btn = CreateFastBtn(self)
        self.fast_btn.create_btn()
        self.back_expand = BackExpand(self)  # 按钮收缩侧边栏

    def show_serial_config(self):
        self.serial_config_window = SerialUi()
        self.serial_config_window.show()

    def show_instruction(self):
        self.instruction_window = InstructionUi()
        self.instruction_window.show()

    def init_singers(self):
        """初始化信号连接"""
        self.close_btn.clicked.connect(self.close)
        self.min_btn.clicked.connect(self.showMinimized)
        self.max_btn.clicked.connect(self.showMaximized)
        self.clear_send_text.clicked.connect(lambda: self.clear_widget(self.command_line))
        self.clear_receive_text.clicked.connect(lambda: self.clear_widget(self.receive_textEdit))
        self.serial_config_btn.clicked.connect(self.show_serial_config)
        self.send_instruction_btn.clicked.connect(self.show_instruction)

    def clear_widget(self, widget):
        """传入控件，清空内容"""
        widget.clear()

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


class SerialUi(QWidget, Serial_Form):
    def __init__(self, parent=None):
        super(SerialUi, self).__init__(parent)
        self.setupUi(self)


class InstructionUi(QWidget, Instruction_Form):
    def __init__(self, parent=None):
        super(InstructionUi, self).__init__(parent)
        self.setupUi(self)
        self.create_instruction = CreateInstruction(self)
        self.create_instruction.create_widget()


if __name__ == '__main__':
    app = QApplication([])
    window = PyCom()
    app.exec_()
