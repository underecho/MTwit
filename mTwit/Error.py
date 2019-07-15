from mTwit.Notification_Ui import NotificationWindow as Ew
from mTwit.Notification_Ui import NotificationMode as Mode


class ErrorNotification(Exception):
    """MTwitでのError基底クラス"""

    def __init__(self, reason, *args):
        self.reason = reason
        super().__init__(*args)

    def show(self):
        """Errorの通知を表示する"""
        Ew(time=2000, message=self.reason).show(Mode.ERROR)

    def __str__(self):
        return self.reason


class MTwitError(ErrorNotification):
    def __init__(self, reason="Unknown Error"):
        super().__init__(reason)
        Exception.__init__(self, reason)
        self.show()


class VerifyError(ErrorNotification):
    def __init__(self, reason="Wrong PINCode or poop Twitter server is here."):
        Exception.__init__(self, reason)
        super().__init__(reason)
        self.show()


class TaskbarError(ErrorNotification):
    def __init__(self, reason="Can't get Taskbar Position"):
        Exception.__init__(self, reason)
        super().__init__(reason)
        pass


if __name__ == "__main__":
    # test reason-able classes
    assert str(MTwitError("john")) == "john"
    assert str(ErrorNotification("john")) == "john"
    assert str(VerifyError("john")) == "john"
    pass
