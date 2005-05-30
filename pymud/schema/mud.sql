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
	4,
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
	4,
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
	RoomItems text,

	-- Exits
	Exit1Names varchar(20) DEFAULT 'North',
	Exit1Room integer,
	Exit2Names varchar(20) DEFAULT 'South',
	Exit2Room integer,
	Exit3Names varchar(20) DEFAULT 'East',
	Exit3Room integer,
	Exit4Names varchar(20) DEFAULT 'West',
	Exit4Room integer,

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
	RoomID, RoomShortName, RoomDescription, Exit1Names, Exit1Room
) VALUES (
	0,
	'Mobile Ave Station',
	'You are standing on the platform of a train station. It is flat, barren and white. There are no exits that you can see - simply a few benches and the station plaque.',
	'North',
	1
);
INSERT INTO Rooms (
	RoomID, RoomShortName, RoomDescription, Exit1Names, Exit1Room
) VALUES (
	1,
	'Mobile Ave Station Restroom',
	'You are in the restroom at Mobile Ave Station. It\'s messay, and generally pretty unpleasant. There are serveral toilet stalls along one wall and sinks opposite them. There\'s something scrawled on the back of the restroom door.',
	'South',
	0
);



-- Create 'Remote Wilderness' 
INSERT INTO Rooms (
	RoomID, RoomShortName, RoomDescription, AreaID, Exit1Names, Exit1Room
) VALUES (
	2, 
	'Rocky Mountain Pass',
	'Nestled between the jagged heights of towering, snow-topped mountains, a narrow pass winds its way downwards. In the far distance, the mountains give way to a fertile valley - lush and green, with a blue-grey river that disappears deep within a dank forest to the south west. Large boulders line the edge of the rocky path, some with hardy trees growing around and through them, though none are tall enough to provide shade. The mountains are too close to make leaving the path advisable: for the non-suicidal, the only real direction is north, towards the valley.',
	1, 
	'South',
	3
);
INSERT INTO Rooms (
	RoomID, RoomShortName, RoomDescription, AreaID, Exit1Names, Exit1Room, Exit2Names, Exit2Room, Exit3Names, Exit3Room
) VALUES (
	3, 
	'Grassy Slopes',
	'The path that winds through the mountains broadens, as it leads down into the valley, sharp, rocky hills gradually becoming shallower, and turning into grassy slopes. This area is still too steep for crops, or grazing all but the hardiest of animals, but the path is not too arduous to walk. The view is spectacular: towering mountain spires to the north, a sea of green grass to the south, and, barely visible to the east, the rushing torrents of water from a mountain waterfall. ',
	1,
	'North',
	2,
	'South',
	4, 
	'East',
	5
);
INSERT INTO Rooms (
	RoomID, RoomShortName, RoomDescription, AreaID, Exit1Names, Exit1Room, Exit2Names, Exit2Room, Exit3Names, Exit3Room, Exit4Names, Exit4Room
) VALUES (
	4,
	'Grassy Valley',
	'Fertile and green, grassy plains extend in all directions, disappearing into a dank forest to the south west, and the towering walls of rocky mountains in every other direction. Small animals can occasionally be seen in the undergrowth; it\'s also possible to find various vegetables and fruits growing wild. In the distance, to the east, a river curves its way down from the mountains, eventually slinking in between the trees of the forest. ',
	1, 
	'North',
	3,
	'South',
	6,
	'East',
	7,
	'West',
	8
);
INSERT INTO Rooms (
	RoomID, RoomShortName, RoomDescription, AreaID, Exit1Names, Exit1Room, Exit2Names, Exit2Room, Exit3Names, Exit3Room
) VALUES (
	5, 
	'Mountain Waterfall',
	'A narrow path from the west leads down and around a gentle cliff, finally widening into an open clearing. Tumbling down a sheer cliff-face to the north is a spectacular waterfall, the spray of which can be felt from the other side of the clearing. There is what looks like an exceptionally narrow path along the wall of the cliff, leading behind the water\'s edge, though it seems hardly wide enough for a man to traverse it. A wide pool extends beneath the waterfall, deep enough to swim in - and clear, fresh, and full of fish. ',
	1, 
	'North', 
	9, 
	'South', 
	10, 
	'West',
	3
);
INSERT INTO Rooms (
	RoomID, RoomShortName, RoomDescription, AreaID, Exit1Names, Exit1Room, Exit2Names, Exit2Room, Exit3Names, Exit3Room
) VALUES (
	6, 
	'Southern Forest',
	'Towards the south-western end of the valley, the grassy plains begin to fade into a woody area, growing steadily more dense the further you travel. Heading south into the forest, the trees are thin, but numerous, their highest branches so densely leaved that it\'s hard to see the sky. Gnarled tree roots rise out of the dying leaves that litter the earthen ground - and there is always the sound of something moving, hidden by the undergrowth or another tree trunk. The forest extends towards the west, growing steadily deeper, while to the south the sound of trickling water suggests the presence of a stream of some kind. ',
	1, 
	'North', 
	4, 
	'South',
	11, 
	'West',
	8
);
INSERT INTO Rooms (
	RoomID, RoomShortName, RoomDescription, AreaID, Exit1Names, Exit1Room, Exit2Names, Exit2Room, Exit3Names, Exit3Room
) VALUES (
	7, 
	'Silty River',
	'A river winds through the valley, born out of a deep pool beneath a waterfall to the north, and disappearing, eventually, into the depths of the forest to the south west. For most of its path, it runs slowly, becoming increasingly silty as the riverbed becomes shallower and flatter. Towards the northern end, there are a few boulders within the stream\'s path, though it is at no point deep enough to be difficult to ford. Across the other side, eastwards, the grass continues, though the land grows increasingly barren as it hits the sharp edge of the mounain range beyond. ', 
	1, 
	'North', 
	10, 
	'South', 
	11, 
	'West', 
	4
);
INSERT INTO Rooms (
	RoomID, RoomShortName, RoomDescription, AreaID, Exit1Names, Exit1Room, Exit2Names, Exit2Room, Exit3Names, Exit3Room
) VALUES (
	8, 
	'Western Forest', 
	'Growing steadily more dense, the forest stretches across the south western corner of the valley. The western end has enormous trees, rising high into the sky, and forbidding all but the faintest amount of sunlight to appear through the canopy. Most of these trees are to tall to climb, their lowest branches too high above a man\'s head, but there are a few that might - if one were especially agile - be reachable. ', 
	1, 
	'East', 
	4, 
	'South', 
	6, 
	'Up', 
	12
); 
INSERT INTO Rooms (
	RoomID, RoomShortName, RoomDescription, AreaID, Exit1Names, Exit1Room
) VALUES (
	9, 
	'Waterfall Cave', 
	'Impossible to get to - save for the very small, or very agile - this is a cave all but hidden behind the raging torrents of the waterfall. Cool and dank, water drips down the walls, and sprays from the waterfall itself - spectacular, especially when the sun shines off of it. The cave is only small, perhaps large enough for two or three people to fit in comfortably, and too damp to be useful for much. ', 
	1, 
	'South', 
	5
); 
INSERT INTO Rooms (
	RoomID, RoomShortName, RoomDescription, AreaID, Exit1Names, Exit1Room, Exit2Names, Exit2Room
) VALUES (
	10, 
	'Waterfall Pool', 
	'Formed beneath the giant waterfall, this deep pool is clear and fresh, and teeming with fish. Though the northern end is dangerous to swim in, thanks to the torrents of water sprawling down the cliff-face, the southern end is deep enough to dive in safely, and much calmer. The water drains further south, forming the slow-moving river that ambles through the valley.  ', 
	1, 
	'North', 
	5, 
	'South', 
	7
); 

INSERT INTO Rooms (
	RoomID, RoomShortName, RoomDescription, AreaID, Exit1Names, Exit1Room, Exit2Names, Exit2Room
) VALUES (
	11, 
	'Shaded Stream', 
	'Deep within the furthest reaches of the forest, a tiny stream winds its way - the last remains of the river that extends across the valley. The water is little more than a trickle, and too dirty to be especially appetising to drink, but it makes a pleasant sound amidst the soft noises of the forest. This is a peaceful place, as the forest goes, sheltered enough to be private - most of the time. ', 
	1, 
	'North', 
	6, 
	'North East', 
	7
);

INSERT INTO Rooms (
	RoomID, RoomShortName, RoomDescription, AreaID, Exit1Names, Exit1Room
) VALUES (
	12, 
	'Ancient Oak Tree', 
	'This is one of the few climbable trees in the western end of the forest - though even this one would be a difficult climb for those lacking strength and agility. The daring can climb high enough to peer through the leaves towards the rest of the valley, but most will find it easier - and safer - to stay lower down. Here, they can stay out of sight of the forest floor, yet still have the ability to see what is going on down there from a safe distance. ',
	1, 
	'Down', 
	8
);

INSERT INTO Items 
VALUES (
	'00000001',
	'0',
	'1',
	'slender,sword,blade',
	'Basic short sword: The base weapon of most militarys, the short sword offers versatility at affordable price.',
	'A slender blade rests against the wall.',
	'need: DMG, to hit, Durability, colour, engraving, personalised name?, any enchantments, any procs, requirements'
);

INSERT INTO Items 
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

