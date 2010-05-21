#-*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import ThesisBase, math

class moveView:
    cursor = QtCore.Qt.OpenHandCursor
    listCursor = QtCore.Qt.ArrowCursor

    @staticmethod
    def mousePressEvent(self, event):
        if (event.button() != QtCore.Qt.LeftButton):
            event.ignore()
            return

        self.sp = event.pos()
        items = self.items(event.pos())
        self.setCursor(QtCore.Qt.ClosedHandCursor)
        if len(items) < 2:
            self.scroll = 1
            return

        self.scroll = 0
        self.cur = items[1]
        thesis = self.searchByView(self.cur)
        if event.modifiers() == QtCore.Qt.ControlModifier:
            thesis.setSelected(not thesis.isSelected())
        else:
            self.emit(QtCore.SIGNAL('selectOne(Thesis *)'), thesis)
        self.cur.setZValue(100000)
        self.move = 1
        self.resort()

    @staticmethod
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

    @staticmethod
    def mouseReleaseEvent(self, event):
        self.move = 0
        self.scroll = 0
        self.resort()
        self.setCursor(QtCore.Qt.OpenHandCursor)

    @staticmethod
    def listItemClicked(self, item):
        pass

    @staticmethod
    def keyReleaseEvent(self, event):
        pass

class rmView:
    cursor = QtCore.Qt.CrossCursor
    listCursor = QtCore.Qt.CrossCursor

    @staticmethod
    def mousePressEvent(self, event):
        if (event.button() != QtCore.Qt.LeftButton):
            event.ignore()
            return
        
        self.resort() 
        self.sp = event.pos()
        items = self.items(event.pos())
        if len(items) < 2:
            self.setLink = 0
            return
        
        self.cur = items[1]
        self.rmView(self.cur)
        self.resort()

    @staticmethod
    def mouseMoveEvent(self, event):
        return

    @staticmethod
    def mouseReleaseEvent(self, event):
        return

    @staticmethod
    def listItemClicked(self, item):
        self.Scheme.delThesis(item)
        self.Scheme.resort()

    @staticmethod
    def keyReleaseEvent(self, event):
        pass

class createLink:
    cursor = QtCore.Qt.UpArrowCursor
    listCursor = QtCore.Qt.ArrowCursor

    @staticmethod
    def mousePressEvent(self, event):
        items = self.items(event.pos())
        if len(items) < 2:
            self.curItem = None
            return
        cur = items[1]
        if self.setLink == 0:
            self.setLink = 1
            self.curItem = self.searchByView(cur)
        cur.setZValue(10001)
        self.pen = QtGui.QPen(QtCore.Qt.gray, 2)
        self.sp = cur.pos()
        self.evPos = event.pos()
        self.curArrow = QtGui.QGraphicsLineItem(0, 0, 0, 0)
        self.curArrow.setPen(self.pen)
        self.curArrow.setZValue(10000)
        self.start = self.mapToScene(self.evPos)
        self.curArrow.moveBy(self.start.x(), self.start.y())
        self.scene.addItem(self.curArrow)

        self.lArr = QtGui.QGraphicsLineItem(0, 0, 0, 0)
        self.lArr.setPen(self.pen)
        self.rArr = QtGui.QGraphicsLineItem(0, 0, 0, 0)
        self.rArr.setPen(self.pen)
        self.scene.addItem(self.lArr)
        self.scene.addItem(self.rArr)

        self.setCursor(QtCore.Qt.BlankCursor)
        self.update()
        self.arrows.update()

    @staticmethod
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
            self.lArr.setPen(self.pen)
            self.scene.addItem(self.lArr)
            self.lArr.setZValue(10000)
            self.lArr.moveBy(end.x(), end.y())

            tmp = QtCore.QPointF(c*n.x() + s*n.y(), -s*n.x() + c*n.y())
            self.rArr = QtGui.QGraphicsLineItem(0, 0, -tmp.x(), -tmp.y())
            self.rArr.setPen(self.pen)
            self.scene.addItem(self.rArr)
            self.rArr.setZValue(10000)
            self.rArr.moveBy(end.x(), end.y())

    @staticmethod
    def mouseReleaseEvent(self, event):
        if (event.button() != QtCore.Qt.LeftButton):
            event.ignore()
            return

        if self.curItem == None:
            return

        self.setCursor(QtCore.Qt.UpArrowCursor)
        self.resort()
        if self.setLink == 1:
            self.scene.removeItem(self.curArrow)
            self.scene.removeItem(self.rArr)
            self.scene.removeItem(self.lArr)

        self.sp = event.pos()
        items = self.items(event.pos())
        if len(items) < 2:
            self.setLink = 0
            self.emit(QtCore.SIGNAL(
                    'createNewThesis(Thesis *, QPointF *)'),
                                    self.curItem, self.mapToScene(self.sp))
            self.updateSelection()
            self.update()
            self.arrows.update()
            return

        self.cur = items[1]

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
#                if not self.searchCircle(self.curItem, link.text()):
                    if (link != self.curItem) & (len(self.curItem.links) < 3):
                        self.curItem.links.append(link.text())
        self.update()
        self.arrows.update()

    @staticmethod
    def listItemClicked(self, item):
        return

    @staticmethod
    def keyReleaseEvent(self, event):
        pass

class rmLink:
    cursor = QtCore.Qt.UpArrowCursor
    listCursor = QtCore.Qt.ArrowCursor

    @staticmethod
    def mousePressEvent(self, event):
        linkToDel = self.arrows.linkToDel
        if len(linkToDel) > 1:
            for lam in self.lams:
                if linkToDel[1].text() in [i.text() for i in lam.labels]:
                    for i in xrange(lam.lvThesis.count()):
                        if (lam.lvThesis.item(i).text() == linkToDel[0].text()):
                            lam.lvThesis.takeItem(i)
                            break
            linkToDel[0].links.pop(linkToDel[0].links.index(linkToDel[1].text()))
            self.arrows.update()
            self.update()

    @staticmethod
    def mouseMoveEvent(self, event):
        self.arrows.rmOn = 1
        self.arrows.pos = self.mapToScene(event.pos())
        self.arrows.update()
        self.update()

    @staticmethod
    def mouseReleaseEvent(self, event):
        pass

    @staticmethod
    def listItemClicked(self, item):
        return

    @staticmethod
    def keyReleaseEvent(self, event):
        pass

class addToScheme:
    cursor = QtCore.Qt.CrossCursor
    listCursor = QtCore.Qt.CrossCursor

    @staticmethod
    def mousePressEvent(self, event):
        self.sp = event.pos()
        items = self.items(event.pos())
        if len(items) < 2:
            self.setLink = 0
            self.emit(QtCore.SIGNAL(
                    'createNewThesis(Thesis *, QPointF *)'),
                                    None, self.mapToScene(self.sp))
            self.updateSelection()
            self.update()
            self.arrows.update()
            return

        cur = items[1]
        curItem = self.searchByView(cur)
        color = cur.color
        self.addThesis(curItem, color)
        self.update()
        self.arrows.update()

    @staticmethod
    def mouseMoveEvent(self, event):
        pass

    @staticmethod
    def mouseReleaseEvent(self, event):
        pass

    @staticmethod
    def listItemClicked(self, item):
        self.Scheme.addThesis(item, QtCore.Qt.green)

    @staticmethod
    def keyReleaseEvent(self, event):
        pass

class addAntider:
    cursor = QtCore.Qt.ArrowCursor
    listCursor = QtCore.Qt.ArrowCursor

    @staticmethod
    def mousePressEvent(self, event):
        if (event.button() != QtCore.Qt.LeftButton):
            event.ignore()
            return

        cand = ''
        self.sp = event.pos()
        items = self.items(event.pos())
        if len(items) < 2:
            self.setLink = 0
            return

        self.cur = items[1]
        self.cur.setZValue(10000)
        self.resort()
        item = self.searchByView(self.cur)
        for link in item.links:
            for key in self.itemsOnScheme.keys():
                if key.text() == link:
                    cand = key
                    break
            for key in self.itemsOnScheme.keys():
                if (key == cand) and (len(self.itemsOnScheme[key]) == 0):
                    self.addThesis(key)
        self.updateSelection()

    @staticmethod
    def mouseMoveEvent(self, event):
        pass

    @staticmethod
    def mouseReleaseEvent(self, event):
        pass

    @staticmethod
    def listItemClicked(self, item):
        for key in self.Scheme.itemsOnScheme.keys():
            if key == item:
                if len(self.Scheme.itemsOnScheme[key]) == 0:
                    self.Scheme.addThesis(item, QtCore.Qt.green)
                    break
        for link in item.links:
            cand = self.Scheme.searchThesis(link)
            if len(self.Scheme.itemsOnScheme[cand]) == 0:
                self.Scheme.addThesis(cand)

    @staticmethod
    def keyReleaseEvent(self, event):
        pass

class addDer:
    cursor = QtCore.Qt.ArrowCursor
    listCursor = QtCore.Qt.ArrowCursor

    @staticmethod
    def mousePressEvent(self, event):
        if (event.button() != QtCore.Qt.LeftButton):
            event.ignore()
            return

        self.sp = event.pos()
        items = self.items(event.pos())
        if len(items) < 2:
            self.setLink = 0
            return

        self.cur = items[1]
        self.cur.setZValue(10000)
        self.resort()
        item = self.searchByView(self.cur)
        text = item.text()

        antiders = []
        for key in self.itemsOnScheme.keys():
            for link in key.links:
                if link == text:
                    antiders.append(key.text())
                    break

        for ader in antiders:
            for key in self.itemsOnScheme.keys():
                if key.text() == ader:
                    cand = key
                    break
            for key in self.itemsOnScheme.keys():
                if key == cand and len(self.itemsOnScheme[key]) == 0:
                    self.addThesis(key)
        self.updateSelection()

    @staticmethod
    def mouseMoveEvent(self, event):
        pass

    @staticmethod
    def mouseReleaseEvent(self, event):
        pass

    @staticmethod
    def listItemClicked(self, item):
        for key in self.Scheme.itemsOnScheme.keys():
            if key == item:
                if len(self.Scheme.itemsOnScheme[key]) == 0:
                    self.Scheme.addThesis(item, QtCore.Qt.green)
                    break

        antiders = []
        text = item.text()
        for key in self.Scheme.itemsOnScheme.keys():
            for link in key.links:
                if link == text:
                    antiders.append(key.text())
                    break

        for ader in antiders:
            cand = self.Scheme.searchThesis(ader)
            if len(self.Scheme.itemsOnScheme[cand]) == 0:
                self.Scheme.addThesis(cand)

    @staticmethod
    def keyReleaseEvent(self, event):
        pass

class convolution:
    cursor = QtCore.Qt.ArrowCursor
    listCursor = QtCore.Qt.ArrowCursor

    @staticmethod
    def mousePressEvent(self, event):
        if (event.button() != QtCore.Qt.LeftButton):
            event.ignore()
            return


        self.sp = event.pos()
        items = self.items(event.pos())
        if len(items) < 2:
            self.setLink = 0
            return

        self.cur = items[1]
        self.cur.setZValue(10000)
        self.resort()
        item = self.searchByView(self.cur)
        if item in self.selItems:
            self.selItems.pop(self.selItems.index(item))
            if item.isSelected():
                self.setColorOfThesis(item, QtCore.Qt.green)
            else:
                self.setColorOfThesis(item)
        else:
            self.setColorOfThesis(item, QtCore.Qt.yellow)
            self.selItems.append(item)

        if len(self.selItems) == 3:
            self.convolution() 
            self.selItems = []
            self.updateSelection()

    @staticmethod
    def mouseMoveEvent(self, event):
        pass

    @staticmethod
    def mouseReleaseEvent(self, event):
        pass

    @staticmethod
    def listItemClicked(self, item):
        self.Scheme.addThesis(item, QtCore.Qt.green)
        if item in self.Scheme.selItems:
            self.Scheme.selItems.pop(self.Scheme.selItems.index(item))
            if item.isSelected():
                self.Scheme.setColorOfThesis(item, QtCore.Qt.green)
            else:
                self.Scheme.setColorOfThesis(item)
        else:
            self.Scheme.setColorOfThesis(item, QtCore.Qt.yellow)
            self.Scheme.selItems.append(item)
        for i in self.Scheme.selItems:
            self.Scheme.setColorOfThesis(i, QtCore.Qt.yellow)

        if len(self.Scheme.selItems) == 3:
            self.Scheme.convolution()
            self.Scheme.selItems = []
            self.Scheme.updateSelection()

    @staticmethod
    def keyReleaseEvent(self, event):
        pass


class delThesis:
    cursor = QtCore.Qt.CrossCursor
    listCursor = QtCore.Qt.CrossCursor

    @staticmethod
    def mousePressEvent(self, event):
        if (event.button() != QtCore.Qt.LeftButton):
            event.ignore()
            return


        self.sp = event.pos()
        items = self.items(event.pos())
        if len(items) < 2:
            self.setLink = 0
            return

        self.cur = items[1]
        self.cur.setZValue(10000)
        self.resort()
        item = self.searchByView(self.cur)
        self.emit(QtCore.SIGNAL('delThesis(Thesis *)'), item)

    @staticmethod
    def mouseMoveEvent(self, event):
        pass

    @staticmethod
    def mouseReleaseEvent(self, event):
        pass

    @staticmethod
    def listItemClicked(self, item):
        self.Scheme.delThesis(item)
        for thesis in self.lvThesis.findItems('', QtCore.Qt.MatchContains):
            for link in thesis.links:
                if link == item.text():
                    thesis.links.pop(thesis.links.index(link))
        self.lvThesis.takeItem(self.lvThesis.row(item))
        for lam in self.Scheme.lams:
            if item.text() in [i.text() for i in lam.labels]:
                lam.close()
            for i in xrange(lam.lvThesis.count()):
                if (lam.lvThesis.item(i).text() == item.text()):
                    lam.lvThesis.takeItem(i)
            

    @staticmethod
    def keyReleaseEvent(self, event):
        pass


class Glue:
    cursor = QtCore.Qt.CrossCursor
    listCursor = QtCore.Qt.CrossCursor

    @staticmethod
    def mousePressEvent(self, event):
        if (event.button() != QtCore.Qt.LeftButton):
            event.ignore()
            return


        self.sp = event.pos()
        items = self.items(event.pos())
        if len(items) < 2:
            self.setLink = 0
            return

        self.cur = items[1]
        self.cur.setZValue(10000)
        self.resort()
        item = self.searchByView(self.cur)
        if item in self.selItems:
            self.selItems.pop(self.selItems.index(item))
            if item.isSelected():
                self.setColorOfThesis(item, QtCore.Qt.green)
            else:
                self.setColorOfThesis(item)
            return
        self.selItems.append(item)
        if QtCore.Qt.ControlModifier != event.modifiers():
            self.glue()
            self.updateSelection()
            self.selItems = []
        else:
            self.setColorOfThesis(item, QtCore.Qt.yellow)
            if len(self.selItems) >= 3:
                self.glue()
                self.selItems = []
                self.updateSelection()


    @staticmethod
    def mouseMoveEvent(self, event):
        pass

    @staticmethod
    def mouseReleaseEvent(self, event):
        pass

    @staticmethod
    def listItemClicked(self, item):
        self.Scheme.addThesis(item, QtCore.Qt.green)
        if item in self.Scheme.selItems:
            self.Scheme.selItems.pop(self.Scheme.selItems.index(item))
            if item.isSelected():
                self.Scheme.setColorOfThesis(item, QtCore.Qt.green)
            else:
                self.Scheme.setColorOfThesis(item)
        else:
            self.Scheme.setColorOfThesis(item, QtCore.Qt.yellow)
            self.Scheme.selItems.append(item)
        for i in self.Scheme.selItems:
            self.Scheme.setColorOfThesis(i, QtCore.Qt.yellow)
#
        if (len(self.Scheme.selItems) >= 3) or (QtCore.Qt.ControlModifier != QtGui.QApplication.keyboardModifiers()):
            self.Scheme.glue()
            self.Scheme.selItems = []
            self.Scheme.updateSelection()

    @staticmethod
    def keyReleaseEvent(self, event):
        self.Scheme.glue()
        self.Scheme.selItems = []
        self.Scheme.resort()
        self.Scheme.updateSelection()

class Lamination:
    cursor = QtCore.Qt.CrossCursor
    listCursor = QtCore.Qt.CrossCursor

    @staticmethod
    def mousePressEvent(self, event):
        if (event.button() != QtCore.Qt.LeftButton):
            event.ignore()
            return


        self.sp = event.pos()
        items = self.items(event.pos())
        if len(items) < 2:
            self.setLink = 0
            return

        self.cur = items[1]
        self.cur.setZValue(10000)
        self.resort()
        item = self.searchByView(self.cur)
        if item in self.selItems:
            self.selItems.pop(self.selItems.index(item))
            if item.isSelected():
                self.setColorOfThesis(item, QtCore.Qt.green)
            else:
                self.setColorOfThesis(item)
            return
        self.selItems.append(item)
        if QtCore.Qt.ControlModifier != event.modifiers():
            self.lamination()
            self.updateSelection()
            self.selItems = []
        else:
            self.setColorOfThesis(item, QtCore.Qt.yellow)
            if len(self.selItems) >= 3:
                self.lamination()
                self.selItems = []
                self.updateSelection()


    @staticmethod
    def mouseMoveEvent(self, event):
        pass

    @staticmethod
    def mouseReleaseEvent(self, event):
        pass

    @staticmethod
    def listItemClicked(self, item):
        self.Scheme.addThesis(item, QtCore.Qt.green)
        if item in self.Scheme.selItems:
            self.Scheme.selItems.pop(self.Scheme.selItems.index(item))
            if item.isSelected():
                self.Scheme.setColorOfThesis(item, QtCore.Qt.green)
            else:
                self.Scheme.setColorOfThesis(item)
        else:
            self.Scheme.setColorOfThesis(item, QtCore.Qt.yellow)
            self.Scheme.selItems.append(item)
        for i in self.Scheme.selItems:
            self.Scheme.setColorOfThesis(i, QtCore.Qt.yellow)

        if len(self.Scheme.selItems) >= 3:
            self.Scheme.lamination()
            self.Scheme.selItems = []
            self.Scheme.updateSelection()

    @staticmethod
    def keyReleaseEvent(self, event):
        self.Scheme.lamination()
        self.Scheme.selItems = []
        self.Scheme.resort()
        self.Scheme.updateSelection()

class Mutation:
    cursor = QtCore.Qt.ArrowCursor
    listCursor = QtCore.Qt.ArrowCursor

    @staticmethod
    def mousePressEvent(self, event):
        if (event.button() != QtCore.Qt.LeftButton):
            event.ignore()
            return

        self.sp = event.pos()
        items = self.items(event.pos())
        if len(items) < 2:
            self.scroll = 1
            return
        self.scroll = 0
        self.cur = items[1]
        thesis = self.searchByView(self.cur)
        if (self.setLink == 0):
            if not self.isFull(thesis):
                return
            self.setLink = 1
            self.mutRoot = thesis
            for key in self.itemsOnScheme.keys():
                self.delThesis(key)
            self.emit(QtCore.SIGNAL('addColorsBar()'))
            self.setColor(QtCore.Qt.red)
            self.viewNine(thesis)
            return
        self.setColorToMutation(thesis)
        if len(self.greenItems + self.redItems + self.yellowItems) == 9:
            self.emit(QtCore.SIGNAL('activateMutation()'))
        else:
            self.emit(QtCore.SIGNAL('disactivateMutation()'))

    @staticmethod
    def mouseMoveEvent(self, event):
        pass

    @staticmethod
    def mouseReleaseEvent(self, event):
        pass

    @staticmethod
    def listItemClicked(self, item):
        if (self.Scheme.setLink == 0):
            if not self.Scheme.isFull(item):
                return
            self.Scheme.setLink = 1
            self.mutRoot = item
            for key in self.Scheme.itemsOnScheme.keys():
                self.Scheme.delThesis(key)
            self.emit(QtCore.SIGNAL('addColorsBar()'))
            self.setColor(QtCore.Qt.red)
            self.viewNine(item)
            return

    @staticmethod
    def keyReleaseEvent(self, event):
        pass


