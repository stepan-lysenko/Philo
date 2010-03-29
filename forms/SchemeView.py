#-*- coding: utf-8 -*-

import sys, string, math
from PyQt4 import QtCore, QtGui

class SchemeView(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        self.setBackgroundBrush(QtGui.QBrush())

        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)
        self.scene.setSceneRect(QtCore.QRectF(-1000, -1000, 2000, 2000))

        self.setRenderHint(QtGui.QPainter.Antialiasing)

        self.arrows = Arrows(self.itemsOnScheme)
        self.scene.addItem(self.arrows)
        self.setCursor(QtCore.Qt.OpenHandCursor)

    curPos = QtCore.QPointF(0, 0)
    itemsOnScheme = {}
    setLink = 0

    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            event.ignore()
            return

        for key in self.itemsOnScheme.keys():
            for item in self.itemsOnScheme[key]:
                item.setZValue(0)

        self.sp = event.pos()
        items = self.items(event.pos())
        if len(items) < 2:
            self.setLink = 0
            self.setCursor(QtCore.Qt.ArrowCursor)
            return

        self.cur = items[1]
        self.cur.setZValue(1)

        if self.setLink == 1:
            self.setLink = 0
            link = self.SearchByView(self.cur)
            self.setCursor(QtCore.Qt.ArrowCursor)
            flag = 0
            if (len(self.curItem.links) < 3) & (link != self.curItem):
                for i in self.curItem.links:
                    if i == link.text():
                        flag = 1
                if flag == 0:
                    self.curItem.links.append(link.text())
        else:
           self.setCursor(QtCore.Qt.ClosedHandCursor)
           self.move = 1
        self.update()
        self.arrows.update()

    def mouseReleaseEvent(self, event):
        if self.move == 1:
            self.setCursor(QtCore.Qt.OpenHandCursor)
            self.move = 0

    def mouseMoveEvent(self, event):
        if self.move == 1:
            dp = event.pos() - self.sp
            self.sp = event.pos()

            self.cur.moveBy(dp.x(), dp.y())
            self.arrows.update()

    def mouseDoubleClickEvent(self, event):
        items = self.items(event.pos())
        if len(items) < 2:
            self.setCursor(QtCore.Qt.ArrowCursor)
            return
        cur = items[1]
        if self.setLink == 0:
            self.setLink = 1
            self.curItem = self.SearchByView(cur)
            self.setCursor(QtCore.Qt.CrossCursor)
        self.update()
        self.arrows.update()

    def SearchByView(self, view):
        for key in self.itemsOnScheme:
            for item in self.itemsOnScheme[key]:
                if item == view:
                    return key
        return 0

    def delThesis(self, thesis):
        if self.itemsOnScheme.has_key(thesis):
            for item in self.itemsOnScheme[thesis]:
                self.scene.removeItem(item)
            self.scene.update()
            self.itemsOnScheme.pop(thesis)
        self.setLink = 0
        self.setCursor(QtCore.Qt.OpenHandCursor)

    def clear(self):
        self.scene.clear()
        self.itemsOnScheme = {}
        self.arrows = Arrows(self.itemsOnScheme)
        self.scene.addItem(self.arrows)
        self.setLink = 0
        self.setCursor(QtCore.Qt.OpenHandCursor)

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
        self.arrows.updateDic(self.itemsOnScheme)
        self.setLink = 0
        self.setCursor(QtCore.Qt.OpenHandCursor)
        

class Arrows(QtGui.QGraphicsItem):
    def __init__(self, dic):
        QtGui.QGraphicsItem.__init__(self)
        self.dic = dic
        self.setZValue(100)

    def updateDic(self, dic):
        self.update()
        self.dic = dic

    def SearchThesis(self, name):
        for key in self.dic.keys():
            if key.text() == name:
                return key
        return 0

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        for key in self.dic.keys():
            for link in key.links:
                thesis = self.SearchThesis(link)
                if thesis != 0:
                    for start in self.dic[key]:
                        StartPoint = QtCore.QPointF(start.x(), start.y())
                        for end in self.dic[thesis]:
                            EndPoint = QtCore.QPointF(end.x(), end.y())
                            n = EndPoint - StartPoint
                            n = n / (0.05 * math.sqrt(n.x() * n.x() +
                                                            n.y() * n.y()))
                            s = math.sin(math.pi / 9.)
                            c = math.cos(math.pi / 9.)

                            if EndPoint.x() == StartPoint.x():
                                if EndPoint.y() > StartPoint.y():
                                    startR = QtCore.QPointF(StartPoint.x(),
                                                        StartPoint.y() + 20)
                                    endR = QtCore.QPointF(StartPoint.x(),
                                                        EndPoint.y() - 20)
                                else:
                                    startR = QtCore.QPointF(StartPoint.x(),
                                                        StartPoint.y() - 20)
                                    endR = QtCore.QPointF(StartPoint.x(),
                                                        EndPoint.y() + 20)
                            elif EndPoint.y() == StartPoint.y():
                                if EndPoint.x() > StartPoint.x():
                                    startR = QtCore.QPointF(StartPoint.x() +
                                                        65, StartPoint.y())
                                    endR = QtCore.QPointF(EndPoint.x() -
                                                        65, EndPoint.y())
                                else:
                                    startR = QtCore.QPointF(StartPoint.x() -
                                                        65, StartPoint.y())
                                    endR = QtCore.QPointF(EndPoint.x() +
                                                        65, EndPoint.y())
                            elif n.x() != 0:
                                k = n.y() / float(n.x())
                                at = abs(20 / 65.)
                                if (abs(k) > at) & (n.y() <= 0):
                                    startR = StartPoint - QtCore.QPointF(
                                                                20. / k, 20)
                                    endR = EndPoint + QtCore.QPointF(
                                                                20. / k, 20)
                                elif (abs(k) > at) & (n.y() > 0):
                                    startR = StartPoint + QtCore.QPointF(
                                                                20. / k, 20)
                                    endR = EndPoint - QtCore.QPointF(
                                                                20. / k, 20)
                                elif (abs(k) < at) & (n.x() > 0):
                                    startR = StartPoint + QtCore.QPointF(
                                                                65, 65 * k)
                                    endR = EndPoint - QtCore.QPointF(
                                                                65, 65 * k)
                                else:
                                    startR = StartPoint - QtCore.QPointF(
                                                                65, 65 * k)
                                    endR = EndPoint + QtCore.QPointF(
                                                                65, 65 * k)

                            r = endR - startR
                            if r.x() * n.x() + r.y() * n.y() <= 0:
                                break

                            painter.drawLine(startR, endR)
                            tmp = QtCore.QPointF(c*n.x() - s*n.y(),
                                                    s*n.x() + c*n.y())
                            painter.drawLine(endR, endR - tmp)
                            tmp = QtCore.QPointF(c*n.x() + s*n.y(),
                                                    -s*n.x() + c*n.y())
                            painter.drawLine(endR, endR - tmp)

    def boundingRect(self):
        return QtCore.QRectF(-1000, -1000, 2000, 2000)

class ThesisView(QtGui.QGraphicsItem):

    form = QtCore.QRectF(-65, -20, 130, 40)

    def __init__(self, item = QtGui.QListWidgetItem(),
                                    color = QtCore.Qt.white):
        QtGui.QGraphicsItem.__init__(self)
        self.color = color
        self.item = item
        self.setZValue(0)

    def setColor(self, color):
        self.color = color
        self.update()

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawRect(self.form)
        font = painter.font()
        font.setPixelSize(13)
        painter.setFont(font)
        painter.drawText(self.form,
                            QtCore.Qt.AlignCenter, self.item.text())

    def boundingRect(self):
        x, y, w, h = self.form.getRect()
        return QtCore.QRectF(x - 0.5, y - 0.5, w + 1, h + 1)
