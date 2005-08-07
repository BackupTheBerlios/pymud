DROP TABLE Users;
DROP TABLE Items;
DROP TABLE Rooms;
DROP TABLE Areas;

CREATE TABLE Users (
	UserID varchar(20) NOT NULL UNIQUE,
	Password varchar(40) NOT NULL,
	Nickname varchar(20) NOT NULL,
	FullName varchar(70) NOT NULL,
	UserLevel integer DEFAULT 0,
	CurrentThreadID varchar(20) DEFAULT '',

	-- Location information
	Location integer NOT NULL DEFAULT 0,

	-- Combat information
	Wounds text,
	
	-- Stats
	Attack integer,
	RealAttack integer,
	Defence integer,
	RealDefence integer,
	Endurance integer,
	RealEndurance integer,

	-- Misc
	Misc text,
	
	-- Items
	Inventory text,

	PRIMARY KEY (UserID)
);

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
	'Sam the Barbarian Wizard Rogue',
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

-- Areas
CREATE TABLE Areas (
	AreaID integer UNIQUE,
	AreaShortName varchar(50) NOT NULL,
	AreaDescription text,

	PRIMARY KEY (AreaID)
);

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

-- Rooms
CREATE TABLE Rooms (
	RoomID integer UNIQUE,
	RoomShortName varchar(50) NOT NULL,
	RoomLongName varchar(150),
	RoomDescription text,
	RoomColour varchar(2) NOT NULL DEFAULT '`7',
	AreaID integer NOT NULL DEFAULT 0,

	-- Exits
	Exits text,

	-- Keys
	PRIMARY KEY (RoomID),
	FOREIGN KEY (AreaID) REFERENCES Areas(AreaID)
);

-- Items
CREATE TABLE Items (
	ItemID varchar(8) UNIQUE,
	ItemLocation integer,
	ItemCount integer NOT NULL,
	ItemKeyWords varchar(150) NOT NULL,
	ItemDescription text NOT NULL,
	ItemRoomDescription varchar(80),
	ItemData text,

	-- Keys
	PRIMARY KEY (ItemID)
);


-- Create 'Mobile Ave Station' - the staging area
INSERT INTO Rooms (
	RoomID, RoomShortName, RoomDescription, Exits
) VALUES (
	0,
	'Mobile Ave Station',
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
INSERT INTO Items (ItemID, ItemLocation, ItemCount, ItemKeyWords, ItemDescription, ItemRoomDescription, ItemData)
VALUES (
	'00000001',
	'0',
	'1',
	'slender,sword,blade',
	'Basic short sword: The base weapon of most militarys, the short sword offers versatility at affordable price.',
	'A slender blade rests against the wall.',
	'need: DMG, to hit, Durability, colour, engraving, personalised name?, any enchantments, any procs, requirements'
);

INSERT INTO Items (ItemID, ItemLocation, ItemCount, ItemKeyWords, ItemDescription, ItemRoomDescription, ItemData)
VALUES (
	'00000002',
	'0',
	'6',
	'leather,jerkin,top',
	'Leather jerkin: Providing protection only to the torso, this is one of the lightest of armours. Should we give them a durability (human readable of couse) here?',
	'Under the plaque is a neatly folded pile of leather tops.',
	'need: AC, stuff, Durability, colour, engraving, personalised name?, any enchantments, any procs, requirements'
);


INSERT INTO Items (ItemID, ItemLocation, ItemKeyWords, ItemDescription, ItemCount)
VALUES (
	'00000003',
	'1',
	'crapper,shitter,toilet,stall',
	'As you\'d suspect the stall contains a toilet. Or at least it contains what is left of a toilet. Generally they don\'t come with so many... extras either.',
	'-1'
);

