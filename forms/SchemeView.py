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

    curPos = QtCore.QPointF(0, 0)
    itemsOnScheme = {}

    def delThesis(self, thesis):
        if self.itemsOnScheme.has_key(thesis):
            self.scene.removeItem(self.itemsOnScheme[thesis])
            self.scene.update()
            self.itemsOnScheme.pop(thesis)

    def addThesis(self, thesis):
        item = ThesisView(thesis)
        item.setPos(self.curPos)
        self.itemsOnScheme[thesis] = item
        self.scene.addItem(item)
        self.curPos += QtCore.QPointF(10, 10)

class ThesisView(QtGui.QGraphicsItem):

    form = QtCore.QRectF(-55, -20, 110, 40)

    def __init__(self, item = QtGui.QListWidgetItem(), color = QtCore.Qt.white):
        QtGui.QGraphicsItem.__init__(self)
        self.setCursor(QtCore.Qt.OpenHandCursor)
        self.color = color
        self.item = item
        self.setZValue(0)

    def setColor(self, color):
        self.color = color

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawRect(self.form)
        font = painter.font()
        font.setPixelSize(12)
        painter.setFont(font)
        painter.drawText(self.form,
                            QtCore.Qt.AlignCenter, self.item.text())

    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            event.ignore()
            return
        self.setCursor(QtCore.Qt.ClosedHandCursor)
        self.sp = event.screenPos()

    def mouseReleaseEvent(self, event):
        self.setCursor(QtCore.Qt.OpenHandCursor)

    def mouseMoveEvent(self, event):
        dp = event.screenPos() - self.sp
        self.sp = event.screenPos()

        self.moveBy(dp.x(), dp.y())

    def boundingRect(self):
        x, y, w, h = self.form.getRect()
        return QtCore.QRectF(x - 0.5, y - 0.5, w + 1, h + 1)
