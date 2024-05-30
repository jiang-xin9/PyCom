from PyQt5.QtCore import QPropertyAnimation, pyqtProperty, QEasingCurve, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QSplitter

class SidebarParameters:
    WIDTH_EXPANDED = 240  # 展开宽度
    ANIM_DURATION = 500  # 动画持续时间（毫秒）
    EXPANDED = "expanded"
    COLLAPSED = "collapsed"

class BackExpand(QWidget):
    def __init__(self, ui):
        super(BackExpand, self).__init__()
        self.ui = ui

        # 连接按钮点击信号到槽函数
        self.ui.open_btn.clicked.connect(self.toggle_sidebar)

        # 初始化侧边栏状态为收缩状态
        self.sidebar_state = SidebarParameters.COLLAPSED

        # 设置图标路径
        self.expand_icon = QIcon(":/icons/icon/EpArrowRight.png")  # 展开图标路径
        self.collapse_icon = QIcon(":/icons/icon/EpArrowLeft.png")  # 收缩图标路径

        # 设置初始图标为收缩图标，因为初始状态为收缩
        self.ui.open_btn.setIcon(self.collapse_icon)

        # 初始化 QSplitter
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)

        # 创建侧边栏框架并设置初始背景颜色
        self.quick_frame = self.ui.quick_frame

        # 将主内容区和 quick_frame 添加到 splitter 中，确保 quick_frame 在右侧
        self.splitter.addWidget(self.ui.serial_frame)  # 你的主内容区控件
        self.splitter.addWidget(self.quick_frame)

        # 将 splitter 添加到主布局中
        self.ui.verticalLayout_3.addWidget(self.splitter)

        # 初始化属性动画
        self.animation = QPropertyAnimation(self, b"sidebar_width")
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.setDuration(SidebarParameters.ANIM_DURATION)

        # 在初始化时设置 quick_frame 的最小宽度为 1 像素
        self.quick_frame.setMinimumWidth(1)

        # 连接动画结束信号到槽函数
        self.animation.finished.connect(self.on_animation_finished)

        # 检测手动拖动事件
        self.splitter.splitterMoved.connect(self.on_splitter_moved)

        # 默认设置侧边栏为收缩状态
        self.set_sidebar_width(1)
        self.quick_frame.setVisible(False)

    def showEvent(self, event):
        super(BackExpand, self).showEvent(event)
        # 确保初始宽度为收缩状态
        self.set_sidebar_width(1)
        self.quick_frame.setVisible(False)

    def get_sidebar_width(self):
        return self.quick_frame.width()

    def set_sidebar_width(self, width):
        main_width = self.splitter.size().width()
        self.splitter.setSizes([main_width - width, width])

    sidebar_width = pyqtProperty(int, get_sidebar_width, set_sidebar_width)

    def toggle_sidebar(self):
        """
        切换侧边栏的显示状态，并启动动画效果
        """
        # 确保每次切换时从当前宽度开始动画
        self.animation.stop()
        self.animation.setStartValue(self.get_sidebar_width())

        if self.sidebar_state == SidebarParameters.EXPANDED:
            self.ui.open_btn.setIcon(self.collapse_icon)
            target_width = 1  # 完全收缩，设置为1像素而不是0
            self.sidebar_state = SidebarParameters.COLLAPSED
        else:
            self.quick_frame.setVisible(True)  # 确保 quick_frame 在动画开始前可见
            self.ui.open_btn.setIcon(self.expand_icon)
            target_width = SidebarParameters.WIDTH_EXPANDED
            self.sidebar_state = SidebarParameters.EXPANDED

        self.animation.setEndValue(target_width)
        self.animation.start()

    def on_animation_finished(self):
        """
        在动画结束时更新 quick_frame 的可见性，并强制设置宽度
        """
        if self.sidebar_state == SidebarParameters.COLLAPSED:
            self.quick_frame.setVisible(False)
            self.set_sidebar_width(1)  # 强制设置宽度为1
        else:
            self.quick_frame.setVisible(True)
            self.set_sidebar_width(SidebarParameters.WIDTH_EXPANDED)

    def on_splitter_moved(self, pos, index):
        """
        检测手动拖动事件并更新按钮图标和状态
        """
        if self.get_sidebar_width() <= 1:
            self.ui.open_btn.setIcon(self.collapse_icon)
            self.sidebar_state = SidebarParameters.COLLAPSED
            self.quick_frame.setVisible(False)
        else:
            self.ui.open_btn.setIcon(self.expand_icon)
            self.sidebar_state = SidebarParameters.EXPANDED
            self.quick_frame.setVisible(True)
