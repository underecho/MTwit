from . import ErrorNotification

class TaskbarError(ErrorNotification):
    def __init__(self, reason="Couldn't get Taskbar Position"):
        Exception.__init__(self, reason)
        super().__init__(reason)
        pass