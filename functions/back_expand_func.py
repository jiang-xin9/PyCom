from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from config.enum_config import SidebarParameters

class BackExpand:
    def __init__(self, ui):
        super(BackExpand, self).__init__()
        self.ui = ui

        # 连接按钮点击信号到槽函数
        self.ui.open_btn.clicked.connect(self.toggle_sidebar)

        # 初始化侧边栏状态为展开状态
        self.sidebar_state = SidebarParameters.EXPANDED

        # 初始化计时器并连接到更新动画函数
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)

        # 设置图标路径
        self.expand_icon = QIcon(":/icons/icon/EpArrowRight.png")  # 展开图标路径
        self.collapse_icon = QIcon(":/icons/icon/EpArrowLeft.png")  # 收缩图标路径

        # 设置初始图标为收缩图标，因为初始状态为展开
        self.ui.open_btn.setIcon(self.expand_icon)

    def toggle_sidebar(self):
        """
        切换侧边栏的显示状态，并启动动画效果
        """
        # 获取当前侧边栏的宽度
        sidebar_width = self.ui.quick_frame.width()

        # 切换图标（在切换状态之前）
        if self.sidebar_state == SidebarParameters.EXPANDED:
            self.ui.open_btn.setIcon(self.collapse_icon)
        else:
            self.ui.open_btn.setIcon(self.expand_icon)

        # 根据当前宽度决定目标宽度
        target_width = SidebarParameters.WIDTH_COLLAPSED.value if sidebar_width > 0 else SidebarParameters.WIDTH_EXPANDED.value

        # 开始动画以平滑地调整侧边栏宽度
        self.start_animation(target_width)

        # 切换侧边栏状态
        self.sidebar_state = SidebarParameters.COLLAPSED if self.sidebar_state == SidebarParameters.EXPANDED else SidebarParameters.EXPANDED

    def start_animation(self, target_width):
        """
        开始侧边栏的动画效果
        """
        # 设置目标宽度
        self.target_width = target_width

        # 启动计时器，根据动画步长和持续时间来更新动画
        self.timer.start(SidebarParameters.ANIM_DURATION.value // SidebarParameters.ANIM_STEP.value)

    def update_animation(self):
        """
        更新侧边栏的宽度以实现动画效果
        """
        # 获取当前侧边栏的宽度
        sidebar_width = self.ui.quick_frame.width()

        # 如果当前宽度已达到目标宽度，停止计时器
        if sidebar_width == self.target_width:
            self.timer.stop()
            return

        # 根据目标宽度和当前宽度，计算新的宽度
        if self.target_width < sidebar_width:
            new_width = max(sidebar_width - SidebarParameters.ANIM_STEP.value, self.target_width)
        else:
            new_width = min(sidebar_width + SidebarParameters.ANIM_STEP.value, self.target_width)

        # 设置侧边栏的新宽度
        self.ui.quick_frame.setFixedWidth(new_width)
