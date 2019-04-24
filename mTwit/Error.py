import PyQt5
import PyQt5.QtWidgets
from PyQt5.QtWidgets import (QMessageBox, QWidget, QErrorMessage)

class ErrorNotification(Exception):
  def __init__(self, reason, *args):
    super().__init__(*args)
    from mTwit.ui import NotificationWindow as Ew
    from mTwit.ui import Notification_Mode as Mode
    Err = Ew() 
    Ew.show(Mode.Error)

class MTwitError(ErrorNotification):
  def __init__(self, reason):
    self.reason = reason
    Exception.__init__(self, reason)
    super().__init__(self.reason)

  def __str__(self):
    return self.reason

class VerifyError(ErrorNotification):
  def __init__(self):
    self.reason = "Wrong PINCode or poop Twitter server is here."
    Exception.__init__(self, self.reason)
    super().__init__(self.reason)

  def __str__(self):
    return self.reason

class TaskbarError(ErrorNotification):
  def __init__(self, *args, **kwargs):
    self.reason = "Can't get Taskbar Position"
    Exception.__init__(self, self.reason)
    super().__init__(self.reason)
    pass

  def __str__(self):
    return self.reason