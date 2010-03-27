#-*- coding: utf-8 -*-

import sys, string
from PyQt4 import QtCore, QtGui

class SchemeView(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        self.setBackgroundBrush(QtGui.QBrush())

        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)
        self.scene.setSceneRect(QtCore.QRectF(-200, -200, 400, 400))

        self.setRenderHint(QtGui.QPainter.Antialiasing)

#        self.arrows = Arrows(self.itemsOnScheme)
#        self.scene.addItem(self.arrows)

    curPos = QtCore.QPointF(0, 0)
    itemsOnScheme = {}

    def delThesis(self, thesis):
        if self.itemsOnScheme.has_key(thesis):
            for item in self.itemsOnScheme[thesis]:
                self.scene.removeItem(item)
            self.scene.update()
            self.itemsOnScheme.pop(thesis)

    def clear(self):
        self.scene.clear()
        self.itemsOnScheme = {}

    def setColorOfThesis(self, thesis, color = QtCore.Qt.white):
        if self.itemsOnScheme.has_key(thesis):
            for item in self.itemsOnScheme[thesis]:
                item.setColor(color)

    def addThesis(self, thesis, color = QtCore.Qt.white, x = None, y = None):
        if not self.itemsOnScheme.has_key(thesis):
            self.itemsOnScheme[thesis] = []
        if (x == None) | (y == None):
            pos = self.curPos
            self.curPos += QtCore.QPointF(10, 10)
        else:
            pos = QtCore.QPointF(x, y)
        item = ThesisView(thesis, color)
        item.setPos(pos)
        self.itemsOnScheme[thesis].append(item)
        self.scene.addItem(item)
#        self.arrows.updateDic(self.itemsOnScheme)
        

class Arrows(QtGui.QGraphicsItem):
    def __init__(self, dic):
        QtGui.QGraphicsItem.__init__(self)
        self.dic = dic
        self.setZValue(100)

    def updateDic(self, dic):
        self.dic = dic
        self.update()

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        for key in self.dic.keys():
            print key.text().toUtf8()
            for link in key.links:
                print link
                for key in self.dic.keys():
                    print key.text()
                    if key.text() == link:
                        LThesis = key
                for start in self.dic[key]:
                    for end in self.dic[LThesis]:
                        a = QtCore.QPointF(start.x(), start.y())
                        b = QtCore.QPointF(end.x(), end.y())
                        painter.drawLine(a, b)
                

    def boundingRect(self):
        return QtCore.QRectF(-50, -50, 100, 100)

class ThesisView(QtGui.QGraphicsItem):

    form = QtCore.QRectF(-55, -20, 110, 40)

    def __init__(self, item = QtGui.QListWidgetItem(),
                                    color = QtCore.Qt.white):
        QtGui.QGraphicsItem.__init__(self)
        self.setCursor(QtCore.Qt.OpenHandCursor)
        self.color = color
        self.item = item
        self.setZValue(0)

    def setColor(self, color):
        self.color = color
        self.update()

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
