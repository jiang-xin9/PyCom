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

        # 初始化开关按钮的状态
        self.check_enter.set_toggled(True)

        # 将 check_enter 传递给 SerialWorker
        self.serial = SerialConfig(
            serial_config_btn=self.serial_config_btn,
            send_btn=self.send_btn,
            command_line=self.command_line,
            receive_text_edit=self.receive_textEdit,
            show_message_box=CustomMessageBox.show_box,
            check_time=self.check_time,
            check_enter=self.check_enter,  # 传递 check_enter 实例
            check_loop_send=self.check_loop_send,
            line_delayed=self.line_delayed
        )

        self.minWidth = 400
        self.minHeight = 300
        self.setMinimumWidth(self.minWidth)
        self.setMinimumHeight(self.minHeight)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.initDrag()  # 设置鼠标跟踪判断默认值

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

    def initDrag(self):
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False
        self._bottom_drag = False
        self._right_drag = False
        self._left_drag = False
        self._right_bottom_corner_drag = False
        self._left_bottom_corner_drag = False

    def mousePressEvent(self, event):
        # 重写鼠标点击的事件
        if (event.button() == Qt.LeftButton) and (self._cursorInBottomRightCorner(event.pos())):
            # 鼠标左键点击右下角边界区域
            self._right_bottom_corner_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (self._cursorInBottomLeftCorner(event.pos())):
            # 鼠标左键点击左下角边界区域
            self._left_bottom_corner_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (self._cursorInLeftRect(event.pos())):
            # 鼠标左键点击左侧边界区域
            self._left_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (self._cursorInRightRect(event.pos())):
            # 鼠标左键点击右侧边界区域
            self._right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (self._cursorInBottomRect(event.pos())):
            # 鼠标左键点击下侧边界区域
            self._bottom_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.y() < self._titleHeight()):
            # 鼠标左键点击标题栏区域
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        # 当鼠标左键点击不放及满足点击区域的要求后，分别实现不同的窗口调整
        if Qt.LeftButton and (self._right_drag or self._left_drag or self._bottom_drag or self._right_bottom_corner_drag or self._left_bottom_corner_drag):
            if self._right_drag:
                # 右侧调整窗口宽度
                self.resize(QMouseEvent.pos().x(), self.height())
            elif self._left_drag:
                # 左侧调整窗口宽度
                new_width = self.width() - QMouseEvent.pos().x()
                if new_width >= self.minWidth:
                    self.resize(new_width, self.height())
                    self.move(self.x() + QMouseEvent.pos().x(), self.y())
            elif self._bottom_drag:
                # 下侧调整窗口高度
                self.resize(self.width(), QMouseEvent.pos().y())
            elif self._right_bottom_corner_drag:
                # 右下角同时调整高度和宽度
                self.resize(QMouseEvent.pos().x(), QMouseEvent.pos().y())
            elif self._left_bottom_corner_drag:
                # 左下角同时调整高度和宽度
                new_width = self.width() - QMouseEvent.pos().x()
                if new_width >= self.minWidth:
                    self.resize(new_width, QMouseEvent.pos().y())
                    self.move(self.x() + QMouseEvent.pos().x(), self.y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._move_drag:
            # 标题栏拖放窗口位置
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        # 鼠标释放后，各扳机复位
        self._move_drag = False
        self._right_bottom_corner_drag = False
        self._bottom_drag = False
        self._right_drag = False
        self._left_drag = False
        self._left_bottom_corner_drag = False

    def eventFilter(self, obj, event):
        if obj == self.command_line and event.type() == QKeyEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                # 将回车键事件转发给发送按钮，实现快速发送数据
                if self.command_line.text():
                    self.send_btn.click()
                return True
        return super().eventFilter(obj, event)

    def _cursorInRightRect(self, pos):
        return pos.x() > self.width() - 5 and pos.x() <= self.width()

    def _cursorInLeftRect(self, pos):
        return pos.x() >= 0 and pos.x() < 5

    def _cursorInBottomRect(self, pos):
        return pos.y() > self.height() - 5 and pos.y() <= self.height()

    def _cursorInBottomRightCorner(self, pos):
        return self._cursorInRightRect(pos) and self._cursorInBottomRect(pos)

    def _cursorInBottomLeftCorner(self, pos):
        return self._cursorInLeftRect(pos) and self._cursorInBottomRect(pos)

    def _titleHeight(self):
        return self.titleWidget.height() if hasattr(self, 'titleWidget') else 30


if __name__ == '__main__':
    app = QApplication([])
    window = PyCom()
    app.exec_()
