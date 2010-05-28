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
#        self.instruments = self.makeInstruments()
#        self.tabs.addTab(self.instruments, self.tr('Instruments'))

        vBox = QtGui.QVBoxLayout(self)
        vBox.addWidget(self.tabs)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply |
                                                QtGui.QDialogButtonBox.Ok) 

        vBox.addWidget(self.buttonBox)

        self.connect(self.buttonBox, QtCore.SIGNAL(
                        "clicked(QAbstractButton*)"), self.abstractClicked) 

    def retranslateUi(self):
        self.setWindowTitle(self.tr('Configuration'))
        self.tabs.setTabText(self.tabs.indexOf(self.base), self.tr('Main'))
        self.tabs.setTabText(self.tabs.indexOf(self.instruments),
                                                self.tr('Instruments'))
        self.lLam.setText(self.tr('Lamination'))

    def abstractClicked(self, button):
        b = self.buttonBox.standardButton(button)
        if b == QtGui.QDialogButtonBox.Ok:
            self.okClicked()
        elif b == QtGui.QDialogButtonBox.Apply:
            self.applyClicked()

    def applyClicked(self):
        self.emit(QtCore.SIGNAL('ChangeLanguage(QString *)'),
                                        self.cLang.currentText())

    def okClicked(self):
        self.applyClicked()
        self.close()

    def makeBase(self):
        w = QtGui.QWidget()

        self.lLang = QtGui.QLabel(self.tr('Language'))

        self.cLang = QtGui.QComboBox()
        for Files, Bill, Bob in os.walk('./tr/'):
            break    
        self.cLang.addItem('English')    
        for f in Bob:
            if len(f) > 3:
                if f[len(f) - 3:] == '.qm':
                    self.cLang.addItem(f[:len(f) - 3])

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.lLang)
        hbox.addWidget(self.cLang)
        
        Box = QtGui.QVBoxLayout(w)
        Box.addLayout(hbox)
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

