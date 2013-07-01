#!/usr/bin/env python
# /usr/pkg/bin/python2.7
# use first on normal python installed system second on QNX
'''
Created on May 16, 2013

@author: ndemusz
'''
'''
    runName
    datatype
    instrument
    pathToDatabase
    runDateStamp
    pathToRun
    
'''
class processPath:
    def __init__(self, path):
        dirPathSplit = path.split('/')
        self.runName
        self.datatype
        self.instrument
        self.pathToDatabase
        self.runDateStamp
        self.pathToRun
        # Processing the split  file path
        for i, item in dirPathSplit :
            if item == "anal" or item == "dump" :
                self.datatype = item
                self.instrument = dirPathSplit[i - 1]
                self.runName = dirPathSplit[i + 1]
                #finding database file
                for x in (i - 1) :
                    self.pathToDatabase = self.pathToDatabase + '/' + dirPathSplit[x]
                self.pathToRun = self.pathToDatabase + '/' + dirPathSplit[i]
            if item == "raw" :
                self.datatype = item
                self.instrument = dirPathSplit[i - 1]
                self.runName = dirPathSplit[i + 2]
                #finding database file
                for x in (i - 1) :
                    self.pathToDatabase = self.pathToDatabase + '/' + dirPathSplit[x]
                self.pathToRun = self.pathToDatabase + '/' + dirPathSplit[i]
        self.pathToRun = self.pathToRun + '/' + self.runName
        self.pathToDatabase = self.pathToDatabase + '/.database/database.sql'
        self.runDateStamp = int(self.runName)
