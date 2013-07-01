'''
Created on May 31, 2013

@author: ndemusz

This will show you all runs with 3 or more copies in a particular DB
'''
import argparse
import os.path
import sqlite3 as lite
def main(path):
    con = None
    if not os.path.exists(path) :
        print "Database file not found, please check supplied path"
    else :
        try :
            con = lite.connect(path)
        except :
            print "unable to connect to database"
    with con:
        cur = con.cursor()
        #need sql statements to search database for appropriate
        #files to delete
        cur.execute("")
        for row in cur.execute("SELECT RunID, Count(*) FROM Archive GROUP RunID HAVING Count(*) > 2"):
            print row

if __name__ == '__main__':
    par = argparse.ArgumentParser()
    par.add_argument("path", help="path to database")
    arg = par.parse_args()
    main(arg.path)