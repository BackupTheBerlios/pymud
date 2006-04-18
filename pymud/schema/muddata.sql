------- Areas -------
-- Create 'Out of Character' area
INSERT INTO Areas VALUES (
	0,
	'Out of Character',
	''
);

-- Create 'Remote Wilderness' area
INSERT INTO Areas VALUES (
	1,
	'Remote Wilderness',
	''
);



------- Rooms -------
-- Create 'Mobil Ave Station' - the staging area
INSERT INTO Rooms (
	RoomID, RoomShortName, RoomDescription, Exits
) VALUES (
	0,
	'Mobil Ave Station',
	'You are standing on the platform of a train station. It is flat, barren and white. There are no exits that you can see - simply a few benches and the station plaque.',
	'Restroom=0|1'
);
INSERT INTO Rooms (
	RoomID, RoomShortName, RoomDescription, Exits
) VALUES (
	1,
	'Mobile Ave Station Restroom',
	'You are in the restroom at Mobile Ave Station. It\'s messay, and generally pretty unpleasant. There are serveral toilet stalls along one wall and sinks opposite them. There\'s something scrawled on the back of the restroom door.',
	'Platform=0|0'
);



------- Users -------
-- Create admin user!
INSERT INTO Users VALUES (
	'admin',
	'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',
	'Gandalf',
	'The Administrator',
	5
);
INSERT INTO Users VALUES (
	'rohan',
	'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',
	'Rohan',
	'Rohan the Bard',
	0,
	'',
	0,
	'',
	60,
	60,
	30,
	30,
	30,
	30
);
INSERT INTO Users VALUES (
	'stips',
	'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',
	'Stips',
	'Stips the Witch',
	0,
	'',
	0,
	'',
	30,
	30,
	30,
	30,
	30,
	30
);
INSERT INTO Users VALUES (
	'sam',
	'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',
	'Sam',
	'Sam the lion witch and wardrobe',
	0,
	'',
	0,
	'',
	30,
	30,
	30,
	30,
	30,
	30
);



------- Items -------
INSERT INTO Items (ItemID, ItemKeyWords, ItemDescription, ItemRoomDescription, ItemData)
VALUES (
	'00000001',
	'slender,sword,blade',
	'The base weapon of most militaries, the short sword offers versatility at affordable price.',
	'A slender blade rests against the wall.',
	'need: DMG, to hit, Durability, colour, engraving, personalised name?, any enchantments, any procs, requirements'
);

INSERT INTO Items (ItemID, ItemKeyWords, ItemDescription, ItemRoomDescription, ItemData)
VALUES (
	'00000002',
	'leather,jerkin,top',
	'Providing protection only to the torso, this is one of the lightest of armours.',
	'Under the plaque is a neatly folded pile of leather tops.',
	'need: AC, stuff, Durability, colour, engraving, personalised name?, any enchantments, any procs, requirements'
);

INSERT INTO Items (ItemID, ItemKeyWords, ItemDescription)
VALUES (
	'00000003',
	'crapper,shitter,toilet,stall',
	'As you\'d suspect the stall contains a toilet. Or at least it contains what is left of a toilet.'
);

INSERT INTO Items (ItemID, ItemKeyWords, ItemDescription)
VALUES (
	'00000004',
	'plaque,sign',
	'The station plaque reads \'Mobil Ave. Station\'.'
);




------- Items in Rooms -------
INSERT INTO Room_Items (ItemID, RoomID, RoomItemCount)
VALUES (
	'00000001',
	0,
	1
);

INSERT INTO Room_Items (ItemID, RoomID, RoomItemCount)
VALUES (
	'00000002',
	0,
	6
);

INSERT INTO Room_Items (ItemID, RoomID, RoomItemCount)
VALUES (
	'00000004',
	0,
	-1
);

INSERT INTO Room_Items (ItemID, RoomID, RoomItemCount)
VALUES (
	'00000003',
	1,
	-1
);
