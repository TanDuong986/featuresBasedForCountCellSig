# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_file/v1.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1399, 797)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 113))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setMaximumSize(QtCore.QSize(98, 100))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(self.frame_4)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/logo_icon/LOGO_TRUONG_CO_NEN.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frame_4)
        self.frame_7 = QtWidgets.QFrame(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.frame_7.setFont(font)
        self.frame_7.setAutoFillBackground(True)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_7)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.app_name = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(28)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.app_name.setFont(font)
        self.app_name.setAutoFillBackground(False)
        self.app_name.setAlignment(QtCore.Qt.AlignCenter)
        self.app_name.setObjectName("app_name")
        self.gridLayout_4.addWidget(self.app_name, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frame_7)
        self.frame_6 = QtWidgets.QFrame(self.frame_2)
        self.frame_6.setMaximumSize(QtCore.QSize(150, 16777215))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.frame_6)
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/logo_icon/Logo25-18.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frame_6)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.frame_3.setFont(font)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.frame_5 = QtWidgets.QFrame(self.frame_3)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.frame_5)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.frame_10 = QtWidgets.QFrame(self.frame_5)
        self.frame_10.setMinimumSize(QtCore.QSize(550, 0))
        self.frame_10.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.frame_10)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.frame_11 = QtWidgets.QFrame(self.frame_10)
        self.frame_11.setMaximumSize(QtCore.QSize(180, 16777215))
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_11)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.true_button = QtWidgets.QPushButton(self.frame_11)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.true_button.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/logo_icon/accept.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.true_button.setIcon(icon)
        self.true_button.setObjectName("true_button")
        self.verticalLayout_2.addWidget(self.true_button)
        self.false_button = QtWidgets.QPushButton(self.frame_11)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.false_button.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/logo_icon/cross.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.false_button.setIcon(icon1)
        self.false_button.setObjectName("false_button")
        self.verticalLayout_2.addWidget(self.false_button)
        self.horizontalLayout_6.addLayout(self.verticalLayout_2)
        self.displayCur = QtWidgets.QLCDNumber(self.frame_11)
        self.displayCur.setMaximumSize(QtCore.QSize(250, 50))
        self.displayCur.setSmallDecimalPoint(False)
        self.displayCur.setDigitCount(5)
        self.displayCur.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.displayCur.setProperty("value", 99999.0)
        self.displayCur.setProperty("intValue", 99999)
        self.displayCur.setObjectName("displayCur")
        self.horizontalLayout_6.addWidget(self.displayCur)
        self.gridLayout_6.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.frame_11, 0, 1, 1, 1)
        self.frame_12 = QtWidgets.QFrame(self.frame_10)
        self.frame_12.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_12.setMaximumSize(QtCore.QSize(500, 1600000))
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_12)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.backward = QtWidgets.QPushButton(self.frame_12)
        self.backward.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.backward.setFont(font)
        self.backward.setStyleSheet("QPushButton {\n"
"    background-color: rgb(0, 255, 0); /* Green */\n"
"    color: rgb(0, 0, 0); /* Black text */\n"
"}")
        self.backward.setObjectName("backward")
        self.horizontalLayout_3.addWidget(self.backward)
        self.forward = QtWidgets.QPushButton(self.frame_12)
        self.forward.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.forward.setFont(font)
        self.forward.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 255, 0); /* Green */\n"
"    color: rgb(0, 0, 0); /* Black text */\n"
"}")
        self.forward.setObjectName("forward")
        self.horizontalLayout_3.addWidget(self.forward)
        self.inputIndex = QtWidgets.QLineEdit(self.frame_12)
        self.inputIndex.setMaximumSize(QtCore.QSize(50, 16777215))
        self.inputIndex.setObjectName("inputIndex")
        self.horizontalLayout_3.addWidget(self.inputIndex)
        self.Jump = QtWidgets.QPushButton(self.frame_12)
        self.Jump.setMaximumSize(QtCore.QSize(100, 16777215))
        self.Jump.setObjectName("Jump")
        self.horizontalLayout_3.addWidget(self.Jump)
        self.gridLayout_5.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.frame_12, 0, 3, 1, 1)
        self.gridLayout_10.addWidget(self.frame_10, 1, 3, 1, 1)
        self.frame_8 = QtWidgets.QFrame(self.frame_5)
        self.frame_8.setMinimumSize(QtCore.QSize(400, 0))
        self.frame_8.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_8)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.frame_8)
        self.label_4.setMaximumSize(QtCore.QSize(170, 16777215))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.src_path = QtWidgets.QLabel(self.frame_8)
        self.src_path.setMinimumSize(QtCore.QSize(0, 0))
        self.src_path.setObjectName("src_path")
        self.horizontalLayout_4.addWidget(self.src_path)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 1, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.header_des = QtWidgets.QLabel(self.frame_8)
        self.header_des.setMaximumSize(QtCore.QSize(170, 16777215))
        self.header_des.setObjectName("header_des")
        self.horizontalLayout_5.addWidget(self.header_des)
        self.destination_path = QtWidgets.QLabel(self.frame_8)
        self.destination_path.setObjectName("destination_path")
        self.horizontalLayout_5.addWidget(self.destination_path)
        self.gridLayout.addLayout(self.horizontalLayout_5, 1, 1, 1, 1)
        self.gridLayout_10.addWidget(self.frame_8, 1, 1, 1, 1)
        self.configuration = QtWidgets.QFrame(self.frame_5)
        self.configuration.setMinimumSize(QtCore.QSize(0, 0))
        self.configuration.setMaximumSize(QtCore.QSize(160000, 100))
        self.configuration.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.configuration.setFrameShadow(QtWidgets.QFrame.Raised)
        self.configuration.setObjectName("configuration")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.configuration)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.toolBarBox = QtWidgets.QFrame(self.configuration)
        self.toolBarBox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.toolBarBox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.toolBarBox.setObjectName("toolBarBox")
        self.gridLayout_11.addWidget(self.toolBarBox, 1, 0, 1, 1)
        self.graph_config = QtWidgets.QLabel(self.configuration)
        self.graph_config.setObjectName("graph_config")
        self.gridLayout_11.addWidget(self.graph_config, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayout_10.addWidget(self.configuration, 1, 0, 1, 1)
        self.graph_frame = QtWidgets.QFrame(self.frame_5)
        self.graph_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.graph_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.graph_frame.setObjectName("graph_frame")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.graph_frame)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.graph_layout = QtWidgets.QVBoxLayout()
        self.graph_layout.setObjectName("graph_layout")
        self.gridLayout_7.addLayout(self.graph_layout, 1, 0, 1, 1)
        self.gridLayout_10.addWidget(self.graph_frame, 0, 0, 1, 4)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_10.addItem(spacerItem, 1, 2, 1, 1)
        self.gridLayout_9.addWidget(self.frame_5, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame_3)
        self.horizontalLayout_2.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1399, 22))
        self.menubar.setObjectName("menubar")
        self.menuLoad = QtWidgets.QMenu(self.menubar)
        self.menuLoad.setObjectName("menuLoad")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExport = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/logo_icon/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExport.setIcon(icon2)
        font = QtGui.QFont()
        self.actionExport.setFont(font)
        self.actionExport.setObjectName("actionExport")
        self.actionContinue = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/logo_icon/continuous-improvement.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionContinue.setIcon(icon3)
        self.actionContinue.setObjectName("actionContinue")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/logo_icon/switch.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon4)
        self.actionExit.setObjectName("actionExit")
        self.menuLoad.addAction(self.actionContinue)
        self.menuLoad.addAction(self.actionExport)
        self.menuLoad.addSeparator()
        self.menuLoad.addAction(self.actionExit)
        self.menubar.addAction(self.menuLoad.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.app_name.setText(_translate("MainWindow", "Cell Labling Application"))
        self.true_button.setText(_translate("MainWindow", "True"))
        self.false_button.setText(_translate("MainWindow", "False"))
        self.backward.setText(_translate("MainWindow", "Backward"))
        self.forward.setText(_translate("MainWindow", "Forward"))
        self.Jump.setText(_translate("MainWindow", "Jump"))
        self.label_4.setText(_translate("MainWindow", "Source Path: "))
        self.src_path.setText(_translate("MainWindow", "Some path"))
        self.header_des.setText(_translate("MainWindow", "Destination Path:"))
        self.destination_path.setText(_translate("MainWindow", "Some path"))
        self.graph_config.setText(_translate("MainWindow", "Configuration"))
        self.menuLoad.setTitle(_translate("MainWindow", "Load"))
        self.actionExport.setText(_translate("MainWindow", "Export Path"))
        self.actionContinue.setText(_translate("MainWindow", "Continue"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
import qrc_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
