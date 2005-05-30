#!/usr/bin/env python
"""
$Id: Errors.py,v 1.1 2005/05/30 02:00:35 rwh Exp $

Error classes.
"""

class GameError(Exception):
	def __init__(self, error = "Unknown Error"):
		self.details = error
		Exception.__init__(self)
	
	def __str__(self):
		return self.details
