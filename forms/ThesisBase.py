#-*- coding: utf-8 -*-

import os, sys, string, hashlib
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtGui import QListWidget
from PyQt4.QtCore import Qt, QString

def loadThesisesToList(QListWidget, path):
    ListDir = []
    for Bill, ListDir, Bob in os.walk(path):
        break
    for dir in ListDir:
        SubDirs = []
        for Bill, SubDirs, Bob in os.walk(path + '/' + dir):
            break
        for sdir in SubDirs:
            QListWidget.addItem(Thesis(path = path + '/' + dir + '/' + sdir))

class Thesis(QListWidgetItem):
    def __init__(self, name='', desc=QString(), links=[], path=''):
        if path == '':
            QListWidgetItem.__init__(self, name)
            self.desc = desc
            self.links = links
            self.hash = hashlib.sha1(str(self.text().toUtf8())).hexdigest()
            self.DescChanged = 1
        if path != '':
            f = open(path + '/name.txt', 'r')
            QListWidgetItem.__init__(self, unicode(f.readline(), 'UTF8'))
            f.close()
            self.hash = hashlib.sha1(str(self.text().toUtf8())).hexdigest()
            self.DescChanged = 0
            self.setFlags(Qt.ItemIsEditable | Qt.ItemIsSelectable
                                                | Qt.ItemIsEnabled)

    def setDesc(self, desc):
        self.desc = desc
        self.DescChanged = 1

    def getDesc(self, path):
        if self.DescChanged == 0:
            file = open(path + '/' + self.hash[:2] + '/' + self.hash[2:] +
                                                        '/desc.txt', 'r')
            desc = ''
            for line in file.readlines():
                desc += unicode(line, 'UTF8')
            file.close()
            return desc
        return self.desc
            
    def loadLinks(self, path):
        return

    def saveDesc(self, path, force=0):
        if (force == 1) | (self.DescChanged == 1):
            file = open(path + '/' + str(self.hash[:2]) + '/' +
                                str(self.hash[2:]) + '/desc.txt', 'w')
            file.write(str(self.desc.toUtf8()))
            file.close()

    def saveLinks():
        return

    def saveThesis(self, path, force=0):
        if (force == 0) & (self.DescChanged == 0):
            return
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
        self.DescChanged = 0
