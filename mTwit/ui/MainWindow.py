import tweepy
from PyQt5.QtCore import (
    Qt,
    QPoint,
    QSize,
    QCoreApplication
)

from PyQt5.QtGui import (
    QIcon,
    QKeySequence
)

from PyQt5.QtWidgets import (
    QDesktopWidget,
    QMainWindow,
    QAction,
    QMenu,
    QPlainTextEdit,
    QShortcut,
    QSystemTrayIcon
)

from system_hotkey import SystemHotkey

from mTwit.ui.ui_base import Win32Window, HoverButton, QuitButton
from .NotificationWindow import NotificationWindow, NotificationMode
from .AuthWindow import AuthWindow

class MainWindow(QMainWindow):
    iconPath = "image/send.png"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.w = Win32Window.from_qwindow(self)

        self.mwidget = QMainWindow(self)
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint)
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
            "color: #FFFFFF;")
        self.textWindow.setPlaceholderText("What's Happening?")

        # Quit Button
        self.qbtn = QuitButton(self)
        self.qbtn.setButtonPosition(self.size())

        # Tweet Button
        self.tbtn = HoverButton(self)
        self.tbtn.resize(48, 48)
        self.tbtn.move(420, 62)
        self.tbtn.setObjectName('tButton')
        self.tbtn.setIcon(QIcon("image/send.png"))
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

    def Firstshow(self):  # check user data and init api

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
        self.restoreAction = QAction(
            "&Restore", self, triggered=self.showNormal)
        self.quitAction = QAction("&Quit", self, triggered=self.quitEvent)
        self.debugMakeWindowAction = QAction(
            "&DebugMakeAuth", self, triggered=self.makeAuthWindow)
        self.debugMakeWindow2Action = QAction(
            "&DebugMake2Auth", self, triggered=self.makeAuthWindow2)
        self.debugMakeWindow3Action = QAction(
            "&DebugMake3(Notification)", self, triggered=self.makeDebugwindow)

    def showEvent_(self):
        self.textWindow.setPlainText("")
        self.show()
        self.w.focus()
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
        fav = NotificationWindow(self, message="Test Message.")
        fav.show(NotificationMode.ERROR)
        """
    try:
      raise MTwitError
    except:
      pass
    """

    def setParam(self, param):
        self.textWindow.setPlainText(param)

    # ---------------------------
