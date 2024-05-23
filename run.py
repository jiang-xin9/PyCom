from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QWidget
from ui.index import Ui_Form
from functions.fast_btn_func import CreateFastBtn
from functions.back_expand_func import BackExpand


class PyCom(QWidget, Ui_Form):

    def __init__(self):
        super(PyCom, self).__init__()
        self.setupUi(self)

        # 设置无边框窗口
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._isTracking = False
        self.init_singers()
        self._startPos = QPoint(0, 0)

        self.fast_btn = CreateFastBtn(self)
        self.fast_btn.create_btn()

        self.back_expand = BackExpand(self)
        self.show()

    def init_singers(self):
        self.close_btn.clicked.connect(self.close)
        self.min_btn.clicked.connect(self.showMinimized)
        self.max_btn.clicked.connect(self.showMaximized)

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


if __name__ == '__main__':
    app = QApplication([])
    window = PyCom()
    app.exec_()
