#!/usr/bin/env python
"""
$Id: pgDB.py,v 1.1 2005/05/30 02:00:36 rwh Exp $

Postgres access utilities.
"""

import pgdb
import config

USERNAME = config.get('dblogin')
DBNAME = config.get('dbname')
DBHOST = config.get('dbhost')

def connect(dbName = DBNAME):
	db = pgdb.connect(database = dbName, host = DBHOST,
			user = USERNAME)
	cursor = db.cursor()
	return (db, cursor)

def executeOne(cursor, query):
	return cursor._pgdbCursor__source.execute(query)

def fetch(cursor, query):
	cursor._pgdbCursor__source.execute(query)
	res = cursor._pgdbCursor__source.fetch(-1)
	return res

def fetchList(cursor, query):
	results = fetch(cursor, query)
	list = []
	for line in results:
		list.append(line[0])
	return list

def execute(cursor, query):
	cursor._pgdbCursor__source.execute(query)

def fetchOne(cursor, query):
	results = fetch(cursor, query)
	try:
		return results[0]
	except IndexError:
		return None

def fetchOneValue(cursor, query):
	resultLine = fetchOne(cursor, query)
	if resultLine:
		try:
			return resultLine[0]
		except IndexError, TypeError:
			return None
	return None

def fetchDict(cursor, query):
	rows = fetch(cursor, query)
	dictList = []
	if not rows:
		return dictList
	# build the list of data dictionaries
	colNames = map(lambda x:x[0], cursor.description)
	for row in rows:
		dict = {}
		for i in range(len(row)):
			dict[colNames[i]] = row[i]
			dictList.append(dict)
	return dictList

def fetchOneDict(cursor, query):
	#FIXME: Horribly inefficent.
	return fetchDict(cursor, query)[0]
