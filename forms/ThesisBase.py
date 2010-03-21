#-*- coding: utf-8 -*-

import os, sys, string

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

def saveThesis(path, name, desc):
    if not os.path.exists(path + '/' + name):
        os.makedirs(path + '/' + name)
    f = open(path + '/' + name + '/' + 'desc.txt', 'w')
    f.write(desc)
    f.close()

def getThesisList(path):
    ListDir = []
    for Bill, ListDir, Bob in os.walk(path):
        break
    return [unicode(thesis, 'UTF8') for thesis in ListDir]

def getDesc(path, name):
    file = open(path + '/' + name + '/desc.txt', 'r')
    desc = ''
    for line in file.readlines():
        desc += unicode(line, 'UTF8')
    file.close()
    return desc

def setDesc(path, name, newdesc):
    file = open(path + '/' + name + '/desc.txt', 'w')
    file.write(newdesc)
    file.close()

def setName(oldname, newname):
    os.rename(path + '/' + oldname, path + '/' + newname)
    
