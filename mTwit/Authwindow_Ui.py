from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtWidgets import (QLabel, QLineEdit, QDialog)

from mTwit.Error import VerifyError


class AuthWindow(QDialog):  # CK, CS, PIN
  def __init__(self, parent=None):
    super(AuthWindow, self).__init__(parent)
    self.parent = parent
    self.resize(400, 120)
    self.setWindowTitle('Auth')
    self.setStyleSheet(
      "QDialog{background-image: url(image/window.png);"
      "border: 0px solid black;}")
    self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
    self.oldPos = self.pos()

  # ここで親ウィンドウに値を渡している
  def setParamOriginal(self):
    self.parent.setParam(self.edit.text())

  def show(self, MODE):
    if MODE == "Consumer":
      self.ui_setConsumer()

    elif MODE == "TwitterPIN":
      self.ui_setTwitterPIN()

    self.exec_()

  def mousePressEvent(self, event):
    super(AuthWindow, self).mousePressEvent(event)
    self.oldPos = event.globalPos()

  def mouseMoveEvent(self, event):
    super(AuthWindow, self).mouseMoveEvent(event)
    delta = QPoint(event.globalPos() - self.oldPos)
    # print(delta)
    self.move(self.x() + delta.x(), self.y() + delta.y())
    self.oldPos = event.globalPos()

  # define UI and action
  def ui_setConsumer(self):  # 2 TextEdit and 1 Button
    self.ConsumerKeyWindow = QLineEdit('', self)
    self.ConsumerKeyWindow.resize(320, 20)
    self.ConsumerKeyWindow.move(10, 30)
    self.ConsumerKeyWindow.setStyleSheet("background-color: rgba(0,0,0,50);"
                    "border: 1px solid gray;"
                    "font: 10pt 'Meiryo UI' ;"
                    "color: #FFFFFF;")

    self.ConsumerSecretWindow = QLineEdit('', self)
    self.ConsumerSecretWindow.resize(320, 20)
    self.ConsumerSecretWindow.move(10, 80)
    self.ConsumerSecretWindow.setStyleSheet("background-color: rgba(0,0,0,50);"
                       "border: 1px solid gray;"
                       "font: 10pt 'Meiryo UI' ;"
                       "color: #FFFFFF;")

    label1 = QLabel("Consumer Key", self)
    label1.move(10, 10)
    label1.resize(180, 20)
    label1.setStyleSheet("color: #EEEEEE; "
               "font: 12pt 'Meiryo UI'; ")

    label2 = QLabel("Consumer Secret", self)
    label2.move(10, 60)
    label2.resize(180, 20)
    label2.setStyleSheet("color: #EEEEEE; "
               "font: 12pt 'Meiryo UI'; ")
    from mTwit.ui import hoverButton

    self.button = hoverButton(self)
    self.button.resize(48, 48)
    self.button.move(340, 65)
    self.button.setObjectName('setCButton')
    self.button.setIcon(QtGui.QIcon("image/send.png"))
    self.button.setIconSize(QSize(32, 32))
    self.button.setStyleSheet("background-color: rgba(200, 200, 200, 0);"
                  "border: 0px solid gray;")
    self.button.clicked.connect(self.setConsumerEvent)

    self.qbtn = quitButton(self)
    self.qbtn.setButtonPosition(self.size())

  def ui_setTwitterPIN(self):  # 1 TextEdit(7 digit) and 1 Button
    label1 = QLabel("PINCode", self)
    label1.move(10, 10)
    label1.resize(180, 20)
    label1.setStyleSheet("color: #EEEEEE; "
                        "font: 12pt 'Meiryo UI'; ")
    self.pin_window = QLineEdit('', self)
    self.pin_window.resize(320, 60)
    self.pin_window.move(10, 40)
    self.pin_window.setStyleSheet("background-color: rgba(0,0,0,50);"
                    "border: 1px solid gray;"
                    "font: 28pt 'Meiryo UI' ;"
                    "color: #FFFFFF;")
    self.pin_window.setMaxLength(7)
    self.pin_window.setAlignment(Qt.AlignCenter)
    self.pin_window.returnPressed.connect(self.setPINEvent)

    self.button = hoverButton(self)
    self.button.resize(48, 48)
    self.button.move(340, 65)
    self.button.setObjectName('setPINButton')
    self.button.setIcon(QtGui.QIcon("image/send.png"))
    self.button.setIconSize(QSize(32, 32))
    self.button.setStyleSheet("background-color: rgba(200, 200, 200, 0);"
                  "border: 0px solid gray;")
    self.button.clicked.connect(self.setPINEvent)

    self.qbtn = quitButton(self)
    self.qbtn.setButtonPosition(self.size())

  def setPINEvent(self):
    # errW = ErrorNotification(self)
    # print(errW.show("test"))
    self.hide()
    try:
      Auth.verify_twitter(Auth, self.pin_window.text())
      self.pin_window.clear()
      self.parent.api = Auth.init_api(Auth) # Debug
    except VerifyError:
      VerifyError()
      pass
      self.show("TwitterPIN")

  def setConsumerEvent(self):
    self.parent.auth = Auth.init_auth(Auth, self.ConsumerKeyWindow.text().strip(), self.ConsumerSecretWindow.text().strip()) # Debug
    if Auth.open_twitterauth(Auth):
      self.hide()
    else:
      self.ConsumerKeyWindow.clear()
      self.ConsumerSecretWindow.clear()
    pass
