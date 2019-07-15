import re
import sys
import tweepy.error
import win32gui
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QCoreApplication, Qt, QPoint, QSize
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (
    QPushButton,
    QDesktopWidget,
    QMainWindow,
    QAction,
    QMenu,
    QPlainTextEdit,
    QShortcut,
    QSystemTrayIcon)
from system_hotkey import SystemHotkey


class WindowMgr:
    """
    WindowMgr class provides utilities for generic window operation.
    The class encapsulates platform-depent features as indepent.
    NOTE: Currently working on Win32 only.
    """

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
        print(self._handle)  # Debug

    def set_foreground(self, Id):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(Id)

    def getTaskbar(self):
        """Return Taskbar position and Size (position, width, height)"""
        desktopSize = QDesktopWidget().availableGeometry()
        screenSize = (QDesktopWidget().screenGeometry().width(),
                      QDesktopWidget().screenGeometry().height())
        taskbarSize = (
            screenSize[0] -
            desktopSize.width(),
            screenSize[1] -
            desktopSize.height())
        if taskbarSize[0] != 0:  # position is left or right
            if desktopSize.x() != 0:  # left
                return "left", taskbarSize[0], screenSize[1]
            else:
                return "right", taskbarSize[0], screenSize[1]

        if taskbarSize[1] != 0:  # position is upper or lower
            if desktopSize.y() != 0:  # upper
                return "upper", screenSize[0], taskbarSize[1]
            else:
                return "lower", screenSize[0], taskbarSize[1]

        raise TaskbarError


class HoverButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

    def enterEvent(self, QEvent):
        self.setStyleSheet("background-color: rgba(200, 200, 200, 0.2);"
                           "border: 0px solid gray;")

    def leaveEvent(self, QEvent):
        self.setStyleSheet("background-color: rgba(200, 200, 200, 0);"
                           "border: 0px solid gray;")


class QuitButton(HoverButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicked.connect(parent.hide)
        self.setIcon(QtGui.QIcon("image/quit.png"))
        self.setStyleSheet("background-color: Transparent;"
                           "left: -2px;"
                           "border: 0px solid gray;")
        self.resize(24, 24)

    def setButtonPosition(self, window_size):
        self.move(window_size.width() - 26, 2)
