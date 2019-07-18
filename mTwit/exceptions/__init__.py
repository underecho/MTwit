# exceptions base
from mTwit.ui import NotificationWindow as Ew
from mTwit.ui.NotificationWindow import NotificationMode as Mode
from debtcollector import removals


class ErrorNotification(Exception):
    """MTwitでのError基底クラス"""

    def __init__(self, reason, *args):
        self.reason = reason
        super().__init__(*args)

    @removals.remove
    def show(self):  # Delete this
        """Errorの通知を表示する"""
        Ew(time=2000, message=self.reason).show(Mode.ERROR)

    def __str__(self):
        return self.reason

