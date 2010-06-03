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

        self.setGeometry(50, 150, 1000, 600)

        self.widget = MainWidget.MainWidget()
        self.connect(self.widget.Scheme, QtCore.SIGNAL('addColorsBar()'),
                                                self.addColorsBar)
        self.connect(self.widget.Scheme, QtCore.SIGNAL('activateMutation()'),
                                                self.activateMutation)
        self.connect(self.widget.Scheme, QtCore.SIGNAL('disactivateMutation()'),
                                                self.disactivateMutation)

        self.setWindowTitle(self.tr('Cognitive assistent v0.5'))

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
        self.aNewThesis.setShortcut('Ctrl+N')
        self.aNewThesis.setStatusTip(self.tr('Add new thesis'))
        self.connect(self.aNewThesis, QtCore.SIGNAL('triggered()'),
                                            self.widget.AddNewThesis)

        self.aClearScheme = QtGui.QAction(QtGui.QIcon('icons/clear_scheme.png'),
                                                self.tr('Clear scheme'), self)
        self.aClearScheme.setStatusTip(self.tr('Clear scheme'))
        self.connect(self.aClearScheme, QtCore.SIGNAL('triggered()'),
                                            self.clearScheme)

        self.aNewWorkspace = QtGui.QAction(QtGui.QIcon('icons/new.png'),
                                                    self.tr('Remove all'), self)
        self.aNewWorkspace.setStatusTip(self.tr('Remove all'))
        self.connect(self.aNewWorkspace, QtCore.SIGNAL('triggered()'),
                                        self.widget.NewWorkspace)

        self.aDelFromScheme = QtGui.QAction(QtGui.QIcon(
                'icons/del_all_from_scheme.png'), self.tr(
                                        'Remove all from scheme'), self)
        self.aDelFromScheme.setStatusTip(self.tr('Remove all thesis from scheme'))
        self.connect(self.aDelFromScheme, QtCore.SIGNAL('triggered()'),
                                        self.widget.delFromScheme)

        self.aZoomOrig = QtGui.QAction(QtGui.QIcon(
                    'icons/zoom_original.png'), self.tr('Zoom Original'), self)
        self.aZoomOrig.setShortcut('Ctrl++')
        self.aZoomOrig.setStatusTip(self.tr('Zoom Original'))
        self.connect(self.aZoomOrig, QtCore.SIGNAL('triggered()'),
                                                self.widget.Scheme.resetTransform)

        self.aZoomIn = QtGui.QAction(QtGui.QIcon(
                    'icons/zoom_in.png'), self.tr('Zoom In'), self)
        self.aZoomIn.setShortcut('Ctrl++')
        self.aZoomIn.setStatusTip(self.tr('Zoom In'))
        self.connect(self.aZoomIn, QtCore.SIGNAL('triggered()'),
                                                self.widget.Scheme.zoomIn)

        self.aZoomOut = QtGui.QAction(QtGui.QIcon(
                    'icons/zoom_out.png'), self.tr('Zoom Out'), self)
        self.aZoomOut.setShortcut('Ctrl+-')
        self.aZoomOut.setStatusTip(self.tr('Zoom Out'))
        self.connect(self.aZoomOut, QtCore.SIGNAL('triggered()'),
                                                self.widget.Scheme.zoomOut)


        self.aInstrConvolution = QtGui.QAction(QtGui.QIcon(
                    'icons/convolution.png'), self.tr('Convolution'), self)
        self.aInstrConvolution.setStatusTip(self.tr(
                            'Instrument to convolution thesises'))
        reg = lambda: self.setInstr(Instruments.convolution)
        self.connect(self.aInstrConvolution, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrGlue = QtGui.QAction(QtGui.QIcon(
                    'icons/glue.png'), self.tr('Glue'), self)
        self.aInstrGlue.setShortcut('Ctrl+G')
        self.aInstrGlue.setStatusTip(self.tr('Glue has made links'))
        reg = lambda: self.setInstr(Instruments.Glue)
        self.connect(self.aInstrGlue, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrMutation = QtGui.QAction(QtGui.QIcon(
                    'icons/mutation.png'), self.tr('Mutation'), self)
        self.aInstrMutation.setShortcut('Ctrl+U')
        self.aInstrMutation.setStatusTip(self.tr('Mutation'))
        reg = lambda: self.setMutation(Instruments.Mutation)
        self.connect(self.aInstrMutation, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrLamination = QtGui.QAction(QtGui.QIcon(
                    'icons/lamination.png'), self.tr('Lamination'), self)
        self.aInstrLamination.setShortcut('Ctrl+Shift+L')
        self.aInstrLamination.setStatusTip(self.tr('Lamination'))
        reg = lambda: self.setInstr(Instruments.Lamination)
        self.connect(self.aInstrLamination, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrAddToScheme = QtGui.QAction(QtGui.QIcon(
                    'icons/add_to_scheme.png'), self.tr('Add to scheme'), self)
        self.aInstrAddToScheme.setStatusTip(self.tr('Add thesis to scheme'))
        reg = lambda: self.setInstr(Instruments.addToScheme)
        self.connect(self.aInstrAddToScheme, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrMove = QtGui.QAction(QtGui.QIcon(
                'icons/move.png'), self.tr('Move'), self)
        self.aInstrMove.setStatusTip(
                            self.tr('This is a hand, you can move thesis on scheme with this'))
        self.aInstrMove.setShortcut('Ctrl+M')
        reg = lambda: self.setInstr(Instruments.moveView)
        self.connect(self.aInstrMove, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrDelThesis = QtGui.QAction(QtGui.QIcon('icons/del_thesis.png'),
                                                self.tr('Remove thesis'), self) 
        self.aInstrDelThesis.setStatusTip(self.tr('Instrument for remove thesis'))
        self.aInstrDelThesis.setShortcut('Ctrl+Shift+D')
        reg = lambda: self.setInstr(Instruments.delThesis)
        self.connect(self.aInstrDelThesis, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrRm = QtGui.QAction(QtGui.QIcon(
                'icons/del_from_scheme.png'), self.tr('Remove from scheme'), self)
        self.aInstrRm.setStatusTip(
                            self.tr('Instrument for remove thesis from scheme'))
        self.aInstrRm.setShortcut('Ctrl+D')
        reg = lambda: self.setInstr(Instruments.rmView)
        self.connect(self.aInstrRm, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrLink = QtGui.QAction(QtGui.QIcon(
                'icons/link.png'), self.tr('Add link'), self)
        self.aInstrLink.setStatusTip(
                            self.tr('Instrument for adding links'))
        self.aInstrLink.setShortcut('Ctrl+L')
        reg = lambda: self.setInstr(Instruments.createLink)
        self.connect(self.aInstrLink, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrRmLink = QtGui.QAction(QtGui.QIcon(
                'icons/rm_link.png'), self.tr('Remove link'), self)
        self.aInstrRmLink.setStatusTip(
                            self.tr('Instrument for remove links'))
        reg = lambda: self.setInstr(Instruments.rmLink)
        self.connect(self.aInstrRmLink, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrAddDer = QtGui.QAction(QtGui.QIcon(
                'icons/add_der.png'), self.tr('Derivatives show'), self)
        self.aInstrAddDer.setStatusTip(
                            self.tr('Instrument for show derivatives'))
        reg = lambda: self.setInstr(Instruments.addDer)
        self.connect(self.aInstrAddDer, QtCore.SIGNAL('triggered()'), reg)

        self.aInstrAddADer = QtGui.QAction(QtGui.QIcon(
                'icons/add_antider.png'), self.tr('Antiderivatives show'), self)
        self.aInstrAddADer.setStatusTip(
                            self.tr('Instrument for show antiderivatives'))
        reg = lambda: self.setInstr(Instruments.addAntider)
        self.connect(self.aInstrAddADer, QtCore.SIGNAL('triggered()'), reg)

        self.aRedColor = QtGui.QAction(QtGui.QIcon(
                'icons/red.png'), self.tr('Red color'), self)
        self.aRedColor.setStatusTip(self.tr('Red color for mutation'))
        reg = lambda: self.widget.Scheme.setColor(QtCore.Qt.red)
        self.connect(self.aRedColor, QtCore.SIGNAL('triggered()'), reg)

        self.aGreenColor = QtGui.QAction(QtGui.QIcon(
                'icons/green.png'), self.tr('Green color'), self)
        self.aGreenColor.setStatusTip(self.tr('Green color for mutation'))
        reg = lambda: self.widget.Scheme.setColor(QtCore.Qt.green)
        self.connect(self.aGreenColor, QtCore.SIGNAL('triggered()'), reg)

        self.aYellowColor = QtGui.QAction(QtGui.QIcon(
                'icons/yellow.png'), self.tr('Yellow color'), self)
        self.aYellowColor.setStatusTip(self.tr('Yellow color for mutation'))
        reg = lambda: self.widget.Scheme.setColor(QtCore.Qt.yellow)
        self.connect(self.aYellowColor, QtCore.SIGNAL('triggered()'), reg)

        self.aDoneMut = QtGui.QAction(QtGui.QIcon(
                'icons/start_mutation.png'), self.tr('Start mutation'), self)
        self.aDoneMut.setStatusTip(self.tr('Start mutation'))
        self.connect(self.aDoneMut, QtCore.SIGNAL('triggered()'),
                                    self.widget.Scheme.activateMutation)
        self.aDoneMut.setEnabled(0)
            

        MenuBar = self.menuBar()
        self.mbFile = MenuBar.addMenu(self.tr('&File'))
        self.mbFile.addAction(self.aNewWorkspace)
        self.mbFile.addAction(self.aOpen)
        self.mbFile.addAction(self.aSave)
        self.mbFile.addAction(self.aSaveAs)
        self.mbFile.addAction(self.aExit)

        self.tbWorkspace = self.addToolBar(self.tr('File'))
        self.tbWorkspace.addAction(self.aNewWorkspace)
        self.tbWorkspace.addAction(self.aOpen)
        self.tbWorkspace.addAction(self.aSave)
        self.tbWorkspace.addAction(self.aSaveAs)
        self.tbWorkspace.addAction(self.aConfig)

        self.tbInstruments = self.addToolBar(self.tr('Base instruments'))

        grInstr = QtGui.QActionGroup(self.tbInstruments)
        self.aInstrAddToScheme.setActionGroup(grInstr)
        self.aInstrDelThesis.setActionGroup(grInstr)
        self.aInstrLink.setActionGroup(grInstr)
        self.aInstrRmLink.setActionGroup(grInstr)
        self.aInstrConvolution.setActionGroup(grInstr)
        self.aInstrMutation.setActionGroup(grInstr)

        self.aInstrMove.setActionGroup(grInstr)
        self.aInstrRm.setActionGroup(grInstr)
        self.aInstrAddADer.setActionGroup(grInstr)
        self.aInstrAddDer.setActionGroup(grInstr)
        self.aInstrGlue.setActionGroup(grInstr)
        self.aInstrLamination.setActionGroup(grInstr)

        self.tbInstruments.addAction(self.aNewThesis)
        self.tbInstruments.addAction(self.aInstrAddToScheme)
        self.tbInstruments.addAction(self.aInstrDelThesis)
        self.tbInstruments.addAction(self.aInstrLink)
        self.tbInstruments.addAction(self.aInstrRmLink)
        self.tbInstruments.addAction(self.aInstrConvolution)
        self.tbInstruments.addAction(self.aInstrMutation)

        self.tbVisioInstr = self.addToolBar(self.tr('Visualisation instruments'))
        self.tbVisioInstr.addAction(self.aInstrMove)
        self.tbVisioInstr.addAction(self.aInstrRm)
        self.tbVisioInstr.addAction(self.aInstrAddADer)
        self.tbVisioInstr.addAction(self.aInstrAddDer)
        self.tbVisioInstr.addAction(self.aInstrGlue)
        self.tbVisioInstr.addAction(self.aInstrLamination)
        self.tbVisioInstr.addAction(self.aClearScheme)
        self.tbVisioInstr.addAction(self.aZoomIn)
        self.tbVisioInstr.addAction(self.aZoomOut)
        self.tbVisioInstr.addAction(self.aZoomOrig)

        self.mbBaseInstr = MenuBar.addMenu(self.tr('&Base'))
        self.mbVisioInstr = MenuBar.addMenu(self.tr('&Visualisation'))

        self.mbBaseInstr.addAction(self.aNewThesis)
        self.mbBaseInstr.addAction(self.aInstrAddToScheme)
        self.mbBaseInstr.addAction(self.aInstrDelThesis)
        self.mbBaseInstr.addAction(self.aInstrLink)
        self.mbBaseInstr.addAction(self.aInstrRmLink)
        self.mbBaseInstr.addAction(self.aInstrConvolution)
        self.mbBaseInstr.addAction(self.aInstrMutation)

        self.mbVisioInstr.addAction(self.aInstrMove)
        self.mbVisioInstr.addAction(self.aInstrRm)
        self.mbVisioInstr.addAction(self.aInstrAddADer)
        self.mbVisioInstr.addAction(self.aInstrAddDer)
        self.mbVisioInstr.addAction(self.aInstrGlue)
        self.mbVisioInstr.addAction(self.aInstrLamination)
        self.mbVisioInstr.addAction(self.aClearScheme)
        self.mbVisioInstr.addAction(self.aZoomIn)
        self.mbVisioInstr.addAction(self.aZoomOut)
        self.mbVisioInstr.addAction(self.aZoomOrig)

        for instr in grInstr.actions():
            instr.setCheckable(1)

        grInstr.setExclusive(1)
        self.aInstrMove.setChecked(1)
        self.tbColors = None

#       self.statusBar()

        self.cfgDialog = ConfigDialog.cfgDialog(self)
        self.connect(self.cfgDialog, QtCore.SIGNAL('ChangeLanguage(QString *)'), self.changLang) 

        self.setCentralWidget(self.widget)

    def clearScheme(self):
        self.widget.Scheme.delAll()
        self.disactivateMutation()

    def activateMutation(self):
        self.aDoneMut.setEnabled(1)

    def disactivateMutation(self):
        self.aDoneMut.setEnabled(0)

    def addColorsBar(self):
        if (self.tbColors != None):
            return
        self.tbColors = self.addToolBar(self.tr('Colors'))
        self.grColors = QtGui.QActionGroup(self.tbColors)
        self.aRedColor.setActionGroup(self.grColors)
        self.aGreenColor.setActionGroup(self.grColors)
        self.aYellowColor.setActionGroup(self.grColors)
        for col in self.grColors.actions():
            col.setCheckable(1)
            self.tbColors.addAction(col)
        self.grColors.setExclusive(1)
        self.aRedColor.setChecked(1)
        self.tbColors.addAction(self.aDoneMut)

    def setMutation(self, instr):
        self.widget.setInstr(instr)
        self.aDoneMut.setEnabled(0)
        self.removeToolBar(self.tbColors)
        self.tbColors = None

    def setInstr(self, instr):
        self.removeToolBar(self.tbColors)
        self.aDoneMut.setEnabled(0)
        self.tbColors = None
        self.widget.setInstr(instr)

    def retranslateUi(self):
        self.setWindowTitle(self.tr('Cognitive assistent v0.5'))

        self.aExit.setText(self.tr('Quit'))
        self.aExit.setStatusTip(self.tr('Quit'))

        self.aSaveAs.setText(self.tr('Save As'))
        self.aSaveAs.setStatusTip(self.tr('Save scheme as'))

        if (self.tbColors != None):
            self.tbColor.setText(self.tr('Colors'))

        self.aConfig.setText(self.tr('Configure')) 
        self.aConfig.setStatusTip(self.tr('Open configure window'))

        self.aClearScheme.setText(self.tr('Clear scheme'))
        self.aClearScheme.setStatusTip(self.tr('Clear scheme'))

        self.aRedColor.setText(self.tr('Red color'))
        self.aRedColor.setStatusTip(self.tr('Red color for mutation'))

        self.aGreenColor.setText(self.tr('Green color'))
        self.aGreenColor.setStatusTip(self.tr('Green color for mutation'))

        self.aYellowColor.setText(self.tr('Yellow color'))
        self.aYellowColor.setStatusTip(self.tr('Yellow color for mutation'))

        self.aDoneMut.setText(self.tr('Start mutation'))
        self.aDoneMut.setStatusTip(self.tr('Start mutation'))

        self.aSave.setText(self.tr('Save'))
        self.aSave.setStatusTip(self.tr('Save scheme'))

        self.aOpen.setText(self.tr('Open'))
        self.aOpen.setStatusTip(self.tr('Select work directory'))

        self.aNewThesis.setText(self.tr('New thesis'))
        self.aNewThesis.setStatusTip(self.tr('Add new thesis'))

        self.aInstrDelThesis.setText(self.tr('Remove thesis')) 
        self.aInstrDelThesis.setStatusTip(self.tr('Remove current thesis'))

        self.aInstrConvolution.setText(self.tr('Convolution'))
        self.aInstrConvolution.setStatusTip(self.tr(
                            'Instrument to convolution thesises'))

        self.aNewWorkspace.setText(self.tr('Remove all')) 
        self.aNewWorkspace.setStatusTip(self.tr('Remove all'))

        self.aDelFromScheme.setText(self.tr('Remove from scheme'))
        self.aDelFromScheme.setStatusTip(self.tr('Remove thesis from scheme'))

        self.aInstrAddToScheme.setText(self.tr('Add to scheme')) 
        self.aInstrAddToScheme.setStatusTip(self.tr('Add thesis to scheme'))

        self.aInstrMove.setText(self.tr('Move'))
        self.aInstrMove.setStatusTip(
                            self.tr('This is a hand, you can move thesis on scheme with this')) 

        self.aInstrMutation.setText(self.tr('Mutation'))
        self.aInstrMutation.setStatusTip(self.tr('Mutation'))

        self.aInstrLamination.setText(self.tr('Lamination'))
        self.aInstrLamination.setStatusTip(self.tr('Lamination'))

        self.aInstrGlue.setText(self.tr('Glue'))
        self.aInstrGlue.setStatusTip(self.tr('Glue has made links'))


        self.aInstrRm.setText(self.tr('Remove from scheme'))
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

        self.aZoomIn.setText(self.tr('Zoom In'))
        self.aZoomIn.setStatusTip(self.tr('Zoom In'))

        self.aZoomOut.setText(self.tr('Zoom Out'))
        self.aZoomOut.setStatusTip(self.tr('Zoom Out'))
        
        self.aZoomIn.setText(self.tr('Zoom Original'))
        self.aZoomIn.setStatusTip(self.tr('Zoom Original'))

        self.mbFile.setTitle(self.tr('&File'))
        self.mbBaseInstr.setTitle(self.tr('&Base'))
        self.mbVisioInstr.setTitle(self.tr('&Visualisation'))

        self.tbWorkspace.setWindowTitle(self.tr('File'))
        self.tbInstruments.setWindowTitle(self.tr('Base instruments'))
        self.tbVisioInstr.setWindowTitle(self.tr('Visualisation instruments')) 

        self.widget.retranslateUi()
        self.cfgDialog.retranslateUi()

    def config(self):
        self.cfgDialog.show()
        

    def changLang(self, lang):
        self.translator.load(lang, './tr')
        self.retranslateUi()
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, self.tr('Are you sure?'),
		self.tr("Quit?"), QtGui.QMessageBox.Yes, 
                                                    QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
#            self.widget.NewWorkspace()
            event.accept()
        else:
            event.ignore()
