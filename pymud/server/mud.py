#!/usr/bin/env python
"""
$Id: mud.py,v 1.7 2006/04/18 14:14:45 stips Exp $
Game Client Handler code class and supporting functions

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
from random import randint
from string import lower

from server.Server import ClientHandler
from server.GameServer import GameServer
from server.Combat import ACTION_MAP as combatActions
from server.Skills import ACTION_MAP as skillActions
import server.DBConstants as DC
import server.interface as SI

from utils import pgDB
from utils import config
from utils.ansi import colorise

constants = """
emote
look
diction
quit
move
stop
examine
get

USERNAME
PASSWORD

INGAME
""".strip().split()

g = globals()
for item in constants:
	g[item] = item

valid_commands = {
	"emote"		: emote,
	"/me"		: emote,
	"say"		: diction,
	"ask"		: diction,
	"look"		: look,
	"quit"		: quit,
	"go"		: move,
	"stop"		: stop,
	"examine"	: examine,
	"get"		: get,
}

class GameClient(ClientHandler):
	"""
	Our actual game client. The generic client-handler code (not specific to
	this game) is in the ClientHandler clas, whcih we inherit from.

	Most of our grunt work is done through the overloaded realHandle method,
	with other methods being referenced from within that.
	"""
	def realHandle(self, command):
		"""
		Grunt work is done here. This is called every time a complete line
		(terminating in a \r\n) is received by the handler loop. 'command' is
		a full-line string, with no trailing newline characters.
		"""
		command = command.strip()
		cmdList = command.split(' ')
		if self.state == USERNAME:
			# No username as yet, let's get one.
			self.username = command
			self.state = PASSWORD
			self.look()
				
		elif self.state == PASSWORD:
			# No password, let's get one.
			password = SI.getPasswordHash(self.cursor, self.username)
			if password == sha.new(command).hexdigest():
				thread = SI.getThreadID(self.cursor, self.username)
				if thread:
					self.write("Sorry, You are already logged in.")
					print "User tried to log in who was already "\
							"connected on thread %s'" % repr(thread)
					self.finish()
					return
				self.fullname = \
					SI.getUserData(self.cursor, self.username, DC.FullName)
				self.nickname = \
					SI.getUserData(self.cursor, self.username, DC.NickName)
				self.userlevel = \
					SI.getUserData(self.cursor, self.username, DC.UserLevel)
				self.state = INGAME
				SI.setThreadID(self.cursor, self.username, self.threadid)
				room = SI.getUserLocation(self.cursor, self.username)
				area = SI.getArea(self.cursor, room)
				self.realMove(area, room, DBUpdate = 0)
				self.look()
				return
			self.username = ""
			self.write("Incorrect username or password. Please try again.")
			self.state = USERNAME
			self.look()
		elif self.state == INGAME:
			# We are in-game. Process the full command.
			firstCommand = lower(cmdList[0])
			if firstCommand in valid_commands.keys():
				function = getattr(self, valid_commands[firstCommand])
				function(cmdList)
			elif firstCommand in combatActions.keys():
				# Combat actions need a target.
				self.server.performAction(self.username, firstCommand,\
						(self.username, cmdList[1], self.threadid, self.room,\
						None))
			elif firstCommand in skillActions.keys():
				# Skill actions need a target, potentially.
				if len(cmdList) == 2:
					target = cmdList[1]
				else:
					target = None
				self.server.performAction(self.username, firstCommand,\
						(self.username, target, self.room, None))
			elif firstCommand in self.exits.keys():
				self.move(["go", firstCommand])
			elif not firstCommand.strip():
				# User just hit enter.
				return
			else:
				self.write("Unknown command.")

	def init(self):
		self.cursor = self.server.getCursor()
		self.state = USERNAME
		self.username = ""
		self.nickname = ""
		self.fullname = ""
		self.exits = {}
		self.userlevel = -1
		# Clear screen and reset cursor to 0,0
		self.sendToSelf(colorise('`7`r0`c'))
		self.look()
	
	def handle_exit(self):
		if self.username:
			SI.setThreadID(self.cursor, self.username, '')
		self.server.child_unregister(self.threadid)
	
	# Game Commands
	def examine(self, cmdList = []):
		if len(cmdList) < 2:
			itemText = "You examine yourself. It might be "\
					 "time to lay off the pastries.\r\n"
		else:
			itemText = SI.getItemDescription(self.cursor, self.room, cmdList)
		self.sendToSelf(itemText)
	
	def get(self, cmdList = []):
		if len(cmdList) < 2:
			getText = "You successfully grab nothing.\r\n"
		else:
			getText = SI.getItemForUser(self.cursor, cmdList,
										self.room, self.username)
		self.sendToSelf(getText)

	def look(self, cmdList = []):
		if self.state == INGAME:
			descr = colorise(SI.getRoomDescription(self.cursor, self.room))
			self.sendToSelf(descr)
			# Print exits
			if not self.exits.items():
				self.sendToSelf("You can see no way out of this area.")
			else:
				exitText = "\r\nYou can see the following exits: "
				exitText += ','.join(self.exits.keys())
				self.write(exitText)
			# Print Items
			items = SI.getRoomItems(self.cursor, self.room)
			if items:
				items = "\r\n" + "\r\n".join(items) + "\r\n"
				self.sendToSelf(items)
		else:
			descr = None
			if self.state == USERNAME:
				descr = colorise("`%Login:")
			elif self.state == PASSWORD:
				descr = colorise("`%Password:")
			else:
				print "Unknown state - '%s'" % self.state
			self.sendToSelf(descr)
	
	def emote(self, cmdList):
		whatToDo = " ".join(cmdList[1:])
		action = "`3%s %s" % (self.nickname, whatToDo)
		action = colorise(action)
		self.server.localPrint("", self.room, action + "\r\n")
	
	def stop(self, cmdList):
		"""
		Stops performing an action.
		"""
		if len(cmdList) < 2:
			self.write("What do you want to stop doing?")
			return
		whatToStop = cmdList[1]
		if not self.server.stopAction(self.username, whatToStop):
			self.write("Unable to stop %s." % whatToStop)

	def diction(self, cmdList):
		if len(cmdList) == 1:
			i = randint(1,3)
			if i == 1:
				self.write("`%You want to say nothing. You succeed admirably.")
			elif i == 2:
				self.write("`%You are speechless.")
			else:
				self.emote("emote looks like they are about to say something, then changes their mind.".split(' '))
			return
		# FIXME: Must be a nicer way of not hard-coding phrases like this.
		operator = ("says", "say")
		if cmdList[-1][-1] == "?":
			operator = ("asks", "ask")
		whatToSay = " ".join(cmdList[1:])
		text = "`9%s %s, '%s`1'" \
				% (self.nickname, operator[0], whatToSay)
		text = colorise(text)
		self.server.localPrint(self.threadid, self.room, text + "\r\n")
		ownOutput = colorise("`9You %s, '%s`1'" % (operator[1], whatToSay))
		self.write(ownOutput)
	
	def move(self, cmdList):
		if len(cmdList) == 1:
			self.write('%sWhere do you want to go?')
			return
		cmdList = cmdList[1:]
		direction = lower(cmdList[0])
		if direction not in self.exits.keys():
			self.write('%sYou want to go where?')
			return
		areaid, roomid = self.exits[direction]
		self.realMove(areaid, roomid)
		self.look()

	def quit(self, cmdList):
		self.finish()

	# Utility methods
	def realMove(self, areaid, roomid, DBUpdate = 1):
		# Stop whatever actions we might be doing.
		self.server.stopAllActions(self.username)
		# FIXME: disengage from combat?
		self.server.changeLocation(
			self.threadid, self.username,
			areaid, roomid, DBUpdate)
		self.exits = SI.getExits(self.cursor, roomid)
		self.area = areaid
		self.room = roomid

def main():
	server = GameServer(config.get('port'), GameClient)
	server.serve_forever()

if __name__=="__main__":
	main()
