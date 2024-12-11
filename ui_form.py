# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QScrollArea, QSizePolicy, QVBoxLayout, QWidget)
import rc_icons

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(788, 540)
        Widget.setMinimumSize(QSize(788, 540))
        Widget.setMaximumSize(QSize(16777215, 16777215))
        icon = QIcon()
        icon.addFile(u":/img/Icons/programmer.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Widget.setWindowIcon(icon)
        Widget.setStyleSheet(u"\n"
"#interface_name{\n"
"	color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.mainframe = QFrame(Widget)
        self.mainframe.setObjectName(u"mainframe")
        self.mainframe.setStyleSheet(u"background-color: rgb(245, 245, 245);\n"
"\n"
"")
        self.mainframe.setFrameShape(QFrame.Shape.NoFrame)
        self.mainframe.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayout_2 = QVBoxLayout(self.mainframe)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.header = QFrame(self.mainframe)
        self.header.setObjectName(u"header")
        self.header.setMinimumSize(QSize(0, 60))
        self.header.setMaximumSize(QSize(16777215, 60))
        self.header.setStyleSheet(u"background-color: rgb(62, 62, 62);")
        self.header.setFrameShape(QFrame.Shape.NoFrame)
        self.header.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout = QHBoxLayout(self.header)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 0, 10, 0)
        self.icon_interface = QLabel(self.header)
        self.icon_interface.setObjectName(u"icon_interface")
        self.icon_interface.setMinimumSize(QSize(50, 50))
        self.icon_interface.setMaximumSize(QSize(50, 50))
        self.icon_interface.setPixmap(QPixmap(u":/img/Icons/programmer.png"))
        self.icon_interface.setScaledContents(True)

        self.horizontalLayout.addWidget(self.icon_interface)

        self.interface_name = QLabel(self.header)
        self.interface_name.setObjectName(u"interface_name")
        font = QFont()
        font.setFamilies([u"Yu Gothic UI Semibold"])
        font.setPointSize(25)
        font.setBold(True)
        self.interface_name.setFont(font)
        self.interface_name.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.interface_name)


        self.verticalLayout_2.addWidget(self.header)

        self.frame_3 = QFrame(self.mainframe)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.scrollAreaFrame = QFrame(self.frame_3)
        self.scrollAreaFrame.setObjectName(u"scrollAreaFrame")
        self.scrollAreaFrame.setStyleSheet(u"QFrame {\n"
"    background-color: rgb(245, 245, 245);\n"
"    border-radius: 20px;\n"
"    border: 2px solid rgb(156, 156, 156); /* Definindo a cor e espessura da borda */\n"
"}")
        self.scrollAreaFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.scrollAreaFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaFrame)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.scrollArea = QScrollArea(self.scrollAreaFrame)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"border: 0px;\n"
"\n"
"\n"
"")
        self.scrollArea.setFrameShape(QFrame.Shape.StyledPanel)
        self.scrollArea.setFrameShadow(QFrame.Shadow.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 746, 418))
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_5.addWidget(self.scrollArea)


        self.verticalLayout_4.addWidget(self.scrollAreaFrame)


        self.verticalLayout_2.addWidget(self.frame_3)

        self.frame_2 = QFrame(self.mainframe)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 20))
        self.frame_2.setMaximumSize(QSize(16777215, 20))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(15, 0, 0, 5)
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"color: rgb(113, 113, 113);")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label)


        self.verticalLayout_2.addWidget(self.frame_2)


        self.verticalLayout.addWidget(self.mainframe)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Reader", None))
        self.icon_interface.setText("")
        self.interface_name.setText(QCoreApplication.translate("Widget", u"CODE TRACKING", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Developed by Junior Tavares", None))
    # retranslateUi

