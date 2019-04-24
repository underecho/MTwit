from PyQt5.QtWidgets import (QMessageBox, QApplication, QWidget, QToolTip, QPushButton,
               QDesktopWidget, QMainWindow, QAction, qApp, QToolBar,
               QComboBox, QLabel, QLineEdit, QMenuBar, QMenu, QStatusBar,
               QPlainTextEdit, QDialog, QFrame, QShortcut, QSystemTrayIcon
               )
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QKeySequence
from PyQt5.QtCore import QCoreApplication, Qt, QBasicTimer, QPoint, QSize
from mTwit.Auth import TwitterMgr as Auth
from mTwit.Error import *
import tweepy.error
import win32gui, re
import time # Debug
from enum import Enum, auto
from system_hotkey import SystemHotkey

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
    print (self._handle) # Debug

  def set_foreground(self, Id):
    """put the window in the foreground"""
    win32gui.SetForegroundWindow(Id)

  def getTaskbar():  
    """Return Taskbar position and Size (position, width, height)"""
    desktopSize = QDesktopWidget().availableGeometry()
    screenSize = (QDesktopWidget().screenGeometry().width(), QDesktopWidget().screenGeometry().height())
    taskbarSize = (screenSize[0] - desktopSize.width(), screenSize[1] - desktopSize.height())
    if taskbarSize[0] != 0: # position is left or right
      if desktopSize.x() != 0: # left
        return ("left", taskbarSize[0], screenSize[1])
      else:
        return ("right", taskbarSize[0], screenSize[1])

    if taskbarSize[1] != 0: # position is upper or lower
      if desktopSize.y() != 0: # upper
        return ("upper", screenSize[0], taskbarSize[1])
      else:
        return ("lower", screenSize[0], taskbarSize[1])

    raise TaskbarError

class hoverButton(QPushButton):
  def __init__(self, parent=None):
    super(hoverButton, self).__init__(parent)

  def enterEvent(self, QEvent):
    self.setStyleSheet("background-color: rgba(200, 200, 200, 0.2);"
               "border: 0px solid gray;")

  def leaveEvent(self, QEvent):
    self.setStyleSheet("background-color: rgba(200, 200, 200, 0);"
               "border: 0px solid gray;")

class quitButton(hoverButton):
  def __init__(self, parent=None):
    super(quitButton, self).__init__(parent)
    self.clicked.connect(parent.hide)
    self.setIcon(QtGui.QIcon("image/quit.png"))
    self.setStyleSheet("background-color: Transparent;"
                "left: -2px;"
                "border: 0px solid gray;")
    self.resize(24, 24)

  def setButtonPosition(self, window_size):
    self.move(window_size.width() - 26, 2)

 
class Notification_Mode(Enum):
  Favorite = auto()
  Retweet = auto()
  Error = auto()
  Unknown = auto()

class NotificationWindow(QDialog):  # ErrorWindowと統合してもいいかもしれない
  def __init__(self, parent=None, *args):
    super(NotificationWindow, self).__init__(parent)
    self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
    desktop = QDesktopWidget()
    self.desktopSize = (\
      desktop.screenGeometry().width(),\
      desktop.screenGeometry().height(),\
      desktop.availableGeometry().width(), \
      desktop.availableGeometry().height() \
      )
    self.resize(self.desktopSize[0] / 1.5, 30)
    self.setupAnim()

  def show(self, MODE=Notification_Mode.Unknown, *args):
    self.Mode = MODE
    if self.Mode == Notification_Mode.Favorite:
      self.setStyleSheet("background-color: rgba(255,193,7,80);"
                         "border: 0px solid gray;"
                         "font: 10pt 'Meiryo UI' ;"
                         "color: #212121;")
    elif self.Mode == Notification_Mode.Retweet: # if -> elif
      self.setStyleSheet("background-color: rgba(0,96,16,80);"
                         "border: 0px solid gray;"
                         "font: 10pt 'Meiryo UI' ;"
                         "color: #E0E0E0;")
    elif self.Mode == Notification_Mode.Error:
      self.setStyleSheet("background-color: rgba(154,0,7,80);"
                         "border: 0px solid gray;"
                         "font: 10pt 'Meiryo UI' ;"
                         "color: #E0E0E0;")
    else:
      self.setStyleSheet("background-color: #263238;"
                         "border: 0px solid gray;"
                         "font: 10pt 'Meiryo UI' ;"
                         "color: #E0E0E0;")
    super().show()
    self.animGroup.start()
    

  def endAnim(self):
    self.hide()

  def setupAnim(self):
    taskbar = WindowMgr.getTaskbar()
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
      self.anim2.setStartValue(QtCore.QPoint(self.desktopSize[2] / 2 - (self.width() / 2), self.desktopSize[1] - self.height()) )
      self.anim2.setEndValue(QtCore.QPoint(self.desktopSize[2] / 2 - (self.width() / 2), self.desktopSize[1]))
      
    # endValue Property of anim2 is set
    self.anim2.finished.connect(self.endAnim)

    self.animGroup = QtCore.QSequentialAnimationGroup()
    self.animGroup.addPause(1)
    self.animGroup.addAnimation(self.anim)
    self.animGroup.addPause(1000)
    self.animGroup.addAnimation(self.anim2)

class AuthWindow(QDialog):  # CK, CS, PIN
  def __init__(self, parent=None):
    super(AuthWindow, self).__init__(parent)
    self.parent = parent
    self.resize(400, 120)
    self.setWindowTitle('Auth')
    self.setStyleSheet("QDialog{background-image: url(image/window.png);"
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
    errW = Errorwindow(self)
    # print(errW.show("test"))
    self.hide()
    try:
      Auth.verify_twitter(Auth, self.pin_window.text())
      self.pin_window.clear()
      self.parent.api = Auth.init_api(Auth) # Debug
    except VerifyError:
      errW.show(VerifyError().__str__())
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


class mainWindow(QMainWindow):
  iconPath = "image/send.png"
  def __init__(self, parent=None):
    super(mainWindow, self).__init__(parent)
    self.mwidget = QMainWindow(self)
    self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
    self.setWindowTitle("MTwit")
    self.wId = self.winId()
    self.w = WindowMgr()

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
    self.textWindow.setStyleSheet("background-color: rgba(0,0,0,50);"
                    "border: 1px solid gray;"
                    "font: 14pt 'Meiryo UI' ;"
                    "color: #FFFFFF;")
    self.textWindow.setPlaceholderText("What's Happening?")

    # Quit Button
    self.qbtn = quitButton(self)
    self.qbtn.setButtonPosition(self.size())

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

    self.Firstshow()
    

  def Firstshow(self): # check user data and init api
    
    pass

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
    print("tweetActivated")
    self.hide()
    text = self.textWindow.document().toPlainText()
    self.textWindow.setPlainText("")
    try:
      self.api.update_status(text)
    except tweepy.error.TweepError as e:
      tb = sys.exc_info()[2]
      print("message:{0}".format(e.with_traceback(tb)))
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
      self.ShowOrHide()

  def ShowOrHide(self, *args):
    if self.isHidden():
      self.showEvent_()
    else:
      self.hide()

  def createTrayIcon(self):
    self.trayIconMenu = QMenu(self)
    self.trayIconMenu.addAction(self.debugMakeWindowAction)
    self.trayIconMenu.addAction(self.debugMakeWindow2Action)
    self.trayIconMenu.addAction(self.debugMakeWindow3Action)
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
    self.debugMakeWindow2Action = QAction("&DebugMake2Auth", self, triggered=self.makeAuthWindow2)
    self.debugMakeWindow3Action = QAction("&DebugMake3(Notification)", self, triggered=self.makeDebugwindow)


  def showEvent_(self):
    self.textWindow.setPlainText("")
    self.show()
    self.w.set_foreground(self.wId)
    self.textWindow.setFocus()

  # Auth Window

  def makeAuthWindow(self):
    authWindow = AuthWindow(self)
    authWindow.show("TwitterPIN")  # Debug

  def makeAuthWindow2(self):
    authWindow = AuthWindow(self)
    authWindow.show("Consumer")

  def makeNotificationWindow(self):
    pass

  def makeDebugwindow(self, *args):
    Fav = NotificationWindow(self)
    Fav.show(Notification_Mode.Favorite)

  def setParam(self, param):
    self.textWindow.setPlainText(param)

  # ---------------------------