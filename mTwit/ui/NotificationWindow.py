import mTwit.ui.ui_base as ui

from enum import Enum, auto

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QLabel, QDialog, QHBoxLayout, QSizePolicy)

from debtcollector import removals


@removals.remove
class NotificationMode(Enum):
    FAVORITE = auto()
    RETWEET = auto()
    ERROR = auto()
    UNKNOWN = auto()


class NotificationWindow(QDialog):  # ErrorWindowと統合してもいいかもしれない
    def __init__(self, parent=None, time=1000, message=''):
        super(NotificationWindow, self).__init__(parent)

        layout: QHBoxLayout = QHBoxLayout()
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        desktop = QtWidgets.QDesktopWidget()

        self.desktopSize: tuple = (
            desktop.screenGeometry().width(),
            desktop.screenGeometry().height(),
            desktop.availableGeometry().width(),
            desktop.availableGeometry().height()
        )

        self.resize(self.desktopSize[0] / 1.5, 30)
        self.icon_label = QLabel("", self)
        self.icon_label.resize(30, 30)
        self.icon_label.move(0, 0)
        self.icon_label.setStyleSheet("background:rgba(0, 0, 0, 0);")

        self.icon_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        layout.setSizeConstraint(layout.SetNoConstraint)
        layout.addWidget(self.icon_label)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(message, self)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # label.move(32, 4)
        label.setStyleSheet("background:rgba(0, 0, 0, 0);")

        layout.addSpacing(20)
        layout.addWidget(label)
        self.setLayout(layout)
        self.setupAnim(time)

    def show(self, mode=NotificationMode.UNKNOWN, *args):
        if mode == NotificationMode.FAVORITE:
            self.icon_label.setPixmap(QPixmap("resources/icon/Favorite.png"))
            self.setStyleSheet("background-color: rgba(255,193,7,80);"
                               "border: 0px solid gray;"
                               "font: 10pt 'Meiryo UI' ;"
                               "color: #212121;")
        elif mode == NotificationMode.RETWEET:  # if -> elif
            self.icon_label.setPixmap(QPixmap("resources/icon/Retweet.png"))
            self.setStyleSheet("background-color: rgba(0,96,16,80);"
                               "border: 0px solid gray;"
                               "font: 10pt 'Meiryo UI' ;"
                               "color: #E0E0E0;")
        elif mode == NotificationMode.ERROR:
            self.icon_label.setPixmap(QPixmap("resources/icon/Error.png"))
            self.setStyleSheet("background-color: rgba(154,0,7,80);"
                               "border: 0px solid gray;"
                               "font: 10pt 'Meiryo UI' ;"
                               "color: #E0E0E0;")
        else:
            self.icon_label.setPixmap(QPixmap("resources/icon/Unknown.png"))
            self.setStyleSheet("background-color: #263238;"
                               "border: 0px solid gray;"
                               "font: 10pt 'Meiryo UI' ;"
                               "color: #E0E0E0;")
        super().show()
        self.animGroup.start()

    def endAnim(self):
        self.hide()

    def setupAnim(self, time=1000):
        taskbar = ui.taskbar_info()
        self.anim = QtCore.QPropertyAnimation(self, b"pos")
        self.anim.setDuration(350)
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        if taskbar[0] == "lower":
            self.anim.setStartValue(QtCore.QPoint(
                self.desktopSize[2] / 2 - (self.width() / 2), self.desktopSize[1]))
            self.anim.setEndValue(QtCore.QPoint(self.desktopSize[2] / 2 - (
                self.width() / 2), self.desktopSize[1] - (taskbar[2] + self.height())))

        else:
            self.anim.setStartValue(QtCore.QPoint(
                self.desktopSize[2] / 2 - (self.width() / 2), self.desktopSize[1]))
            self.anim.setEndValue(QtCore.QPoint(
                self.desktopSize[2] / 2 - (self.width() / 2), self.desktopSize[1] - self.height()))

        self.anim2 = QtCore.QPropertyAnimation(self, b"pos")
        self.anim2.setDuration(350)
        self.anim2.setEasingCurve(QtCore.QEasingCurve.InCubic)

        if taskbar[0] == "lower":
            self.anim2.setStartValue(QtCore.QPoint(self.desktopSize[2] / 2 - (
                self.width() / 2), self.desktopSize[1] - (taskbar[2] + self.height())))
            self.anim2.setEndValue(QtCore.QPoint(
                self.desktopSize[2] / 2 - (self.width() / 2), self.desktopSize[1]))

        else:
            self.anim2.setStartValue(QtCore.QPoint(
                self.desktopSize[2] / 2 - (self.width() / 2), self.desktopSize[1] - self.height()))
            self.anim2.setEndValue(QtCore.QPoint(
                self.desktopSize[2] / 2 - (self.width() / 2), self.desktopSize[1]))

        # endValue Property of anim2 is set
        self.anim2.finished.connect(self.endAnim)

        self.animGroup = QtCore.QSequentialAnimationGroup()
        self.animGroup.addPause(1)
        self.animGroup.addAnimation(self.anim)
        self.animGroup.addPause(time)
        self.animGroup.addAnimation(self.anim2)
