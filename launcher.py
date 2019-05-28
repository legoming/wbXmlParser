# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
import sys
import main_window

__author__ = 'Jet CHEN'


if __name__ == '__main__':
    sys.setrecursionlimit(10000)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon/launcher.png'))
    mainWin = QMainWindow()
    ui = main_window.Ui_MainWindow()
    ui.setupUi(mainWin)
    mainWin.show()
    sys.exit(app.exec_())
