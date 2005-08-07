#!/usr/bin/env python
"""
$Id: misc.py,v 1.1 2005/08/07 07:25:51 rwh Exp $

Useful functions of randomness.
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
