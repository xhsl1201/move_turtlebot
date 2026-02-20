# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'k_move_control.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(595, 611)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(70, 70, 301, 151))
        self.btn_go = QPushButton(self.centralwidget)
        self.btn_go.setObjectName(u"btn_go")
        self.btn_go.setGeometry(QRect(170, 270, 95, 71))
        self.btn_left = QPushButton(self.centralwidget)
        self.btn_left.setObjectName(u"btn_left")
        self.btn_left.setGeometry(QRect(50, 360, 95, 71))
        self.btn_right = QPushButton(self.centralwidget)
        self.btn_right.setObjectName(u"btn_right")
        self.btn_right.setGeometry(QRect(290, 360, 95, 71))
        self.btn_back = QPushButton(self.centralwidget)
        self.btn_back.setObjectName(u"btn_back")
        self.btn_back.setGeometry(QRect(170, 450, 95, 71))
        self.btn_stop = QPushButton(self.centralwidget)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setGeometry(QRect(170, 360, 95, 71))
        self.lbl_linear = QLabel(self.centralwidget)
        self.lbl_linear.setObjectName(u"lbl_linear")
        self.lbl_linear.setGeometry(QRect(420, 80, 151, 41))
        self.lbl_angular = QLabel(self.centralwidget)
        self.lbl_angular.setObjectName(u"lbl_angular")
        self.lbl_angular.setGeometry(QRect(420, 160, 151, 41))
        self.btn_safety_on = QPushButton(self.centralwidget)
        self.btn_safety_on.setObjectName(u"btn_safety_on")
        self.btn_safety_on.setGeometry(QRect(440, 340, 111, 41))
        self.btn_safety_off = QPushButton(self.centralwidget)
        self.btn_safety_off.setObjectName(u"btn_safety_off")
        self.btn_safety_off.setGeometry(QRect(440, 400, 111, 41))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(450, 290, 91, 41))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 595, 27))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_go.setText(QCoreApplication.translate("MainWindow", u"GO", None))
        self.btn_left.setText(QCoreApplication.translate("MainWindow", u"LEFT", None))
        self.btn_right.setText(QCoreApplication.translate("MainWindow", u"RIGHT", None))
        self.btn_back.setText(QCoreApplication.translate("MainWindow", u"BACK", None))
        self.btn_stop.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.lbl_linear.setText("")
        self.lbl_angular.setText("")
        self.btn_safety_on.setText(QCoreApplication.translate("MainWindow", u"ON", None))
        self.btn_safety_off.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"     \uc548\uc804\ubaa8\ub4dc", None))
    # retranslateUi

