from PyQt5.QtCore import QPropertyAnimation, Qt, pyqtProperty, QEasingCurve
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect


class NewQPushButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setMouseTracking(True)  # 启用鼠标跟踪
        self.hover = False  # 初始化hover状态
        self.circle_pos = None  # 圆圈位置
        self.click_effect_value = 1.0  # 点击效果值
        self._color = QColor("#f0f0f0")  # 初始化颜色

        # 定义按钮的默认样式
        self.default_style = """
            QPushButton {
                border: none;
                background-color: rgb(64, 158, 255);
                border-radius: 4px;
                color: rgb(255, 255, 255);
                padding: 5px 10px;
            }
        """
        # 定义按钮的悬停样式
        self.hover_style = """
            QPushButton:hover {
                border: none;
                background-color: rgb(121, 187, 255);
                color: rgb(255, 255, 255);
            }
        """
        # 定义按钮的禁用样式
        self.disabled_style = """
            QPushButton:disabled {
                background-color: rgb(144, 147, 153);
                color: white;
                border-radius: 4px;
            }
        """
        # 应用样式
        self.setStyleSheet(self.default_style + self.hover_style + self.disabled_style)

        # 初始化阴影效果
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(0)
        self.shadow.setOffset(0, 0)
        self.shadow.setColor(QColor(0, 0, 0, 0))  # 设置初始阴影颜色为完全透明
        self.setGraphicsEffect(self.shadow)

        # 初始化点击动画
        self.click_anim = QPropertyAnimation(self, b"click_effect")
        self.click_anim.setDuration(200)
        self.click_anim.setStartValue(1.0)
        self.click_anim.setEndValue(0.0)
        self.click_anim.setEasingCurve(QEasingCurve.OutCubic)

        # 初始化颜色动画
        self.color_anim = QPropertyAnimation(self, b"color")
        self.color_anim.setDuration(200)
        self.color_anim.setStartValue(QColor("#f0f0f0"))
        self.color_anim.setEndValue(QColor("#c0c0c0"))
        self.color_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.color_anim.finished.connect(self.reset_color)

    def reset_color(self):
        """重置按钮颜色到初始状态。"""
        self.setStyleSheet(self.default_style + self.hover_style + self.disabled_style)
        self.update()  # 强制更新

    def enterEvent(self, event):
        """处理鼠标进入事件以应用悬停效果。"""
        if self.isEnabled():
            self.hover = True
            self.setStyleSheet(self.default_style + self.hover_style + self.disabled_style)
            self.shadow.setBlurRadius(20)
            self.shadow.setColor(QColor(0, 0, 0, 50))  # 修改阴影颜色为半透明
            self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """处理鼠标离开事件以移除悬停效果。"""
        if self.isEnabled():
            self.hover = False
            self.setStyleSheet(self.default_style + self.hover_style + self.disabled_style)
            self.shadow.setBlurRadius(0)
            self.shadow.setColor(QColor(0, 0, 0, 0))  # 设置阴影颜色为完全透明
            self.update()
        super().leaveEvent(event)

    def mouseMoveEvent(self, event):
        """处理鼠标移动事件以更新圆圈位置。"""
        if self.isEnabled():
            self.circle_pos = event.pos()
            self.update()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        """处理鼠标按下事件以启动点击动画。"""
        if self.isEnabled():
            self.click_anim.stop()
            self.click_anim.setDirection(QPropertyAnimation.Forward)
            self.click_anim.start()

            self.color_anim.stop()
            self.color_anim.setDirection(QPropertyAnimation.Forward)
            self.color_anim.start()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """处理鼠标释放事件以反转点击动画。"""
        if self.isEnabled():
            self.click_anim.stop()
            self.click_anim.setDirection(QPropertyAnimation.Backward)
            self.click_anim.start()

            self.color_anim.stop()
            self.color_anim.setDirection(QPropertyAnimation.Backward)
            self.color_anim.start()

        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        """处理绘制事件以绘制自定义效果。"""
        super().paintEvent(event)
        if self.isEnabled() and self.hover and self.circle_pos:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)
            gradient = QColor(255, 255, 255, int(150 * self.click_effect_value))
            painter.setBrush(gradient)
            radius = 15
            painter.drawEllipse(self.circle_pos, radius, radius)

    def get_click_effect(self):
        """获取当前点击效果值。"""
        return self.click_effect_value

    def set_click_effect(self, value):
        """设置点击效果值。"""
        self.click_effect_value = value
        self.update()

    def get_color(self):
        """获取当前按钮颜色。"""
        return self._color

    def set_color(self, value):
        """设置按钮颜色。"""
        self._color = value
        self.setStyleSheet(f"""
            QPushButton {{
                border: none;
                border-radius: 4px;
                background-color: {value.name()};
                color: rgb(255, 255, 255);
                padding: 5px 10px;
            }}
            QPushButton:hover {{
                border: none;
                background-color: rgb(121, 187, 255);
                color: rgb(255, 255, 255);
            }}
            QPushButton:disabled {{
                background-color: rgb(144, 147, 153);
                color: white;
                border-radius: 4px;
            }}
        """)

    # 定义动画属性
    click_effect = pyqtProperty(float, get_click_effect, set_click_effect)
    color = pyqtProperty(QColor, get_color, set_color)

    def setDisabled(self, disabled):
        """重写setDisabled以确保正确更新样式。"""
        super().setDisabled(disabled)
        self.update()  # 强制更新
