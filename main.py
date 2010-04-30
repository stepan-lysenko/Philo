#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore 
from forms import MainWindow

def main():
    app = QtGui.QApplication(sys.argv)
    translator = QtCore.QTranslator()
    translator.load(QtCore.QLocale.system().name(), './tr')
    app.installTranslator(translator)
    window = MainWindow.MainWindow()
    window.show()
    sys.exit(app.exec_())
	
if __name__ == "__main__":
    main()
