#-*- coding: utf-8 -*-

import os, sys, string, hashlib
from PyQt4.QtGui import QListWidgetItem

def rmgeneric(path, __func__):
    try:
        __func__(path)
    except OSError, (errno, strerror):
    	return {'path': path, 'error': strerror}
    return 0
	

def removeall(path):
    if not os.path.isdir(path):
        return

    files=os.listdir(path)

    for x in files:
        fullpath=os.path.join(path, x)
        if os.path.isfile(fullpath):
            f=os.remove
            rmgeneric(fullpath, f)
        elif os.path.isdir(fullpath):
            removeall(fullpath, widget)
            f=os.rmdir
            rmgeneric(fullpath, f)

class Thesis(QListWidgetItem):
    def __init__(self, name='', desc='', links=[], path=''):
        if path == '':
            QListWidgetItem.__init__(self, name)
            self.desc = desc
            self.links = links
            self.hash = hashlib.sha1(str(self.text().toUtf8())).hexdigest()
        if path != '':
            f = open(path + '//name.txt', 'r')
            QListWidgetItem.__init__(unicode(f.readline(), 'UTF8'))
            f.close()
            self.hash = hashlib.sha1(str(self.text().toUtf8())).hexdigest()
            tmp = path.split('/')
            tmp.pop()
            tmp.pop()
            npath = ''
            for i in tmp:
                npath += '/' + i
            self.loadDesc(self, npath)
            self.loadLinks(self, npath)

    def loadDesc(self, path):
        file = open(path + '/' + self.hash[:2] + '/' + self.hash[2:] +
                                                        '/desc.txt', 'r')
        self.desc = ''
        for line in file.readlines():               
            self.desc += unicode(line, 'UTF8')
        file.close()

    def loadLinks(self, path):
        return

    def saveDesc(self, path):
        file = open(path + '/' + self.hash[:2] + '/' + self.hash[2:] +
                                                            '/desc.txt', 'w')
        file.write(self.desc)
        file.close()

    def saveLinks():
        return

    def saveThesis(self, path):
        if not os.path.exists(path + '/' + str(self.text().toUtf8())):
            os.makedirs(path + '/' + str(self.text().toUtf8()))
        self.saveDesc(path)
        f = open(path + '/' + self.hash[:2] + '/' + self.hash[2:] + '/' +
                                                            'name.txt', 'w')
        f.write(str(self.text().toUft8()))      
        f.close()
