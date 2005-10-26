#!/usr/bin/env python
"""
$Id: Combat.py,v 1.2 2005/10/26 06:20:55 rwh Exp $
Combat logic and items.

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

from server.Actions import Action
from game.dice import d100, d10
from game import Maelstrom
from game.constants import *
import server.DBConstants as DC
from server.interface import getUserData

Attack = "attack"
Attacking = "attacking"

class AttackAction(Action):
	def start(self):
		self.attacker, self.target, self.threadid, self.room,\
				other = self.params
		self.realName = getUserData(self.server.cursor, self.attacker,\
				DC.NickName)
		# FIXME: this has to change for mobs
		# FIXME: text defined by weapon type
		self.targetName = getUserData(self.server.cursor, self.target,\
				DC.NickName)
		self.publicPrint("`@%s whips out their weapon." % self.realName)
		self.privatePrint("`@You whip out your weapon.")
		return True
	
	def publicPrint(self, message):
		self.server.display(self.threadid, self.room, message)
	
	def privatePrint(self, message):
		self.server.sendMessage(self.threadid, message)
	
	def allPrint(self, message):
		self.server.display('', self.room, message)
	
	def think(self):
		targetDef, targetEnd, wounds = getUserData(self.server.cursor, self.target,
				(DC.RealDefence, DC.RealEndurance, DC.Wounds))
		attackSkill = int(getUserData(self.server.cursor, self.target, DC.RealAttack))
		targetDef = int(targetDef)

		info = {
			"attackerAttackSkill": attackSkill,
			"defenderDefenceSkill": targetDef,
			# FIXME hack
			"attackerDamage": d10,
			"attackerDamageType": DAMAGE_BLUDGEONING,
		}
		
		"""
		# ATTACK!
		attack = d100()
		print "%s attacks %s (rolled %s, needed %s" \
				% (self.attacker, self.target, attack, attackSkill)
		if attack > attackSkill:
			# Fail totally.
			self.publicPrint("`@%s takes a swing at %s and misses."\
					% (self.attacker, self.target))
			self.privatePrint("`@You take a swing at %s and miss."\
					% self.target)
			return
		defend = d100()
		print "%s defending against %s (rolled %s, needed %s)" \
				% (self.attacker, self.target, defend, targetDef)
		if defend <= targetDef:
			# Successfully defended.
			# FIXME: crits
			# FIXME: parry or sidestep? figure it out
			self.publicPrint("`@%s `%%blocks `@a swing from %s."\
					% (self.target, self.attacker))
			self.privatePrint("`@%s `%%blocks `@your attack."\
					% self.target)
			return
		# Hit
		damage = d10(2)
		location = d10()
		print "location = %s" % location
		if location == 1:
			# HEAD HIT!
			# FIXME: Move to Maelstrom.py
			damage *= 2
		print "%s point hit to %s" % (damage, BODY_LOCATIONS[location]) 
		self.publicPrint("`@%s `!hits`@ %s's %s!"\
				% (self.attacker, self.target, BODY_LOCATIONS[location]))
		self.privatePrint("`@You `!successfully`@ hit %s's %s!"\
				% (self.target, BODY_LOCATIONS[location]))
		"""

	def stop(self):
		self.publicPrint("`@%s stopped attacking %s." % (self.attacker, self.target))
		self.privatePrint("`@You stop attacking %s." % self.target)

ACTION_MAP = {
	Attack: (2, AttackAction),
}

VERB_MAP = {
	Attacking: Attack,
}
