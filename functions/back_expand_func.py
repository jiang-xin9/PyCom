from PyQt5.QtCore import QTimer, QPropertyAnimation, pyqtProperty, QEasingCurve
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from config.enum_config import SidebarParameters

class BackExpand(QWidget):
    def __init__(self, ui):
        super(BackExpand, self).__init__()
        self.ui = ui

        # 连接按钮点击信号到槽函数
        self.ui.open_btn.clicked.connect(self.toggle_sidebar)

        # 初始化侧边栏状态为展开状态
        self.sidebar_state = SidebarParameters.EXPANDED

        # 设置图标路径
        self.expand_icon = QIcon(":/icons/icon/EpArrowRight.png")  # 展开图标路径
        self.collapse_icon = QIcon(":/icons/icon/EpArrowLeft.png")  # 收缩图标路径

        # 设置初始图标为收缩图标，因为初始状态为展开
        self.ui.open_btn.setIcon(self.expand_icon)

        # 初始化属性动画
        self.animation = QPropertyAnimation(self, b"sidebar_width")
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.setDuration(SidebarParameters.ANIM_DURATION.value)

        self._sidebar_width = SidebarParameters.WIDTH_EXPANDED.value

    def get_sidebar_width(self):
        return self.ui.quick_frame.width()

    def set_sidebar_width(self, width):
        self.ui.quick_frame.setFixedWidth(width)

    sidebar_width = pyqtProperty(int, get_sidebar_width, set_sidebar_width)

    def toggle_sidebar(self):
        """
        切换侧边栏的显示状态，并启动动画效果
        """
        # 切换图标（在切换状态之前）
        if self.sidebar_state == SidebarParameters.EXPANDED:
            self.ui.open_btn.setIcon(self.collapse_icon)
            target_width = SidebarParameters.WIDTH_COLLAPSED.value
        else:
            self.ui.open_btn.setIcon(self.expand_icon)
            target_width = SidebarParameters.WIDTH_EXPANDED.value

        # 设置动画目标值并启动动画
        self.animation.stop()
        self.animation.setStartValue(self.ui.quick_frame.width())
        self.animation.setEndValue(target_width)
        self.animation.start()

        # 切换侧边栏状态
        self.sidebar_state = SidebarParameters.COLLAPSED if self.sidebar_state == SidebarParameters.EXPANDED else SidebarParameters.EXPANDED

