#!/usr/bin/env python
"""
$Id: Skills.py,v 1.1 2005/05/30 02:00:35 rwh Exp $

Skill use actions.
"""
from random import Random
import server.DBConstants as DC
from server.Actions import Action
from server.interface import getUserData

rnd = Random()

Dance = "dance"
Dancing = "dancing"

DANCE_STRINGS = (
		"%s dances around.",
		"%s twirls about.",
		"%s spins and prances.",
		"%s gracefully swirls.",
)

class DanceAction(Action):
	def start(self):
		self.player, self.target, self.room, other = self.params
		self.realName = getUserData(self.server.cursor, self.player,\
				DC.NickName)
		self.server.display("", self.room, "`9%s strikes up a pose."\
				% self.realName)
		return True
	
	def think(self):
		i = rnd.randint(0, len(DANCE_STRINGS) - 1)
		self.server.display("", self.room, "`9" + DANCE_STRINGS[i]\
				% self.realName)
	
	def stop(self):
		self.server.display("", self.room, "`9%s has finished dancing."\
				% self.realName)

ACTION_MAP = {
	Dance: (5, DanceAction),
}

VERB_MAP = {
	Dancing: Dance,
}
