#-*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import MainWidget
import Instruments

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setGeometry(100, 150, 850, 550)

        widget = MainWidget.MainWidget()
        self.setWindowTitle(u"Редактор когнитивных схем v0.4")

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

        aConfig = QtGui.QAction(QtGui.QIcon('icons/config.png'),
                                                    u'Конфигурация', self)
        aConfig.setStatusTip(u'Открыть окно конфигурации')
        self.connect(aConfig, QtCore.SIGNAL('triggered()'),
                                            widget.config)

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

        aDelFromScheme = QtGui.QAction(QtGui.QIcon(
                'icons/del_all_from_scheme.png'), u'Удалить со схемы', self)
        aDelFromScheme.setStatusTip(u'Удалить понятие со схемы')
        self.connect(aDelFromScheme, QtCore.SIGNAL('triggered()'),
                                        widget.delFromScheme)

        aInstrAddToScheme = QtGui.QAction(QtGui.QIcon(
                    'icons/add_to_scheme.png'), u'Добавить на схему', self)
        aInstrAddToScheme.setStatusTip(u'Добавить понятие на схему')
        reg = lambda : widget.setInstr(Instruments.addToScheme)
        self.connect(aInstrAddToScheme, QtCore.SIGNAL('triggered()'), reg)

        aInstrMove = QtGui.QAction(QtGui.QIcon(
                'icons/move.png'), u'Передвинуть экземпляр', self)
        aInstrMove.setStatusTip(
                            u'Инструмент для перемещения экземпляров')
        aInstrMove.setShortcut('Ctrl+M')
        reg = lambda : widget.setInstr(Instruments.moveView)
        self.connect(aInstrMove, QtCore.SIGNAL('triggered()'), reg)

        aInstrRm = QtGui.QAction(QtGui.QIcon(
                'icons/del_from_scheme.png'), u'Удалить экземпляр', self)
        aInstrRm.setStatusTip(
                            u'Инструмент для удаления экземпляров')
        aInstrRm.setShortcut('Ctrl+D')
        reg = lambda : widget.setInstr(Instruments.rmView)
        self.connect(aInstrRm, QtCore.SIGNAL('triggered()'), reg)

        aInstrLink = QtGui.QAction(QtGui.QIcon(
                'icons/link.png'), u'Установить связь', self)
        aInstrLink.setStatusTip(
                            u'Инструмент для создания связей')
        aInstrLink.setShortcut('Ctrl+L')
        reg = lambda : widget.setInstr(Instruments.createLink)
        self.connect(aInstrLink, QtCore.SIGNAL('triggered()'), reg)

        aInstrRmLink = QtGui.QAction(QtGui.QIcon(
                'icons/rm_link.png'), u'Удалить связь', self)
        aInstrRmLink.setStatusTip(
                            u'Инструмент для удаления связей')
        reg = lambda : widget.setInstr(Instruments.rmLink)
        self.connect(aInstrRmLink, QtCore.SIGNAL('triggered()'), reg)

        aInstrAddDer = QtGui.QAction(QtGui.QIcon(
                'icons/add_der.png'), u'Проявить производные', self)
        aInstrAddDer.setStatusTip(
                            u'Инструмент для проявления производных')
        reg = lambda : widget.setInstr(Instruments.addDer)
        self.connect(aInstrAddDer, QtCore.SIGNAL('triggered()'), reg)

        aInstrAddADer = QtGui.QAction(QtGui.QIcon(
                'icons/add_antider.png'), u'Проявить первообразные', self)
        aInstrAddADer.setStatusTip(
                            u'Инструмент для проявления первообразных')
        reg = lambda : widget.setInstr(Instruments.addAntider)
        self.connect(aInstrAddADer, QtCore.SIGNAL('triggered()'), reg)


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
#        self.tbWorkspace.addAction(aConfig)

        self.tbThesis = self.addToolBar(u'Понятия')
        self.tbThesis.addAction(aNewThesis)
        self.tbThesis.addAction(aDelThesis)

        self.tbInstruments = self.addToolBar(u'Инструменты')
        grInstr = QtGui.QActionGroup(self.tbInstruments)
        aInstrAddDer.setActionGroup(grInstr)
        aInstrMove.setActionGroup(grInstr)
        aInstrRm.setActionGroup(grInstr)
        aInstrLink.setActionGroup(grInstr)
        aInstrRmLink.setActionGroup(grInstr)
        aInstrAddToScheme.setActionGroup(grInstr)
        aInstrAddADer.setActionGroup(grInstr)

        for instr in grInstr.actions():
            instr.setCheckable(1)
        grInstr.setExclusive(1)

        self.tbInstruments.addAction(aInstrMove)
        aInstrMove.setChecked(1)
        self.tbInstruments.addAction(aInstrRm)
        self.tbInstruments.addAction(aInstrLink)
        self.tbInstruments.addAction(aInstrRmLink)
        self.tbInstruments.addAction(aInstrAddToScheme)
        self.tbInstruments.addAction(aInstrAddDer)
        self.tbInstruments.addAction(aInstrAddADer)

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
