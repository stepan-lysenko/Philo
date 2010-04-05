#-*- coding: utf-8 -*-

import sys, os
from PyQt4 import QtCore, QtGui

class cfgDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowTitle(u'Настройка')
