#-*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import MainWidget

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setGeometry(300, 300, 550, 550)

        widget = MainWidget.MainWidget()
        self.setWindowTitle("Philo")

        aExit = QtGui.QAction(QtGui.QIcon('icons/exit.png'),
                                                'Exit', self)
        aExit.setShortcut('Ctrl+Q')
        aExit.setStatusTip('Exit application')
        self.connect(aExit, QtCore.SIGNAL('triggered()'),
        QtCore.SLOT('close()'))

        aSaveAs = QtGui.QAction(QtGui.QIcon('icons/save_as.png'),
                                                    'Save', self)
        aSaveAs.setShortcut('Ctrl+S')
        aSaveAs.setStatusTip('Save data as')
        self.connect(aSaveAs, QtCore.SIGNAL('triggered()'),
                                            widget.currentTab.SaveListAs)

        aOpen = QtGui.QAction(QtGui.QIcon('icons/open.png'),
                                                    'Open', self)
        aOpen.setShortcut('Ctrl+O')
        aOpen.setStatusTip('Open file with data')
        self.connect(aOpen, QtCore.SIGNAL('triggered()'),
                                            widget.currentTab.OpenList)

        aNewThesis = QtGui.QAction(QtGui.QIcon('icons/new_thesis.png'),
                                                'New Thesis', self)
        aNewThesis.setShortcut('Ctrl+N')
        aNewThesis.setStatusTip('Create new thesis')
        self.connect(aNewThesis, QtCore.SIGNAL('triggered()'),
                                            widget.currentTab.AddNewThesis)

        aDelThesis = QtGui.QAction(QtGui.QIcon('icons/del_thesis.png'),
                                                'Delete Thesis', self)
        aDelThesis.setStatusTip('Delete current thesis')
        self.connect(aDelThesis, QtCore.SIGNAL('triggered()'),
                                        widget.currentTab.DelCurrentThesis)


        MenuBar = self.menuBar()
        File = MenuBar.addMenu('&File')
        File.addAction(aExit)
        File.addAction(aOpen)
        File.addAction(aSaveAs)

        self.ToolBar = self.addToolBar('Open/Save')
        self.ToolBar.addAction(aOpen)
        self.ToolBar.addAction(aSaveAs)
        self.ToolBar.addAction(aNewThesis)
        self.ToolBar.addAction(aDelThesis)

#       self.statusBar()

        self.setCentralWidget(widget)

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
                        "Are you sure to quit?", QtGui.QMessageBox.Yes, 
                                                    QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
