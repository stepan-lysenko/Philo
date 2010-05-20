#-*- coding: utf-8 -*-

import sys, os, ThesisBase
from PyQt4 import QtCore, QtGui

class lamDialog(QtGui.QDialog):
    curName = QtCore.QString()
    allThesises = {}

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

        self.makeConMenu()
        self.lvThesis = QtGui.QListWidget()
        self.lvThesis.contextMenuEvent = self.listMenu
        self.connect(self.lvThesis, QtCore.SIGNAL(
                'itemSelectionChanged()'), self.selectionChanged)
#        self.connect(self.lvThesis, QtCore.SIGNAL(
#                'itemChanged(QListWidgetItem *)'), self.itemChanged)
        self.connect(self.lvThesis, QtCore.SIGNAL(
                'itemClicked(QListWidgetItem *)'), self.itemClicked)

        self.lvThesis.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.lvThesis.setSelectionMode(
                        QtGui.QAbstractItemView.ExtendedSelection)

        vBox.addWidget(self.lvThesis)
    
    def itemChanged(self, item):
        for i in self.allThesises.keys():
            if (item.text() == i.text()):
                item.setText(self.curName)
                return 0
            if (i.text() == self.curName):
                i.setText(item.text())
        self.curName = self.lvThesis.currentItem().text()
        return 1       
        

    def itemClicked(self, item):
        self.emit(QtCore.SIGNAL('itemOnLamClicked(Thesis *)'), item)

    def selectionChanged(self):
        self.curName = self.lvThesis.currentItem().text()
        self.emit(QtCore.SIGNAL('lamSelectionChanged(list)'),
                    self.lvThesis.findItems('', QtCore.Qt.MatchContains))

    def makeConMenu(self):
        self.conMenu = QtGui.QMenu(self)
        self.aSort1 = QtGui.QAction(QtGui.QIcon(
                'icons/sort_by_ascending_order.png'),
                        self.tr('Sort by ascending order'), self)

        self.aSort2 = QtGui.QAction(QtGui.QIcon(
                'icons/sort_by_descending_order.png'),
                        self.tr('Sort by descending order'), self)

        self.connect(self.aSort1, QtCore.SIGNAL('triggered()'),
                                            self.sortByAscendingOrder)
        self.connect(self.aSort2, QtCore.SIGNAL('triggered()'),
                                            self.sortByDescendingOrder)

        self.conMenu.addAction(self.aSort1)
        self.conMenu.addAction(self.aSort2)

    def sortByAscendingOrder(self):
        self.lvThesis.sortItems(QtCore.Qt.AscendingOrder)

    def sortByDescendingOrder(self):
        self.lvThesis.sortItems(QtCore.Qt.DescendingOrder)

    def addThesis(self, thesis):
        self.lvThesis.addItem(thesis)

    def retranslateUi(self):
        self.setWindowTitle(self.tr('Lamination'))
        self.aSort1.setText(self.tr('Sort by ascending order'))
        self.aSort2.setText(self.tr('Sort by descending order'))
        self.basename = self.tr('New Thesis')

    def listMenu(self, event):
        self.conMenu.exec_(event.globalPos())

    def closeEvent(self, event):
            self.emit(QtCore.SIGNAL('closeLam(QDialog *)'), self)
            event.accept()

