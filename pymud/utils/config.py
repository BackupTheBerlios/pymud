#!/usr/bin/env python
"""
$Id: config.py,v 1.1 2005/05/30 02:00:36 rwh Exp $

Config file system.
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
