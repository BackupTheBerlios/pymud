-- Items
CREATE TABLE Items (
	ItemID varchar(8) UNIQUE,
	ItemKeyWords varchar(150) NOT NULL,
	ItemDescription text NOT NULL,
	ItemRoomDescription varchar(80),
	ItemData text,

	-- Keys
	PRIMARY KEY (ItemID)
);

-- Areas
CREATE TABLE Areas (
	AreaID integer UNIQUE,
	AreaShortName varchar(50) NOT NULL,
	AreaDescription text,

	PRIMARY KEY (AreaID)
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

--Users
CREATE TABLE Users (
	UserID varchar(20) NOT NULL UNIQUE,
	Password varchar(40) NOT NULL,
	Nickname varchar(20) NOT NULL,
	FullName varchar(70) NOT NULL,
	UserLevel integer DEFAULT 0,
	CurrentThreadID varchar(20) DEFAULT '',

	-- Location information
	RoomID integer NOT NULL DEFAULT 0,

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
	
	-- Keys
	PRIMARY KEY (UserID),
	FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
);


CREATE TABLE Room_Items (
	ItemID varchar(8) NOT NULL,
	RoomID integer NOT NULL,
	RoomItemCount integer NOT NULL,

	-- Keys
	PRIMARY KEY (ItemID,RoomID),
	FOREIGN KEY (ItemID) REFERENCES Items(ItemID),
	FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
);

CREATE TABLE User_Items (
	ItemID varchar(8) NOT NULL,
	UserID varchar(20) NOT NULL,
	UserItemCount integer NOT NULL DEFAULT 1,

	-- Keys
	PRIMARY KEY (ItemID, UserID),
	FOREIGN KEY (ItemID) REFERENCES Items(ItemID),
	FOREIGN KEY (UserID) REFERENCES Users(UserID)
);


