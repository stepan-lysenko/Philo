#-*- coding: utf-8 -*-

import sys, string
from PyQt4 import QtCore, QtGui

class SchemeView(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        self.setBackgroundBrush(QtGui.QBrush())

        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)
        self.scene.setSceneRect(QtCore.QRectF(-50, -50, 100, 100))

        self.setRenderHint(QtGui.QPainter.Antialiasing)

        item1 = ThesisView(u'text1')
        item1.setPos(0, 0)
        self.scene.addItem(item1)

        item2 = ThesisView(u'text2')
        item2.setPos(-40, 40)
        self.scene.addItem(item2)

    def dropEvent(self, event):
        print 'dropEvent in Scheme'

class ThesisView(QtGui.QGraphicsItem):
    def __init__(self, text = '', color = QtCore.Qt.white):
        QtGui.QGraphicsItem.__init__(self)
        self.setCursor(QtCore.Qt.OpenHandCursor)
        self.color = color
        self.text = text

    def setColor(self, color):
        self.color = color

    def setText(self, text):
        self.text = text

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawRect(-20, -20, 40, 40)
        painter.drawText(QtCore.QRectF(-20, -20, 40, 40),
                            QtCore.Qt.AlignCenter, self.text)

    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            event.ignore()
            return
        self.setCursor(QtCore.Qt.ClosedHandCursor)
        self.sp = event.screenPos()
        self.setZValue(self.zValue() + 1)

    def mouseReleaseEvent(self, event):
        self.setCursor(QtCore.Qt.OpenHandCursor)
        self.setZValue(self.zValue() - 1)

    def mouseMoveEvent(self, event):
        dp = event.screenPos() - self.sp
        self.sp = event.screenPos()

        self.moveBy(dp.x(), dp.y())

    def boundingRect(self):
        return QtCore.QRectF(-20.5, -20.5, 41, 41);
