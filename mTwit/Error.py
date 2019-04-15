import PyQt5
import PyQt5.QtWidgets
from PyQt5.QtWidgets import (QMessageBox, QWidget, QErrorMessage)

class Errorwindow(QErrorMessage):
  def __init__(self, parent=None):
    super(Errorwindow, self).__init__(parent)

    self.parent = parent

  def show(self, message):
    return self.showMessage(message)

class MTwitError(Exception):
  def __init__(self, reason):
    self.reason = reason
    Exception.__init__(self, reason)

  def __str__(self):
    return self.reason

class VerifyError(Exception):
  def __init__(self):
    self.reason = "Wrong PINCode or poop Twitter server is here."
    Exception.__init__(self, self.reason)
    pass

  def __str__(self):
    return self.reason