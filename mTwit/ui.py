import re
import sys
import tweepy.error
import win32gui
import warnings
from mTwit.Error import TaskbarError
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QCoreApplication, Qt, QPoint, QSize
from PyQt5.QtGui import QIcon, QKeySequence, QWindow
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


class Win32Window:

    @classmethod
    def from_qwindow(cls, window: QWindow):
        return cls(window.winId())

    @classmethod
    def find(cls, class_name: str, window_name: str):
        return cls(win32gui.FindWindow(class_name, window_name))

    def __init__(self, handle):
        self._handle = handle

    @property
    def handle(self):
        return self._handle

    def focus(self):
        win32gui.SetForegroundWindow(self.handle)


def taskbar_info() -> (str, int, int):
    desktop_rect = QDesktopWidget().availableGeometry()
    screen_rect = QDesktopWidget().screenGeometry()

    taskbar_size = QSize(
        screen_rect.width() - desktop_rect.width(),
        screen_rect.height() - desktop_rect.height()
    )

    # if horizontal
    if taskbar_size.width() != 0:
        if desktop_rect.x() != 0:
            return "left", taskbar_size.width(), screen_rect.height()
        else:
            return "right", taskbar_size.width(), screen_rect.height()

    # if vertical
    if taskbar_size.height() != 0:
        if desktop_rect.y() != 0:
            return "upper", screen_rect.width(), taskbar_size.height()
        else:
            return "lower", screen_rect.width(), taskbar_size.height()

    # unreachable
    raise TaskbarError


def deprecated(a: any):
    warnings.warn(f"{a.__name__} is deprecated.", DeprecationWarning)
    return a


@deprecated
class WindowMgr:
    """
    WindowMgr class provides utilities for generic window operation.
    The class encapsulates platform-depent features as indepent.
    NOTE: Currently working on Win32 only.
    """

    def __init__(self):
        """Constructor"""
        self._handle = None

    @deprecated
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

    @deprecated
    def set_foreground(self, Id):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(Id)

    @deprecated
    def getTaskbar(self):
        return taskbar_info()


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
