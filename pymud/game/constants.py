#!/usr/bin/env python
"""
$Id: constants.py,v 1.2 2005/10/26 06:14:38 rwh Exp $
Enums required for Maelstrom

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

# Attack enums
ATTACK_MISSED = 0
ATTACK_BLOCKED = 1
ATTACK_BLOCKED_CRITICAL = 2
ATTACK_ABSORBED = 3		# For armour absorbtion or mercenary absorbtion
ATTACK_BLUDGEON = 4
ATTACK_BLUDGEON_WOUND = 5
ATTACK_BODGE = 6
ATTACK_HIT = 7
ATTACK_HIT_SERIOUS = 7
ATTACK_HIT_CRITICAL = 8
ATTACK_HIT_MAGIC = 10
ATTACK_DEFENDER_BODGE = 11

# Damage enums
DAMAGE_BLUDGEONING = 0
DAMAGE_SERIOUS = 1

