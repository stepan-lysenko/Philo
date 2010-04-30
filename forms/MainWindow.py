#-*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import MainWidget
import Instruments

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setGeometry(100, 150, 850, 550)

        widget = MainWidget.MainWidget()
        self.setWindowTitle(self.tr('Cognitive assistent v0.3'))

        aExit = QtGui.QAction(QtGui.QIcon('icons/exit.png'),
                                                self.tr('Quit'), self)
        aExit.setShortcut('Ctrl+Q')
        aExit.setStatusTip(self.tr('Quit'))
        self.connect(aExit, QtCore.SIGNAL('triggered()'),
        QtCore.SLOT('close()'))

        aSaveAs = QtGui.QAction(QtGui.QIcon('icons/save_as.png'),
                                                    self.tr('Save As'), self)
        aSaveAs.setStatusTip(self.tr('Save scheme as'))
        self.connect(aSaveAs, QtCore.SIGNAL('triggered()'),
                                            widget.SaveListAs)

        aConfig = QtGui.QAction(QtGui.QIcon('icons/config.png'),
                                                    self.tr('Configure'), self)
        aConfig.setStatusTip(self.tr('Open configure window'))
        self.connect(aConfig, QtCore.SIGNAL('triggered()'),
                                            widget.config)

        aSave = QtGui.QAction(QtGui.QIcon('icons/save.png'),
                                                    self.tr('Save'), self)
        aSave.setStatusTip(self.tr('Save scheme'))
        self.connect(aSave, QtCore.SIGNAL('triggered()'),
                                            widget.SaveList)

        aOpen = QtGui.QAction(QtGui.QIcon('icons/open.png'),
                                                    self.tr('Open'), self)
        aOpen.setShortcut('Ctrl+O')
        aOpen.setStatusTip(self.tr('Select work directory'))
        self.connect(aOpen, QtCore.SIGNAL('triggered()'),
                                            widget.OpenList)

        aNewThesis = QtGui.QAction(QtGui.QIcon('icons/new_thesis.png'),
                                                self.tr('New thesis'), self)
        aNewThesis.setStatusTip(self.tr('Add new thesis'))
        self.connect(aNewThesis, QtCore.SIGNAL('triggered()'),
                                            widget.AddNewThesis)

        aDelThesis = QtGui.QAction(QtGui.QIcon('icons/del_thesis.png'),
                                                self.tr('Remove thesis'), self)
        aDelThesis.setStatusTip(self.tr('Remove current thesis'))
        self.connect(aDelThesis, QtCore.SIGNAL('triggered()'),
                                        widget.DelCurrentThesis)

        aNewWorkspace = QtGui.QAction(QtGui.QIcon('icons/new.png'),
                                                    self.tr('Remove all'), self)
        aNewWorkspace.setStatusTip(self.tr('Remove all'))
        self.connect(aNewWorkspace, QtCore.SIGNAL('triggered()'),
                                        widget.NewWorkspace)

        aDelFromScheme = QtGui.QAction(QtGui.QIcon(
                'icons/del_all_from_scheme.png'), self.tr('Remove from scheme'), self)
        aDelFromScheme.setStatusTip(self.tr('Remove thesis from scheme'))
        self.connect(aDelFromScheme, QtCore.SIGNAL('triggered()'),
                                        widget.delFromScheme)

        aInstrAddToScheme = QtGui.QAction(QtGui.QIcon(
                    'icons/add_to_scheme.png'), self.tr('Add to scheme'), self)
        aInstrAddToScheme.setStatusTip(self.tr('Add thesis to scheme'))
        reg = lambda : widget.setInstr(Instruments.addToScheme)
        self.connect(aInstrAddToScheme, QtCore.SIGNAL('triggered()'), reg)

        aInstrMove = QtGui.QAction(QtGui.QIcon(
                'icons/move.png'), self.tr('Move'), self)
        aInstrMove.setStatusTip(
                            self.tr('This is a hand, you can move thesis on scheme with this'))
        aInstrMove.setShortcut('Ctrl+M')
        reg = lambda : widget.setInstr(Instruments.moveView)
        self.connect(aInstrMove, QtCore.SIGNAL('triggered()'), reg)

        aInstrRm = QtGui.QAction(QtGui.QIcon(
                'icons/del_from_scheme.png'), self.tr('Remove'), self)
        aInstrRm.setStatusTip(
                            self.tr('Instrument for remove thesis from scheme'))
        aInstrRm.setShortcut('Ctrl+D')
        reg = lambda : widget.setInstr(Instruments.rmView)
        self.connect(aInstrRm, QtCore.SIGNAL('triggered()'), reg)

        aInstrLink = QtGui.QAction(QtGui.QIcon(
                'icons/link.png'), self.tr('Add link'), self)
        aInstrLink.setStatusTip(
                            self.tr('Instrument for adding links'))
        aInstrLink.setShortcut('Ctrl+L')
        reg = lambda : widget.setInstr(Instruments.createLink)
        self.connect(aInstrLink, QtCore.SIGNAL('triggered()'), reg)

        aInstrRmLink = QtGui.QAction(QtGui.QIcon(
                'icons/rm_link.png'), self.tr('Remove link'), self)
        aInstrRmLink.setStatusTip(
                            self.tr('Instrument for remove links'))
        reg = lambda : widget.setInstr(Instruments.rmLink)
        self.connect(aInstrRmLink, QtCore.SIGNAL('triggered()'), reg)

        aInstrAddDer = QtGui.QAction(QtGui.QIcon(
                'icons/add_der.png'), self.tr('Derivatives show'), self)
        aInstrAddDer.setStatusTip(
                            self.tr('Instrument for show derivatives'))
        reg = lambda : widget.setInstr(Instruments.addDer)
        self.connect(aInstrAddDer, QtCore.SIGNAL('triggered()'), reg)

        aInstrAddADer = QtGui.QAction(QtGui.QIcon(
                'icons/add_antider.png'), self.tr('Antiderivatives show'), self)
        aInstrAddADer.setStatusTip(
                            self.tr('Instrument for show antiderivatives'))
        reg = lambda : widget.setInstr(Instruments.addAntider)
        self.connect(aInstrAddADer, QtCore.SIGNAL('triggered()'), reg)


        MenuBar = self.menuBar()
        mbFile = MenuBar.addMenu(self.tr('&File'))
        mbFile.addAction(aNewWorkspace)
        mbFile.addAction(aOpen)
        mbFile.addAction(aSave)
        mbFile.addAction(aSaveAs)
        mbFile.addAction(aExit)

        mbThesis = MenuBar.addMenu(self.tr('&Thesises'))
        mbThesis.addAction(aNewThesis)
        mbThesis.addAction(aDelThesis)
	
        self.tbWorkspace = self.addToolBar(self.tr('File'))
        self.tbWorkspace.addAction(aNewWorkspace)
        self.tbWorkspace.addAction(aOpen)
        self.tbWorkspace.addAction(aSave)
        self.tbWorkspace.addAction(aSaveAs)
#        self.tbWorkspace.addAction(aConfig)

        self.tbThesis = self.addToolBar(self.tr('Thesises'))
        self.tbThesis.addAction(aNewThesis)
        self.tbThesis.addAction(aDelThesis)

        self.tbInstruments = self.addToolBar(self.tr('Instruments'))
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
        reply = QtGui.QMessageBox.question(self, self.tr('Are you sure?'),
		u"Вы действительно хотите выйти?", QtGui.QMessageBox.Yes, 
                                                    QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
