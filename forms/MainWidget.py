#-*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import string

class MainWidget(QtGui.QWidget):

    def NewTab(self):
        Tab = PhiloTab()
        self.TabWidget.addTab(Tab, "Tab1")

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.TabWidget = QtGui.QTabWidget()
        self.NewTab()

        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(self.TabWidget)

    def SaveListAs(self):
        return

    def OpenList(self):
        return

class PhiloTab(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.lvThesis = QtGui.QListWidget()
        self.lvThesis.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.lvThesis.setSortingEnabled(1)

        spacer1 = QtGui.QSpacerItem(5, 0, QtGui.QSizePolicy.Minimum,
                                                QtGui.QSizePolicy.Maximum)

        self.teThesisView = QtGui.QTextEdit()

        spacer2 = QtGui.QSpacerItem(5, 0, QtGui.QSizePolicy.Minimum,
                                                QtGui.QSizePolicy.Maximum)

        Box = QtGui.QHBoxLayout(self)
        Box.addWidget(self.lvThesis)
        Box.addItem(spacer1)
        Box.addWidget(self.teThesisView)
        Box.addItem(spacer2)
