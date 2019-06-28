from enum import Enum, auto

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QLabel, QDialog, QHBoxLayout)


class Notification_Mode(Enum):
  Favorite = auto()
  Retweet = auto()
  Error = auto()
  Unknown = auto()


class NotificationWindow(QDialog):  # ErrorWindowと統合してもいいかもしれない
  def __init__(self, parent=None, time=1000, message=''):
    from mTwit.ui import WindowMgr
    self.WindowMgr = WindowMgr()
    super(NotificationWindow, self).__init__(parent)

    layout = QHBoxLayout()
    self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
    desktop = QtWidgets.QDesktopWidget()

    self.desktopSize = (
      desktop.screenGeometry().width(),
      desktop.screenGeometry().height(),
      desktop.availableGeometry().width(),
      desktop.availableGeometry().height()
      )

    self.resize(self.desktopSize[0] / 1.5, 30)
    self.icon_label = QLabel("", self)
    self.icon_label.move(0, 0)
    self.icon_label.setScaledContents(True)

    layout.addItem(self.icon_label)

    label = QLabel(message, self)
    label.move(32, 4)
    label.setStyleSheet("background:rgba(0, 0, 0, 0);")

    layout.addSpacing(5)
    layout.addItem(label)

    self.setupAnim(time)

  def show(self, mode=Notification_Mode.Unknown, *args):
    if mode == Notification_Mode.Favorite:
      self.icon_label.setPixmap(QPixmap("image/Favorite.png"))
      self.setStyleSheet("background-color: rgba(255,193,7,80);"
                         "border: 0px solid gray;"
                         "font: 10pt 'Meiryo UI' ;"
                         "color: #212121;")
    elif mode == Notification_Mode.Retweet:  # if -> elif
      self.icon_label.setPixmap(QPixmap("image/Retweet.png"))
      self.setStyleSheet("background-color: rgba(0,96,16,80);"
                         "border: 0px solid gray;"
                         "font: 10pt 'Meiryo UI' ;"
                         "color: #E0E0E0;")
    elif mode == Notification_Mode.Error:
      self.icon_label.setPixmap(QPixmap("image/Error.png"))
      self.setStyleSheet("background-color: rgba(154,0,7,80);"
                         "border: 0px solid gray;"
                         "font: 10pt 'Meiryo UI' ;"
                         "color: #E0E0E0;")
    else:
      self.icon_label.setPixmap(QPixmap("image/Unknown.png"))
      self.setStyleSheet("background-color: #263238;"
                         "border: 0px solid gray;"
                         "font: 10pt 'Meiryo UI' ;"
                         "color: #E0E0E0;")
    super().show()
    self.animGroup.start()

  def endAnim(self):
    self.hide()

  def setupAnim(self, time=1000):
    taskbar = self.WindowMgr.getTaskbar()
    self.anim = QtCore.QPropertyAnimation(self, b"pos")
    self.anim.setDuration(350)
    self.anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
    if taskbar[0] == "lower":
      self.anim.setStartValue(QtCore.QPoint(self.desktopSize[2] / 2 - (self.width() / 2), self.desktopSize[1]))
      self.anim.setEndValue(QtCore.QPoint(self.desktopSize[2] / 2 - (self.width() / 2), self.desktopSize[1] - (taskbar[2] + self.height()) ) )

    else:
      self.anim.setStartValue(QtCore.QPoint(self.desktopSize[2] / 2 - (self.width() / 2), self.desktopSize[1]))
      self.anim.setEndValue(QtCore.QPoint(self.desktopSize[2] / 2 - (self.width() / 2), self.desktopSize[1] - self.height()) )

    self.anim2 = QtCore.QPropertyAnimation(self, b"pos")
    self.anim2.setDuration(350)
    self.anim2.setEasingCurve(QtCore.QEasingCurve.InCubic)

    if taskbar[0] == "lower": 
      self.anim2.setStartValue(QtCore.QPoint(self.desktopSize[2] / 2 - (self.width() / 2), self.desktopSize[1] - (taskbar[2] + self.height()) ) )
      self.anim2.setEndValue(QtCore.QPoint(self.desktopSize[2] / 2 - (self.width() / 2), self.desktopSize[1]))

    else:
      self.anim2.setStartValue(QtCore.QPoint(self.desktopSize[2] / 2 - (self.width() / 2), self.desktopSize[1] - self.height()))
      self.anim2.setEndValue(QtCore.QPoint(self.desktopSize[2] / 2 - (self.width() / 2), self.desktopSize[1]))
      
    # endValue Property of anim2 is set
    self.anim2.finished.connect(self.endAnim)

    self.animGroup = QtCore.QSequentialAnimationGroup()
    self.animGroup.addPause(1)
    self.animGroup.addAnimation(self.anim)
    self.animGroup.addPause(time)
    self.animGroup.addAnimation(self.anim2)
