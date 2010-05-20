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

    def glue(self):
        if len(self.selItems) == 0:
            return
#        elemsToView = self.searchAntiDers(self.selItems[0])
        elemsToView = self.selItems[0].links                            #
        for item in self.selItems:
#            elemsToView = list(set(elemsToView) &
#                            set(self.searchAntiDers(item)))
            elemsToView = list(set(item.links) & set(elemsToView))      #
        elemsToView = [self.searchThesis(elem) for elem in elemsToView] #
        for elems in elemsToView:
            self.addThesis(elems)
        if len(elemsToView) == 0:
            self.emit(QtCore.SIGNAL('glue(list)'), self.selItems)

    def searchAntiDers(self, thesis):
        res = []
        for item in self.itemsOnScheme.keys():
            if thesis.text() in item.links:
                res.append(item)
        return res
        
                
    def mouseDoubleClickEvent(self, event):
        if (event.button() != QtCore.Qt.LeftButton):
           event.ignore()
           return
        self.sp = event.pos()
        items = self.items(self.sp)
        if len(items) < 2:
            self.scroll = 1
            return
        
        self.cur = items[1]
        thesis = self.searchByView(self.cur)
        self.emit(QtCore.SIGNAL('editThesisName(Thesis *)'), thesis)
        
    def convolution(self):
        cand = []
        for thesis in self.itemsOnScheme.keys():
            for link in thesis.links:
                for item in self.selItems:
                    if item.text() == link:
                        cand.append(thesis)
        cand = list(set(cand))
        for item in cand:
            selTexts = [a.text() for a in self.selItems]
            f = lambda a: a in item.links
            if len(filter(f, selTexts)) == 3:
                self.addThesis(item)
                self.updateSelection()
                self.arrows.update()
                self.update()
                return

        self.emit(QtCore.SIGNAL('convolution(list)'), self.selItems)
        self.arrows.update()
        self.update()
            
 
    def updateSelection(self):
        for thesis in self.itemsOnScheme.keys():
            if thesis.isSelected():
                self.setColorOfThesis(thesis, QtCore.Qt.green)
            else:
                self.setColorOfThesis(thesis)
                
    def resort(self):
        views = {}
        for key in self.itemsOnScheme.keys():
            for view in self.itemsOnScheme[key]:
                views[view.zValue()] = view
        keys = views.keys()
        keys.sort()
        nz = 0
        for z in keys:
            views[z].setZValue(nz)
            nz += 1
            
    def rmView(self, view):
        thesis = self.searchByView(view)
        if len(self.itemsOnScheme[thesis]) < 1:
#            self.itemsOnScheme.pop(thesis)
            pass
        else:
            self.itemsOnScheme[thesis].remove(view)
        self.scene.removeItem(view)
        self.arrows.update()
        self.update()

    def mouseMoveEvent(self, event):
        self.MouseMoveEvent(self, event)

        
    def keyReleaseEvent(self, event):
        self.KeyReleaseEvent(self, event)

    def mousePressEvent(self, event):
        self.MousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.MouseReleaseEvent(self, event)

    def setInstr(self, instr):
        self.selItems = []
        self.arrows.rmOn = 0
        self.updateSelection()
        self.MouseMoveEvent = instr.mouseMoveEvent
        self.MouseReleaseEvent = instr.mouseReleaseEvent
        self.MousePressEvent = instr.mousePressEvent
        self.KeyReleaseEvent = instr.keyReleaseEvent
        self.setCursor(instr.cursor)

    def getSubGraph(self, root, sub = []):
        list = []
        for i in self.getChain(root, 0):
            list.append(i)
        for i in self.getChain(root, 1):
            list.append(i)
        return list

    def getChain(self, root, dir):
        chain = []
        if dir == 0:
            for link in root.links:
                the = self.searchThesis(link)
                chain.append(the)
                for lnk in self.getChain(the, 0):
                    chain.append(lnk)
        else:
            for key in self.itemsOnScheme.keys():
                for i in key.links:
                    if i == root.text():
                        chain.append(key)
                        for t in self.getChain(key, 1):
                            chain.append(t)
            
        return chain

    def searchCircle(self, root, link):
        graph = self.getSubGraph(root)
        lnk = self.searchThesis(link)
        graph.append(lnk)
        graph += self.getChain(lnk, 0)
        if self.searchCircleInGraph(root, link, graph):
            QtGui.QMessageBox.warning(self, self.tr('Cycle'),
                self.tr('Adding this link will lead to a cycle'))
            return 1
        return 0

    def searchCircleInGraph(self, root, link, graph, parent = QtCore.QString()):
        cand = []
        for i in root.links:
            if i != parent:
                it = self.searchThesis(i)
                if it in graph:
                    cand.append(i)
        for key in self.itemsOnScheme.keys():
            for i in key.links:
                if key.text() != parent:
                    if i == root.text():
                        if key in graph:
                            cand.append(key.text())
        if len(cand) == 0:
            return 0
        for i in cand:
            if i == link:
                return 1
            item = self.searchThesis(i)
            if self.searchCircleInGraph(item, link, graph, root.text()):
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
        self.update()

    def addThesis(self, thesis, color = QtCore.Qt.white, x = None, y = None, setCenter = 1):
        if not self.itemsOnScheme.has_key(thesis):
            self.itemsOnScheme[thesis] = []
        if len(self.itemsOnScheme[thesis]) == 1:
            return
        if (x == None) | (y == None):
            pos = self.curPos
            self.curPos += QtCore.QPointF(10, 10)
        else:
            pos = QtCore.QPointF(x, y)
        item = ThesisView(thesis, color)
        item.setZValue(10000)
        item.setPos(pos)
        self.itemsOnScheme[thesis].append(item)
        self.scene.addItem(item)
        self.arrows.updateDic(self.itemsOnScheme)
        self.setLink = 0
        if setCenter:
            self.centerOn(item)
        self.resort()

class Arrows(QtGui.QGraphicsItem):
    rmOn = 0
    linkToDel = []
    sp = QtCore.QPointF(-99999, -99999)
    ep = QtCore.QPointF(-9999, -9999)
    pos = QtCore.QPointF(-99999, -99999)
    flag = 0
    def __init__(self, dic):
        QtGui.QGraphicsItem.__init__(self)
        self.dic = dic
        self.setZValue(10000000)

    def updateDic(self, dic):
        self.update()
        self.dic = dic

    def searchThesis(self, name):
        for key in self.dic.keys():
            if key.text() == name:
                return key
        return 0

    def paint(self, painter, option, widget):
        det0 = (self.pos.y() - self.sp.y() + 20) / (self.ep.y() - self.sp.y() + 0.0000001)  
        det0 -= (self.pos.x() - self.sp.x() + 20) / (self.ep.x() - self.sp.x() + 0.0000001)  
        det1 = (self.pos.y() - self.sp.y() - 20) / (self.ep.y() - self.sp.y() + 0.0000001)  
        det1 -= (self.pos.x() - self.sp.x() - 20) / (self.ep.x() - self.sp.x() + 0.0000001)  
        det2 = self.pos.y() - self.sp.y() - self.pos.x() + self.sp.x() 
        det3 = self.pos.y() - self.sp.y() - self.pos.x() + self.ep.x() 
        if not ((det0 * det1 < 0) and (det2 * det3 < 0)):
            self.linkToDel = []
            self.flag = 0

        for key in self.dic.keys():
            for link in key.links:
                thesis = self.searchThesis(link)
                if thesis != 0:
                    for start in self.dic[key]:
                        StartPoint = QtCore.QPointF(start.x(), start.y())
                        for end in self.dic[thesis]:
                            painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
                            if self.rmOn and (not self.flag) and (start.x() != end.x()) and (start.y() != end.y()):
                                det0 = (self.pos.y() - start.y() + 20) / (end.y() - start.y())
                                det0 -= (self.pos.x() - start.x() + 20) / (end.x() - start.x())
                                det1 = (self.pos.y() - start.y() - 20) / (end.y() - start.y())
                                det1 -= (self.pos.x() - start.x() - 20) / (end.x() - start.x())
                                det2 = self.pos.y() - start.y() - self.pos.x() + start.x()
                                det3 = self.pos.y() - end.y() - self.pos.x() + end.x()

                                if (det0 * det1 < 0) and (det2 * det3 < 0):
                                    painter.setPen(QtGui.QPen(
                                                    QtCore.Qt.red, 2))
                                    self.linkToDel.append(key)
                                    self.linkToDel.append(thesis)
                                    self.sp = start.pos()
                                    self.ep = end.pos()
                                    self.flag = 1
                            if len(self.linkToDel) > 0:
                                if (key == self.linkToDel[0]) and (thesis == self.linkToDel[1]):
                                    painter.setPen(QtGui.QPen(QtCore.Qt.red, 2))
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
        self.setZValue(100000)

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
        text = self.item.text()
        len = text.length()
        if len < 16:
            painter.drawText(self.form,
                            QtCore.Qt.AlignCenter, text)
        else:
            painter.drawText(self.form, QtCore.Qt.AlignCenter,
                text.remove(13, len - 13) + QtCore.QString(u'...'))
        self.setToolTip(self.item.text())

    def boundingRect(self):
        x, y, w, h = self.form.getRect()
        return QtCore.QRectF(x - 0.5, y - 0.5, w + 1, h + 1)
