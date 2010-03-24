#-*- coding: utf-8 -*-

import sys, string
from PyQt4 import QtCore, QtGui

class SchemeView(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        item1 = ThesisView(QtCore.Qt.green)
        item1.setPos(0, 0)
        self.scene.addItem(item1)
        item2 = ThesisView(QtCore.Qt.blue)
        item2.setPos(-40, 40)
        self.scene.addItem(item2)

class ThesisView(QtGui.QGraphicsItem):
    def __init__(self, color=QtCore.Qt.white):
        QtGui.QGraphicsItem.__init__(self)
        self.color = color

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawRect(0, 0, 40, 40)

    def boundingRect(self):
        return QtCore.QRectF(-15.5, -15.5, 34, 34);
