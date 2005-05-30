#!/usr/bin/env python
"""
$Id: GameServer.py,v 1.1 2005/05/30 02:00:34 rwh Exp $

The actual game server handler. This class is derived from the
ThreadedServer class in server.py, but contains game-specific functions,
such as monitoring of where each connected player is.
"""

import os, threading, signal
import server.DBConstants as DC
from utils import pgDB
from utils.ansi import colorise
from server.interface import updateLocation, clearLoggedInUsers, getThreadsInRoom, getThreads
from server.Server import ThreadedServer
from Actions import ActionHandler
from Combat import ACTION_MAP as combatActions, VERB_MAP as combatVerbs
from Skills import ACTION_MAP as skillActions, VERB_MAP as skillVerbs

VERBS = {}
VERBS.update(combatVerbs)
VERBS.update(skillVerbs)

class GameServer(ThreadedServer):
	def __init__(self, port, RequestHandlerClass):
		self.clients = {}
		self.db, self.cursor = pgDB.connect()
		self.combatHandler = ActionHandler("combat", self, combatActions)
		self.skillHandler = ActionHandler("skill", self, skillActions)
		clearLoggedInUsers(self.cursor)
		self.combatHandler.start()
		self.skillHandler.start()
		self.running = True
		ThreadedServer.__init__(self, port, RequestHandlerClass)
	
	def serve_forever(self):
		"""
		This one should be pretty obvious.
		"""
		while self.running:
			try:
				self.handle_request()
			except KeyboardInterrupt:
				print "Dying on request!"
				self.running = False
		self.combatHandler = None
		self.skillHandler = None
		self.killThreads()
	
	def performAction(self, userid, action, params):
		print "Got an action, %s, from %s." % (action, userid)
		if action in self.combatHandler.actions():
			self.combatHandler.addAction(userid, action, params)
		elif action in self.skillHandler.actions():
			self.skillHandler.addAction(userid, action, params)
	
	def stopAction(self, userid, action):
		if action in VERBS.keys():
			action = VERBS[action]
		if action in self.combatHandler.actions():
			return self.combatHandler.stopAction(userid)
		elif action in self.skillHandler.actions():
			return self.skillHandler.stopAction(userid)
		return False

	def stopAllActions(self, userid):
		self.skillHandler.stopAction(userid)
	
	def changeLocation(self, threadid, userid, area, room, DBUpdate = 1):
		if DBUpdate:
			updateLocation(self.cursor, userid, room)
		if not self.clients.has_key(userid):
			# Player has just entered the game.
			print "%s has entered the game world in room %s." % (userid, room)
			self.display(threadid, room, "`$%s appears in a puff of logic." % userid)
		else:
			# Player has entered from another place.
			self.display(threadid, self.clients[userid][DC.RoomID],\
					"`$%s has left the area." % userid)
			print "%s has moved to the room %s." % (userid, room)
			self.display(threadid, room, "`$%s has entered the area."\
					% userid)
			
		#FIXME: REDUNDANT! Getting from DB. May want to use
		# this later though, to push some load into memory and
		# CPU rather than postgres
		self.clients[userid] = {
			DC.UserID: userid,
			DC.AreaID: area,
			DC.RoomID: room,
		}
	
	def getCursor(self):
		return self.db.cursor()

	def sendMessage(self, threadid, text):
		text = colorise(text, firstLetterCap = 1)
		os.write(self.outbox[int(threadid)], text + "\r\n")

	def display(self, ownThreadid, roomid, text):
		text = colorise(text, firstLetterCap = 1)
		self.localPrint(ownThreadid, roomid, text + "\r\n")
	
	def localPrint(self, ownThreadid, roomid, text):
		threads = getThreadsInRoom(self.cursor, roomid)
		for thread in threads:
			print "%s, %s" % (type(thread), thread)
			if int(thread) != ownThreadid:
				os.write(self.outbox[int(thread)], text)
