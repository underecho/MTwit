from PyQt5.QtWidgets import (QMessageBox,QApplication, QWidget, QToolTip, QPushButton,
                             QDesktopWidget, QMainWindow, QAction, qApp, QToolBar, QVBoxLayout,
                             QComboBox,QLabel,QLineEdit,QGridLayout,QMenuBar,QMenu,QStatusBar,
                             QPlainTextEdit,QDialog,QFrame,QProgressBar,QShortcut,QSystemTrayIcon
                             )
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon,QFont,QPixmap,QPalette,QKeySequence
from PyQt5.QtCore import QCoreApplication, Qt,QBasicTimer, QPoint, QSize
import sys
import Auth
import tweepy.error
import win32gui, re
from system_hotkey import SystemHotkey

api = Auth.api
auth = Auth.auth


class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
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


class tbtn(QPushButton):
    def __init__(self, parent=None):
        super(tbtn, self).__init__(parent)

    def enterEvent(self, QEvent):
        self.setStyleSheet("background-color: rgba(200, 200, 200, 60);"
                           "border: 0px solid gray;")

    def leaveEvent(self, QEvent):
        self.setStyleSheet("background-color: rgba(200, 200, 200, 0);"
                           "border: 0px solid gray;")


class mainWindow(QMainWindow):
    iconPath = "image/send.png"
    w = WindowMgr()
    w.find_window_wildcard("MTwit")

    def __init__(self, parent=None):
        super(mainWindow, self).__init__()

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
        self.textWindow.resize(400,100)
        self.textWindow.move(10,10)
        self.textWindow.setStyleSheet("background-color: rgba(0,0,0,50);"
                                      "border: 1px solid gray;"
                                      "font: 14pt 'Meiryo UI' ;"
                                      "color: #FFFFFF;")
        self.textWindow.setPlaceholderText("What's Happening?")

        # Quit Button
        self.qbtn = QPushButton('', self)
        self.qbtn.clicked.connect(self.hide)
        self.qbtn.setIcon(QtGui.QIcon("image/quit.png"))
        self.qbtn.setStyleSheet("background-color: Transparent;"
                                "left: -2px;"
                                "border: 1px solid gray;")
        self.qbtn.resize(24, 24)
        self.qbtn.move(455, 2)

        # Tweet Button
        self.tbtn = tbtn(self)
        self.tbtn.resize(48, 48)
        self.tbtn.move(420, 62)
        self.tbtn.setObjectName('tButton')
        self.tbtn.setIcon(QtGui.QIcon("image/send.png"))
        self.tbtn.setIconSize(QSize(32,32))
        self.tbtn.setStyleSheet("background-color: rgba(200, 200, 200, 0);")
        self.tbtn.clicked.connect(self.tweetEvent)

        # tweet Shortcut
        self.tShortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Return), self)
        self.tShortcut.activated.connect(self.tweetEvent)

        # window show Shortcut
        hk = SystemHotkey(consumer=self.ShowOrHide)
        hk.register(('alt', 'shift', 'f1'))

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
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    # windowMove End --
    def tweetEvent(self):
        print("tweetActivated")
        self.hide()
        text = self.textWindow.document().toPlainText()
        self.textWindow.setPlainText("")
        try:
            api.update_status(text)
        except tweepy.error.TweepError:
            pass



    def quitEvent(self):
        self.trayIcon.hide()
        hk.unregister(('alt', 'shift', 'f1'))
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

    def ShowOrHide(self, arg1, arg2, arg3):
        if self.isHidden():
            self.showEvent_()
        else:
            self.hide()

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
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

    def showEvent_(self):
        self.textWindow.setPlainText("")
        self.show()
        self.w.set_foreground()

app = QApplication(sys.argv)
app.setStyleSheet("QMainWindow{background-image: url(image/window.png);border: 0px solid black};"
                  "QPushButton{background-color: black};")

ex = mainWindow()
sys.exit(app.exec_())