#-*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import MainWidget
import Instruments
import ConfigDialog

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.translator = QtCore.QTranslator()   
        lang = QtCore.QLocale.languageToString(
                    QtCore.QLocale.system().language())
        self.translator.load(lang, './tr')

        self.setGeometry(100, 150, 850, 550)

        self.widget = MainWidget.MainWidget()
        self.setWindowTitle(self.tr('Cognitive assistent v0.3'))

        self.aExit = QtGui.QAction(QtGui.QIcon('icons/exit.png'),
                                                self.tr('Quit'), self)
        self.aExit.setShortcut('Ctrl+Q')
        self.aExit.setStatusTip(self.tr('Quit'))
        self.connect(self.aExit, QtCore.SIGNAL('triggered()'),
                                                QtCore.SLOT('close()'))

        self.aSaveAs = QtGui.QAction(QtGui.QIcon('icons/save_as.png'),
                                                    self.tr('Save As'), self)
        self.aSaveAs.setStatusTip(self.tr('Save scheme as'))
        self.connect(self.aSaveAs, QtCore.SIGNAL('triggered()'),
                                            self.widget.SaveListAs)

        self.aConfig = QtGui.QAction(QtGui.QIcon('icons/config.png'),
                                                    self.tr('Configure'), self)
        self.aConfig.setStatusTip(self.tr('Open configure window'))
        self.connect(self.aConfig, QtCore.SIGNAL('triggered()'),
                                            self.config)

        self.aSave = QtGui.QAction(QtGui.QIcon('icons/save.png'),
                                                    self.tr('Save'), self)
        self.aSave.setStatusTip(self.tr('Save scheme'))
        self.connect(self.aSave, QtCore.SIGNAL('triggered()'),
                                            self.widget.SaveList)

        self.aOpen = QtGui.QAction(QtGui.QIcon('icons/open.png'),
                                                    self.tr('Open'), self)
        self.aOpen.setShortcut('Ctrl+O')
        self.aOpen.setStatusTip(self.tr('Select work directory'))
        self.connect(self.aOpen, QtCore.SIGNAL('triggered()'),
                                            self.widget.OpenList)

        self.aNewThesis = QtGui.QAction(QtGui.QIcon('icons/new_thesis.png'),
                                                self.tr('New thesis'), self)
        self.aNewThesis.setStatusTip(self.tr('Add new thesis'))
        self.connect(self.aNewThesis, QtCore.SIGNAL('triggered()'),
                                            self.widget.AddNewThesis)

        self.aDelThesis = QtGui.QAction(QtGui.QIcon('icons/del_thesis.png'),
                                                self.tr('Remove thesis'), self)
        self.aDelThesis.setStatusTip(self.tr('Remove current thesis'))
        self.connect(self.aDelThesis, QtCore.SIGNAL('triggered()'),
                                        self.widget.DelCurrentThesis)

        self.aNewWorkspace = QtGui.QAction(QtGui.QIcon('icons/new.png'),
                                                    self.tr('Remove all'), self)
        self.aNewWorkspace.setStatusTip(self.tr('Remove all'))
        self.connect(self.aNewWorkspace, QtCore.SIGNAL('triggered()'),
                                        self.widget.NewWorkspace)

        self.aDelFromScheme = QtGui.QAction(QtGui.QIcon(
                'icons/del_all_from_scheme.png'), self.tr(
                                        'Remove from scheme'), self)
        self.aDelFromScheme.setStatusTip(self.tr('Remove thesis from scheme'))
        self.connect(self.aDelFromScheme, QtCore.SIGNAL('triggered()'),
                                        self.widget.delFromScheme)

        self.aInstrAddToScheme = QtGui.QAction(QtGui.QIcon(
                    'icons/add_to_scheme.png'), self.tr('Add to scheme'), self)
        self.aInstrAddToScheme.setStatusTip(self.tr('Add thesis to scheme'))
        reg = lambda : self.widget.setInstr(Instruments.addToScheme)
        self.connect(self.aInstrAddToScheme, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrMove = QtGui.QAction(QtGui.QIcon(
                'icons/move.png'), self.tr('Move'), self)
        self.aInstrMove.setStatusTip(
                            self.tr('This is a hand, you can move thesis on scheme with this'))
        self.aInstrMove.setShortcut('Ctrl+M')
        reg = lambda : self.widget.setInstr(Instruments.moveView)
        self.connect(self.aInstrMove, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrRm = QtGui.QAction(QtGui.QIcon(
                'icons/del_from_scheme.png'), self.tr('Remove'), self)
        self.aInstrRm.setStatusTip(
                            self.tr('Instrument for remove thesis from scheme'))
        self.aInstrRm.setShortcut('Ctrl+D')
        reg = lambda : self.widget.setInstr(Instruments.rmView)
        self.connect(self.aInstrRm, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrLink = QtGui.QAction(QtGui.QIcon(
                'icons/link.png'), self.tr('Add link'), self)
        self.aInstrLink.setStatusTip(
                            self.tr('Instrument for adding links'))
        self.aInstrLink.setShortcut('Ctrl+L')
        reg = lambda : self.widget.setInstr(Instruments.createLink)
        self.connect(self.aInstrLink, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrRmLink = QtGui.QAction(QtGui.QIcon(
                'icons/rm_link.png'), self.tr('Remove link'), self)
        self.aInstrRmLink.setStatusTip(
                            self.tr('Instrument for remove links'))
        reg = lambda : self.widget.setInstr(Instruments.rmLink)
        self.connect(self.aInstrRmLink, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrAddDer = QtGui.QAction(QtGui.QIcon(
                'icons/add_der.png'), self.tr('Derivatives show'), self)
        self.aInstrAddDer.setStatusTip(
                            self.tr('Instrument for show derivatives'))
        reg = lambda : self.widget.setInstr(Instruments.addDer)
        self.connect(self.aInstrAddDer, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrAddADer = QtGui.QAction(QtGui.QIcon(
                'icons/add_antider.png'), self.tr('Antiderivatives show'), self)
        self.aInstrAddADer.setStatusTip(
                            self.tr('Instrument for show antiderivatives'))
        reg = lambda : self.widget.setInstr(Instruments.addAntider)
        self.connect(self.aInstrAddADer, QtCore.SIGNAL('triggered()'), reg)


        MenuBar = self.menuBar()
        self.mbFile = MenuBar.addMenu(self.tr('&File'))
        self.mbFile.addAction(self.aNewWorkspace)
        self.mbFile.addAction(self.aOpen)
        self.mbFile.addAction(self.aSave)
        self.mbFile.addAction(self.aSaveAs)
        self.mbFile.addAction(self.aExit)

        self.mbThesis = MenuBar.addMenu(self.tr('&Thesises'))
        self.mbThesis.addAction(self.aNewThesis)
        self.mbThesis.addAction(self.aDelThesis)
	
        self.tbWorkspace = self.addToolBar(self.tr('File'))
        self.tbWorkspace.addAction(self.aNewWorkspace)
        self.tbWorkspace.addAction(self.aOpen)
        self.tbWorkspace.addAction(self.aSave)
        self.tbWorkspace.addAction(self.aSaveAs)
        self.tbWorkspace.addAction(self.aConfig)

        self.tbThesis = self.addToolBar(self.tr('Thesises'))
        self.tbThesis.addAction(self.aNewThesis)
        self.tbThesis.addAction(self.aDelThesis)

        self.tbInstruments = self.addToolBar(self.tr('Instruments'))
        grInstr = QtGui.QActionGroup(self.tbInstruments)
        self.aInstrAddDer.setActionGroup(grInstr)
        self.aInstrMove.setActionGroup(grInstr)
        self.aInstrRm.setActionGroup(grInstr)
        self.aInstrLink.setActionGroup(grInstr)
        self.aInstrRmLink.setActionGroup(grInstr)
        self.aInstrAddToScheme.setActionGroup(grInstr)
        self.aInstrAddADer.setActionGroup(grInstr)

        for instr in grInstr.actions():
            instr.setCheckable(1)
        grInstr.setExclusive(1)

        self.tbInstruments.addAction(self.aInstrMove)
        self.aInstrMove.setChecked(1)
        self.tbInstruments.addAction(self.aInstrRm)
        self.tbInstruments.addAction(self.aInstrLink)
        self.tbInstruments.addAction(self.aInstrRmLink)
        self.tbInstruments.addAction(self.aInstrAddToScheme)
        self.tbInstruments.addAction(self.aInstrAddDer)
        self.tbInstruments.addAction(self.aInstrAddADer)

#       self.statusBar()

        self.cfgDialog = ConfigDialog.cfgDialog(self)
        self.connect(self.cfgDialog, QtCore.SIGNAL('ChangeLanguage(QString *)'), self.changLang) 

        self.setCentralWidget(self.widget)

    def retranslateUi(self):
        self.setWindowTitle(self.tr('Cognitive assistent v0.3'))

        self.aExit.setText(self.tr('Quit'))
        self.aExit.setStatusTip(self.tr('Quit'))

        self.aSaveAs.setText(self.tr('Save As'))
        self.aSaveAs.setStatusTip(self.tr('Save scheme as'))

        self.aConfig.setText(self.tr('Configure')) 
        self.aConfig.setStatusTip(self.tr('Open configure window'))

        self.aSave.setText(self.tr('Save'))
        self.aSave.setStatusTip(self.tr('Save scheme'))

        self.aOpen.setText(self.tr('Open'))
        self.aOpen.setStatusTip(self.tr('Select work directory'))

        self.aNewThesis.setText(self.tr('New thesis'))
        self.aNewThesis.setStatusTip(self.tr('Add new thesis'))

        self.aDelThesis.setText(self.tr('Remove thesis')) 
        self.aDelThesis.setStatusTip(self.tr('Remove current thesis'))

        self.aNewWorkspace.setText(self.tr('Remove all')) 
        self.aNewWorkspace.setStatusTip(self.tr('Remove all'))

        self.aDelFromScheme.setText(self.tr('Remove from scheme'))
        self.aDelFromScheme.setStatusTip(self.tr('Remove thesis from scheme'))

        self.aInstrAddToScheme.setText(self.tr('Add to scheme')) 
        self.aInstrAddToScheme.setStatusTip(self.tr('Add thesis to scheme'))

        self.aInstrMove.setText(self.tr('Move'))
        self.aInstrMove.setStatusTip(
                            self.tr('This is a hand, you can move thesis on scheme with this')) 

        self.aInstrRm.setText(self.tr('Remove'))
        self.aInstrRm.setStatusTip(
                            self.tr('Instrument for remove thesis from scheme')) 

        self.aInstrLink.setText(self.tr('Add link'))
        self.aInstrLink.setStatusTip(
                            self.tr('Instrument for adding links'))

        self.aInstrRmLink.setText(self.tr('Remove link'))
        self.aInstrRmLink.setStatusTip(
                            self.tr('Instrument for remove links'))

        self.aInstrAddDer.setText(self.tr('Derivatives show'))
        self.aInstrAddDer.setStatusTip(
                            self.tr('Instrument for show derivatives'))

        self.aInstrAddADer.setText(self.tr('Antiderivatives show')) 
        self.aInstrAddADer.setStatusTip(
                            self.tr('Instrument for show antiderivatives'))

        self.mbFile.setTitle(self.tr('&File'))
        self.mbThesis.setTitle(self.tr('&Thesises'))

        self.tbWorkspace.setWindowTitle(self.tr('File'))
        self.tbThesis.setWindowTitle(self.tr('Thesises'))
        self.tbInstruments.setWindowTitle(self.tr('Instruments'))

        self.widget.retranslateUi()
        self.cfgDialog.retranslateUi()

    def config(self):
        self.cfgDialog.show()
        

    def changLang(self, lang):
        self.translator.load(lang, './tr')
        self.retranslateUi()
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, self.tr('Are you sure?'),
		u"Вы действительно хотите выйти?", QtGui.QMessageBox.Yes, 
                                                    QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
