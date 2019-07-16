from . import ErrorNotification

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


