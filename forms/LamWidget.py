#-*- coding: utf-8 -*-

import sys, os, ThesisBase
from PyQt4 import QtCore, QtGui

class lamDialog(QtGui.QDialog):
    def __init__(self, parent, items):
        QtGui.QDialog.__init__(self, parent)

        self.setGeometry(100, 150, 200, 300)
        self.setMaximumSize(300, 500)
#        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowTitle(self.tr('Lamination'))

        vBox = QtGui.QVBoxLayout(self)

        self.labels = []
        for i in items:
            tmp = QtGui.QLabel(i.text())
            self.labels.append(tmp)
            vBox.addWidget(tmp)

        self.lvThesis = QtGui.QListWidget()
        self.lvThesis.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.lvThesis.setSelectionMode(
                        QtGui.QAbstractItemView.ExtendedSelection)

        vBox.addWidget(self.lvThesis)

    def addThesis(self, thesis):
        self.lvThesis.addItem(thesis)

    def retranslateUi(self):
        self.setWindowTitle(self.tr('Lamination'))

    def closeEvent(self, event):
            event.accept()

