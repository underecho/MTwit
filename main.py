#!/usr/bin/env py -3-32
# -*- coding: utf-8 -*-

import sys
from mTwit.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication

# api = Auth.api  # Twitter Rest API Object (Option GUI Required)
# auth = Auth.auth # Tweepy Auth Object (Option GUI Required)

app = QApplication(sys.argv)
app.setStyleSheet(
    "QMainWindow{background-image: url('image/window.png');border: 0px solid black;}")

window = MainWindow()
sys.exit(app.exec_())
