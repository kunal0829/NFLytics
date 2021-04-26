from app import app
from flask import render_template, redirect, request, url_for
from app import database as db_helper
import string

teams_arr = ['HOU', 'LV', 'MIA', 'ATL', 'WAS', 'SF', 'NO', 'SD', 'DAL', 'DET', 'TEN', 'SEA', 'KC', 'CLE', 'PHI', 'MIN', 'DEN', 'BUF', 'BAL', 'NE', 'TB', 'CHI', 'ARI', 'NYJ', 'GB', 'PIT', 'NYG', 'CAR', 'CIN', 'LA', 'JAX', 'IND']
divisions = {'AFCN':'AFC North', 'AFCS':'AFC South', 'AFCE':'AFC East', 'AFCW':'AFC West', 'NFCN':'NFC North', 'NFCS':'NFC South', 'NFCE':'NFC East', 'NFCW':'NFC West'}

ADMIN_LOGINS = {"Shashank":"royal", "Kunal":"capitals", "Amandeep":"sunrisers", "Arpandeep":"superkings", "Nandini":"ksdjfsdfsd"}
# admin_access = False
# CURR_USER = "Guest"
# print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

db_helper.init()

@app.route("/")
def homepage():
    return render_template("mainpage.html", user=db_helper.get_curr_user())


@app.route("/teams")
@app.route("/teams/")
@app.route("/teams/<team>")
@app.route("/teams/<team>/<year>")
def teams(team=None,year=None):
    if team:
        if year:
            team = db_helper.fetch_teamfromid(team)
            roster = db_helper.fetch_roster(team,year)
            return render_template("teampage.html", team=team,roster=roster,user=db_helper.get_curr_user())
        else:
            team = db_helper.fetch_teamfromid(team)
            return render_template("teampage.html", team=team,roster=None,user=db_helper.get_curr_user())
    else:
        teams = db_helper.fetch_teamdata()
        return render_template("teams.html", teams=teams,user=db_helper.get_curr_user())

@app.route("/players")
@app.route("/players/")
@app.route("/players/<player>")
def players(player=None):
    if str(player).upper() == "KASA" :
        players = db_helper.fetch_demoplayerquery(player)
        return render_template("playerquery.html",players=players,user=db_helper.get_curr_user())
    if player:
        players = db_helper.fetch_playerquery(player)
        return render_template("playerquery.html",players=players,user=db_helper.get_curr_user())
    else:
        return render_template("players.html",user=db_helper.get_curr_user())


@app.route("/player/<id>")
def player(id=None):
    if id:
        player = db_helper.fetch_playerfromid(id)
        print(str(player["position"]) + "yo")
        if player["position"] in ["QB","RB","WR","TE","SF","CB","DT","DE","LB"]:
            columns,stats = db_helper.fetch_playerpagestats(player)
            return render_template("playerpage.html",player=player,columns=columns,stats=stats)
        
        return render_template("playerpage.html",player=player)


# we want an app route to carry out the action of adding the player
# since this action is based on the submission of a form it is considered a POST http request
@app.route("/add", methods = ['POST'])
def add():
    print("hello")
    # when a POST is made to this endpoint we can get the data submitted as a dictionary (request.form)
    # add_id = request.form['id']
    add_id = db_helper.fetch_empty_id()
    add_first_name = request.form['firstname']
    add_last_name = request.form['lastname']
    add_pos = request.form['position']
    print("{} - {} - {} - {}".format(add_id, add_first_name, add_last_name, add_pos)) # to check if it worked
    # now you have all four stuff and can check or do whatever and if good addplayer to DB
    db_helper.addplayer(add_id, add_first_name, add_last_name, add_pos)
    return redirect("/player/"+str(add_id)) # this will look for addplayer route (the one below)

@app.route("/addplayer")
def addplayer():
    if db_helper.get_admin_access():
        return render_template("addplayer.html",user=db_helper.get_curr_user())
    return render_template("accesserror.html",user=db_helper.get_curr_user())

@app.route("/removeplayer/<id>",methods = ['POST'])
def removeplayer(id=None):
    if not db_helper.get_admin_access():
        return render_template("accesserror.html",user=db_helper.get_curr_user())
    elif id:
        db_helper.removeplayer(id)
        return redirect("/players")
    return redirect("/players")

@app.route("/updateplayer/<id>",methods = ['POST'])
def updateplayer(id=None):
    if not db_helper.get_admin_access():
        return render_template("accesserror.html",user=db_helper.get_curr_user())
    elif id:
        player = db_helper.fetch_playerfromid(id)
        return render_template("updateplayer.html",player=player,user=db_helper.get_curr_user())
    return render_template("updateplayer.html",player=None,user=db_helper.get_curr_user())

@app.route("/updateplayer/updated/<id>", methods = ['POST'])
def updated(id = None):
    if id: 
        update_first_name = request.form['firstname']
        update_last_name = request.form['lastname']
        update_pos = request.form['position']
        db_helper.update_player(id, update_first_name, update_last_name, update_pos)
        print("Complete")
    return redirect("/player/" + str(id)) # this will look for addplayer route (the one below)



@app.route("/stats")
def stats():
        return render_template("stats.html",user=db_helper.get_curr_user())

@app.route("/stats/team/<statistic>")
def teamstats(statistic=None):
    if statistic == "4dc4q":
        query = db_helper.fetch_stastics(statistic)
        return  render_template("teamstat.html",query=query,fields=["Team","Avg 4th Down Conv in 4th"],user=db_helper.get_curr_user())
    elif statistic == "tfl":
        query = db_helper.fetch_stastics(statistic)
        return  render_template("teamstat.html",query=query,fields=["Team","# of Tackles for Loss"],user=db_helper.get_curr_user())

    elif statistic == "avgteampassyd":
        query = db_helper.fetch_stastics(statistic)
        return  render_template("teamstat.html",query=query,fields=["Team","Average Passing Yards"],user=db_helper.get_curr_user())
    elif statistic == "avgteamrecyd":
        query = db_helper.fetch_stastics(statistic)
        return  render_template("teamstat.html",query=query,fields=["Team","Average Receiving Yards"],user=db_helper.get_curr_user())
    elif statistic == "avgteamrushyd":
        query = db_helper.fetch_stastics(statistic)
        return  render_template("teamstat.html",query=query,fields=["Team","Average Rushing Yards"],user=db_helper.get_curr_user())
    elif statistic == "avgteampasstd":
        query = db_helper.fetch_stastics(statistic)
        return  render_template("teamstat.html",query=query,fields=["Team","Average Passing TDs"],user=db_helper.get_curr_user())
    elif statistic == "avgteamrectd":
        query = db_helper.fetch_stastics(statistic)
        return  render_template("teamstat.html",query=query,fields=["Team","Average Receiving TDs"],user=db_helper.get_curr_user())
    elif statistic == "avgteamrushtd":
        query = db_helper.fetch_stastics(statistic)
        return  render_template("teamstat.html",query=query,fields=["Team","Average Rushing TDs"],user=db_helper.get_curr_user())
    else:
         return render_template("stats.html",user=db_helper.get_curr_user())

@app.route("/stats/player/<statistic>")
def playerstats(statistic=None):
    if statistic == "avgplayerpassyd":
        query = db_helper.fetch_stastics(statistic)
        return  render_template("playerstat.html",query=query,fields=["Player","Average Passing Yards"],user=db_helper.get_curr_user())
    elif statistic == "avgplayerrecyd":
        query = db_helper.fetch_stastics(statistic)
        return  render_template("playerstat.html",query=query,fields=["Player","Average Receiving Yards"],user=db_helper.get_curr_user())
    elif statistic == "avgplayerrushyd":
        query = db_helper.fetch_stastics(statistic)
        return  render_template("playerstat.html",query=query,fields=["Player","Average Rushing Yards"],user=db_helper.get_curr_user())
    elif statistic == "avgplayerpasstd":
        query = db_helper.fetch_stastics(statistic)
        return  render_template("playerstat.html",query=query,fields=["Player","Average Passing TDs"],user=db_helper.get_curr_user())
    elif statistic == "avgplayerrectd":
        query = db_helper.fetch_stastics(statistic)
        return  render_template("playerstat.html",query=query,fields=["Player","Average Receiving TDs"],user=db_helper.get_curr_user())
    elif statistic == "avgplayerrushtd":
        query = db_helper.fetch_stastics(statistic)
        return  render_template("playerstat.html",query=query,fields=["Player","Average Rushing TDs"],user=db_helper.get_curr_user())
    else:
         return render_template("stats.html",user=db_helper.get_curr_user())


#SHANK ROUTES

@app.route("/plays/updated", methods = ['POST'])
def update_play():
    db_helper.update_play(request.form)
    return render_template("plays.html",user=db_helper.get_curr_user())

@app.route("/plays/add_play", methods = ['POST'])
def add_play():
    print("=======ADDED PLAYS=======")
    db_helper.create_play(request.form)
    return render_template("plays.html",user=db_helper.get_curr_user())

@app.route("/plays")
@app.route("/plays/")
@app.route("/plays/<operation>")
@app.route("/plays/<operation>/")
@app.route("/plays/<operation>/<id>")
@app.route("/plays/<operation>/<id>/")
def plays(operation=None, id=None):
    if operation:
        if operation == "search":
            if (id):
                ids = id.split('-')
                if (len(ids) >= 3):
                    plays = db_helper.fetch_play(ids[2], offenseTeam=ids[0], defenseTeam=ids[1])
                    return render_template("playsearchquery.html", plays=plays,user=db_helper.get_curr_user())
                else:
                    return render_template("playsearch.html", teams=teams_arr,user=db_helper.get_curr_user())
            else:
                return render_template("playsearch.html", teams=teams_arr,user=db_helper.get_curr_user())
        elif operation == "updateplay":
            if not db_helper.get_admin_access():
                return render_template("accesserror.html")
            elif id:
                play = db_helper.fetch_play_by_id(id)
                return render_template("playupdate.html", play=play,user=db_helper.get_curr_user())
            else:
                return render_template("plays.html")
        elif operation == "deleteplay":
            if not db_helper.get_admin_access():
                return render_template("accesserror.html")
            elif id:
                play = db_helper.delete_play(id)
                return render_template("plays.html", play=play,user=db_helper.get_curr_user())
            else:
                return render_template("plays.html",user=db_helper.get_curr_user())
        elif operation == "addplay":
            if not db_helper.get_admin_access():
                return render_template("accesserror.html",user=db_helper.get_curr_user())
            return render_template("playsadd.html",user=db_helper.get_curr_user())
        else:
            return render_template("plays.html",user=db_helper.get_curr_user())
    else:
        return render_template("plays.html",user=db_helper.get_curr_user())

@app.route("/seasons")
@app.route("/seasons/")
def seasons():
    return render_template("seasons.html", divisions=divisions,user=db_helper.get_curr_user())

@app.route("/seasons/<id>")
@app.route("/seasons/<id>/")
def season_search(id):
    if id:
        ids = id.split('-')
        if (len(ids) >= 2):
            team_outcome = db_helper.fetch_team_outcome(ids[0], ids[1])
            return render_template("seasonquery.html", results=team_outcome,user=db_helper.get_curr_user())
        else:
            return render_template("seasons.html", divisions=divisions,user=db_helper.get_curr_user())
    else:
        return render_template("seasons.html", divisions=divisions,user=db_helper.get_curr_user())


@app.route("/login")
@app.route("/login/")
def login():
    db_helper.set_curr_user("Guest")
    db_helper.set_admin_access(False)
    return render_template("login.html", status="first",user=db_helper.get_curr_user())

@app.route("/login", methods=['POST'])
def login_process():
    uname = request.form['uname']
    pwd = request.form['password']
    
    if (uname == "Guest"):
        db_helper.set_admin_access(False)
        db_helper.set_curr_user("Guest")
        return render_template("mainpage.html", user=db_helper.get_curr_user())
    elif (uname in ADMIN_LOGINS.keys()  and  ADMIN_LOGINS[uname] == pwd):
        db_helper.set_admin_access(True)
        db_helper.set_curr_user(uname)
        return render_template("mainpage.html", user=db_helper.get_curr_user())
    else:
        db_helper.set_admin_access(False)
        db_helper.set_curr_user("Guest")
        return render_template("login.html", status="incorrect",user=db_helper.get_curr_user())
