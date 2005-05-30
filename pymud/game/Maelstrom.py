#!/usr/bin/env python
"""
$Id: Maelstrom.py,v 1.1 2005/05/30 02:00:35 rwh Exp $

Maelstrom-specific rules.
"""

from game.constants import *
from server.Errors import GameError
from game.dice import d10, d100

BODY_LOCATIONS = (
	'',
	'head',
	'torso',
	'torso',
	'torso',
	'torso',
	'torso',
	'left arm',
	'right arm',
	'left leg',
	'right leg',
)

CRIT_UPPER = 96
CRIT_LOWER = 5

def criticalSuccess(i):
	if i >= 95:
		return True
	return False

def criticalFail(i):
	if i <= 5:
		return True
	return False

def getWounds(rawWounds):
	"""
	Tally up the number of wounds a person has.
	"""
	if not rawWounds:
		return ([], 0)
	realWounds = []
	totalWounds = 0
	wounds = rawWounds.split(',')
	for wound in wounds:
		location, size = wound.split(':')
		realWounds.append((location, size))
		totalWounds += size
	return (realWounds, totalWounds)

def calcAttack(info):
	"""
	Figures out the result of an attack on another entity.
	Details should be provided in the following format:
	{
		attackerAttackSkill: x,
		defenderDefenceSkill: x,
		attackerDamage: x,
		attackerDamageType: enum DamageType,
	}
	Results should be as follows:
	{
		Result: enum Result,
		Damage: x,
		DamageType: enum DamageType,
		DamageLocation: x,
	}
	"""
	try:
		attackerAttackSkill = info["attackerAttackSkill"]
		defenderDefenceSkill = info["defenderDefenceSkill"]
		attackerDamage = info["attackerDamage"]
		attackerDamageType = info["attackerDamageType"]
	except KeyError:
		raise GameError("Incomplete data sent to attack routine.")
	res = {}
	attack = d100()
	
	if attack >= CRIT_UPPER:
		res["Result"] = ATTACK_BODGE
		# FIXME: Bodge result calcs
		return res
	
	if attack > attackerAttackSkill:
		# Fail totally.
		res["Result"] = ATTACK_MISSED
		return res
	
	defend = d100()
	
	if defend >= CRIT_UPPER:
		res["Result"] = ATTACK_DEFENDER_BODGE
		return res
	
	if defend <= defenderDefenceSkill:
		if defend <= CRIT_LOWER:
			# Critical defend, meaning a free strike.
			res["Result"] = ATTACK_BLOCKED_CRITICAL
			return res
		res["Result"] = ATTACK_BLOCKED
		return res

	# A hit.
	res["Result"] = ATTACK_HIT
	if info["DamageType"] == DAMAGE_BLUDGEONING:
		res["DamageType"] = DAMAGE_BLUDGEONING
	elif info["Damagetype"] == DAMAGE_SERIOUS:
		res["DamageType"] = DAMAGE_SERIOUS
	res["Damage"] = attackerDamage()
	res["DamageLocation"] = d10()
	if res["DamageLocation"] == 1:
		# Head shot. Double it.
		res["Damage"] *= 2
	return res
