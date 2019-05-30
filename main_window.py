# -*- coding: utf-8 -*-

import binascii
import os
import platform
import subprocess
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QMenuBar, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget

# import wbxml # wbxml only support python2, and cannot install properly on mojave

sys.setrecursionlimit(10000)

dirWorking = os.getcwd()
# print("current working dir is " + dirWorking)
try:
    dirScript = sys._MEIPASS
# print("current running dir of tool is " + dirScript)
except Exception:
    dirScript = os.path.dirname(os.path.realpath(__file__))
# print("current running dir of script is " + dirScript)


class Ui_MainWindow(object):
    def text_inputChanged(self):
        self.timer_wait_to_refresh.start(1500)

    def refresh_output_when_timeout(self):
        self.timer_wait_to_refresh.stop()
        a_input = self.text_input.toPlainText()
        print('\ninputed data\n' + a_input)
        cmd = 'wbxml2xml'
        try:
            ishex = int(a_input[:5], 16)
            finput = open(dirScript + '/input_file', 'wb')
            a_input = "".join(a_input.split())
            a = [a_input[i:i + 2] for i in range(0, len(a_input), 2)]
            for aa in a:
                finput.write(binascii.unhexlify(aa))
            finput.close()
        except Exception as e:
            finput = open(dirScript + '/input_file', 'w')
            finput.writelines(a_input)
            finput.close()
            cmd = 'xml2wbxml'
        fullcmd = 'export PATH=/usr/local/bin:$PATH;' + cmd + ' -o ' + dirScript + '/output_file ' + dirScript + '/input_file'
        output = subprocess.getstatusoutput(fullcmd)
        self.label_parse_result.setText(cmd) if output[0] == 0 else self.label_parse_result.setText(cmd + " failed")
        if output[0] == 0:
            if cmd == "xml2wbxml":
                try:
                    with open(dirScript + '/output_file', "rb") as binary_file:
                        # Read the whole file at once
                        data = binary_file.read()
                        chs = ""
                        for ch in data:
                            chs += "{0:02x}".format(ch)
                        print('\nconverted wbxml\n' + chs)
                        self.text_output.setText(chs)
                except Exception as e:
                    print(str(e))
                    self.text_output.setText('Exception:\n' + str(e))
            else:
                try:
                    with open(dirScript + '/output_file', 'r') as xml_file:
                        data = xml_file.read()
                        print('\nconverted xml\n' + data)
                        self.text_output.setPlainText(data)
                except Exception as e:
                    print(str(e))
                    self.text_output.setText('Exception:\n' + str(e))
        else:
            self.text_output.setText(output[1])

    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1024, 600)
        # self.centralwidget = QtWidgets.QWidget(main_window)
        # self.centralwidget.setObjectName("centralwidget")
        # main_window.setCentralWidget(self.centralwidget)
        font = QFont('Roboto')
        font.setPointSize(16)

        fontmono = QFont('SF Mono')

        self.menubar = QMenuBar(main_window)
        if platform.uname().system == 'Darwin':
            self.menubar.setNativeMenuBar(True)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.subtitle = QHBoxLayout()
        self.label_input = QLabel()
        self.label_input.setFont(font)
        self.label_input.setAlignment(Qt.AlignCenter)
        self.label_input.setText("copy paste XML/WBXML here")

        self.label_parse_result = QLabel()
        self.label_parse_result.setFont(font)
        self.label_parse_result.setAlignment(Qt.AlignCenter)
        self.label_parse_result.setText("converted output")

        self.subtitle.addWidget(self.label_input)
        self.subtitle.addWidget(self.label_parse_result)

        self.text_input = QTextEdit()
        self.text_input.setAcceptRichText(False)
        self.text_input.setFont(fontmono)
        self.text_input.resize(450, 600)
        self.text_input.textChanged.connect(self.text_inputChanged)
        self.timer_wait_to_refresh = QTimer()
        self.timer_wait_to_refresh.setSingleShot(True)
        self.timer_wait_to_refresh.timeout.connect(self.refresh_output_when_timeout)

        self.text_output = QTextEdit()
        self.text_output.setFont(fontmono)
        self.text_output.resize(450, 600)
        self.text_output.setReadOnly(True)
        # self.text_output.setStyleSheet("background-color: gray")

        self.hbox = QHBoxLayout()
        # self.hbox.addStretch()
        self.hbox.addWidget(self.text_input)
        self.hbox.addWidget(self.text_output)
        # self.hbox.addStretch()

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.subtitle)
        self.vbox.addLayout(self.hbox)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.vbox)
        main_window.setCentralWidget(self.mainWidget)

        main_window.setWindowTitle('JC WBXML Decoder')

        QtCore.QMetaObject.connectSlotsByName(main_window)
