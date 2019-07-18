import win32gui  # need manual install pywin32
import warnings
from mTwit.exceptions.ui import TaskbarError
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import (
    QPushButton,
    QDesktopWidget)


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

    taskbar_size: QSize = QSize(
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
        self.setIcon(QtGui.QIcon("resources/icon/quit.png"))
        self.setStyleSheet("background-color: Transparent;"
                           "left: -2px;"
                           "border: 0px solid gray;")
        self.resize(24, 24)

    def setButtonPosition(self, window_size):
        self.move(window_size.width() - 26, 2)
