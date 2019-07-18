#!/usr/bin/env -S py -3.7

import sys
from mTwit.ui import MainWindow
from PyQt5.QtWidgets import QApplication


app = QApplication(sys.argv)
app.setStyleSheet(
    "QMainWindow{background-image: url('resources/backgrounds/window.png');border: 0px solid black;}")

window = MainWindow()
sys.exit(app.exec_())
