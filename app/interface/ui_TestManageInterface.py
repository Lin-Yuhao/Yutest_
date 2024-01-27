# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TestManageInterface.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QListWidgetItem,
    QSizePolicy, QVBoxLayout, QWidget)

from qfluentwidgets import (CardWidget, ComboBox, CommandBar, HorizontalSeparator,
    ListWidget, PushButton, SimpleCardWidget, SmoothScrollArea,
    TransparentPushButton)
from qfluentwidgetspro import TransparentComboBox

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(942, 708)
        self.horizontalLayout = QHBoxLayout(Frame)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.Case_SimpleCardWidget = SimpleCardWidget(Frame)
        self.Case_SimpleCardWidget.setObjectName(u"Case_SimpleCardWidget")
        self.verticalLayout_2 = QVBoxLayout(self.Case_SimpleCardWidget)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.TransparentPushButton = TransparentPushButton(self.Case_SimpleCardWidget)
        self.TransparentPushButton.setObjectName(u"TransparentPushButton")
        self.TransparentPushButton.setMinimumSize(QSize(0, 34))
        self.TransparentPushButton.setMaximumSize(QSize(16777215, 34))

        self.verticalLayout_2.addWidget(self.TransparentPushButton)

        self.HorizontalSeparator = HorizontalSeparator(self.Case_SimpleCardWidget)
        self.HorizontalSeparator.setObjectName(u"HorizontalSeparator")

        self.verticalLayout_2.addWidget(self.HorizontalSeparator)

        self.ListWidget = ListWidget(self.Case_SimpleCardWidget)
        self.ListWidget.setObjectName(u"ListWidget")

        self.verticalLayout_2.addWidget(self.ListWidget)


        self.horizontalLayout.addWidget(self.Case_SimpleCardWidget)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.SimpleCardWidget_2 = SimpleCardWidget(Frame)
        self.SimpleCardWidget_2.setObjectName(u"SimpleCardWidget_2")
        self.SimpleCardWidget_2.setMinimumSize(QSize(0, 43))
        self.SimpleCardWidget_2.setMaximumSize(QSize(16777215, 43))
        self.horizontalLayout_2 = QHBoxLayout(self.SimpleCardWidget_2)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.TransparentComboBox = TransparentComboBox(self.SimpleCardWidget_2)
        self.TransparentComboBox.setObjectName(u"TransparentComboBox")
        self.TransparentComboBox.setMaximumSize(QSize(150, 40))

        self.horizontalLayout_2.addWidget(self.TransparentComboBox)

        self.CommandBar = CommandBar(self.SimpleCardWidget_2)
        self.CommandBar.setObjectName(u"CommandBar")

        self.horizontalLayout_2.addWidget(self.CommandBar)


        self.verticalLayout_4.addWidget(self.SimpleCardWidget_2)

        self.Node_SimpleCardWidget = SimpleCardWidget(Frame)
        self.Node_SimpleCardWidget.setObjectName(u"Node_SimpleCardWidget")
        self.verticalLayout = QVBoxLayout(self.Node_SimpleCardWidget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.SmoothScrollArea = SmoothScrollArea(self.Node_SimpleCardWidget)
        self.SmoothScrollArea.setObjectName(u"SmoothScrollArea")
        self.SmoothScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 644, 638))
        self.SmoothScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.SmoothScrollArea)


        self.verticalLayout_4.addWidget(self.Node_SimpleCardWidget)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.SimpleCardWidget = SimpleCardWidget(Frame)
        self.SimpleCardWidget.setObjectName(u"SimpleCardWidget")
        self.verticalLayout_3 = QVBoxLayout(self.SimpleCardWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")

        self.horizontalLayout.addWidget(self.SimpleCardWidget)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 5)
        self.horizontalLayout.setStretch(2, 1)

        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.TransparentPushButton.setText("")
        self.TransparentComboBox.setPrefix(QCoreApplication.translate("Frame", u"\u6d4f\u89c8\u5668", None))
    # retranslateUi

