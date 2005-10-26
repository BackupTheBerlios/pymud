#!/usr/bin/env python
"""
$Id: config.py,v 1.2 2005/10/26 06:13:22 rwh Exp $
Config file system.

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

import os

config = {
	'port': '3000',
	'dbhost': 'localhost',
	'dbname': 'mud',
	'dblogin': 'root',
}

HOMEDIR = os.getenv('HOME')
CONFIGFILE = os.path.join(HOMEDIR, '.mudrc')

BLANKLINES = (None, '', '\n', '\r\n')

try:
	os.stat(CONFIGFILE)
except OSError:
	print "ERROR: Config file not found, defaults will be used"

configFile = open(CONFIGFILE, 'r')
while 1:
	line = configFile.readline()
	if not line:
		break
	line = line.strip()
	if line and line[0] == '#':
		# A comment line.
		continue
	try:
		key, value = line.split('=')
		try:
			config[key.strip()] = int(value.strip())
		except ValueError:
			config[key.strip()] = value.strip()
	except ValueError:
		if line not in BLANKLINES:
			print "ERROR: Malformed line '%s' in config file '%s'." \
					% (line, CONFIGFILE)

# Access functions
def get(key):
	return config.get(key)
