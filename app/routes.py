from app import app
from flask import render_template, redirect, request, url_for
from app import database as db_helper
import string


@app.route("/")
def homepage():
    teams = db_helper.fetch_teamdata()
    return render_template("mainpage.html")


@app.route("/teams")
@app.route("/teams/")
@app.route("/teams/<team>")
def teams(team=None):
    if team:
        team = db_helper.fetch_teamfromid(team)
        return render_template("teampage.html", team=team)
    else:
        teams = db_helper.fetch_teamdata()
        return render_template("teams.html", teams=teams)

@app.route("/players")
@app.route("/players/")
@app.route("/players/<player>")
def players(player=None):
    if str(player).upper() == "KASA" :
        players = db_helper.fetch_demoplayerquery(player)
        return render_template("playerquery.html",players=players)
    if player:
        players = db_helper.fetch_playerquery(player)
        return render_template("playerquery.html",players=players)
    else:
        return render_template("players.html")


@app.route("/player/<id>")
def player(id=None):
    if id:
        player = db_helper.fetch_playerfromid(id)
        return render_template("playerpage.html",player=player)


# we want an app route to carry out the action of adding the player
# since this action is based on the submission of a form it is considered a POST http request
@app.route("/add", methods = ['POST'])
def add():
    print("hello")
    # when a POST is made to this endpoint we can get the data submitted as a dictionary (request.form)
    add_id = request.form['id'] #the key should match up to the name of the textbox on addplayer.html
    add_first_name = request.form['firstname']
    add_last_name = request.form['lastname']
    add_pos = request.form['position']
    print("{} - {} - {} - {}".format(add_id, add_first_name, add_last_name, add_pos)) # to check if it worked
    # now you have all four stuff and can check or do whatever and if good addplayer to DB
    db_helper.addplayer(add_id, add_first_name, add_last_name, add_pos)
    return redirect("/player/"+str(add_id)) # this will look for addplayer route (the one below)

@app.route("/addplayer")
def addplayer():
    return render_template("addplayer.html")

@app.route("/removeplayer/<id>",methods = ['POST'])
def removeplayer(id=None):
    if id:
        db_helper.removeplayer(id)
        return redirect("/players")
    return redirect("/players")

@app.route("/updateplayer/<id>",methods = ['POST'])
def updateplayer(id=None):
    if id:
        player = db_helper.fetch_playerfromid(id)
        return render_template("updateplayer.html",player=player)
    return render_template("updateplayer.html",player=None)

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
        return render_template("stats.html")

@app.route("/stats/team/<statistic>")
def teamstats(statistic=None):
    if statistic == "4dc4q":
        query = db_helper.fetch_stastics(statistic)
        return  render_template("teamstat.html",query=query,fields=["Team","Avg 4th Down Conv in 4th"])
    elif statistic == "tfl":
        query = db_helper.fetch_stastics(statistic)
        return  render_template("teamstat.html",query=query,fields=["Team","# of Tackles for Loss"])
    else:
         return render_template("stats.html")


#SHANK ROUTES

@app.route("/plays/updated", methods = ['POST'])
def update_play():
    db_helper.update_play(request.form)
    return render_template("plays.html")

@app.route("/plays/add_play", methods = ['POST'])
def add_play():
    print("=======ADDED PLAYS=======")
    db_helper.create_play(request.form)
    return render_template("plays.html")

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
                if (len(id) >= 3):
                    plays = db_helper.fetch_play(ids[2], offenseTeam=ids[0], defenseTeam=ids[1])
                    return render_template("playsearchquery.html", plays=plays)
                else:
                    return render_template("playsearch.html")
            else:
                return render_template("playsearch.html")
        elif operation == "updateplay":
            if id:
                play = db_helper.fetch_play_by_id(id)
                return render_template("playupdate.html", play=play)
            else:
                return render_template("plays.html")
        elif operation == "deleteplay":
            if id:
                play = db_helper.delete_play(id)
                return render_template("plays.html", play=play)
            else:
                return render_template("plays.html")
        elif operation == "addplay":
            return render_template("playsadd.html")
        else:
            return render_template("plays.html")
    else:
        return render_template("plays.html")
