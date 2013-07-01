#!/usr/bin/env python
# /usr/pkg/bin/python2.7
# use first on normal python installed system second on QNX

#run this in instrument dir
import os.walk
import os.path
import sqlite3 as lite
import sys
import re
import addrun
import argparse

parser = argparse.ArgumentParser(description="Run this in instruments home dir: name \"description\" archive")
parser.add_argument("instName", help="Instrument name, should match name of instrument home")
parser.add_argument("instDesc", help="\"Instrument Description\"")
parser.add_argument("archiveName", help="Name of Archive")
parser.add_argument("location", help="location description")
args = parser.parse_args()

# create dot named directory under instrument folder
if not os.path.exists(".database"):
	try: 
		os.makedirs(".database")
	except OSError:
		print "unable to create database directory, check write permission"
else:
	print "database already exists"
	sys.exit()

#initialize the database file and generate tables
con = None
qry = ""

#regex object to match "6 digits" + "." + "one or more [0-9]"
prog = re.compile(r'\d{6}\.\d{1+}')

archivePath = os.path.dirname(os.path.abspath('.database'))

'''
The following builds a list of runs and puts them into reverse order that it finds them.
This is so that the oldest will be first, if this is wrong then change insert to:
append(os.path.join(dirname, rundir)) to add at tail of list
'''
pathsToRuns = []
for dirname, dirnames, rundir in os.walk('.'):
	for run in rundir:
		if prog.match(run):
			pathsToRuns.insert(0, os.path.join(dirname, rundir)) #inserts at front of list
			
			
		
try:		
	#qry = open( 'initdatabase.sql', 'r').read()
	con = lite.connect('.database/database.db')
except:
	print "unable to open database file"
	
with con:
	''' #Old Schema pretty sure is wrong
	cur = con.cursor()
	cur.execute( "PRAGMA foreign_keys = ON;")
	cur.execute("CREATE TABLE IF NOT EXISTS Archive(\
		ArchID INT PRIMARY KEY,\
		ArchName TEXT UNIQUE,\
		ArchPath TEXT,\
		RunID TEXT REFERENCES Run(RunID) );")
	cur.execute( "CREATE TABLE IF NOT EXISTS Instrument(\
		InstID INT PRIMARY KEY,\
		InstName TEXT UNIQUE,\
	 	InstDesc TEXT,\
	 	ArchiveID INT REFERENCES Archive(ArchID) );")
	cur.execute("CREATE TABLE IF NOT EXISTS Run(\
		RunID INT PRIMARY KEY,\
		RunExpID TEXT,\
		RunName TEXT UNIQUE,\
		RunType TEXT,\
		RunDesc TEXT,\
		RunDateStamp INT, \
		RunSize INT, \
		chksumExists INT );")
	cur.execute("CREATE TABLE IF NOT EXISTS Dataset(\
		DatasetID INT PRIMARY KEY,\
		RunName TEXT REFERENCES Run(RunName),\
		DsVerifyTS TEXT,\
		DsDeletedTS TEXT,\
		DsCreatedTS TEXT,\
		DsDeleted INT,\
		DsVerified INT );")
	'''
	cur = con.cursor()
	cur.execute( "PRAGMA foreign_keys = ON;")
	#Archive is many to 1 Run
	#Each run should only exist in a particular archive once
	cur.execute("CREATE TABLE IF NOT EXISTS Archive(\
		id INT PRIMARY KEY,\
		name TEXT UNIQUE,\
		path TEXT,\
		run_id INT REFERENCES Run(id)\
		location TEXT );")
	#Instrument is 1 to many Runs.
	cur.execute( "CREATE TABLE IF NOT EXISTS Instrument(\
		id INT PRIMARY KEY,\
		name TEXT UNIQUE,\
	 	desc TEXT);")
	#Runs is 1 to many Archives.
	cur.execute("CREATE TABLE IF NOT EXISTS Run(\
		id INT PRIMARY KEY,\
		instrument_id INT REFERENCES Instrument(id), \
		expID TEXT,\
		name TEXT UNIQUE,\
		type TEXT,\
		desc TEXT,\
		date_stamp INT, \
		size INT, \
		chksum_exists INT );")
	#Dataset is 1 to 1 with Run
	#Deleted and verified are just intended to be boolean
	cur.execute("CREATE TABLE IF NOT EXISTS Dataset(\
		id INT PRIMARY KEY,\
		run_name TEXT REFERENCES Run(name),\
		verifyTS TEXT,\
		deletedTS TEXT,\
		createdTS TEXT,\
		deleted INT,\
		verified INT );")

try:		

	con = lite.connect('.database/database.db')
except:
	print "Created database file; unable to open it"
with con:
	cur = con.cursor()	
	# add instrument
	cur.execute("INSERT INTO Instrument VALUES(?,?,?)", ['NULL', args.instName, args.instDesc])

# insert all of the current runs
for run in pathsToRuns:
	addrun.main(run, args.archiveName, args.location)
