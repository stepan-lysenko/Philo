#-*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import string, os

REMOVE_ERROR = u"""Ошибка удаления: %(path), %(error) """

def rmgeneric(path, __func__, widget):
    try:
        __func__(path)
    except OSError, (errno, strerror):
        QtGui.QMessageBox.warning(widget, 'Error', REMOVE_ERROR % 
                                {'path' : path, 'error': strerror })

def removeall(path, widget):
    if not os.path.isdir(path):
        return

    files=os.listdir(path)

    for x in files:
        fullpath=os.path.join(path, x)
        if os.path.isfile(fullpath):
            f=os.remove
            rmgeneric(fullpath, f, widget)
        elif os.path.isdir(fullpath):
            removeall(fullpath, widget)
            f=os.rmdir
            rmgeneric(fullpath, f, widget)

class MainWidget(QtGui.QWidget):


#    def NewTab(self):
#        self.currentTab = PhiloTab(self)
#        self.TabWidget.addTab(self.currentTab, "Tab1")

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

#        self.TabWidget = QtGui.QTabWidget()
#        self.NewTab()

        layout = QtGui.QHBoxLayout(self)
        self.currentTab = PhiloTab(self)
#        layout.addWidget(self.TabWidget)
        layout.addWidget(self.currentTab)

class PhiloTab(QtGui.QWidget):

    currentItem = QtGui.QListWidgetItem()
    currentItem.desc = QtCore.QString()
    curItemText = ''
    path = ''

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.lvThesis = QtGui.QListWidget()
        self.lvThesis.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.lvThesis.setSortingEnabled(1)
        self.connect(self.lvThesis, QtCore.SIGNAL('itemSelectionChanged()'), 
                                                        self.SelectionChanged)
        self.connect(self.lvThesis, QtCore.SIGNAL(
                'itemChanged(QListWidgetItem *)'), self.ItemChanged)

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

    def ItemChanged(self, item):
        for i in xrange(self.lvThesis.count()):
            if (item.text() == self.lvThesis.item(i).text()) & (
                                self.lvThesis.item(i) != self.currentItem):
                QtGui.QMessageBox.warning(self, u'Ошибка',
			u'Понятие с данным именем уже присутствует в списке')
                item.setText(self.curItemText)
                return
        self.curItemText = self.lvThesis.currentItem().text()

    def SearchName(self, name):
	n = QtCore.QString(name)
        for i in xrange(self.lvThesis.count()):
            if n == self.lvThesis.item(i).text():
                return 1
        return 0

    def SaveList(self):
        if self.lvThesis.count() <= 0:
            QtGui.QMessageBox.warning(self, u'Сохрание',
					u'Список понятий пуст.')
            return
        if self.path == '':
            self.SaveListAs()
            return
        removeall(self.path, self)
        self.currentItem.desc = self.teThesisView.toPlainText()
        for i in xrange(self.lvThesis.count()):
            name = str(self.lvThesis.item(i).text().toUtf8())
            if not os.path.exists(self.path + '/' + name):
                os.makedirs(self.path + '/' + name)
            file = open(self.path + '/' + name + '/desc.txt', 'w')
            file.write(str(self.lvThesis.item(i).desc.toUtf8()))
            file.close()
                
    def SaveListAs(self):
        if self.lvThesis.count() <= 0:
            QtGui.QMessageBox.warning(self, u'Сохранение',
					u'Список понятий пуст')
            return
        path = str(QtGui.QFileDialog.getExistingDirectory(self,
						u"Сохранить Как", './',
				QtGui.QFileDialog.ShowDirsOnly).toUtf8())
        if path == '':
            return
        removeall(path, self)
        self.currentItem.desc = self.teThesisView.toPlainText()
        for i in xrange(self.lvThesis.count()):
            name = str(self.lvThesis.item(i).text().toUtf8())
            if not os.path.exists(path + '/' + name):
                os.makedirs(path + '/' + name)
            file = open(path + '/' + name + '/desc.txt', 'w')
            file.write(str(self.lvThesis.item(i).desc.toUtf8()))
            file.close()
        self.path = path

    def OpenList(self):
        if self.lvThesis.count() > 0:
            reply = QtGui.QMessageBox.question(self, u"Открыть?",
              u"Если вы продолжите, все изменения будут потеряны",
                                QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return
        path = str(QtGui.QFileDialog.getExistingDirectory(self, u"Открытие",
                            './', QtGui.QFileDialog.ShowDirsOnly).toUtf8())
        self.path = path
        if path == '':
            return
        self.lvThesis.clear()
        ListDir = []
        for Bill, ListDir, Bob in os.walk(path):
            break
        for name in ListDir:
            item = QtGui.QListWidgetItem(unicode(name, 'UTF8'))
            item.setFlags(QtCore.Qt.ItemIsEditable |
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            file = open(path + '/' + name + '/desc.txt', 'r')
            item.desc = QtCore.QString()
            for i in file.readlines():
                item.desc += QtCore.QString(unicode(i, 'UTF8'))
            file.close()
            self.lvThesis.addItem(item)

    def NewWorkspace(self):
        self.lvThesis.clear()
        self.teThesisView.clear()
        self.path = ''
        self.currentItem = QtGui.QListWidgetItem()
        self.desc = QtCore.QString()
        self.curItemText = ''

    def DelCurrentThesis(self):
        i = self.lvThesis.currentRow()
        if i < 0:
            return
        self.lvThesis.takeItem(i)
        

    def SelectionChanged(self):
        if self.lvThesis.currentRow() < 0:
            self.teThesisView.setText('')
            self.currentItem = QtGui.QListWidgetItem()
            return
        self.currentItem.desc = self.teThesisView.toPlainText()
        self.currentItem = self.lvThesis.currentItem()
        self.teThesisView.setText(self.currentItem.desc)
        self.curItemText = self.lvThesis.currentItem().text()

    def AddNewThesis(self):
        i = 0
        name = u'Новое Понятие'
        tmp = u''
        while self.SearchName(name + tmp) == 1:
            i += 1
            if i < 10:
                tmp = unicode(str(0) + str(i), 'UTF8')
            else:
                tmp = unicode(str(i), 'UTF8')
        if 0 < i < 10:
            name += unicode(str(0) + str(i), 'UTF8')
        elif i >= 10:
            name += unicode(str(i), 'UTF8')
        tmp = QtGui.QListWidgetItem(name)
        tmp.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable
                                                    | QtCore.Qt.ItemIsEnabled)
        tmp.desc = QtCore.QString()
        self.lvThesis.addItem(tmp)
        self.lvThesis.setCurrentItem(tmp)
        self.lvThesis.editItem(self.lvThesis.currentItem())
        self.curItemText = self.lvThesis.currentItem().text()

