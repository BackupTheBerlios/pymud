#!/usr/bin/env python
"""
$Id: Server.py,v 1.3 2005/11/14 00:55:04 rwh Exp $

The actual game server and base handler classes.

The purpose of the two classes in this file are as follows:

	ThreadedServer uses the python TCPServer and Threading server to
	start listening on a given port. In addition to this, it allows
	tracking the child thread that handle each individual connecton.

	ClientHandler deals with each individual connection, looping over
	both the TCP Socket handle to retrieve and handle data from the
	client, and to also dole out data to the client that appears in
	the child's in-tray.

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

import socket, select, os, re, thread, threading, signal
import SocketServer
from SocketServer import TCPServer, StreamRequestHandler, ThreadingMixIn

class ThreadedServer(ThreadingMixIn, TCPServer):
	def __init__(self, port, RequestHandlerClass):
		self.port = port
		TCPServer.__init__(self, ('', port), RequestHandlerClass)
		self.inbox = {}
		self.outbox = {}

	def server_bind(self):
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		SocketServer.TCPServer.server_bind(self)
		print "Server started. Accepting connections on port %s" % self.port
	
	def child_register(self, tid):
		inputLine, outputLine = os.pipe()
		self.inbox[tid] = inputLine
		self.outbox[tid] = outputLine
		return inputLine

	def child_unregister(self, tid):
		if self.inbox.has_key(tid):
			del self.inbox[tid]
		if self.outbox.has_key(tid):
			del self.outbox[tid]
	
	def killThreads(self):
		remaining = threading.enumerate()
		thisThread = threading.currentThread()
		badThreads = []
		for t in remaining:
			if t != thisThread and t.isAlive():
				badThreads.append(t.getName())
		if badThreads:
			print "Bad death. Killing manually (threads %s)" % badThreads
			os.kill(os.getpid(), signal.SIGKILL)
	
	# Overridable methods for game purposes
	def changeLocation(self, **kwargs):
		print "This method is to be defined in a subclass."
	
class ClientHandler(StreamRequestHandler):
	def realHandle(self, command):
		print "This method is to be defined in a subcless."

	def init(self):
		print "This method is to be defined in a subcless."

	def handle_exit(self):
		print "This method is to be defined in a subcless."

	def handle(self):
		self.threadid = thread.get_ident()
		self.messageSocket = self.server.child_register(self.threadid)
		self.init()
		print "Client connected from %s in thread %s." \
				% (self.client_address[0], self.threadid)
		try:
			while self.server.running:
				try:
					# Poll our sockets for data.
					res = select.select([self.rfile.fileno(), \
							self.messageSocket], [], [], 0)
					if res== ([], [], []):
						continue
				except AttributeError:
					# This is reached if fileno() is
					# not an attribute of rfile, meaning
					# our client has been disconnected.
					break
				# Time to read data.
				if self.messageSocket in res[0]:
					# Message from server to client
					message = os.read(self.messageSocket, 8192)
					os.write(self.rfile.fileno(), message)
				elif self.rfile.fileno() in res[0]:
					# Data from client to server
					# FIXME: need timeouts for this stuff
					data = os.read(self.rfile.fileno(), 8192)
					if not data:
						return
					print "Got %s bytes, '%r'" % (len(data), data)
					lines = data.split('\r\n')
					for line in lines:
						print "sending %s" % line
						if line:
							self.realHandle(line)
			print "Client %s disconnected." % self.threadid
			self.handle_exit()
			self.finish()
		except socket.error, msg:
			print "Disconnected from client at %s." % self.client_address[0]
			self.handle_exit()
		except KeyboardInterrupt:
			return
	
	def sendToSelf(self, data, immediate = False):
		if immediate:
			os.write(self.rfile.fileno(), data)
		else:
			try:
				os.write(self.server.outbox[self.threadid], data)
			except IndexError:
				print "Was told to send a message to a client "\
						"who didn't have pipes set up properly. (TID = '%s')"\
						% self.threadid
	
	def write(self, data):
		self.sendToSelf(data + "\r\n")
