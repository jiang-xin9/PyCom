import sys
from PyQt5.QtCore import QPropertyAnimation, Qt, pyqtProperty, QEasingCurve
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect


class NewQPushButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setMouseTracking(True)
        self.hover = False
        self.circle_pos = None
        self.click_effect_value = 1.0
        self._color = QColor("#f0f0f0")  # Initialize the color

        self.default_style = """
            QPushButton {
                border: 0.5px solid rgb(64, 158, 255);
                background-color: rgb(64, 158, 255);
                border-radius: 4px;
                color: rgb(255, 255, 255);
            }
        """
        self.hover_style = """
            QPushButton {
                border: 1.5px solid #8f8f91;
                border-radius: 4px;
                background-color: rgb(121, 187, 255);
                color: rgb(255, 255, 255);
            }
        """
        self.setStyleSheet(self.default_style)

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(0)
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)

        self.click_anim = QPropertyAnimation(self, b"click_effect")
        self.click_anim.setDuration(200)
        self.click_anim.setStartValue(1.0)
        self.click_anim.setEndValue(0.0)
        self.click_anim.setEasingCurve(QEasingCurve.OutCubic)

        self.color_anim = QPropertyAnimation(self, b"color")
        self.color_anim.setDuration(200)
        self.color_anim.setStartValue(QColor("#f0f0f0"))
        self.color_anim.setEndValue(QColor("#c0c0c0"))
        self.color_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.color_anim.finished.connect(self.reset_color)

    def reset_color(self):
        self.setStyleSheet(self.default_style)

    def enterEvent(self, event):
        self.hover = True
        self.setStyleSheet(self.hover_style)
        self.shadow.setBlurRadius(20)
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hover = False
        self.setStyleSheet(self.default_style)
        self.shadow.setBlurRadius(0)
        self.update()
        super().leaveEvent(event)

    def mouseMoveEvent(self, event):
        self.circle_pos = event.pos()
        self.update()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        self.click_anim.stop()
        self.click_anim.setDirection(QPropertyAnimation.Forward)
        self.click_anim.start()

        self.color_anim.stop()
        self.color_anim.setDirection(QPropertyAnimation.Forward)
        self.color_anim.start()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.click_anim.stop()
        self.click_anim.setDirection(QPropertyAnimation.Backward)
        self.click_anim.start()

        self.color_anim.stop()
        self.color_anim.setDirection(QPropertyAnimation.Backward)
        self.color_anim.start()

        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.hover and self.circle_pos:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)
            gradient = QColor(255, 255, 255, int(150 * self.click_effect_value))
            painter.setBrush(gradient)
            radius = 15
            painter.drawEllipse(self.circle_pos, radius, radius)

    def get_click_effect(self):
        return self.click_effect_value

    def set_click_effect(self, value):
        self.click_effect_value = value
        self.update()

    def get_color(self):
        return self._color

    def set_color(self, value):
        self._color = value
        self.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid #8f8f91;
                border-radius: 4px;
                background-color: {value.name()};
            }}
        """)

    click_effect = pyqtProperty(float, get_click_effect, set_click_effect)
    color = pyqtProperty(QColor, get_color, set_color)

