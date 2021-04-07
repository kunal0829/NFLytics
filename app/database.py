from app import db

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
        'firstname': player[0][2],
        'lastname': player[0][1],
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


def convertDiv(division):
    if division[len(division) - 1] == 'W':
        return division[:len(division) - 1] + " West"
    elif division[len(division) - 1] == 'N':
        return division[:len(division) - 1] + " North"
    elif division[len(division) - 1] == 'S':
        return division[:len(division) - 1] + " South"
    else: 
        return division[:len(division) - 1] + " East"