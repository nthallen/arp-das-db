#!/usr/bin/env python
# /usr/pkg/bin/python2.7
# use first on normal python installed system second on QNX
'''
Created on Apr 17, 2013

@author: ndemusz
'''
import sqlite3 as lite
import os.getcwd
import os.path.exists
import argparse

par = argparse.ArgumentParser("Retrieves the last X run(s) entered into database")
par.add_argument("num", type=int, help="Number of rows to retrieve", default=1)
path = os.getcwd() + "/.database/database.db"
arg = par.parse_args()
#open database file
con = None
if not os.path.exists(path) :
    print "Database file not found"
else :
    try :
        con = lite.connect(path)
    except :
        print "unable to connect to database"

    #insert into Runs table
    with con:
        cur = con.cursor()
        lastrun = cur.execute("SELECT MAX(RunID) FROM Runs;")
        if(lastrun > arg.num) :
            lastrun -= arg.num
        for row in cur.execute("SELECT * FROM Runs WHERE RunID > %d;", lastrun):
            print row