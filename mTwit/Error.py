import PyQt5
import PyQt5.QtWidgets
from PyQt5.QtWidgets import (QMessageBox, QWidget, QErrorMessage)
from mTwit.Notification_Ui import NotificationWindow as Ew
from mTwit.Notification_Ui import Notification_Mode as Mode


class ErrorNotification(Exception):
  """MTwitでのError基底クラス"""

  def __init__(self, reason, *args):
    self.reason = reason
    super().__init__(*args)

  def show(self):
    """Errorの通知を表示する"""
    Ew(time=2000, message=self.reason).show(Mode.Error)


class MTwitError(ErrorNotification):
  def __init__(self, reason="Unknown Error"):
    self.reason = reason
    super().__init__(reason)
    Exception.__init__(self, reason)
    self.show()

  def __str__(self):
    return self.reason


class VerifyError(ErrorNotification):
  def __init__(self, reason="Wrong PINCode or poop Twitter server is here."):
    self.reason = reason
    Exception.__init__(self, self.reason)
    super().__init__(self.reason)
    self.show()

  def __str__(self):
    return self.reason


class TaskbarError(ErrorNotification):
  def __init__(self):
    self.reason = "Can't get Taskbar Position"
    Exception.__init__(self, self.reason)
    super().__init__(self.reason)
    pass

  def __str__(self):
    return self.reason