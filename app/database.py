from app import db
import math
import random


def fetch_teamdata():
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """
    teamdata = []

    # for i in range (32):
    #     teamdata.append({'id':'SDF','name':'Team'+str(i),'city':'City' + str(i),'div':convertDiv('AFCS')})

    conn = db.connect()
    teams = conn.execute("SELECT * FROM Teams ORDER BY Division;").fetchall()
    conn.close()
    teamdata = []
    for team in teams: 
        current = {
            'id': team[0],
            'city': team[2],
            'name': team[1],
            'div': convertDiv(team[3])
        }
        teamdata.append(current)
    return teamdata

def fetch_playerquery(player):
    playerquery = []
    # for i in range (10):
    #     playerquery.append({'firstname':'Tom','lastname':'Brady'+str(i),'position':'QB','id':i})

    query = "SELECT * FROM PlayersInfo WHERE CONCAT(FirstName,' ',LastName) LIKE " +  "\"" + "%%" + str(player)+ "%%"  + "\""
    conn = db.connect()
    players = conn.execute(str(query)).fetchall()
    conn.close()
    for player in players: 
        current = {
            'id': player[0],
            'firstname': player[1],
            'lastname': player[2],
            'position': player[3]
        }
        playerquery.append(current)
    return playerquery

def fetch_demoplayerquery(player):
    playerquery = []
    # for i in range (10):
    #     playerquery.append({'firstname':'Tom','lastname':'Brady'+str(i),'position':'QB','id':i})

    query = "SELECT * FROM PlayersInfo WHERE PlayerId <= 100"
    conn = db.connect()
    players = conn.execute(str(query)).fetchall()
    conn.close()
    for player in players: 
        current = {
            'id': player[0],
            'firstname': player[1],
            'lastname': player[2],
            'position': player[3]
        }
        playerquery.append(current)
    return playerquery

def fetch_teamfromid(teamid):
    #WRITE THE TEAM QUERY HERE
    query = "SELECT * FROM Teams WHERE TeamId = " + "\"" + str(teamid) + "\""
    conn = db.connect()
    team = conn.execute(str(query)).fetchall()
    conn.close()
    current = {
        'id': team[0][0],
        'city': team[0][2],
        'name': team[0][1],
        'div': convertDiv(team[0][3])
    }
    
    return current

def fetch_playerfromid(playerid):
    query = "SELECT * FROM PlayersInfo WHERE PlayerId = " + "\"" + str(playerid) + "\""
    conn = db.connect()
    player = conn.execute(str(query)).fetchall()
    conn.close()
    current = {
        'id': player[0][0],
        'firstname': player[0][1],
        'lastname': player[0][2],
        'position': player[0][3]
    }
    return current


# function we want to call from page
def addplayer(id,firstname,lastname,position):
    query = "INSERT INTO PlayersInfo(PlayerId,FirstName,LastName,Position) VALUES (" + str(id) + ",\"" + str(firstname) + "\",\"" + str(lastname) + "\",\"" + str(position) + "\")"
    conn = db.connect()
    conn.execute(str(query))
    conn.close()
    return
    
def fetch_empty_id():
    id = random.randint(1, 99)
    query = "SELECT PlayerId FROM PlayersInfo WHERE PlayerId = " + str(id)
    conn = db.connect()
    check = conn.execute(str(query)).fetchall()
    while len(check) > 0:
        id = random.randint(1, 99)
        query = "SELECT PlayerId FROM PlayersInfo WHERE PlayerId = " + str(id)
        check = conn.execute(str(query)).fetchall()
    conn.close()
    print(id)
    return id



def removeplayer(id):
    query = "DELETE FROM PlayersInfo WHERE PlayerId = " + str(id)
    conn = db.connect()
    conn.execute(str(query))
    conn.close()
    return


def convertDiv(division):
    if division[len(division) - 1] == 'W':
        return division[:len(division) - 1] + " West"
    elif division[len(division) - 1] == 'N':
        return division[:len(division) - 1] + " North"
    elif division[len(division) - 1] == 'S':
        return division[:len(division) - 1] + " South"
    else: 
        return division[:len(division) - 1] + " East"

def fetch_play(seasonYear, offenseTeam=None, defenseTeam=None):
    attrs = "PlayId, Quarter, OffenseTeam, DefenseTeam, YardLine, Yards, Description, SeasonYear"

    query = "SELECT " + attrs + " FROM Plays WHERE OffenseTeam LIKE \"" + offenseTeam + "\" AND DefenseTeam LIKE \""  + defenseTeam + "\" AND SeasonYear = " + str(seasonYear) + " ORDER BY GameDate DESC, Quarter ASC;"

    conn = db.connect()
    plays = conn.execute(query).fetchall()
    conn.close()

    ret = []
    for play in plays:
        curr_play = {
            'playid': play[0],
            'quarter': play[1],
            'oteam': play[2],
            'dteam': play[3],
            'yardLine': play[4],
            'yards': play[5],
            'description': play[6],
            'season': play[7]
        }
        ret.append(curr_play)
    return ret;

def fetch_play_by_id(playid):
    attrs = "PlayId, Quarter, OffenseTeam, DefenseTeam, YardLine, Yards, Description, SeasonYear"

    query = "SELECT " + attrs + " FROM Plays WHERE PlayId = " + str(playid) + ";";

    conn = db.connect()
    plays = conn.execute(query).fetchall()
    conn.close()

    if not plays:
        return None
    
    play = plays[0]

    print("======Fetching=====")
    print(play)

    curr_play = {
        'playid': play[0],
        'quarter': play[1],
        'oteam': play[2],
        'dteam': play[3],
        'yardLine': play[4],
        'yards': play[5],
        'description': play[6],
        'season': play[7]
    }

    return curr_play

def update_play(dict):
    if (dict):
        query = "UPDATE Plays SET Quarter = " + dict['quarter'] + ", OffenseTeam = \"" + dict['oteam'] + "\", DefenseTeam = \"" + dict['dteam'] + "\", YardLine = \"" + dict['yardLine'] + "\", Yards = \"" + dict['yards'] + "\", Description = \"" + dict['description'] + "\", SeasonYear = \"" + dict['season'] + "\" WHERE PlayId = " + dict['playid'] + ";";

        print(query)

        conn = db.connect()
        conn.execute(query)
        conn.close()


def delete_play(playid):
    if (dict):
        query = "DELETE FROM Plays WHERE PlayId = " + playid + ";";

        print(query)

        conn = db.connect()
        conn.execute(query)
        conn.close()

def create_play(dict):
    if dict:
        attrs = "PlayId, GameId, GameDate, Quarter, OffenseTeam, DefenseTeam, Down, ToGo, YardLine, Yards, Description, SeasonYear"
        # query = "INSERT INTO Plays(" + attrs + ") VALUES(" + dict['playid'] + ", " + dict['gameid'] + ", TO_DATE(\"" + dict['gamedate'] + "\", \"MM/DD/YY\"), " + dict['quarter'] + ", \"" + dict['oteam'] + "\", \"" + dict['dteam'] + "\", " + dict['down'] + ", " + dict['togo'] + ", " + dict['yardLine'] + ", " + dict['yards'] + ", \"" + dict['description'] + "\", " + dict['season'] + ");"
        pid = random.randrange(2**20)
        while (fetch_play_by_id(pid)):
            pid = random.randrange(2**20)

        query = "INSERT INTO Plays(" + attrs + ") VALUES(" + str(pid) + ", " + dict['gameid'] + ", \"" + dict['gamedate'] + "\", " + dict['quarter'] + ", \"" + dict['oteam'] + "\", \"" + dict['dteam'] + "\", " + dict['down'] + ", " + dict['togo'] + ", " + dict['yardLine'] + ", " + dict['yards'] + ", \"" + dict['description'] + "\", " + dict['season'] + ");"

        print(query)

        conn = db.connect()
        conn.execute(query)
        conn.close()


def fetch_stastics(statistic):
    if statistic == "4dc4q":
        query = "SELECT t.name AS \"Team Name\",averageplaysran.averageplays as \"Avg # of Conversions in 4th\" FROM (SELECT p.offenseteam as team, count(*)/4 as averageplays from Plays as p WHERE down = 4 AND yards >= togo AND quarter = 4 GROUP BY p.offenseteam) AS averageplaysran JOIN Teams t ON averageplaysran.team = t.teamid ORDER BY averageplaysran.averageplays DESC;"
    elif statistic == "tfl":
        query = "SELECT t.name, COUNT(*) as numTFLs FROM (Plays p JOIN Teams t ON (p.defenseteam = t.teamid)) JOIN SeasonOutcomes s ON (t.teamid = s.teamid AND p.seasonYear = s.Year) WHERE yards < 0 AND s.Year = 2015 GROUP BY t.name, s.wins ORDER BY s.wins DESC, numTFLs DESC;"
    teamquery = []
    conn = db.connect()
    teams = conn.execute(str(query)).fetchall()
    conn.close()
    for team in teams:
        current = {
            'teamname': team[0],
            'avg': team[1],
        }
        teamquery.append(current)
    return teamquery

def update_player(id, first, last, position):
    #PlayerId,FirstName,LastName,Position
    query = "UPDATE PlayersInfo SET FirstName = \"" + str(first) + "\", LastName = \"" + str(last) + "\", Position = \"" + str(position) + "\" WHERE PlayerId = " + str(id) + ";"
    conn = db.connect()
    conn.execute(str(query))
    conn.close()
    return

