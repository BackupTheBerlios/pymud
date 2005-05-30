#!/usr/bin/env python
"""
$Id: dice.py,v 1.1 2005/05/30 02:00:35 rwh Exp $

Support funtions for dice-rolling, non engine-specific.
"""

from random import Random

rnd = Random()


def d6(dice = 1):
	return rnd.randint(dice, dice * 6)

def d10(dice = 1):
	return rnd.randint(dice, dice * 10)

def d100(dice = 1):
	return rnd.randint(dice, dice * 100)
