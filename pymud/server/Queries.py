#!/usr/bin/env python
"""
$Id: Queries.py,v 1.4 2006/04/18 12:20:33 stips Exp $
Database queries.

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

import DBConstants as DC

# User Queries.
CreateUser = """
INSERT INTO TABLE Users
(%(UserID)s, %(Password)s, %(NickName)s, %(FullName)s, %(UserLevel)s)
VALUES
(%%(UserID)s, %%(Password)s, %%(NickName)s, %%(FullName)s,
%%(UserLevel)s)
""" % DC.__dict__

GetPassword = """
SELECT Password FROM %(Users)s WHERE %(UserID)s = '%%(UserID)s'
""" % DC.__dict__

GetAllUserData = """
SELECT * FROM %(Users)s WHERE %(UserID)s = '%%(UserID)s'
""" % DC.__dict__

GetUserData = """
SELECT %%s FROM %(Users)s WHERE %(UserID)s = '%%s'
""" % DC.__dict__

GetThreadID = """
SELECT %(CurrentThreadID)s
FROM %(Users)s
WHERE %(UserID)s = '%%(UserID)s'
""" % DC.__dict__

SetThreadID = """
Update %(Users)s
Set %(CurrentThreadID)s = '%%(CurrentThreadID)s'
WHERE %(UserID)s = '%%(UserID)s';
""" % DC.__dict__

ClearLoggedInUsers = """
Update %(Users)s
Set %(CurrentThreadID)s = '';
""" % DC.__dict__

GetThreads = """
SELECT %(CurrentThreadID)s
FROM %(Users)s
WHERE %(UserID)s IN %%s
""" % DC.__dict__

# Request Queries.
GetRoomDescription = """
SELECT %(RoomDescription)s 
FROM %(Rooms)s 
WHERE %(RoomID)s = %%(RoomID)s
""" % DC.__dict__

GetExits = """
SELECT
%(Exits)s
FROM %(Rooms)s
WHERE %(RoomID)s = '%%(RoomID)s'
""" % DC.__dict__

GetAreaID = """
SELECT %(AreaID)s FROM %(Rooms)s
WHERE %(RoomID)s = '%%(RoomID)s'
""" % DC.__dict__

GetUserRoomID = """
SELECT %(RoomID)s
FROM %(Users)s
WHERE %(UserID)s = '%%(UserID)s'
""" % DC.__dict__

GetUsersInRoom = """
SELECT %(UserID)s
FROM %(Users)s
WHERE %(RoomID)s = '%%(RoomID)s'
""" % DC.__dict__

GetThreadsInRoom = """
SELECT %(CurrentThreadID)s
FROM %(Users)s
WHERE %(RoomID)s = '%%(RoomID)s'
AND %(CurrentThreadID)s != ''
""" % DC.__dict__

GetItemsInRoom = """
SELECT %(ItemRoomDescription)s
FROM %(Items)s
WHERE %(ItemID)s in (
	SELECT %(ItemID)s 
	FROM %(Room_Items)s
	WHERE %(RoomID)s = '%%(RoomID)s'
	AND %(RoomItemCount)s != 0
	AND %(RoomItemCount)s != '-1');
""" % DC.__dict__

GetItemDescription = """
SELECT %(ItemDescription)s, %(ItemKeyWords)s
FROM %(Items)s
WHERE %(ItemID)s in (
	SELECT %(ItemID)s 
	FROM %(Room_Items)s
	WHERE %(RoomID)s = '%%(RoomID)s'
	AND %(RoomItemCount)s != 0);
""" % DC.__dict__

GetItemsForUser = """
SELECT i.%(ItemID)s, i.%(ItemKeyWords)s, ri.%(RoomItemCount)s
FROM %(Items)s as i, %(Room_Items)s as ri
WHERE i.%(ItemID)s = ri.%(ItemID)s
AND ri.%(RoomID)s = '%%(RoomID)s'
AND ri.%(RoomItemCount)s NOT in (0,-1)
""" % DC.__dict__

GetUserItems = """
SELECT i.%(ItemID)s, ui.%(UserItemCount)s
FROM %(Items)s as i, %(User_Items)s as ui
WHERE i.%(UserID)s = ui.%%(UserID)s
"""

# Update Queries.
UpdateRoomItemCount = """
UPDATE %(Room_Items)s
SET %(RoomItemCount)s = '%%(ItemCount)s'
WHERE %(ItemID)s = '%%(ItemID)s'
AND %(RoomID)s = '%%(RoomID)s'
""" % DC.__dict__

UpdateUserItemCount = """
UPDATE %(User_Items)s
SET %(UserItemCount)s = '%%(ItemCount)s'
WHERE %(ItemID)s = '%%(ItemID)s'
AND %(UserID)s = '%%(UserID)s'
""" % DC.__dict__

UpdateUserInventory = """
INSERT INTO User_Items
(%(UserID)s, %(ItemID)s, %(UserItemCount)s)
VALUES
('%%(UserID)s', '%%(ItemID)s', '%%(ItemCount)s')
""" % DC.__dict__

UpdateRoomID = """
Update %(Users)s
Set %(RoomID)s = %%(RoomID)s
WHERE %(UserID)s = '%%(UserID)s'
""" % DC.__dict__
