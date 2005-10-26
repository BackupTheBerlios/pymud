#!/usr/bin/env python
"""
$Id: misc.py,v 1.2 2005/10/26 06:13:22 rwh Exp $
Useful functions of randomness.

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

def getDict(data, itemDelimiter = ";", valueDelimiter = "="):
	"""
	Takes a string which contains a representation of key-value
	pairs and converts them into a dictionary.
	"""
	properData = data.split(itemDelimiter)
	temp = []
	dict = {}
	for item in properData:
		temp.append(item.split(valueDelimiter))
	for key, value in temp:
		try:
			newValue = int(value)
		except ValueError:
			if value[0] == '"' and value[-1] == '"':
				newValue = value[1:-1]
			else:
				newValue = value
		dict[key] = newValue
	return dict.copy()
