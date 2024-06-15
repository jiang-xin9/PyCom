# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'upgrade.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Upgrade_Form(object):
    def setupUi(self, upgrade):
        upgrade.setObjectName("upgrade")
        upgrade.resize(383, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icon/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        upgrade.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(upgrade)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(upgrade)
        self.frame.setMinimumSize(QtCore.QSize(0, 30))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.file_bin_path = QtWidgets.QLineEdit(self.frame)
        self.file_bin_path.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.file_bin_path.setFont(font)
        self.file_bin_path.setStyleSheet("QLineEdit {\n"
"    border-radius: 4px;\n"
"    border: 1px solid #ced4da;\n"
"}")
        self.file_bin_path.setObjectName("file_bin_path")
        self.verticalLayout_2.addWidget(self.file_bin_path)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.get_bin_file = NewQPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.get_bin_file.sizePolicy().hasHeightForWidth())
        self.get_bin_file.setSizePolicy(sizePolicy)
        self.get_bin_file.setMinimumSize(QtCore.QSize(80, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.get_bin_file.setFont(font)
        self.get_bin_file.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.get_bin_file.setObjectName("get_bin_file")
        self.horizontalLayout.addWidget(self.get_bin_file)
        self.start_upgrade_btn = NewQPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_upgrade_btn.sizePolicy().hasHeightForWidth())
        self.start_upgrade_btn.setSizePolicy(sizePolicy)
        self.start_upgrade_btn.setMinimumSize(QtCore.QSize(80, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.start_upgrade_btn.setFont(font)
        self.start_upgrade_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.start_upgrade_btn.setObjectName("start_upgrade_btn")
        self.horizontalLayout.addWidget(self.start_upgrade_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.frame, 0, QtCore.Qt.AlignTop)
        self.frame_2 = QtWidgets.QFrame(upgrade)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(upgrade)
        QtCore.QMetaObject.connectSlotsByName(upgrade)

    def retranslateUi(self, upgrade):
        _translate = QtCore.QCoreApplication.translate
        upgrade.setWindowTitle(_translate("upgrade", "Form"))
        self.file_bin_path.setPlaceholderText(_translate("upgrade", "选择需要升级的bin"))
        self.get_bin_file.setText(_translate("upgrade", "获取文本"))
        self.start_upgrade_btn.setText(_translate("upgrade", "开始执行"))
        self.label.setText(_translate("upgrade", "ymodem"))
from coustom_ui.pushbutton import NewQPushButton
from . import resources