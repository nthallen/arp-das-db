#!/usr/bin/env python
# /usr/pkg/bin/python2.7
# use first on normal python installed system second on QNX
'''
Created on Jun 14, 2013

@author: ndemusz
'''
import sqlite3 as lite
import os.path.exists
import processPath
import argparse
def main(path, archivename, location):
    data = processPath(path)
    con = None
    if not os.path.exists(data.pathToDatabase) :
        print "Database file not found"
    else :
        try :
            con = lite.connect(data.pathToDatabase)
        except :
            print "unable to connect to database"
    with con:
        cur = con.cursor()
        runid = cur.execute("SELECT id FROM Run WHERE name = %s", data.runname)
        cur.execute("INSERT INTO Archive VALUES(?,?,?,?)", 'NULL', archivename, path, runid, location)
    
if __name__ == '__main__':
    par = argparse.ArgumentParser()
    par.add_argument("path", help="path to run")
    par.add_argument("name", help="Name of Archive")
    par.add_argument("location", help="storage type/location/description")
    arg = par.parse_args()
    main(arg.path, arg.name, arg.location)