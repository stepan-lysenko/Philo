#-*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import string, os, ThesisBase
from SchemeView import SchemeView
import Instruments

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

        self.basename = self.tr('New Thesis')

        self.lvThesis = QtGui.QListWidget()
        self.lvThesis.setMaximumWidth(300)
        self.lvThesis.setMinimumWidth(100)
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
        self.connect(self.Scheme, QtCore.SIGNAL('delThesis(Thesis *)'),
                                                    self.itemClicked)
        self.connect(self.Scheme, QtCore.SIGNAL('convolution(list)'),
                                                    self.convolution)
        self.connect(self.Scheme, QtCore.SIGNAL('glue(list)'),
                                                    self.glue)
        self.connect(self.Scheme, QtCore.SIGNAL('itemOnLamClicked(Thesis *)'),
                                                    self.itemOnLamClicked)
        self.connect(self.Scheme, QtCore.SIGNAL('renameOnScheme(QString *, QListWidgetItem *)'),
                                                    self.rename)

        Box = QtGui.QHBoxLayout(self)

        splitter.addWidget(self.lvThesis)
        splitter.addWidget(self.teThesisView)
        splitter.addWidget(self.Scheme)
        splitter.setSizes([130, 150, 500])
        Box.addWidget(splitter)

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

    def keyReleaseEvent(self, event):
        self.KeyReleaseEvent(self, event)

    @staticmethod
    def KeyReleaseEvent(self, event):
        pass

    def itemOnLamClicked(self, it):
        item = self.lvThesis.findItems(it.text(), QtCore.Qt.MatchExactly)
        if (len(item) == 0):
            return
        item = item[0]
        self.itemClicked(item)
        

    def glue(self, list):
        for item in list:                 #
            if len(item.links) >= 3:      #
                return                    #

        tmp = self.AddNewThesis()
        for item in list:                 #
            item.links.append(tmp.text()) #
#        for item in list:
#            tmp.links.append(item.text())
        self.Scheme.addThesis(tmp, setCenter=0)


    def convolution(self, list):
        tmp = self.AddNewThesis()
        self.Scheme.addThesis(tmp, setCenter=0)
        for item in list:
            tmp.links.append(item.text())

    @staticmethod
    def listItemClicked(self, item):
        pass

    def editThesisName(self, thesis):
        self.lvThesis.setCurrentItem(thesis)
        self.lvThesis.editItem(thesis)

    def newToScheme(self, thesis, point):
        if thesis == None:
            tmp = self.AddNewThesis()
            self.Scheme.addThesis(tmp, x=point.x(), y=point.y(), setCenter=0)
            return
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
        self.KeyReleaseEvent = instr.keyReleaseEvent
        for lam in self.Scheme.lams:
            lam.lvThesis.setCursor(instr.listCursor)

    def retranslateUi(self):
        self.aSort1.setText(self.tr('Sort by ascending order'))
        self.aSort2.setText(self.tr('Sort by descending order'))
        self.basename = self.tr('New Thesis')

    def listMenu(self, event):
        self.conMenu.exec_(event.globalPos())

    def sortByAscendingOrder(self):
        self.lvThesis.sortItems(QtCore.Qt.AscendingOrder)

    def sortByDescendingOrder(self):
        self.lvThesis.sortItems(QtCore.Qt.DescendingOrder)

    def rename(self, oldname, item):
        for key in self.Scheme.itemsOnScheme.keys():
            for view in self.Scheme.itemsOnScheme[key]:
                if key == item:
                    view.setText(item.text())
                view.update()
        for i in xrange(self.lvThesis.count()):
            if (item.text() == self.lvThesis.item(i).text()) & (
                                self.lvThesis.item(i) != self.currentItem):
                QtGui.QMessageBox.warning(self, self.tr('Error'),
                    self.tr('Thesis with that name olready is the list'))
                item.setText(oldname)
                return 0
        for i in xrange(self.lvThesis.count()):
            for link in self.lvThesis.item(i).links:
                if link == oldname:
                    self.lvThesis.item(i).links.remove(link)
                    self.lvThesis.item(i).links.append(
                                    self.lvThesis.currentItem().text())
        for lam in self.Scheme.lams:
            for lb in lam.labels:
                if lb.text() == self.curItemText:
                    lb.setText(item.text())
            for i in xrange(lam.lvThesis.count()):
                tmp = lam.lvThesis.item(i)
                if (tmp.text() == self.curItemText):
                    tmp.setText(item.text())
        self.curItemText = self.lvThesis.currentItem().text()
        return 1


    def itemChanged(self, item):
        self.rename(self.curItemText, item)

    def SearchName(self, name):
        n = QtCore.QString(name)
        for i in xrange(self.lvThesis.count()):
            if n == self.lvThesis.item(i).text():
                return 1
        return 0

    def SaveList(self):
        if self.lvThesis.count() <= 0:
            QtGui.QMessageBox.warning(self, self.tr('Save'),
					self.tr('List empty.'))
            return
        if self.path == '':
            path = str(QtGui.QFileDialog.getExistingDirectory(self,
                                    self.tr('Select directory'), './',
                                QtGui.QFileDialog.ShowDirsOnly).toUtf8())
            if path == '':
                return
            for Bill, SubDirs, Bob in os.walk(path):
                break
            for dir in SubDirs:
                if len(dir) != 2:
                    QtGui.QMessageBox.warning(self, self.tr('Save'),
                            self.tr('That directory is not valid'))
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
            QtGui.QMessageBox.warning(self, self.tr('Save'),
					self.tr('Empty list'))
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
            reply = QtGui.QMessageBox.question(self, self.tr("Open"),
              self.tr("All changes will be lost. Continue?"),
                                QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return
        path = str(QtGui.QFileDialog.getExistingDirectory(self, self.tr("Open"),
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
        
#        for lam in self.Scheme.lams:
#            for thesis in lam.lvThesis.findItems('', QtCore.Qt.MatchContains):
#                if thesis.text() in [it.text() for it in self.lvThesis.selectedItems()]:
#                    thesis.setSelected(1)
#                else:
#                    thesis.setSelected(0)

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
        name = QtCore.QString(self.basename)
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
