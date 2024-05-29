from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QFontMetrics

class CustomToggleButton(QWidget):
    def __init__(self, parent=None, off_text=None, on_text=None, default_state=False):
        super().__init__(parent)
        self.off_text = off_text
        self.on_text = on_text
        self.toggled = default_state

        # 获取控件的高度
        self.height = self.height() if self.height() > 0 else 25

        self.initUI()

    def initUI(self):
        # 初始化开关的宽度
        self.toggle_frame_width = 2 * self.height  # 宽度设置为高度的两倍
        self.indicator_diameter = self.height - 6  # 指示器直径比高度小 6 像素
        self.indicator_margin = 3  # 指示器边距

        # 计算需要的总宽度
        self.calculate_widths()

        # 创建并设置开关框架
        self.toggle_frame = QFrame(self)
        self.toggle_frame.setFixedSize(self.toggle_frame_width, self.height)
        self.toggle_frame.setStyleSheet(f"background-color: #e0e0e0; border-radius: {self.height // 2}px;")

        # 创建并设置指示器
        self.indicator = QFrame(self.toggle_frame)
        self.indicator.setFixedSize(self.indicator_diameter, self.indicator_diameter)
        self.indicator.setStyleSheet(f"background-color: white; border-radius: {self.indicator_diameter // 2}px;")

        # 创建并设置标签
        self.label = QLabel(self.off_text, self)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 确保文本左对齐并垂直居中

        # 设置布局
        layout = QHBoxLayout()
        layout.addWidget(self.toggle_frame)
        layout.addWidget(self.label)
        layout.setSpacing(10)  # 调整控件间的间距
        layout.setContentsMargins(0, 0, 0, 0)  # 调整布局的外边距

        self.setLayout(layout)
        self.setFixedHeight(self.height)  # 设置固定高度

        # 绑定鼠标点击事件
        self.toggle_frame.mousePressEvent = self.toggle

        # 设置动画效果
        self.anim = QPropertyAnimation(self.indicator, b"geometry")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.OutQuad)

        # 根据默认状态初始化外观
        if self.toggled:
            self.set_on(animate=False)
        else:
            self.set_off(animate=False)

    def calculate_widths(self):
        # 使用 QFontMetrics 计算文本宽度
        font_metrics = QFontMetrics(self.font())
        off_text_width = font_metrics.width(self.off_text)
        on_text_width = font_metrics.width(self.on_text)
        max_text_width = max(off_text_width, on_text_width)
        total_width = self.toggle_frame_width + max_text_width + 30  # 计算总宽度并增加额外空间
        self.setFixedSize(total_width, self.height)

    def setText(self, text):
        # 设置 off 状态的文本
        self.off_text = text
        self.label.setText(self.off_text)
        self.calculate_widths()  # 重新计算宽度

    def setToggleTexts(self, off_text=None, on_text=None):
        # 设置开关的文本
        if off_text:
            self.off_text = off_text
        if on_text:
            self.on_text = on_text
        if not self.toggled:
            self.label.setText(self.off_text)
        self.calculate_widths()  # 重新计算宽度

    def toggle(self, event=None):
        # 切换开关状态
        self.toggled = not self.toggled
        self.animate_toggle()

    def animate_toggle(self):
        # 执行动画效果
        if self.toggled:
            self.set_on()
        else:
            self.set_off()
        self.anim.start()

    def set_on(self, animate=True):
        end_value = QRect(self.toggle_frame_width - self.indicator_margin - self.indicator_diameter, self.indicator_margin,
                          self.indicator_diameter, self.indicator_diameter)
        if animate:
            self.anim.setEndValue(end_value)
        else:
            self.indicator.setGeometry(end_value)
        self.toggle_frame.setStyleSheet(f"background-color: #6200ea; border-radius: {self.height // 2}px;")
        if self.on_text:
            self.label.setText(self.on_text)

    def set_off(self, animate=True):
        end_value = QRect(self.indicator_margin, self.indicator_margin, self.indicator_diameter, self.indicator_diameter)
        if animate:
            self.anim.setEndValue(end_value)
        else:
            self.indicator.setGeometry(end_value)
        self.toggle_frame.setStyleSheet(f"background-color: #e0e0e0; border-radius: {self.height // 2}px;")
        if self.off_text:
            self.label.setText(self.off_text)

    def set_toggled(self, state):
        self.toggled = state
        if state:
            self.set_on(animate=False)
        else:
            self.set_off(animate=False)
