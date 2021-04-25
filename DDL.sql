DROP TABLE IF EXISTS WatchList;
DROP TABLE IF EXISTS SeasonOutcomes;
DROP TABLE IF EXISTS Plays;
DROP TABLE IF EXISTS RushingStats;
DROP TABLE IF EXISTS PassingStats;
DROP TABLE IF EXISTS ReceivingStats;
DROP TABLE IF EXISTS DefensiveStats;
DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS PlayersInfo;
DROP TABLE IF EXISTS Teams;

#Assumption: This table stay unchanged
CREATE TABLE Teams(
	TeamId VARCHAR(3),
	Name VARCHAR(255),
	Location VARCHAR(255),
	Division VARCHAR(4),
	PRIMARY KEY(TeamId)
);

CREATE TABLE PlayersInfo(
	PlayerId INTEGER,
	FirstName VARCHAR(40) NOT NULL,
	LastName VARCHAR(40) NOT NULL,
	Position VARCHAR(2),
	PRIMARY KEY(PlayerId)
);


CREATE TABLE Players(
	PlayerId INTEGER,
	Year INTEGER,
	Team VARCHAR(3),
	Side VARCHAR(7),	
	PRIMARY KEY(PlayerId,Year,Team),
	FOREIGN KEY(Team) REFERENCES Teams(TeamId),
	FOREIGN KEY(PlayerId) REFERENCES PlayersInfo(PlayerId) ON DELETE CASCADE
);

CREATE TABLE DefensiveStats(
	PlayerId INTEGER,
	Year INTEGER,
	Sacks FLOAT,
	Ints INTEGER,
	TotalTackles INTEGER,
	Team VARCHAR(3),
	PRIMARY KEY (PlayerId,Year, Team),
	FOREIGN KEY(PlayerId,Year,Team) REFERENCES Players(PlayerId,Year,Team) ON DELETE CASCADE
);

CREATE TABLE PassingStats(
	PlayerId INTEGER,
	Year INTEGER,
	TDPasses INTEGER,
	PassingYards INTEGER,
	PassesAttempted INTEGER,
	Ints INTEGER,
	Team VARCHAR(3),
	PRIMARY KEY (PlayerId,Year,Team),
	FOREIGN KEY(PlayerId,Year,Team) REFERENCES Players(PlayerId,Year,Team) ON DELETE CASCADE
);

CREATE TABLE ReceivingStats(
	PlayerId INTEGER,
	Year INTEGER,
	ReceivingTDs INTEGER,
	ReceivingYards INTEGER,
	Receptions INTEGER,
	Fumbles INTEGER,
	Team VARCHAR(3),
	PRIMARY KEY(PlayerId,Year,Team),
	FOREIGN KEY(PlayerId,Year,Team) REFERENCES Players(PlayerId,Year,Team) ON DELETE CASCADE
);

CREATE TABLE RushingStats(
	PlayerId INTEGER,
	Year INTEGER,
	RushingTDS INTEGER,
	RushingYards INTEGER,
	RushingAttempts INTEGER,
	Fumbles INTEGER,
	Team VARCHAR(3),
	PRIMARY KEY(PlayerId,Year,Team),
	FOREIGN KEY(PlayerId,Year,Team) REFERENCES Players(PlayerId,Year,Team) ON DELETE CASCADE
);

CREATE TABLE Plays(
	PlayId INTEGER NOT NULL,
	GameId INTEGER NOT NULL,
	GameDate DATE NOT NULL,
	Quarter INTEGER,
	OffenseTeam VARCHAR(3) NOT NULL,
	DefenseTeam VARCHAR(3) NOT NULL,
	Down INTEGER,
	ToGo INTEGER,
	YardLine INTEGER,
	Yards INTEGER,
	Description VARCHAR(750),
	SeasonYear INTEGER,
	PRIMARY KEY(PlayId),
	FOREIGN KEY(OffenseTeam) REFERENCES Teams(TeamId),
	FOREIGN KEY(DefenseTeam) REFERENCES Teams(TeamId)
);

CREATE TABLE SeasonOutcomes(
	TeamId VARCHAR(3),
	Wins INTEGER,
	Losses INTEGER,
	Tied INTEGER,
	OSRS FLOAT,
	DSRS FLOAT,
	Year INTEGER,
	PRIMARY KEY(TeamID,Year),
	FOREIGN KEY(TeamId) REFERENCES Teams(TeamId)
);

CREATE TABLE WatchList(
	PlayerId INTEGER,
	PRIMARY KEY(PlayerId),
	FOREIGN KEY(PlayerId) REFERENCES PlayersInfo(PlayerId) ON DELETE CASCADE
);