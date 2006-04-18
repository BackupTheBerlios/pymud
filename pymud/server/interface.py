#!/usr/bin/env python
"""
$Id: interface.py,v 1.6 2006/04/18 13:51:11 stips Exp $

Data handlers and objects - IE, all hard-coded data and database access
utility functions.

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
import sha
from types import ListType, TupleType
from string import lower, strip
from utils import pgDB, misc
import server.Queries as Q
import server.DBConstants as DC

# Different userlevels

Admin = 5
Player = 0

def getUsersInRoom(cursor, roomid):
	query = Q.GetUsersInRoom % {DC.Location: roomid}
	return pgDB.fetch(cursor, query)

def getThreadsInRoom(cursor, roomid):
	query = Q.GetThreadsInRoom % {DC.RoomID: roomid}
	return pgDB.fetchList(cursor, query)

def updateLocation(cursor, userid, location):
	queryDict = {
		DC.UserID: userid,
		DC.Location: location,
	}
	query = Q.UpdateLocation % queryDict
	pgDB.execute(cursor, query)

def getUserLocation(cursor, userid):
	queryDict = {
		DC.UserID: userid,
	}
	query = Q.GetUserRoomID % queryDict
	return pgDB.fetchOneValue(cursor, query)

def clearLoggedInUsers(cursor):
	query = Q.ClearLoggedInUsers
	pgDB.execute(cursor, query)

def getThreadID(cursor, userid):
	query = Q.GetThreadID % {DC.UserID: userid}
	return pgDB.fetchOneValue(cursor, query)

def setThreadID(cursor, userid, threadid):
	query = Q.SetThreadID % {DC.UserID: userid, DC.CurrentThreadID: threadid}
	pgDB.execute(cursor, query)

def getThreads(cursor, useridList):
	print useridList
	users = "('" + "','".join(useridList) + "')"
	query = Q.GetThreads % users
	return pgDB.fetch(cursor, query)

def createUser(cursor, nickname, charname, password, userlevel = Player):
	password = sha.new(password).hexdigest()
	queryDict = {
		DC.UserID: userid,
		DC.UserLevel: userlevel,
		DC.NickName: nickname,
		DC.FullName: charname,
		DC.Password: password,
	}
	query = Q.CreateUser % queryDict
	pgDB.execute(query)

def getArea(cursor, roomid):
	query = Q.GetAreaID % {DC.RoomID: roomid}
	return pgDB.fetchOneValue(cursor, query)

def getPasswordHash(cursor, userid):
	query = Q.GetPassword % {DC.UserID: userid}
	return pgDB.fetchOneValue(cursor, query)

def getUserData(cursor, userid, field = None):
	"""
	Return either one, some, or all of the fields in the UserData
	table for the given userid.
	"""
	if not field:
		query = Q.GetAllUserData % {DC.UserID: userid}
		res = pgDB.fetchDict(cursor, query)
		return res[0]
	else:
		if type(field) in (ListType, TupleType):
			field = ','.join(field)
			query = Q.GetUserData % (field, userid)
			return pgDB.fetchOne(cursor, query)
		else:
			query = Q.GetUserData % (field, userid)
			return pgDB.fetchOneValue(cursor, query)

def getExits(cursor, roomid):
	query = Q.GetExits % {DC.RoomID: roomid}
	res = pgDB.fetchOneValue(cursor, query)
	try:
		 exitDict = misc.getDict(res)
	except TypeError:
		# Area does not exist.
		print "ERROR! User attempted to go to room %s, which, "\
		"seemingly, does not exist." % roomid
	exits = {}
	for exit, data in exitDict.items():
		exits[lower(exit)] = data.split('|')
	return exits

# Area/Room information
def getRoomDescription(cursor, roomid):
	"""
	Gets the room decription from the database.
	"""
	query = Q.GetRoomDescription % {DC.RoomID: roomid}
	res = pgDB.fetchOneValue(cursor, query)
	if not res:
		#FIXME We need an /unstick command that resets peoples location.
		res = "You seem to be stuck. Please contact an"\
		" administrator and tell them that you've gotten somewhere"\
		" you shouldn't be able to get to."
	return res

def getRoomItems(cursor, roomID):
	"""
	Gets items in the room from the database.
	"""
	query = Q.GetItemsInRoom % {DC.RoomID: roomID}
	res = pgDB.fetchList(cursor, query)
	return res
			
def getItemDescription(cursor, roomid, cmd):
	query = Q.GetItemDescription % {DC.RoomID: roomid}
	res = pgDB.fetch(cursor, query)
	cmd = cmd[1]
	desc = "You look around but you can't see a %s.\r\n" %cmd
	for description, keywords in res:
		keywords = keywords.split(",")
		if cmd in keywords:
			desc = description + "\r\n"
	return desc

def getItemForUser(cursor, cmdList, roomID, userID):
	"""
	Takes an item from a room and places it in the users inventory.
	"""
	query = Q.GetItemsForUser % {DC.RoomID: roomID}
	res = pgDB.fetch(cursor, query)
	cmd = cmdList[1]
	desc = "You screw your eyes shut and wish really hard for a %s.\r\n" %cmd
	for itemID, keywords, roomItemCount in res:
		keywords = keywords.split(",")
		if cmd in keywords:
			if int(roomItemCount) > 0:
				# Remove one of the item(s) from the room it was in.
				itemCount = int(roomItemCount) - 1
				updateCount = Q.UpdateRoomItemCount % {"ItemID":itemID,
												"ItemCount":roomItemCount,
												"RoomID":roomID}
				pgDB.executeOne(cursor, updateCount)

				#Create/update a stack of items if the user already has one.
				userItemCountQ = Q.GetUserItemCount % { "ItemID" : itemID,
														"UserID" : userID}
				userItemCount = pgDB.fetchOne(cursor, userItemCountQ)

				#increment the item count and update the database
				if not userItemCount:
					userItemCount = 1

					updateInvQ = Q.CreateUserItem % {"UserID":userID,
													"ItemID": itemID,
													"ItemCount": userItemCount}
				else:
					userItemCount = int(userItemCount[0]) + 1

					updateInvQ = Q.UpdateUserItem % {"UserID":userID,
													"ItemID": itemID,
													"ItemCount": userItemCount}

				res	= pgDB.executeOne(cursor, updateInvQ)
				desc = "You pickup the %s.\r\n" %cmd
	return desc
