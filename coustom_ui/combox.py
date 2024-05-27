
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate, QGraphicsDropShadowEffect, QStyle
from PyQt5.QtGui import QFont, QPalette


class CustomDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.sizeHint = option.fontMetrics.size(0, index.data())
        option.sizeHint.setHeight(30)  # Set the height of each item

    def paint(self, painter, option, index):
        # Draw the background
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        else:
            painter.fillRect(option.rect, option.palette.base())

        # Set font and color
        font = QFont("微软雅黑", 10)
        painter.setFont(font)
        painter.setPen(option.palette.color(QPalette.Text))

        # Draw the text with padding
        text_rect = option.rect.adjusted(10, 0, 0, 0)
        painter.drawText(text_rect, Qt.AlignVCenter, index.data())


class NewComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setItemDelegate(CustomDelegate(self))

        # 设置样式表
        self.setStyleSheet("""
            QComboBox {
                border: 1px solid #ced4da;
                border-radius: 4px; /* Set border-radius for rounded corners */
                padding: 5px;
                font-size: 10pt; /* 设置字体大小 */
                font-family: '微软雅黑'; /* 设置字体为微软雅黑 */
                padding-left: 10px;
                height: 25px; /* Adjust the height as needed */
                background-color: white;
            }
            QComboBox:hover {
                border: 1px solid #007bff; /* Blue border when hovered */
                border-radius: 4px; /* Keep rounded corners on hover */
            }
            QComboBox::drop-down {
                border-left: 1px solid #ced4da; /* Left border for the drop-down arrow */
                padding-right: 5px; /* Adjust the padding to align the arrow */
                width: 25px; /* Width of the drop-down area */
                subcontrol-origin: padding;
                subcontrol-position: top right;
                border-top-right-radius: 4px; /* Rounded top-right corner */
                border-bottom-right-radius: 4px; /* Rounded bottom-right corner */
            }
            QComboBox::down-arrow {
                image: url(:icons/icon/EpArrowDown.png); /* Provide the path to the down arrow icon */
                width: 16px;
                height: 16px;
                margin-left: 5px; /* Adjust the margin to align the arrow */
            }
            QComboBox::down-arrow:on { /* When the combo box is open */
                image: url(:icons/icon/EpArrowUp.png); /* Provide the path to the up arrow icon */
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ced4da;
                border-radius: 4px; /* Add border-radius to make the corners rounded */
                padding-top: 5px; /* Add padding to the top to create distance from the top */
                padding-bottom: 5px; /* Add padding to the bottom */
                selection-background-color: rgb(245,245,250);
                selection-color: #000000;
                font-size: 14px;
                color: rgb(11,113,116);
                background-color: white; /* Match the background color */
                border-top-left-radius: 4px; /* Rounded top-left corner */
                border-top-right-radius: 4px; /* Rounded top-right corner */
                border-bottom-left-radius: 4px; /* Rounded bottom-left corner */
                border-bottom-right-radius: 4px; /* Rounded bottom-right corner */
            }
            QComboBox QAbstractItemView::item {
                min-height: 30px; /* Match the height of the combo box items */
                padding: 5px; /* Add padding to ensure the items are not cramped */
            }
        """)

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self:
            if event.type() == event.Enter:
                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(15)
                shadow.setColor(Qt.gray)
                shadow.setOffset(0, 0)
                self.setGraphicsEffect(shadow)
            elif event.type() == event.Leave:
                self.setGraphicsEffect(None)
        return super().eventFilter(obj, event)

