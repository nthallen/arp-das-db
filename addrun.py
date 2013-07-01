#!/usr/bin/env python
# /usr/pkg/bin/python2.7
# use first on normal python installed system second on QNX
import sqlite3 as lite
import os.path.exists
import argparse
import updatechecksum
import processPath
import updateArchive
#expected input is machine/home/instrument/datatype/(runtype)/yymmdd.#
# datatype is raw || anal || dump
# () means may or may not be included.
def main( path, archive, location ):
	# Processing the split  file path
	data = processPath(path)
	chksumExists = 0
	# Read line from Saverun.log
	saverun = ""
	try:
		f = open(path + '/Saverun.log')
		saverun = f.readline()
		f.close()
	except IOError:
		print 'cannot open Saverun.log', arg

	#open database file
	con = None
	if not os.path.exists(data.pathToDatabase) :
		print "Database file not found, please run setup"
	else :
		try :
			con = lite.connect(data.pathToDatabase)
		except :
			print "unable to connect to database"
		#insert into Runs table
	with con:
		cur = con.cursor()
		instid = cur.execute("SELECT id FROM Instrument WHERE name = %s", data.instrument)
		cur.execute("INSERT INTO Runs VALUES(?,?,?,?,?,?)", 'NULL', instid, data.runname, data.datatype, saverun, data.rundatestamp, chksumExists)
		#need to add update to archive
	
	updateArchive(path, archive, location)
	#check and update md5sum
	updatechecksum( path )
if __name__ == "__main__":
	par = argparse.ArgumentParser()
	par.add_argument("path", help="expected input is machine/home/instruement/datatype/(runtype)/yymmdd.#")
	par.add_argument("archive", help="name of archive")
	par.add_argument("location", help="description of location")
	arg = par.parse_args()
	main(arg.path, arg.archive, arg.location)
