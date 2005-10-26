#!/usr/bin/env python
"""
$Id: Queries.py,v 1.3 2005/10/26 06:20:55 rwh Exp $
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

GetLocation = """
SELECT %(Location)s
FROM %(Users)s
WHERE %(UserID)s = '%%(UserID)s'
""" % DC.__dict__

GetUsersInRoom = """
SELECT %(UserID)s
FROM %(Users)s
WHERE %(Location)s = '%%(Location)s'
""" % DC.__dict__

GetThreadsInRoom = """
SELECT %(CurrentThreadID)s
FROM %(Users)s
WHERE %(Location)s = '%%(Location)s'
AND %(CurrentThreadID)s != ''
""" % DC.__dict__

GetItemsInRoom = """
SELECT %(ItemRoomDescription)s
FROM %(Items)s
WHERE %(ItemLocation)s = '%%(RoomID)s'
AND %(ItemCount)s != 0 
AND %(ItemCount)s != '-1'
""" % DC.__dict__

GetItemDescription = """
SELECT %(ItemDescription)s, %(ItemKeyWords)s
FROM %(Items)s
WHERE %(ItemLocation)s = '%%(RoomID)s'
AND %(ItemCount)s != 0
""" % DC.__dict__

GetItemsForUser = """
SELECT %(ItemID)s, %(ItemKeyWords)s, %(ItemCount)s
FROM %(Items)s
WHERE %(ItemLocation)s = '%%(RoomID)s'
AND %(ItemCount)s != 0
AND %(ItemCount)s != '-1'
""" % DC.__dict__

GetUserInventory = """
SELECT %(Inventory)s
FROM %(Users)s
WHERE %(UserID)s = '%%(UserID)s'
""" % DC.__dict__

# Update Queries.
UpdateItemCount = """
UPDATE %(Items)s
SET %(ItemCount)s = '%%(ItemCount)s'
WHERE %(ItemID)s = '%%(ItemID)s'
""" % DC.__dict__

UpdateUserInventory = """
UPDATE %(Users)s
SET %(Inventory)s = '%%(Inventory)s'
WHERE %(UserID)s = '%%(UserID)s';
""" % DC.__dict__

UpdateLocation = """
Update %(Users)s
Set %(Location)s = %%(Location)s
WHERE %(UserID)s = '%%(UserID)s';
""" % DC.__dict__
