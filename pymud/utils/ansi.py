#!/usr/bin/env python 
"""
$Id: ansi.py,v 1.3 2005/10/26 06:09:59 rwh Exp $
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
from string import upper

"""
constants = "
BLACK
RED
GREEN
YELLOW
BLUE
MAGENTA
CYAN
WHITE

RESET
BOLD
REVERSE

BLACK_BG
RED_BG
GREEN_BG
YELLOW_BG
BROWN_BG
BLUE_BG
MAGENTA_BG
CYAN_BG
WHITE_BG

CLEAR_SCR
".strip().split()

g = globals()
for item in constants:
	g[item] = item

# Extraneous, just here for reference
ANSI_CODES = {
	BLACK : '\033[30m',
	RED : '\033[31m',
	GREEN : '\033[32m',
	YELLOW : '\033[33m',
	BLUE : '\033[34m',
	MAGENTA : '\033[35m',
	CYAN : '\033[36m',
	WHITE : '\033[37m',

	RESET : '\033[40;37m',
	BOLD : '\033[1m',
	REVERSE : '\033[2m',

	BLACKBG : '\033[40m',
	REDBG : '\033[41m',
	GREENBG : '\033[42m',
	YELLOWBG : '\033[43m',
	BROWNBG : '\033[0;43m',
	BLUEBG : '\033[44m',
	MAGENTABG : '\033[45m',
	CYANBG : '\033[46m',
	WHITEBG : '\033[47m',

	CLEARSCR : '\033[2J\033[0;0f',
}
"""

def colorise(text, firstLetterCap = 0):
	"""
	Split up text on every `, and map the following character to these colours:
	1 - dark blue
	2 - dark green
	3 - dark cyan
	4 - dark red
	5 - dark purple
	6 - brown
	7 - grey
	8 - dark grey
	9 - bright blue
	0 - bright green
	! - bright cyan
	@ - bright red
	# - bright purple
	$ - yellow
	% - white
	` - an actual ` character
	r - background colour change. interpret the character after the 'r' as:
		0 - black, default
		1 - blue
		2 - green
		3 - cyan
		4 - red
		5 - purple
		6 - brown
		7 - grey
	
	the last line of the code will automatically change the background
	colour back to normal.

	Colours such as grey and brown appear to be degrees of a parent
	colour.

		0: dark 1: bold(light) 4: Underscore, 5: Blink, 7: Inverse, 
			and 8: Concealed

	"""
	# ansi prefix
	ans = "\033["
	
	localColour = {
		"c" :	'\033[2J\033[0;0f',	# - clear screen
		
		"1" :	';34m',		# - dark blue
		"2" :	';32m',		# - dark green
		"3" :	';36m',		# - dark cyan
		"4" :	';31m',		# - dark red
		"5" :	';35m',		# - dark magenta 
		"6" :	';33m',		# - brown
		"7" :	';37m',		# - grey
		"8" :	';30;1m',	# - dark grey
		"9" :	';34;1m',	# - bright blue
		"0" :	';32;1m',	# - bright green
		"!" :	';36;1m',	# - bright cyan
		"@"	:	';31;1m',	# - bright red
		"#" :	';35;1m',	# - bright magenta
		"$" :	';33;1m',	# - yellow
		"%" :	';37;1m',	# - white
		"`" :	'`',				# - an actual ` character
	}
		
	# r - background colour change. interpret the character after the 'r' as:
	bgColour = {
        "0" :   '40',     # - black, default
		"1" :   '44',     # - blue
		"2" :   '42',     # - green
		"3" :   '46',     # - cyan
		"4" :   '41',     # - red
		"5" :   '45',     # - magenta
		"6" :   '0;43',   # - brown
		"7" :   '1;30',   # - grey
		"8" :   '43',     # - yellow
	}
	


	string = ""
	cList = text.split('`')
	if len(cList) > 1:
		firstItem = 1
		for colour in cList[1:]:
			try:
				if firstItem and firstLetterCap and len(colour) > 2:
					# Capitalise the first letter.
					colour = colour[0] + upper(colour[1]) + colour[2:]
					firstItem = 0
				# FIXME: bad constant here. Need a way to look up the text 
				# colour to retain when changing the background.
#				BG = bgColour.get("0")
				BG = '40'
				LC = ans + BG + localColour.get(colour[:1])
				string = string + LC + colour[1:]	
			except TypeError:
				print "Incorrect colour code." 

	if string:
		string = RESET + string + RESET
		return string
	return text

