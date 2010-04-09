#-*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import ThesisBase, math

class moveView:
    cursor = QtCore.Qt.OpenHandCursor
    listCursor = QtCore.Qt.ArrowCursor

    def mousePressEvent(self, event):
        if (event.button() != QtCore.Qt.LeftButton) & (event.button() != 
                                                    QtCore.Qt.RightButton):
            event.ignore()
            return


        for key in self.itemsOnScheme.keys():
            for item in self.itemsOnScheme[key]:
                item.setZValue(0)

        self.sp = event.pos()
        items = self.items(event.pos())
        self.setCursor(QtCore.Qt.ClosedHandCursor)
        if len(items) < 2:
            self.scroll = 1
            return
        self.scroll = 0
        self.cur = items[1]
        self.cur.setZValue(1)
        self.move = 1

    def mouseMoveEvent(self, event):
        if self.move == 1:
            dp = event.pos() - self.sp
            self.sp = event.pos()
            self.cur.moveBy(dp.x(), dp.y())
            self.arrows.update()
        if self.scroll == 1:
            dp = event.pos() - self.sp
            self.sp = event.pos()
            x = self.horizontalScrollBar().value() - dp.x()
            y = self.verticalScrollBar().value() - dp.y()
            self.horizontalScrollBar().setSliderPosition(x)
            self.verticalScrollBar().setSliderPosition(y)

    def mouseReleaseEvent(self, event):
        self.move = 0
        self.scroll = 0
        self.setCursor(QtCore.Qt.OpenHandCursor)

    @staticmethod
    def listItemClicked(self, item):
        return

class rmView:
    cursor = QtCore.Qt.CrossCursor
    listCursor = QtCore.Qt.CrossCursor

    def mousePressEvent(self, event):
        if (event.button() != QtCore.Qt.LeftButton):
            event.ignore()
            return
        
        for key in self.itemsOnScheme.keys():
            for item in self.itemsOnScheme[key]:
                item.setZValue(0)
    
        self.sp = event.pos()
        items = self.items(event.pos())
        if len(items) < 2:
            self.setLink = 0
            return
        
        self.cur = items[1]
        self.cur.setZValue(1)
        self.rmView(self.cur)

    def mouseMoveEvent(self, event):
        return

    def mouseReleaseEvent(self, event):
        return

    @staticmethod
    def listItemClicked(self, item):
        self.Scheme.delThesis(item)

class createLink:
    cursor = QtCore.Qt.UpArrowCursor
    listCursor = QtCore.Qt.ArrowCursor

    def mousePressEvent(self, event):
        items = self.items(event.pos())
        if len(items) < 2:
            return
        cur = items[1]
        if self.setLink == 0:
            self.setLink = 1
            self.curItem = self.searchByView(cur)
        cur.setZValue(11)
        self.sp = cur.pos()
        self.evPos = event.pos()
        self.curArrow = QtGui.QGraphicsLineItem(0, 0, 0, 0)
        self.curArrow.setZValue(10)
        self.start = self.mapToScene(self.evPos)
        self.curArrow.moveBy(self.start.x(), self.start.y())
        self.scene.addItem(self.curArrow)

        self.lArr = QtGui.QGraphicsLineItem(0, 0, 0, 0)
        self.rArr = QtGui.QGraphicsLineItem(0, 0, 0, 0)
        self.scene.addItem(self.lArr)
        self.scene.addItem(self.rArr)

        self.setCursor(QtCore.Qt.BlankCursor)
        self.update()
        self.arrows.update()

    def mouseMoveEvent(self, event):
        if self.setLink == 1:
            self.curArrow.setLine(0, 0, event.pos().x() - self.evPos.x(),
                                        event.pos().y() - self.evPos.y())

            end = self.mapToScene(event.pos())

            n = QtCore.QPointF(event.pos() - self.evPos)
            n = n / (0.05 * math.sqrt(n.x() * n.x() + n.y() * n.y()))

            s = math.sin(math.pi / 9.)
            c = math.cos(math.pi / 9.)

            self.scene.removeItem(self.lArr)
            self.scene.removeItem(self.rArr)

            tmp = QtCore.QPointF(c*n.x() - s*n.y(), s*n.x() + c*n.y())
            self.lArr = QtGui.QGraphicsLineItem(0, 0, -tmp.x(), -tmp.y())
            self.scene.addItem(self.lArr)
            self.lArr.setZValue(10)
            self.lArr.moveBy(end.x(), end.y())

            tmp = QtCore.QPointF(c*n.x() + s*n.y(), -s*n.x() + c*n.y())
            self.rArr = QtGui.QGraphicsLineItem(0, 0, -tmp.x(), -tmp.y())
            self.scene.addItem(self.rArr)
            self.rArr.setZValue(10)
            self.rArr.moveBy(end.x(), end.y())


    def mouseReleaseEvent(self, event):
        if (event.button() != QtCore.Qt.LeftButton) & (event.button() !=
                                                    QtCore.Qt.RightButton):
            event.ignore()
            return


        self.setCursor(QtCore.Qt.UpArrowCursor)

        for key in self.itemsOnScheme.keys():
            for item in self.itemsOnScheme[key]:
                item.setZValue(0)
        if self.setLink == 1:
            self.scene.removeItem(self.curArrow)
            self.scene.removeItem(self.rArr)
            self.scene.removeItem(self.lArr)

        self.sp = event.pos()
        items = self.items(event.pos())
        if len(items) < 2:
            self.setLink = 0
            return

        self.cur = items[1]
        self.cur.setZValue(1)

        if self.setLink == 1:
            self.setLink = 0
            link = self.searchByView(self.cur)
            if link == self.curItem:
                return
            flag = 0
            for i in self.curItem.links:
                if i == link.text():
                    flag = 1
                    if (len(self.curItem.links) > 0):
                        return
            if flag == 0:
                if self.searchCircle(link, self.curItem.text()):
                    QtGui.QMessageBox.warning(self, u'Цикл',
                        u'Добавление данной связи приведёт к возникновению цикла') 
                else:
                    if (link != self.curItem) & (len(self.curItem.links) < 3):
                        self.curItem.links.append(link.text())
        self.update()
        self.arrows.update()

    @staticmethod
    def listItemClicked(self, item):
        return

class rmLink:
    cursor = QtCore.Qt.UpArrowCursor
    listCursor = QtCore.Qt.ArrowCursor

    def mousePressEvent(self, event):
        items = self.items(event.pos())
        if len(items) < 2:
            return
        cur = items[1]
        if self.setLink == 0:
            self.setLink = 1
            self.curItem = self.searchByView(cur)
        self.update()
        self.arrows.update()

    def mouseMoveEvent(self, event):
        return

    def mouseReleaseEvent(self, event):
        if (event.button() != QtCore.Qt.LeftButton) & (event.button() !=
                                                    QtCore.Qt.RightButton):
            event.ignore()
            return


        for key in self.itemsOnScheme.keys():
            for item in self.itemsOnScheme[key]:
                item.setZValue(0)

        self.sp = event.pos()
        items = self.items(event.pos())
        if len(items) < 2:
            self.setLink = 0
            return

        self.cur = items[1]
        self.cur.setZValue(1)

        if self.setLink == 1:
            self.setLink = 0
            link = self.searchByView(self.cur)
            if link == self.curItem:
                return
            flag = 0
            for i in self.curItem.links:
                if i == link.text():
                    flag = 1
                    if (len(self.curItem.links) > 0):
                        self.curItem.links.remove(link.text())
        self.update()
        self.arrows.update()

    @staticmethod
    def listItemClicked(self, item):
        return

class addToScheme:
    cursor = QtCore.Qt.CrossCursor
    listCursor = QtCore.Qt.CrossCursor

    def mousePressEvent(self, event):
        items = self.items(event.pos())
        if len(items) < 2:
            return
        cur = items[1]
        curItem = self.searchByView(cur)
        color = cur.color
        self.addThesis(curItem, color)
        self.update()
        self.arrows.update()

    def mouseMoveEvent(self, event):
        pass
    def mouseReleaseEvent(self, event):
        pass

    @staticmethod
    def listItemClicked(self, item):
        self.Scheme.addThesis(item, QtCore.Qt.green)
