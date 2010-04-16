#-*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import string, os, ThesisBase
from SchemeView import SchemeView
import ConfigDialog, Instruments

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
        if os.path.isdir(fullpath):
            removeall(fullpath, widget)
            f = os.rmdir
            rmgeneric(fullpath, f, widget)
        elif os.path.isfile(fullpath):
            f = os.remove
            rmgeneric(fullpath, f, widget)

class MainWidget(QtGui.QWidget):

    currentItem = ThesisBase.Thesis()
    curItemText = QtCore.QString()
    path = ''

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.lvThesis = QtGui.QListWidget()
        self.lvThesis.setMaximumWidth(300)
        self.lvThesis.setMinimumWidth(50)
        self.lvThesis.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.lvThesis.setSelectionMode(
                        QtGui.QAbstractItemView.ExtendedSelection)

        self.connect(self.lvThesis, QtCore.SIGNAL('itemSelectionChanged()'), 
                                                        self.SelectionChanged)
        self.connect(self.lvThesis, QtCore.SIGNAL(
                'itemChanged(QListWidgetItem *)'), self.itemChanged)
        self.connect(self.lvThesis, QtCore.SIGNAL(
                'itemClicked(QListWidgetItem *)'), self.itemClicked)

        self.lvThesis.contextMenuEvent = self.listMenu

        splitter = QtGui.QSplitter()
        splitter.setOpaqueResize(1)

        self.teThesisView = QtGui.QTextEdit()
        self.teThesisView.setMaximumWidth(500)
        self.teThesisView.setMinimumWidth(150)

        self.Scheme = SchemeView()
        self.Scheme.setMinimumWidth(250)
        self.Scheme.setMaximumWidth(2000)
        self.connect(self.Scheme, QtCore.SIGNAL('selectOne(Thesis *)'),
                                                    self.selectOne)
        self.connect(self.Scheme, QtCore.SIGNAL(
                'createNewThesis(Thesis *, QPointF *)'), self.newToScheme)
        self.connect(self.Scheme, QtCore.SIGNAL('editThesisName(Thesis *)'),
                                                    self.editThesisName)

        Box = QtGui.QHBoxLayout(self)

        splitter.addWidget(self.lvThesis)
        splitter.addWidget(self.teThesisView)
        splitter.addWidget(self.Scheme)
        splitter.setSizes([130, 150, 500])
        Box.addWidget(splitter)

    @staticmethod
    def listItemClicked(self, item):
        pass

    def editThesisName(self, thesis):
        self.lvThesis.editItem(thesis)

    def newToScheme(self, thesis, point):
        if len(thesis.links) >= 3:
            return
        tmp = self.AddNewThesis()
        thesis.links.append(tmp.text())
        self.Scheme.addThesis(tmp, x=point.x(), y=point.y(), setCenter=0)

    def selectOne(self, thesis):
        self.lvThesis.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        thesis.setSelected(1)
        self.lvThesis.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

    def itemClicked(self, item):
        self.listItemClicked(self, item)

    def setInstr(self, instr):
        self.listItemClicked = instr.listItemClicked
        self.Scheme.setInstr(instr)
        self.lvThesis.setCursor(instr.listCursor)

    def listMenu(self, event):
        menu = QtGui.QMenu(self)
        aSort1 = QtGui.QAction(QtGui.QIcon(
                'icons/sort_by_ascending_order.png'),
                        u'Сортировать по убыванию', self)
        
        aSort2 = QtGui.QAction(QtGui.QIcon(
                'icons/sort_by_descending_order.png'),
                        u'Сортировать по возрастанию', self)
        self.connect(aSort1, QtCore.SIGNAL('triggered()'),
                                            self.sortByAscendingOrder)
        self.connect(aSort2, QtCore.SIGNAL('triggered()'),
                                            self.sortByDescendingOrder)

        menu.addAction(aSort1)
        menu.addAction(aSort2)
        menu.exec_(event.globalPos())

    def sortByAscendingOrder(self):
        self.lvThesis.sortItems(QtCore.Qt.AscendingOrder)

    def sortByDescendingOrder(self):
        self.lvThesis.sortItems(QtCore.Qt.DescendingOrder)

    def itemChanged(self, item):
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
        for i in xrange(self.lvThesis.count()):
            for link in self.lvThesis.item(i).links:
                if link == self.curItemText:
                    self.lvThesis.item(i).links.remove(link)
                    self.lvThesis.item(i).links.append(
                                    self.lvThesis.currentItem().text())
                
        self.curItemText = self.lvThesis.currentItem().text()

    def config(self):
        cfgDialog = ConfigDialog.cfgDialog(self)
        cfgDialog.show()

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
            for Bill, SubDirs, Bob in os.walk(path):
                break
            for dir in SubDirs:
                if len(dir) != 2:
                    QtGui.QMessageBox.warning(self, u'Сохранение',
                            u'Данная папка не является хранилищем тезисов')
                    return
            self.path = path
        for Bill, SubDirs, Bob in os.walk(self.path):
            break
        for dir in SubDirs:
            removeall(self.path + '/' + dir, self)
        self.currentItem.setDesc(self.teThesisView.toPlainText())
        for i in xrange(self.lvThesis.count()):
            self.lvThesis.item(i).saveThesis(self.path, 1)
        ThesisBase.saveScheme(self.Scheme, self.path + '/scheme.sch')

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
        for thesis in self.lvThesis.findItems('', QtCore.Qt.MatchContains):
            for link in thesis.links:
                if link == self.lvThesis.item(i).text():
                    thesis.links.pop(thesis.links.index(link))
        self.lvThesis.takeItem(i)
        

    def SelectionChanged(self):
        if self.lvThesis.currentRow() < 0:
            self.teThesisView.setText('')
            self.currentItem = ThesisBase.Thesis()
            return
        for item in self.Scheme.itemsOnScheme.keys():
            self.Scheme.setColorOfThesis(item)
        sel = self.lvThesis.selectedItems()
        if len(sel) <= 0:
            if not self.teThesisView.isReadOnly():
                self.currentItem.setDesc(self.teThesisView.toPlainText())
            self.curItemText = ''
            self.curItem = ThesisBase.Thesis()
            self.teThesisView.setText('')
            self.teThesisView.setReadOnly(1)
            return
        if len(sel) == 1:
            if not self.teThesisView.isReadOnly():
                self.currentItem.setDesc(self.teThesisView.toPlainText())
            self.teThesisView.setTextColor(QtCore.Qt.black)
            self.Scheme.setColorOfThesis(self.currentItem)
            self.currentItem = sel.pop()
            self.Scheme.setColorOfThesis(self.currentItem, QtCore.Qt.green)
            self.teThesisView.setText(self.currentItem.getDesc(self.path))
            tmp = self.lvThesis.selectedItems().pop()
            self.curItemText = tmp.text()
            self.teThesisView.setReadOnly(0)
            return
        self.teThesisView.setTextColor(QtCore.Qt.gray)
        self.teThesisView.setReadOnly(1)
        text = QtCore.QString('')
        sel.sort()
        for item in sel:
            item.getDesc(self.path)
            text += item.text() + ':\n'
            text += item.desc + '\n'
            self.Scheme.setColorOfThesis(item, QtCore.Qt.green)

        self.teThesisView.setText(text)
        

#        text = QtCore.QString()
#        for link in tmp.links:
#            text = text + link + QtCore.QString('\n')
#        self.teThesisView.setText(text)
        


    def AddNewThesis(self):
        self.lvThesis.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
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
        self.Scheme.itemsOnScheme[tmp] = []
        self.lvThesis.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        return tmp
