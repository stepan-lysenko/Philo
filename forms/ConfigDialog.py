#-*- coding: utf-8 -*-

import sys, os
from PyQt4 import QtCore, QtGui

class cfgDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setGeometry(100, 150, 300, 200)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowTitle(self.tr('Configuration'))
        self.tabs = QtGui.QTabWidget(self)

        self.base = self.makeBase()
        self.tabs.addTab(self.base, self.tr('Main'))
        self.instruments = self.makeInstruments()
        self.tabs.addTab(self.instruments, self.tr('Instruments'))

        vBox = QtGui.QVBoxLayout(self)
        vBox.addWidget(self.tabs)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply |
                                                QtGui.QDialogButtonBox.Ok) 

        vBox.addWidget(self.buttonBox)

        self.connect(self.buttonBox, QtCore.SIGNAL(
                        "clicked(QAbstractButton*)"), self.abstractClicked) 

    def retranslateUI(self):
        self.setWindowTitle(self.tr('Configuration'))
        self.tabs.setTabText(self.tabs.indexOf(self.base), self.tr('Main'))
        self.tabs.setTabText(self.tabs.indexOf(self.instuments),
                                                self.tr('Instrumments'))
        self.lLam.setText(self.tr('Lamination'))

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
        self.lLam = QtGui.QLabel(self.tr('Lamination'))
        vlInstr1.addWidget(self.lLam)
        self.derLevel = QtGui.QLineEdit('2')
        self.derLevel.setMaximumWidth(50)
        vlInstr1.addWidget(self.derLevel)
        

        vBox.addLayout(vlInstr1)

        return w

