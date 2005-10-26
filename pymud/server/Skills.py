#!/usr/bin/env python
"""
$Id: Skills.py,v 1.2 2005/10/26 06:20:55 rwh Exp $
Skill use actions.

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
