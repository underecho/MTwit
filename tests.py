import sys
import re

from PyQt5.QtWidgets import (QApplication, QFormLayout, QLabel, QDialog, QLineEdit, QPushButton)

from PyQt5 import QtCore, QtGui


class AnimatedLabel(QLabel):
    def __init__(self):
        QLabel.__init__(self)

        color1 = QtGui.QColor(255, 0, 0)
        color2 = QtGui.QColor(255, 144, 0)
        color3 = QtGui.QColor(255, 255, 0)
        color4 = QtGui.QColor(224, 192, 192)

        color5 = QtGui.QColor(192, 224, 192)
        color6 = QtGui.QColor(192, 192, 192)
        color7 = QtGui.QColor(212, 208, 200)

        self.co_get = 0
        self.co_set = 0

        byar = QtCore.QByteArray()
        byar.append('zcolor')
        self.color_anim = QtCore.QPropertyAnimation(self, byar)
        self.color_anim.setStartValue(color4)
        self.color_anim.setKeyValueAt(0.15, color1)
        self.color_anim.setKeyValueAt(0.3, color2)
        self.color_anim.setKeyValueAt(0.5, color3)
        self.color_anim.setKeyValueAt(0.75, color2)
        self.color_anim.setEndValue(color4)
        self.color_anim.setDuration(2000)
        self.color_anim.setLoopCount(1)

        self.color_anim_ok = QtCore.QPropertyAnimation(self, byar)
        self.color_anim_ok.setStartValue(color5)
        self.color_anim_ok.setKeyValueAt(0.5, color6)
        self.color_anim_ok.setEndValue(color7)
        self.color_anim_ok.setDuration(1000)
        self.color_anim_ok.setLoopCount(-1)

        self.custom_anim = QtCore.QPropertyAnimation(self, byar)

    def parseStyleSheet(self):
        ss = self.styleSheet()
        sts = [s.strip() for s in ss.split(';') if len(s.strip())]
        return sts

    def getBackColor(self):
        self.co_get += 1
        # print(fuin(), self.co_get)
        return self.palette().color(self.pal_ele)

    def setBackColor(self, color):
        self.co_set += 1
        sss = self.parseStyleSheet()
        bg_new = 'background-color: rgba(%d,%d,%d,%d);' % (color.red(), color.green(), color.blue(), color.alpha())

        for k, sty in enumerate(sss):
            if re.search('\Abackground-color:', sty):
                sss[k] = bg_new
                break
        else:
            sss.append(bg_new)

        # pal = self.palette()
        # pal.setColor(self.pal_ele, color)
        # self.setPalette(pal)
        self.setStyleSheet('; '.join(sss))

    pal_ele = QtGui.QPalette.Window
    zcolor = QtCore.pyqtProperty(QtGui.QColor, getBackColor, setBackColor)


# this class is only for test
class SomeDia2(QDialog):
    def __init__(self, parent=None):
        """Sets up labels in form"""
        QDialog.__init__(self, parent)

        self.co_press = 0

        self.setModal(True)
        self.setWindowTitle('Animation Example')

        self.edit_pad =  QLineEdit('-1')
        self.edit_rad =  QLineEdit('-1')
        self._mapHeight = QLineEdit('0')

        self.layout = QFormLayout()
        self.lab_pad = QLabel('Padding (px):')
        self.lab_rad = QLabel('Radius (px):' )
        self.layout.addRow(self.lab_pad, self.edit_pad)
        self.layout.addRow(self.lab_rad, self.edit_rad)

        self.anila = AnimatedLabel()
        self.anila.setText('Label for animation:')
        # self.anila.setStyleSheet('padding: 0 4px; border-radius: 4px;')
        self.layout.addRow(self.anila, self._mapHeight)

        self.ok = QPushButton()
        self.ok.setText('OK -- change animation')
        self.ok.clicked.connect(self._okPress)

        self.layout.addRow(self.ok)
        self.layout.setLabelAlignment(QtCore.Qt.AlignRight)

        self.setLayout(self.layout)
        self.set_initial_data()

    def set_initial_data(self):
        pad_vali = QtGui.QIntValidator(0, 20)
        rad_vali = QtGui.QIntValidator(0, 10)

        self.edit_pad.setValidator(pad_vali)
        self.edit_rad.setValidator(rad_vali)

        pad, rad = 4, 4
        self.edit_pad.setText(str(pad))
        self.edit_rad.setText(str(rad))

        self.set_ss(pad, rad)

        # slots
        self.edit_pad.textChanged.connect(self.change_padrad)
        self.edit_rad.textChanged.connect(self.change_padrad)

    def set_ss(self, pad, rad):
        self.anila.setStyleSheet('padding: 0 %dpx; border-radius: %dpx;' % (pad, rad))
        for lab in [self.lab_rad, self.lab_pad]:
            lab.setStyleSheet('padding: 0 %dpx;' % pad)

    def change_padrad(self):
        try:
            pad = int(self.edit_pad.text())
            rad = int(self.edit_rad.text())
            # print(pad, rad)
            self.set_ss(pad, rad)
        except Exception as ex:
            print(type(ex).__name__)

    def _okPress(self, flag):
        # print('OK PRESS', flag)
        self.co_press += 1
        typ = self.co_press % 3
        if 0 == typ:
            print('Animation NO')
            self.anila.color_anim.stop()
            self.anila.color_anim_ok.stop()
        elif 1 == typ:
            print('Animation type 1')
            self.anila.color_anim_ok.stop()
            self.anila.color_anim.start()
        elif 2 == typ:
            print('Animation type 2')
            self.anila.color_anim.stop()
            self.anila.color_anim_ok.start()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    dia = SomeDia2()
    dia.show()

    app.exec_()