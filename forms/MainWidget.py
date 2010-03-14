#-*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import string

class MainWidget(QtGui.QWidget):
	
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        TabWidget = QtGui.QTabWidget()

        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(TabWidget)

    def SaveListAs(self):
        return

    def OpenList(self):
        return
