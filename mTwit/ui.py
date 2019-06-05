from mTwit.Authwindow_Ui import *
from mTwit.Error import *
import tweepy.error
import win32gui, re
import time # Debug

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

  def getTaskbar(self):
    """Return Taskbar position and Size (position, width, height)"""
    desktopSize = QDesktopWidget().availableGeometry()
    screenSize = (QDesktopWidget().screenGeometry().width(), QDesktopWidget().screenGeometry().height())
    taskbarSize = (screenSize[0] - desktopSize.width(), screenSize[1] - desktopSize.height())
    if taskbarSize[0] != 0: # position is left or right
      if desktopSize.x() != 0: # left
        return ("left", taskbarSize[0], screenSize[1])
      else:
        return ("right", taskbarSize[0], screenSize[1])

    if taskbarSize[1] != 0:  # position is upper or lower
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
    self.textWindow.setStyleSheet(
      "background-color: rgba(0,0,0,50);"
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
      print(self.api.update_status(text))
      # print(self.api.mentions_timeline(count=200))
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
    from mTwit.Notification_Ui import NotificationWindow
    from mTwit.Notification_Ui import Notification_Mode
    # fav = NotificationWindow(self)
    # fav.show(Notification_Mode.Error)
    try:
      raise MTwitError
    except:
      pass

  def setParam(self, param):
    self.textWindow.setPlainText(param)

  # ---------------------------