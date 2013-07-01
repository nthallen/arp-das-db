#!/usr/bin/env python
# /usr/pkg/bin/python2.7
# use first on normal python installed system second on QNX
'''
Created on May 2, 2013

@author: ndemusz
'''
import argparse
import sqlite3 as lite
import processPath
import os.path
def main( path ):
    data = processPath(path)
    chksumExists = 0
    con = None
    
    if os.path.exists(path + '/.MD5SUM') :
        chksumExists = 1
    if not os.path.exists(data.pathToDatabase) :
        print "Database file not found"
    else :
        try :
            con = lite.connect(data.pathToDatabase)
        except :
            print "unable to connect to database, check file permissions"
        #insert into Runs table
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Run SET chksum_exists=%d WHERE %s",chksumExists, data.runName)

if __name__ == '__main__':
    par = argparse.ArgumentParser()
    par.add_argument("pathToRun", help="file path to run")
    main(par.pathToRun)