DELIMITER //
DROP PROCEDURE IF EXISTS GetQuery//
CREATE Procedure GetQuery(input VARCHAR(25))
BEGIN
	IF (input="avgplayerpassyd") THEN
		SELECT CONCAT(sq.FirstName,' ', sq.LastName) as Name, AVG(sq.PassingYards) as AvgPassingYards
		FROM (SELECT pl.FirstName, pl.LastName, ps.Year, MAX(ps.PassingYards) as PassingYards
			FROM( PlayersInfo pl JOIN Players p on pl.PlayerID=p.PlayerID) JOIN PassingStats ps on p.PlayerID = ps.playerID
			GROUP BY pl.PlayerID,ps.Year
			ORDER BY PassingYards desc) as sq
		GROUP BY Name
		ORDER BY AvgPassingYards desc
		LIMIT 25;
	ELSEIF (input="avgplayerrecyd") THEN
		SELECT CONCAT(sq.FirstName,' ',sq.LastName) as Name, AVG(sq.ReceivingYards) as AvgReceivingYards
		FROM (SELECT pl.FirstName, pl.LastName, re.Year, MAX(re.ReceivingYards) as ReceivingYards
			FROM(PlayersInfo pl JOIN Players p on pl.PlayerID=p.PlayerID) JOIN ReceivingStats re on p.PlayerID 
    			= re.playerID 
				GROUP BY pl.PlayerID,re.Year
				ORDER BY ReceivingYards desc) as sq
		GROUP BY Name
		ORDER BY AvgReceivingYards desc
		LIMIT 25;


	ELSEIF (input="avgplayerrushyd") THEN
		SELECT CONCAT(sq.FirstName,' ',sq.LastName) as Name, AVG(sq.RushingYards) as AvgRushingYards
		FROM (SELECT pl.FirstName, pl.LastName, ru.Year, MAX(ru.RushingYards) as RushingYards
			FROM( PlayersInfo pl JOIN Players p on pl.PlayerID=p.PlayerID) JOIN RushingStats ru on p.PlayerID = ru.playerID
			GROUP BY pl.PlayerID,ru.Year
			ORDER BY RushingYards desc) as sq
		GROUP BY Name
		ORDER BY AvgRushingYards desc
		LIMIT 25;

	ELSEIF (input="avgteampassyd") THEN
		SELECT t.Name, SUM(p.PassingYards)/4 as AvgPassingYards
        FROM Teams t JOIN Players pl on t.TeamId = pl.Team NATURAL JOIN PlayersInfo pi JOIN PassingStats p ON (pi.PlayerId=p.PlayerId AND pl.Year=p.Year)
        GROUP BY t.TeamID
        ORDER By AvgPassingYards desc;

	ELSEIF (input="avgteamrecyd") THEN
		SELECT t.Name, SUM(r.ReceivingYards)/4 as AvgReceivingYards
		FROM Teams t JOIN Players pl on t.TeamId = pl.Team NATURAL JOIN PlayersInfo pi JOIN ReceivingStats r ON (pi.PlayerId=r.PlayerId AND pl.Year=r.Year)
		GROUP BY t.TeamID
		ORDER By AvgReceivingYards desc;

	ELSEIF (input="avgteamrushyd") THEN
		SELECT t.Name, SUM(r.RushingYards)/4 as AvgRushingYards
		FROM Teams t JOIN Players pl on t.TeamId = pl.Team NATURAL JOIN PlayersInfo pi JOIN RushingStats r ON (pi.PlayerId=r.PlayerId AND pl.Year=r.Year)
		GROUP BY t.TeamID
		ORDER By AvgRushingYards desc;
	

	ELSEIF (input="avgplayerpasstd") THEN
		SELECT CONCAT(sq.FirstName,' ',sq.LastName) as Name, AVG(sq.TDPasses) as AvgPassingTDs
		FROM (SELECT pl.FirstName, pl.LastName, ps.Year, MAX(ps.TDPasses) as TDPasses
			FROM( PlayersInfo pl JOIN Players p on pl.PlayerID=p.PlayerID) JOIN PassingStats ps on p.PlayerID = ps.playerID
			GROUP BY pl.PlayerID,ps.Year
			ORDER BY TDPasses desc) as sq
		GROUP BY Name
		ORDER BY AvgPassingTDs desc
		LIMIT 25;

	ELSEIF (input="avgplayerrectd") THEN
		SELECT CONCAT(sq.FirstName,' ',sq.LastName) as Name, AVG(sq.ReceivingTDs) as AvgReceivingTDs
		FROM (SELECT pl.FirstName, pl.LastName, re.Year, MAX(re.ReceivingTDs) as ReceivingTDs
			FROM(PlayersInfo pl JOIN Players p on pl.PlayerID=p.PlayerID) JOIN ReceivingStats re on p.PlayerID 
    		= re.playerID 
			GROUP BY pl.PlayerID,re.Year
			ORDER BY ReceivingTDs desc) as sq
		GROUP BY Name
		ORDER BY AvgReceivingTDs desc
		LIMIT 25;
	ELSEIF (input="avgplayerrushtd") THEN
		SELECT CONCAT(sq.FirstName,' ',sq.LastName) as Name, AVG(sq.RushingTDs) as AvgRushingTDs
		FROM (SELECT pl.FirstName, pl.LastName, ru.Year, MAX(ru.RushingTDs) as RushingTDs
			FROM( PlayersInfo pl JOIN Players p on pl.PlayerID=p.PlayerID) JOIN RushingStats ru on p.PlayerID = ru.playerID
			GROUP BY pl.PlayerID,ru.Year
			ORDER BY RushingTDs desc) as sq
		GROUP BY Name
		ORDER BY AvgRushingTDs desc
		LIMIT 25;
	ELSEIF (input="avgteampasstd") THEN
        SELECT t.Name, SUM(p.TDPasses)/4 as AvgPassingTDs
        FROM Teams t JOIN Players pl on t.TeamId = pl.Team NATURAL JOIN PlayersInfo pi JOIN PassingStats p ON (pi.PlayerId=p.PlayerId)
        WHERE pl.Year = 2013
        GROUP BY t.TeamID
        ORDER By AvgPassingTDs desc;
    ELSEIF (input="avgteamrectd") THEN
        SELECT t.Name, SUM(r.ReceivingTDs)/4 as AvgReceivingTDs
        FROM Teams t JOIN Players pl on t.TeamId = pl.Team NATURAL JOIN PlayersInfo pi JOIN ReceivingStats r ON (pi.PlayerId=r.PlayerId AND pl.Year=r.Year)
        GROUP BY t.TeamID
        ORDER By AvgReceivingTDs desc;
    ELSEIF (input="avgteamrushtd") THEN
        SELECT t.Name, SUM(r.RushingTDs)/4 as AvgRushingTDs
        FROM Teams t JOIN Players pl on t.TeamId = pl.Team NATURAL JOIN PlayersInfo pi JOIN RushingStats r ON (pi.PlayerId=r.PlayerId AND pl.Year=r.Year)
        GROUP BY t.TeamID
        ORDER By AvgRushingTDs desc;
    ELSEIF (input="4dc4q") THEN 
        SELECT t.name AS "Team Name",averageplaysran.averageplays as "Avg # of Conversions in 4th" 
        FROM (SELECT p.offenseteam as team, count(*)/4 as averageplays from Plays as p WHERE down = 4 AND yards >= togo AND quarter = 4 
        GROUP BY p.offenseteam) AS averageplaysran JOIN Teams t ON averageplaysran.team = t.teamid 
        ORDER BY averageplaysran.averageplays DESC;
    ELSEIF (input="tfl") THEN 
        SELECT t.name, COUNT(*) as numTFLs FROM (Plays p JOIN Teams t ON (p.defenseteam = t.teamid)) JOIN SeasonOutcomes s ON (t.teamid = s.teamid AND p.seasonYear = s.Year) 
        WHERE yards < 0 AND s.Year = 2015 
        GROUP BY t.name, s.wins 
        ORDER BY numTFLs DESC;    
    END IF;
END //

DELIMITER ;