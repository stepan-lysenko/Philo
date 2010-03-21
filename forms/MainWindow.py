#-*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import MainWidget

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setGeometry(100, 150, 850, 550)

        widget = MainWidget.MainWidget()
        self.setWindowTitle(u"Редактор когнитивных схем")

        aExit = QtGui.QAction(QtGui.QIcon('icons/exit.png'),
                                                u'Выход', self)
        aExit.setShortcut('Ctrl+Q')
        aExit.setStatusTip(u'Выход')
        self.connect(aExit, QtCore.SIGNAL('triggered()'),
        QtCore.SLOT('close()'))

        aSaveAs = QtGui.QAction(QtGui.QIcon('icons/save_as.png'),
                                                    u'Сохранить как', self)
        aSaveAs.setStatusTip(u'Сохранить схему как')
        self.connect(aSaveAs, QtCore.SIGNAL('triggered()'),
                                            widget.SaveListAs)

        aSave = QtGui.QAction(QtGui.QIcon('icons/save.png'),
                                                    u'Сохранить', self)
        aSave.setStatusTip(u'Сохранить схему')
        self.connect(aSave, QtCore.SIGNAL('triggered()'),
                                            widget.SaveList)

        aOpen = QtGui.QAction(QtGui.QIcon('icons/open.png'),
                                                    u'Открыть', self)
        aOpen.setShortcut('Ctrl+O')
        aOpen.setStatusTip(u'Выбрать рабочую папку')
        self.connect(aOpen, QtCore.SIGNAL('triggered()'),
                                            widget.OpenList)

        aNewThesis = QtGui.QAction(QtGui.QIcon('icons/new_thesis.png'),
                                                u'Добавить понятие', self)
        aNewThesis.setStatusTip(u'Добавить новое понятие')
        self.connect(aNewThesis, QtCore.SIGNAL('triggered()'),
                                            widget.AddNewThesis)

        aDelThesis = QtGui.QAction(QtGui.QIcon('icons/del_thesis.png'),
                                                u'Удалить понятие', self)
        aDelThesis.setStatusTip(u'Удалить выбранное понятие')
        self.connect(aDelThesis, QtCore.SIGNAL('triggered()'),
                                        widget.DelCurrentThesis)

        aNewWorkspace = QtGui.QAction(QtGui.QIcon('icons/new.png'),
                                                    u'Очистить список', self)
        aNewWorkspace.setStatusTip(u'Очистить список понятий')
        self.connect(aNewWorkspace, QtCore.SIGNAL('triggered()'),
                                        widget.NewWorkspace)
        
        MenuBar = self.menuBar()
        mbFile = MenuBar.addMenu(u'&Файл')
        mbFile.addAction(aNewWorkspace)
        mbFile.addAction(aOpen)
	mbFile.addAction(aSave)
        mbFile.addAction(aSaveAs)
	mbFile.addAction(aExit)

	mbThesis = MenuBar.addMenu(u'&Понятия')
	mbThesis.addAction(aNewThesis)
	mbThesis.addAction(aDelThesis)
	
        self.tbWorkspace = self.addToolBar(u'Файл')
        self.tbWorkspace.addAction(aNewWorkspace)
        self.tbWorkspace.addAction(aOpen)
        self.tbWorkspace.addAction(aSave)
        self.tbWorkspace.addAction(aSaveAs)

        self.tbThesis = self.addToolBar(u'Понятия')
        self.tbThesis.addAction(aNewThesis)
        self.tbThesis.addAction(aDelThesis)

#       self.statusBar()

        self.setCentralWidget(widget)

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, u'Вы уверены?',
		u"Вы действительно хотите выйти?", QtGui.QMessageBox.Yes, 
                                                    QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
