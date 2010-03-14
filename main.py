#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui 
from forms import MainWindow

def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow.MainWindow()
    window.show()
    sys.exit(app.exec_())
	
if __name__ == "__main__":
    main()

