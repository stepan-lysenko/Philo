#-*- coding: utf-8 -*-

import sys, string, math, Instruments, LamWidget, ThesisBase
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
    redItems = []
    greenItems = []
    yellowItems = []
    curColor = QtCore.Qt.red
    setLink = 0
    lams = []
    mutRoot = None
    matrix = None

    def delAll(self):
        for key in self.itemsOnScheme.keys():
            for view in self.itemsOnScheme[key]:
                self.rmView(view)
        self.scene.update()

    def searchAderForMut(self, item):
        for it in [self.searchThesis(i) for i in self.mutRoot.links]:
            if item.text() in it.links:
                return it

    def makeMatrix():
        self.matrix = {}
        self.aders = {}
        for i in self.redItems:
            self.aders[self.redItems.index(i)] = self.searchAderForMut(i)
        for items in self.redItems:
            pass

    def activateMutation():
       pass 
    def viewNine(self, item):
        coords_lnk = [[0, -70], [100, 50], [-100, 50]]
        coords = []
        coords.append([[0, -140], [-150, -70], [150, -70]])
        coords.append([[250, 50], [250, 150], [100, 150]])
        coords.append([[-250, 50], [-250, 150], [-100, 150]])
        self.addThesis(item, x=0, y=0)
        i = 0
        for lnk in [self.searchThesis(it) for it in item.links]:
            self.addThesis(lnk, x=coords_lnk[i][0],
                        y=coords_lnk[i][1], setCenter=0)
            j = 0
            for link in [self.searchThesis(ite) for ite in lnk.links]:
                self.addThesis(link, x=coords[i][j][0],
                        y=coords[i][j][1], setCenter=0)
                j += 1
            i += 1
            
        

    def setColor(self, color):
        self.curColor = color

    def isFull(self, item):
        if (len(item.links) < 3):
            QtGui.QMessageBox.warning(self, self.tr('Mutation'),
                        self.tr('This elem can not be mutate'))
            return 0
        links = []
        for lnk in [self.searchThesis(it) for it in item.links]:
            links.append(lnk.links)
        links = set(links)
        if (len(links) < 9):
            QtGui.QMessageBox.warning(self, self.tr('Mutation'),
                           self.tr('This elem can not be mutate'))
            return 0
        return 1

    def setColorToMutation(self, thesis):
        if thesis in self.greenItems:
            self.greenItems.pop(self.greenItems.index(thesis))
            for view in self.itemsOnScheme[thesis]:
                view.setColor(QtCore.Qt.white)
            if self.curColor == QtCore.Qt.green:
                return
        if thesis in self.redItems:
            self.redItems.pop(self.redItems.index(thesis))
            for view in self.itemsOnScheme[thesis]:
                view.setColor(QtCore.Qt.white)
            if self.curColor == QtCore.Qt.red:
                return
        if thesis in self.yellowItems:
            self.yellowItems.pop(self.yellowItems.index(thesis))
            for view in self.itemsOnScheme[thesis]:
                view.setColor(QtCore.Qt.white)
            if self.curColor == QtCore.Qt.yellow:
                return

        if self.curColor == QtCore.Qt.green:
            ls = self.greenItems
        if self.curColor == QtCore.Qt.red:
            ls = self.redItems
        if self.curColor == QtCore.Qt.yellow:
            ls = self.yellowItems
        ln = len(ls)
        if thesis in ls:
            ls.pop(ls.index(thesis))
            for view in self.itemsOnScheme[thesis]:
                view.setColor(QtCore.Qt.white)
            return
        if ln >= 3:
            for view in self.itemsOnScheme[ls[0]]:
                view.setColor(QtCore.Qt.white)
            ls.pop(0)
        ln = len(ls)
        lnks = self.mutRoot.links
        if (thesis.text() in self.mutRoot.links) or (thesis == self.mutRoot):
            return
        if ln == 0:
            ls.append(thesis)
            for i in self.itemsOnScheme[thesis]:
                i.setColor(self.curColor)
            return
        aders = [self.searchThesis(i) for i in self.mutRoot.links]
        for ad in aders:
            if (thesis.text() in ad.links):
                if (ls[0].text() in ad.links):
                    for view in self.itemsOnScheme[ls[0]]:
                        view.setColor(QtCore.Qt.white)
                    ls.pop(0)
                    ls.append(thesis)
                    for view in self.itemsOnScheme[thesis]:
                        view.setColor(self.curColor)
                    return
                if ln > 1:
                    if (ls[1].text() in ad.links):
                        for view in self.itemsOnScheme[ls[1]]:
                            view.setColor(QtCore.Qt.white)
                        ls.pop(1)
                        ls.append(thesis)
                        for view in self.itemsOnScheme[thesis]:
                            view.setColor(self.curColor)
                        return

        ls.append(thesis)
        for view in self.itemsOnScheme[thesis]:
            view.setColor(self.curColor)

    def lamination(self):
        if (len(self.selItems) == 0) or (len(self.lams) >= 3):
            return
        lam = LamWidget.lamDialog(self, self.selItems)
        self.connect(lam, QtCore.SIGNAL('closeLam(QDialog *)'),
                                                    self.delDialog)
        self.connect(lam, QtCore.SIGNAL('itemOnLamClicked(Thesis *)'),
                                                self.itemOnLamClicked)
        elemsToView = self.searchAntiDers(self.selItems[0])
        for item in self.selItems:
            elemsToView = list(set(elemsToView) &
                            set(self.searchAntiDers(item)))
        for elem in elemsToView:
            tmp = elem.clone()
            tmp.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
#            if elem.isSelected():
#                tmp.setSelected(1)
            lam.addThesis(tmp)
#        self.emit(QtCore.SIGNAL('newLam(QDialog *)'), lam)             
        lam.show()
        self.lams.append(lam)
        lam.allThesises = self.itemsOnScheme

    def itemOnLamClicked(self, item):
        self.emit(QtCore.SIGNAL('itemOnLamClicked(Thesis *)'), item)

    def lamSelectionChanged(self, list):
        for item in list:
            for t in self.itemsOnScheme.keys():
                if t.text() == item.text():
                    t.setSelected(item.isSelected())   


    def delDialog(self, dialog):
        self.lams.pop(self.lams.index(dialog))

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
#        if len(elemsToView) == 0:
#            self.emit(QtCore.SIGNAL('glue(list)'), self.selItems)

    def searchAntiDers(self, thesis):
        res = []
        for item in self.itemsOnScheme.keys():
            if thesis.text() in item.links:
                res.append(item)
        return res
        
                
    def MmouseDoubleClickEvent(self, event):
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

#    def keyReleaseEvent(self, event):
#        self.KeyReleaseEvent(self, event)

    def mousePressEvent(self, event):
        self.MousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.MouseReleaseEvent(self, event)

    def setInstr(self, instr):
        self.selItems = []
        self.delAllGags()
        self.arrows.rmOn = 0
        self.setLink = 0
        self.updateSelection()
        self.redItems = []
        self.greenItems = []
        self.yellowItems = []
        self.MouseMoveEvent = instr.mouseMoveEvent
        self.MouseReleaseEvent = instr.mouseReleaseEvent
        self.MousePressEvent = instr.mousePressEvent
#        self.KeyReleaseEvent = instr.keyReleaseEvent
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
                self.rmView(item)
            self.scene.update()

    def clear(self):
        self.scene.clear()
        self.itemsOnScheme = {}
        self.arrows = Arrows(self.itemsOnScheme)
        self.scene.addItem(self.arrows)

    def setColorOfThesis(self, thesis, color = QtCore.Qt.white):
        if self.itemsOnScheme.has_key(thesis):
            for item in self.itemsOnScheme[thesis]:
                item.setColor(color)
        self.update()

    def newGag(self, links, color = QtCore.Qt.white, x = None, y = None):
        tmp = ThesisBase.Thesis()
        self.itemsOnScheme[tmp] = []
        tmp.links = links
        item = ThesisView(tmp, color)
        item.setText(QtCore.QString('???'))
        item.setTextInteractionFlags(QtCore.Qt.TextEditable)
        self.connect(item, QtCore.SIGNAL('contentsChanged()'), self.gagChanged)
        self.itemsOnScheme[tmp].append(item)
        item.setZValue(10000)
        if (x == None) | (y == None):
            pos = self.curPos
            self.curPos += QtCore.QPointF(10, 10)
        else:
            pos = QtCore.QPointF(x, y)
        item.setPos(pos)
        self.scene.addItem(item)
        self.arrows.updateDic(self.itemsOnScheme)
        self.resort()

    def gagChanged(self):
        print 1234

    def delAllGags(self):
        for key in self.itemsOnScheme.keys():
            for view in self.itemsOnScheme[key]:
                if (view.textInteractionFlags() == QtCore.Qt.TextEditable):
                    for v in self.itemsOnScheme[key]:
                        self.rmView(v)
                    self.itemsOnScheme.pop(key)
                    break
            

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
                        dltx = -50
                        dlty = -13
                        StartPoint = QtCore.QPointF(start.x() - dltx, start.y() - dlty)
                        for end in self.dic[thesis]:
                            painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
                            if self.rmOn and (not self.flag) and (start.x() != end.x()) and (start.y() != end.y()):
                                det0 = (self.pos.y() - start.y() + 20) / (end.y() - start.y())
                                det0 -= (self.pos.x() - start.x() + 20) / (end.x() - start.x())
                                det1 = (self.pos.y() - start.y() - 20) / (end.y() - start.y())
                                det1 -= (self.pos.x() - start.x() - 20) / (end.x() - start.x())
                                det2 = self.pos.y() - start.y() - self.pos.x() + start.x()
                                det3 = self.pos.y() - end.y() - self.pos.x() + end.x()

                                if ((det0 * det1 < 0) and (det2 * det3 < 0)):
                                    painter.setPen(QtGui.QPen(
                                                    QtCore.Qt.red, 2))
                                    self.linkToDel.append(key)
                                    self.linkToDel.append(thesis)
                                    self.sp = start.pos()
                                    self.ep = end.pos()
                                    self.flag = 1
                            if (len(self.linkToDel) > 0):
                                if ((key == self.linkToDel[0]) and (thesis == self.linkToDel[1])):
                                    painter.setPen(QtGui.QPen(QtCore.Qt.red, 2))
                            EndPoint = QtCore.QPointF(end.x() - dltx, end.y() - dlty)
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

class ThesisView(QtGui.QGraphicsTextItem):

    form = QtCore.QRectF(-15, -7, 130, 40)

    def __init__(self, item = QtGui.QListWidgetItem(),
                                    color = QtCore.Qt.white):
        QtGui.QGraphicsTextItem.__init__(self)
        self.setText(item.text())
        self.color = color
        self.item = item
        self.font = QtGui.QFont()
        self.font.setPixelSize(13)
        self.setFont(self.font)
        self.setDefaultTextColor(QtCore.Qt.black)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.setTextWidth(120)
#        self.setX(0)
#        self.setY(0)
        self.setZValue(100000)

    def setText(self, text):
        self.setToolTip(text)
        len = text.length()
        if len < 16:
            self.setPlainText(text)
        else:
            self.setPlainText(text.remove(13, len - 13) + QtCore.QString(u'...'))

    def setColor(self, color):
        self.color = color
        self.update()

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawRect(self.form)
        super(ThesisView, self).paint(painter, option, widget)

    def boundingRect(self):
        x, y, w, h = self.form.getRect()
        return QtCore.QRectF(x - 0.5, y - 0.5, w + 1, h + 1)
