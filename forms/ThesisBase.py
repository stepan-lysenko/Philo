#-*- coding: utf-8 -*-

import os, sys, string, hashlib
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtGui import QListWidget
from PyQt4.QtCore import Qt, QString
from SchemeView import SchemeView

def saveScheme(scheme, path):
    f = open(path, 'w')
    for key in scheme.itemsOnScheme.keys():
        for item in scheme.itemsOnScheme[key]:
            f.write(str(key.text().toUtf8()) + '  ' +
                str(item.x()) + ' ' + str(item.y()) + '\n')
    f.close()

def loadScheme(path, list, scheme):
    scheme.clear()
    if not os.path.exists(path):
        return
    f = open(path, 'r')
    for line in f.readlines():
        tmp = line.split()
        y = float(tmp.pop())
        x = float(tmp.pop())
        name = ''
        for s in tmp:
            name += ' ' + s
        name = name[1:]
        item = SearchInList(list, QString(unicode(name, 'UTF8')))
        if item != 0:
            scheme.addThesis(item, x = x, y = y)

    l = list.findItems('', Qt.MatchContains)
    for i in l:
        if not scheme.itemsOnScheme.has_key(i):
            scheme.itemsOnScheme[i] = []
            
    
   
def SearchInList(list, name):
    n = QString(name)
    for i in xrange(list.count()):
        if n == list.item(i).text():
            return list.item(i)
    return 0
 
    

def loadThesisesToList(QListWidget, path):
    ListDir = []
    for Bill, ListDir, Bob in os.walk(path):
        break
    for dir in ListDir:
        SubDirs = []
        for Bill, SubDirs, Bob in os.walk(path + '/' + dir):
            break
        for sdir in SubDirs:
            tmp = Thesis(path = path + '/' + dir + '/' + sdir)
            tmp.getDesc(path)
            QListWidget.addItem(tmp)

class Thesis(QListWidgetItem):
    def __init__(self, name='', desc=QString(), path=''):
        if path == '':
            QListWidgetItem.__init__(self, name)
            self.desc = desc
            self.links = []
            self.hash = hashlib.sha1(str(self.text().toUtf8())).hexdigest()
            self.DescChanged = 1
            self.LinksChanged = 1
        if path != '':
            self.desc = QString()
            f = open(path + '/name.txt', 'r')
            QListWidgetItem.__init__(self, unicode(f.readline(), 'UTF8'))
            f.close()
            self.hash = hashlib.sha1(str(self.text().toUtf8())).hexdigest()
            self.DescChanged = 0
            self.setFlags(Qt.ItemIsEditable | Qt.ItemIsSelectable
                                                | Qt.ItemIsEnabled)
            f = open(path + '/links.txt', 'r')
            self.links = [QString(unicode(l[:len(l) - 1], 'UTF8')) for l in f.readlines()]
            f.close()
            self.LinksChanged = 0

    def setDesc(self, desc):
        self.desc = desc
        self.DescChanged = 1

    def getDesc(self, path):
        if self.DescChanged == 0:
            self.hash = hashlib.sha1(str(self.text().toUtf8())).hexdigest()
            file = open(path + '/' + self.hash[:2] + '/' + self.hash[2:] +
                                                        '/desc.txt', 'r')
            desc = ''
            for line in file.readlines():
                desc += QString(unicode(line, 'UTF8'))
            file.close()
            self.desc = desc
            return desc
        return self.desc
            
    def loadLinks(self, path):
        return

    def saveDesc(self, path, force=1):
        if (force == 1) | (self.DescChanged == 1):
            self.hash = hashlib.sha1(str(self.text().toUtf8())).hexdigest()
            file = open(path + '/' + str(self.hash[:2]) + '/' +
                                str(self.hash[2:]) + '/desc.txt', 'w')
            file.write(str(self.desc.toUtf8()))
            file.close()
            self.DescChanged = 0

    def saveLinks(self, path, force=1):
        if (force == 1) | (self.LinksChanged == 1):
            self.hash = hashlib.sha1(str(self.text().toUtf8())).hexdigest()
            f = open(path + '/' + str(self.hash[:2]) + '/' +
                                str(self.hash[2:]) + '/links.txt', 'w')
            for l in self.links:
                f.write(str(l.toUtf8()) + '\n')
            f.close()
            self.ListChanged = 0

    def saveThesis(self, path, force=1):
        if (force == 0) & (self.DescChanged == 0):
            return
        self.hash = hashlib.sha1(str(self.text().toUtf8())).hexdigest()
        if not os.path.exists(path + '/' + str(self.hash[:2])):
            os.makedirs(path + '/' + str(self.hash[:2]))
        if not os.path.exists(path + '/' + str(self.hash[:2]) + '/' +
                                                    str(self.hash[2:])):
            os.makedirs(path + '/' + str(self.hash[:2]) + '/' +
                                                    str(self.hash[2:]))
        self.saveDesc(path, force)
        f = open(path + '/' + self.hash[:2] + '/' + self.hash[2:] + '/' +
                                                            'name.txt', 'w')
        f.write(str(self.text().toUtf8()))      
        f.close()
        self.saveLinks(path, force)
