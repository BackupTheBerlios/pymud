#!/usr/bin/env python
"""
$Id: pgDB.py,v 1.2 2005/10/26 06:13:22 rwh Exp $
Postgres access utilities.

The Pythonic Mud
Copyright (C) 2005 by Rohan Harris

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
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
