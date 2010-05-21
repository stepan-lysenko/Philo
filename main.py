##!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore 
from forms import MainWindow

def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow.MainWindow()
    app.installTranslator(window.translator)
    window.retranslateUi()
    window.show()
    sys.exit(app.exec_())
	
if __name__ == "__main__":
    main()
