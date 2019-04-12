import PyQt5
import PyQt5.QtWidgets
from PyQt5.QtWidgets import (QMessageBox, QWidget, QErrorMessage)

class Errorwindow(QErrorMessage):
    def __init__(self, parent=None):
        super(Errorwindow, self).__init__(parent)

        self.parent = parent

    def show(self, message):
        return self.showMessage(message)
