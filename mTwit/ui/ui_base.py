import win32gui
import pywintypes
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QDesktopWidget

from mTwit.exceptions.ui import TaskbarError


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
        try:  # This code is ignore exception
            win32gui.SetForegroundWindow(self.handle)
        except pywintypes.error:
            pass


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
