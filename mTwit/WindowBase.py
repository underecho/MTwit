from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QDesktopWidget


class MTwitWindow(QWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)

    def moveToCenter(self):
        desktop = QDesktopWidget()
        desktopSize = (
            desktop.screenGeometry().width(),
            desktop.screenGeometry().height(),
            desktop.availableGeometry().width(),
            desktop.availableGeometry().height()
        )

        self.resize(desktopSize[0] / 1.5, 30)
