#-*- coding: utf-8 -*-

import sys, string, math, Instruments
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
        self.setInstr(Instruments.moveView)

        self.horizontalScrollBar().setRange(-1000, 1000)
        self.horizontalScrollBar().setPageStep(1)
        self.verticalScrollBar().setRange(-1000, 1000)
        self.verticalScrollBar().setPageStep(1)

    curPos = QtCore.QPointF(0, 0)
    itemsOnScheme = {}
    setLink = 0

    def rmView(self, view):
        thesis = self.searchByView(view)
        if len(self.itemsOnScheme[thesis]) <= 1:
            self.itemsOnScheme.pop(thesis)
        else:
            self.itemsOnScheme[thesis].remove(view)
        self.scene.removeItem(view)
        self.arrows.update()
        self.update()

    def setInstr(self, instr):
        self.mouseMoveEvent = instr.mouseMoveEvent
        self.mouseReleaseEvent = instr.mouseReleaseEvent
        self.mousePressEvent = instr.mousePressEvent
        self.setCursor(instr.cursor)

    def searchCircle(self, root, link, parent = QtCore.QString()):
        cand = []
        for i in root.links:
            if i != parent:
                cand.append(i)
        for key in self.itemsOnScheme.keys():
            for i in key.links:
                if key.text() != parent:
                    if i == root.text():
                            cand.append(key.text())
        if len(cand) == 0:
            return 0
        for i in cand:
            if i == link:
                return 1
            item = self.searchThesis(i)
            if self.searchCircle(item, link, root.text()):
                return 1
            
    def searchThesis(self, name):
        for key in self.itemsOnScheme.keys():
            if key.text() == name:
                return key
        return 0

    def searchByView(self, view):
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

    def clear(self):
        self.scene.clear()
        self.itemsOnScheme = {}
        self.arrows = Arrows(self.itemsOnScheme)
        self.scene.addItem(self.arrows)
        self.setLink = 0

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
        self.centerOn(item)
        

class Arrows(QtGui.QGraphicsItem):
    def __init__(self, dic):
        QtGui.QGraphicsItem.__init__(self)
        self.dic = dic
        self.setZValue(100)

    def updateDic(self, dic):
        self.update()
        self.dic = dic

    def searchThesis(self, name):
        for key in self.dic.keys():
            if key.text() == name:
                return key
        return 0

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        for key in self.dic.keys():
            for link in key.links:
                thesis = self.searchThesis(link)
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
