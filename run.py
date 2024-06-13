import asyncio
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeyEvent, QIcon
from PyQt5.QtWidgets import QApplication
from qasync import QEventLoop
from ui.index import Ui_Form
from functions.tool import Tool
from functions.fast_btn_func import CreateFastBtn
from functions.back_expand_func import BackExpand
from functions.serial_config import SerialConfig
from functions.instruction_config import InstructionConfig
from coustom_ui.message_prompt import CustomMessageBox
from functions.reset_window_size_func import CFramelessBase
from functions.create_upgrade_ui import CreateUpgradeUi


class PyCom(CFramelessBase, Ui_Form):
    def __init__(self):
        super(PyCom, self).__init__()
        self.setupUi(self)
        CustomMessageBox.default_parent = self  # 设置默认父窗口
        self.tool = Tool()
        self.init_ui_components()
        self.init_signals()

        self.is_maximized = False  # 用于跟踪窗口是否最大化
        self.normalGeometry = self.geometry()  # 保存正常状态下的窗口几何

        # 初始化开关按钮的状态
        self.check_enter.set_toggled(True)

        # 将 check_enter 传递给 SerialWorker
        self.serial = SerialConfig(
            serial_config_btn=self.serial_config_btn,
            send_btn=self.send_btn,
            command_line=self.command_line,
            serial_com=self.serial_com,
            receive_text_edit=self.receive_textEdit,
            show_message_box=CustomMessageBox.show_box,
            check_time=self.check_time,
            check_enter=self.check_enter,  # 传递 check_enter 实例
            check_loop_send=self.check_loop_send,
            line_delayed=self.line_delayed,
            check_save_log=self.check_save_log,
            line_log=self.line_log,
            check_hex_receive=self.check_hex_receive,
            check_hex_send=self.check_hex_send,
            parameter_filter_btn = self.parameter_filter_btn
        )

        # 添加拖拽功能到 top_Frame
        self.top_Frame.installEventFilter(self)

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
        self.instruction_config = InstructionConfig(self.serial)
        self.instruction_config.show_instruction_config()

    def show_upgrade(self):
        self.upgrade_window = CreateUpgradeUi()
        # self.upgrade_window.upgrade_signal.connect(self.serial)
        self.upgrade_window.show()

    def init_signals(self):
        """初始化信号连接"""
        self.close_btn.clicked.connect(self.close)
        self.min_btn.clicked.connect(self.showMinimized)
        self.max_btn.clicked.connect(self.toggle_maximize_restore)
        self.clear_send_text.clicked.connect(lambda: self.tool.clear_widget(self.command_line))
        self.clear_receive_text.clicked.connect(lambda: self.tool.clear_widget(self.receive_textEdit))
        self.send_instruction_btn.clicked.connect(self.show_instruction)
        self.upgrade_btn.clicked.connect(self.show_upgrade)
        self.command_line.installEventFilter(self)

    def toggle_maximize_restore(self):
        """切换窗口的最大化和恢复"""
        if self.is_maximized:
            self.setGeometry(self.normalGeometry)
            self.max_btn.setIcon(QIcon(':icons/icon/EpFullScreen.png'))  # 设定放大图标
            self.is_maximized = False
        else:
            self.normalGeometry = self.geometry()
            screen_geometry = QApplication.primaryScreen().availableGeometry()
            self.setGeometry(screen_geometry.adjusted(-5, -5, 5, 5))  # 手动增加尺寸
            self.max_btn.setIcon(QIcon(':icons/icon/MageMinimize.png'))  # 设定最小化图标
            self.is_maximized = True

    def eventFilter(self, obj, event):
        if obj == self.top_Frame:
            if event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    self.isDragging = True
                    self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
                    event.accept()
                    return True
            elif event.type() == QEvent.MouseMove:
                if self.isDragging:
                    self.move(event.globalPos() - self.dragPosition)
                    event.accept()
                    return True
            elif event.type() == QEvent.MouseButtonRelease:
                self.isDragging = False
                return True
        if obj == self.command_line and event.type() == QKeyEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                # 将回车键事件转发给发送按钮，实现快速发送数据
                if self.command_line.text():
                    self.send_btn.click()
                return True
        return super().eventFilter(obj, event)


if __name__ == '__main__':
    app = QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = PyCom()
    window.show()
    with loop:
        loop.run_forever()
