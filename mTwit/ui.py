from PyQt5.QtWidgets import (QMessageBox, QApplication, QWidget, QToolTip, QPushButton,
    QDesktopWidget, QMainWindow, QAction, qApp, QToolBar, QVBoxLayout,
    QComboBox, QLabel, QLineEdit, QGridLayout, QMenuBar, QMenu, QStatusBar,
  	QPlainTextEdit, QDialog, QFrame, QProgressBar, QShortcut, QSystemTrayIcon
		)
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QKeySequence
from PyQt5.QtCore import QCoreApplication, Qt, QBasicTimer, QPoint, QSize
from system_hotkey import SystemHotkey

import re
import win32gui

class WindowMgr:
  """Encapsulates some calls to the winapi for window management"""

  def __init__(self):
    """Constructor"""
    self._handle = None

  def find_window(self, class_name, window_name=None):
    """find a window by its class_name"""
    self._handle = win32gui.FindWindow(class_name, window_name)

  def _window_enum_callback(self, hwnd, wildcard):
    """Pass to win32gui.EnumWindows() to check all the opened windows"""
    if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
      self._handle = hwnd

  def find_window_wildcard(self, wildcard):
    """find a window whose title matches the wildcard regex"""
    self._handle = None
    win32gui.EnumWindows(self._window_enum_callback, wildcard)

  def set_foreground(self):
    """put the window in the foreground"""
    win32gui.SetForegroundWindow(self._handle)


class hoverButton(QPushButton):
  def __init__(self, parent=None):
    super(hoverButton, self).__init__(parent)

  def enterEvent(self, QEvent):
    self.setStyleSheet("background-color: rgba(200, 200, 200, 0.2);"
               "border: 0px solid gray;")

  def leaveEvent(self, QEvent):
    self.setStyleSheet("background-color: rgba(200, 200, 200, 0);"
               "border: 0px solid gray;")

"""
class ErrorWindow(QWidget):  # ここ出来上がらんとやばみ
  def __init__(self):
    super(QMessageBox).__init__()
    self.msgBox = QMessageBox()
    self.msgBox.setText("Connect or abort?")
    self.connectButton = self.msgBox.addButton("Connect", QMessageBox.ActionRole)
    self.abortButton = self.msgBox.addButton(QMessageBox.Abort)

  def show(self):
    return self.msgBox.exec_()
"""

class NotificationWindow(QWidget):  # ErrorWindowと統合してもいいかもしれない
  def __init__(self):
    self.super(QWidget).__init__()


class AuthWindow(QDialog):  # CK, CS, PIN
  def __init__(self, parent=None):
    super().__init__(parent)
    self.parent = parent
    self.resize(400, 120)
    self.setWindowTitle('Auth')
    self.setStyleSheet(
			"QDialog{background-image: url(image/window.png);"
      "border: 0px solid black;}"
			)
    self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
    self.oldPos = self.pos()
    # self.Auth = TwitterMgr()

  # ここで親ウィンドウに値を渡している
  def setParamOriginal(self):
    self.parent.setParam(self.edit.text())

  def show(self, MODE):
    if MODE == "Consumer":
      self.ui_setConsumer()

    elif MODE == "TwitterPIN":
      self.Auth.open_twitterauth()
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
    self.ConsumerKeyWindow.setStyleSheet(
			"background-color: rgba(0,0,0,50);"
      "border: 1px solid gray;"
      "font: 10pt 'Meiryo UI' ;"
      "color: #FFFFFF;"
			)

    self.ConsumerSecretWindow = QLineEdit('', self)
    self.ConsumerSecretWindow.resize(320, 20)
    self.ConsumerSecretWindow.move(10, 80)
    self.ConsumerSecretWindow.setStyleSheet(
			"background-color: rgba(0,0,0,50);"
      "border: 1px solid gray;"
      "font: 10pt 'Meiryo UI' ;"
      "color: #FFFFFF;"
			)

    label_CK = QLabel("Consumer Key", self)
    label_CK.move(10, 10)
    label_CK.resize(180, 20)
    label_CK.setStyleSheet(
			"color: #EEEEEE; "
      "font: 12pt 'Meiryo UI'; "
			)

    label_CS = QLabel("Consumer Secret", self)
    label_CS.move(10, 60)
    label_CS.resize(180, 20)
    label_CS.setStyleSheet(
			"color: #EEEEEE; "
      "font: 12pt 'Meiryo UI'; "
			)

    self.button = hoverButton(self)
    self.button.resize(48, 48)
    self.button.move(340, 65)
    self.button.setObjectName('setCButton')
    self.button.setIcon(QtGui.QIcon("image/send.png"))
    self.button.setIconSize(QSize(32, 32))
    self.button.setStyleSheet(
			"background-color: rgba(200, 200, 200, 0);"
      "border: 0px solid gray;"
			)
    self.button.clicked.connect(self.setConsumerEvent)

  def ui_setTwitterPIN(self):  # 1 TextEdit(7 digit) and 1 Button
    label_PIN = QLabel("PINCode", self)
    label_PIN.move(10, 10)
    label_PIN.resize(180, 20)
    label_PIN.setStyleSheet(
			"color: #EEEEEE; "
      "font: 12pt 'Meiryo UI'; "
			)

    self.pin_form = QLineEdit('', self)
    self.pin_form.resize(320, 60)
    self.pin_form.move(10, 40)
    self.pin_form.setStyleSheet(
			"background-color: rgba(0,0,0,50);"
      "border: 1px solid gray;"
      "font: 28pt 'Meiryo UI' ;"
    	"color: #FFFFFF;"
			)

    self.pin_form.setMaxLength(7)
    self.pin_form.setAlignment(Qt.AlignCenter)

    self.button = hoverButton(self)
    self.button.resize(48, 48)
    self.button.move(340, 65)
    self.button.setObjectName('setPINButton')
    self.button.setIcon(QtGui.QIcon("image/send.png"))
    self.button.setIconSize(QSize(32, 32))
    self.button.setStyleSheet(
			"background-color: rgba(200, 200, 200, 0);"
      "border: 0px solid gray;"
			)
    self.button.clicked.connect(self.setPINEvent)

  def setPINEvent(self):
    if self.Auth.verify_twitter(self.pin_form.text().strip()):
      print("Success") 
    else:
      # Error (Failed get AT,AS)
      print("Failed")
      pass
    self.hide()

  def setConsumerEvent(self):
    self.Auth = TwitterMgr(self.ConsumerKeyWindow.text().strip(), self.ConsumerSecretWindow.text().strip())
    self.hide()
    pass


class mainWindow(QMainWindow):
  iconPath = "image/send.png"
  w = WindowMgr()
  w.find_window_wildcard("MTwit")

  def __init__(self, parent=None):
    super(mainWindow, self).__init__(parent)

    self.mwidget = QMainWindow(self)
    self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
    self.setWindowTitle("MTwit")

    # window size
    self.setFixedSize(480, 120)
    self.center()

    # TrayIcon
    self.createActions()
    self.createTrayIcon()
    self.trayIcon.show()
    self.trayIcon.activated.connect(self.iconActivated)

    # Textwindow
    self.textWindow = QPlainTextEdit('', self)
    self.textWindow.resize(400, 100)
    self.textWindow.move(10, 10)
    self.textWindow.setStyleSheet(
			"background-color: rgba(0,0,0,50);"
      "border: 1px solid gray;"
    	"font: 14pt 'Meiryo UI' ;"
      "color: #FFFFFF;"
			)
    self.textWindow.setPlaceholderText("What's Happening?")

    # Quit Button
    self.qbtn = QPushButton('', self)
    self.qbtn.clicked.connect(self.hide)
    self.qbtn.setIcon(QtGui.QIcon("image/quit.png"))
    self.qbtn.setStyleSheet(
			"background-color: Transparent;"
      "left: -2px;"
      "border: 1px solid gray;"
			)
    self.qbtn.resize(24, 24)
    self.qbtn.move(455, 2)

    # Tweet Button
    self.tbtn = hoverButton(self)
    self.tbtn.resize(48, 48)
    self.tbtn.move(420, 62)
    self.tbtn.setObjectName('tButton')
    self.tbtn.setIcon(QtGui.QIcon("image/send.png"))
    self.tbtn.setIconSize(QSize(32, 32))
    self.tbtn.setStyleSheet("background-color: rgba(200, 200, 200, 0);")

    self.tbtn.clicked.connect(self.tweetEvent)

    # tweet Shortcut
    self.tShortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Return), self)
    self.tShortcut.activated.connect(self.tweetEvent)

    # window show Shortcut
    self.hk = SystemHotkey(consumer=self.ShowOrHide)
    self.hk.register(('alt', 'shift', 'f1'))

    # label
    """self.lbl = QLabel(self)
    self.lbl.setText("")
    self.lbl.setStyleSheet("background-color: rgb(0,0,0);"
                 "border: 0px solid red;"
                 "color: rgb(255,255,255);"
                 "font: bold italic 20pt 'Times New Roman';")
    self.lbl.setGeometry(5,5,60,40)
    """

    self.oldPos = self.pos()

    self.show()
    self.w.find_window_wildcard("MTwit")

  # windowMove --
  def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

  def mousePressEvent(self, event):
    self.oldPos = event.globalPos()

  def mouseMoveEvent(self, event):
    delta = QPoint(event.globalPos() - self.oldPos)
    self.move(self.x() + delta.x(), self.y() + delta.y())
    self.oldPos = event.globalPos()

  # windowMove End --

  def tweetEvent(self):
    print("tweetEventActivated")
    self.hide()
    text = self.textWindow.document().toPlainText()
    self.textWindow.setPlainText("")
    try:
      self.api.update_status(text)
    except tweepy.error.TweepError:
      pass

  def quitEvent(self):
    self.trayIcon.hide()
    self.hk.unregister(('alt', 'shift', 'f1'))
    QCoreApplication.instance().quit()
    pass

  def templateTweetEvent(self):
    pass

  def iconActivated(self, reason):
    if reason == 3:
      self.trayClickAction()

  def trayClickAction(self):
    if self.isHidden():
      self.showEvent_()
    else:
      self.hide()

  def ShowOrHide(self, *args):
    if self.isHidden():
      self.showEvent_()
    else:
      self.hide()

  def createTrayIcon(self):
    self.trayIconMenu = QMenu(self)
    self.trayIconMenu.addAction(self.debugMakePINAction)
    self.trayIconMenu.addAction(self.debugMakeWindowAction)
    self.trayIconMenu.addSeparator()
    self.trayIconMenu.addAction(self.minimizeAction)
    self.trayIconMenu.addAction(self.restoreAction)
    self.trayIconMenu.addSeparator()
    self.trayIconMenu.addAction(self.quitAction)
    self.trayIcon = QSystemTrayIcon(self)
    self.trayIcon.setContextMenu(self.trayIconMenu)
    self.trayIcon.setIcon(QIcon(self.iconPath))

  def createActions(self):
    self.minimizeAction = QAction("Mi&nimize", self, triggered=self.hide)
    self.restoreAction = QAction("&Restore", self, triggered=self.showNormal)
    self.quitAction = QAction("&Quit", self, triggered=self.quitEvent)
    self.debugMakeWindowAction = QAction("&DebugMakeAuth", self, triggered=self.makeAuthWindow)
    self.debugMakePINAction = QAction("&DebugMakePIN", self, triggered=self.makePINWindow)

  def showEvent_(self):
    self.textWindow.setPlainText("")
    self.show()
    self.makeAuthWindow() # Debug
    self.w.set_foreground()

  # Auth Window

  def makeAuthWindow(self):
    self.authWindow = AuthWindow(self)
    self.authWindow.show("Consumer")  # Debug
  
  def makePINWindow(self):
    if not (self.authWindow) :
      self.authWindow = AuthWindow(self)
    self.authWindow.show("TwitterPIN")

  def setParam(self, param):
    self.textWindow.setPlainText(param)

  # ---------------------------

