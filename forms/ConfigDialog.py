#-*- coding: utf-8 -*-

import sys, os
from PyQt4 import QtCore, QtGui

class cfgDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setGeometry(100, 150, 300, 200)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowTitle(u'Настройка')
        self.tabs = QtGui.QTabWidget(self)

        base = self.makeBase()
        self.tabs.addTab(base, u'Приложени')
        instruments = self.makeInstruments()
        self.tabs.addTab(instruments, u'Инструменты')

        vBox = QtGui.QVBoxLayout(self)
        vBox.addWidget(self.tabs)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply |
                                                QtGui.QDialogButtonBox.Ok) 

        vBox.addWidget(self.buttonBox)

        self.connect(self.buttonBox, QtCore.SIGNAL("clicked(QAbstractButton*)"),
                                                    self.abstractClicked) 

    def abstractClicked(self, button):
        b = self.buttonBox.standardButton(button)
        if b == QtGui.QDialogButtonBox.Ok:
            self.okClicked()
        elif b == QtGui.QDialogButtonBox.Apply:
            self.applyClicked()

    def applyClicked(self):
        print 'apply'

    def okClicked(self):
        print 'ok'

    def makeBase(self):
        w = QtGui.QWidget()
        return w

    def makeInstruments(self):
        w = QtGui.QWidget()

        vBox = QtGui.QVBoxLayout(w)

        vlInstr1 = QtGui.QHBoxLayout()
        vlInstr1.addWidget(QtGui.QLabel(u'Расслоение'))
        self.derLevel = QtGui.QLineEdit('2')
        self.derLevel.setMaximumWidth(50)
        vlInstr1.addWidget(self.derLevel)
        

        vBox.addLayout(vlInstr1)

        return w

