from app import app
from flask import render_template, redirect, request, url_for
from app import database as db_helper



@app.route("/")
def homepage():
    teams = db_helper.fetch_teamdata()
    return render_template("mainpage.html")


@app.route("/teams")
@app.route("/teams/<team>")
def teams(team=None):
    if team:
        team = db_helper.fetch_teamfromid(team)
        return render_template("teampage.html", team=team)
    else:
        teams = db_helper.fetch_teamdata()
        return render_template("teams.html", teams=teams)

@app.route("/players")
@app.route("/players/<player>")
def players(player=None):
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
    return redirect((url_for('addplayer'))) # this will look for addplayer route (the one below)


@app.route("/addplayer")
def addplayer():
    print("hi")
    return render_template("addplayer.html")

@app.route("/removeplayer")
def removeplayer():
    return render_template("removeplayer.html")

@app.route("/stats")
@app.route("/players/<statistic>")
def stats(statistic=None):
    if statistic:
        statistics = db_helper.fetch_stastics(statistic)
        statistictype = db_helper.fetch_stastic_type(statistic)
        if statistictype == "Team":
            return render_template("teamstatistics.html")
        else: 
            return render_template("playerstatistics.html")
    else:
        return render_template("stats.html")


#SHANK ROUTES
@app.route("/plays")
def plays():
    return render_template("plays.html")

