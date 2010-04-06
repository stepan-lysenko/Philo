#-*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class moveView:
    cursor = QtCore.Qt.OpenHandCursor
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
        if len(items) < 2:
            self.setLink = 0
            return

        self.cur = items[1]
        self.cur.setZValue(1)
        self.move = 1
        self.setCursor(QtCore.Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self.move == 1:
            dp = event.pos() - self.sp
            self.sp = event.pos()
    
            self.cur.moveBy(dp.x(), dp.y())
            self.arrows.update()

    def mouseReleaseEvent(self, event):
        self.move = 0
        self.setCursor(QtCore.Qt.OpenHandCursor)

class rmView:
    cursor = QtCore.Qt.CrossCursor
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

class createLink:
    cursor = QtCore.Qt.UpArrowCursor
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
            if flag == 0:
                if self.searchCircle(link, self.curItem.text()):
                    QtGui.QMessageBox.warning(self, u'Цикл',
                        u'Добавление данной связи приведёт к возникновению цикла') 
                else:
                    if (link != self.curItem) & (len(self.curItem.links) < 3):
                        self.curItem.links.append(link.text())
        self.update()
        self.arrows.update()
