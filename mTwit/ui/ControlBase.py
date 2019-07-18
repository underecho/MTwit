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
