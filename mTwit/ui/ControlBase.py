from PyQt5 import QtGui
from PyQt5.QtWidgets import QPushButton


class MTwitButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.styleSheet(
            """
            MTwitButton {
                background-color: rgba(200, 200, 200, 0);
                border: 0px solid gray;
            }

            MTwitButton:hover {
                background-color: rgba(200, 200, 200, 0.2);
            }
            """
        )


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
