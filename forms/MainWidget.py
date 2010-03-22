#-*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import string, os, ThesisBase
from SchemeView import SchemeView

REMOVE_ERROR = u"""Ошибка удаления: %(path), %(error)"""

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

    currentItem = ThesisBase.Thesis()
    curItemText = QtCore.QString()
    path = ''

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.lvThesis = QtGui.QListWidget()
        self.lvThesis.setMaximumWidth(150)
        self.lvThesis.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.lvThesis.setSortingEnabled(1)
        self.connect(self.lvThesis, QtCore.SIGNAL('itemSelectionChanged()'), 
                                                        self.SelectionChanged)
        self.connect(self.lvThesis, QtCore.SIGNAL(
                'itemChanged(QListWidgetItem *)'), self.ItemChanged)

        spacer1 = QtGui.QSpacerItem(5, 0, QtGui.QSizePolicy.Minimum,
                                                QtGui.QSizePolicy.Maximum)

        self.teThesisView = QtGui.QTextEdit()
        self.teThesisView.setMaximumWidth(200)

        spacer2 = QtGui.QSpacerItem(5, 0, QtGui.QSizePolicy.Minimum,
                                                QtGui.QSizePolicy.Maximum)

        self.Scheme = SchemeView()


        Box = QtGui.QHBoxLayout(self)
        Box.addWidget(self.lvThesis)
        Box.addSpacerItem(spacer1)
        Box.addWidget(self.teThesisView)
        Box.addSpacerItem(spacer2)
        Box.addWidget(self.Scheme)

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
            path = str(QtGui.QFileDialog.getExistingDirectory(self,
                                    u"Выбор папки для сохранения", './',
                                QtGui.QFileDialog.ShowDirsOnly).toUtf8())
            if path == '':
                return
            self.path = path
        removeall(self.path, self)
        self.currentItem.setDesc(self.teThesisView.toPlainText())
        for i in xrange(self.lvThesis.count()):
            self.lvThesis.item(i).saveThesis(self.path, 1)
                
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
        self.currentItem.setDesc(self.teThesisView.toPlainText())
        for i in xrange(self.lvThesis.count()):
            self.lvThesis.item(i).saveThesis(path, 1)
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
        if path == '':
            return
        self.path = path
        self.lvThesis.clear()
        ThesisBase.loadThesisesToList(self.lvThesis, path)

    def NewWorkspace(self):
        self.lvThesis.clear()
        self.teThesisView.clear()
        self.path = ''
        self.currentItem = ThesisBase.Thesis()
        self.desc = QtCore.QString()
        self.curItemText = QtCore.QString()

    def DelCurrentThesis(self):
        i = self.lvThesis.currentRow()
        if i < 0:
            return
        self.lvThesis.takeItem(i)
        

    def SelectionChanged(self):
        if self.lvThesis.currentRow() < 0:
            self.teThesisView.setText('')
            self.currentItem = ThesisBase.Thesis()
            return
        sel = self.lvThesis.selectedItems()
        if len(sel) <= 0:
            return
        self.currentItem.setDesc(self.teThesisView.toPlainText())
        self.currentItem = sel.pop()
        self.teThesisView.setText(self.currentItem.getDesc(self.path))
        self.curItemText = self.lvThesis.selectedItems().pop().text()

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
        tmp = ThesisBase.Thesis(name)
        tmp.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable
                                                    | QtCore.Qt.ItemIsEnabled)
        self.lvThesis.addItem(tmp)
        self.lvThesis.setCurrentItem(tmp)
        self.lvThesis.editItem(self.lvThesis.currentItem())
        self.curItemText = self.lvThesis.currentItem().text()
        self.teThesisView.clear()
        

