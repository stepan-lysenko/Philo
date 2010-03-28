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

    def sortByAscendingOrder(self):
        self.lvThesis.sortItems(QtCore.Qt.AscendingOrder)

    def sortByDescendingOrder(self):
        self.lvThesis.sortItems(QtCore.Qt.DescendingOrder)

    def ItemChanged(self, item):
        for key in self.Scheme.itemsOnScheme.keys():
            for view in self.Scheme.itemsOnScheme[key]:
                view.update()
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
        QtGui.QMessageBox.warning(self, u'Сохранение',
                    u"Функция временно не доступна, используйте 'Сохранить Как' в пустую папку")
#        removeall(self.path, self)
#        self.currentItem.setDesc(self.teThesisView.toPlainText())
#        for i in xrange(self.lvThesis.count()):
#            self.lvThesis.item(i).saveThesis(self.path, 1)
#        ThesisBase.saveScheme(self.Scheme, self.path + '/scheme.sch')


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
        ThesisBase.saveScheme(self.Scheme, self.path + '/scheme.sch')

    def addToScheme(self):
        i = self.lvThesis.currentRow()
        if i < 0:
            return
        self.Scheme.addThesis(self.lvThesis.item(i), QtCore.Qt.green)

    def delFromScheme(self):
        i = self.lvThesis.currentRow()
        if i < 0:
            return
        self.Scheme.delThesis(self.lvThesis.item(i))

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
        self.NewWorkspace()
        self.path = path
        ThesisBase.loadThesisesToList(self.lvThesis, path)
        ThesisBase.loadScheme(path + '/scheme.sch', self.lvThesis, self.Scheme)

    def NewWorkspace(self):
        self.lvThesis.clear()
        self.teThesisView.clear()
        self.path = ''
        self.currentItem = ThesisBase.Thesis()
        self.desc = QtCore.QString()
        self.curItemText = QtCore.QString()
        self.Scheme.clear()

    def DelCurrentThesis(self):
        i = self.lvThesis.currentRow()
        if i < 0:
            return
        self.Scheme.delThesis(self.lvThesis.item(i))
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
        self.Scheme.setColorOfThesis(self.currentItem)
        self.currentItem = sel.pop()
        self.Scheme.setColorOfThesis(self.currentItem, QtCore.Qt.green)
        self.teThesisView.setText(self.currentItem.getDesc(self.path))
        tmp = self.lvThesis.selectedItems().pop()
        self.curItemText = tmp.text()

        text = QtCore.QString()
        for link in tmp.links:
            text = text + link + QtCore.QString('\n')
        self.teThesisView.setText(text)
        


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
        tmp = ThesisBase.Thesis(name = name)
        tmp.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable
                                                    | QtCore.Qt.ItemIsEnabled)
        self.lvThesis.addItem(tmp)
        self.lvThesis.setCurrentItem(tmp)
        self.lvThesis.editItem(self.lvThesis.currentItem())
        self.curItemText = self.lvThesis.currentItem().text()
        self.teThesisView.clear()
