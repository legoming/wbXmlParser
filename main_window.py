# -*- coding: utf-8 -*-

import sys
import os
import platform
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QMenuBar, QTextEdit, QAction, QFileDialog, QTableWidgetItem, QPushButton, QDialog, QMessageBox, QDesktopWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QWidget
from PyQt5.QtCore import QPoint, QTimer
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor, QPalette
from enum import Enum, unique
from lxml import etree
# import wbxml # wbxml only support python2, and cannot install properly on mojave

sys.setrecursionlimit(10000)

dirWorking = os.getcwd()
#print("current working dir is " + dirWorking)
try:
	dirScript = sys._MEIPASS
	#print("current running dir of tool is " + dirScript)
except Exception:
	dirScript = os.path.dirname(os.path.realpath(__file__))
	#print("current running dir of script is " + dirScript)

class Ui_MainWindow(object):
    def textInput1Changed(self):
        self.timer1.start(1500)

    def time1Timeout(self):
        self.timer1.stop()
        a_input = self.textInput1.toPlainText()
        print(a_input)
        cmd = '/usr/local/Cellar/libwbxml/0.11.6_1/bin/wbxml2xml -l WML10 -m0'
        try:
            ishex = int(a_input[:5], 16)
            label = 'wbxml -> xml'
            print(label)
            a_input = a_input.strip()
            print(a_input)
        except Exception as e:
            label = 'xml -> wbxml'
            print(label)
            cmd = '/usr/local/Cellar/libwbxml/0.11.6_1/bin/xml2wbxml -a -v 1.0'
        cmd = cmd + ' -o ' + dirScript + '/output_file ' + dirScript + '/input_file'
        finput = open(dirScript + '/input_file', 'w')
        finput.writelines(a_input)
        finput.close()
        output = subprocess.getstatusoutput(cmd)
        print(cmd)
        print(output)
        self.lable2.setText("Parsed " + label + " Done") if output[0] == 0 else self.lable2.setText("Parsed " + label + " Failed")
        if output[0] == 0:
            if label == "xml -> wbxml":
                try:
                    with open(dirScript + '/output_file', "rb") as binary_file:
                        # Read the whole file at once
                        data = binary_file.read()
                        chs = ""
                        for ch in data:
                            chs += "{0:02x}".format(ch)
                        self.textInput2.setText(chs)
                except Exception as e:
                    print(str(e))
                    self.textInput2.setText('Exception:\n' + str(e))
        else:
            self.textInput2.setText(output[1])


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)
        # self.centralwidget = QtWidgets.QWidget(MainWindow)
        # self.centralwidget.setObjectName("centralwidget")
        # MainWindow.setCentralWidget(self.centralwidget)
        font = QFont()
        font.setPointSize(15)

        self.menubar = QMenuBar(MainWindow)
        if platform.uname().system == 'Darwin':
            self.menubar.setNativeMenuBar(True)
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 50))
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.subtitle = QHBoxLayout()
        self.lable1 = QLabel()
        self.lable1.setText("Copy paste WBXML or XML here")

        self.lable2 = QLabel()
        self.lable2.setText("Parsed Output")

        self.subtitle.addWidget(self.lable1)
        self.subtitle.addWidget(self.lable2)

        self.textInput1 = QTextEdit()
        self.textInput1.setAcceptRichText(False)
        self.textInput1.resize(450, 600)
        self.textInput1.textChanged.connect(self.textInput1Changed)
        self.timer1 = QTimer()
        self.timer1.setSingleShot(True)
        self.timer1.timeout.connect(self.time1Timeout)

        self.textInput2 = QTextEdit()
        self.textInput2.resize(450, 600)
        self.textInput2.setReadOnly(True)
        #self.textInput2.setStyleSheet("background-color: gray")

        self.hbox = QHBoxLayout()
        #self.hbox.addStretch()
        self.hbox.addWidget(self.textInput1)
        self.hbox.addWidget(self.textInput2)
        #self.hbox.addStretch()

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.subtitle)
        self.vbox.addLayout(self.hbox)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.vbox)
        MainWindow.setCentralWidget(self.mainWidget)

        MainWindow.setWindowTitle('JC WBXML Parser')

        QtCore.QMetaObject.connectSlotsByName(MainWindow)


