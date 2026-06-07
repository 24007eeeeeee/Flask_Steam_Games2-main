from flask import Flask, g, render_template
import sqlite3

DATABASE = 'database.db'

#initialise app
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    #Closes the database connection automatically when the application context ends
    db = getattr(g, '_database', None)
    if db is not None:
        db.close() 

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def home():
               # Selecting GameID(0), Studio Name(1), ImageURL(2), Cost(3), Description(4), and VideoURL(6)
    sql = """
            SELECT SteamGames.GameID, SteamGames.Game, SteamGames.ImageURL, SteamGames.Cost, SteamGames.Description, SteamGames.VideoURL
            FROM SteamGames
            JOIN Studios ON Studios.StudioID=SteamGames.StudioID;"""
    results = query_db(sql)
    return render_template("home.html", results=results)

@app.route("/game/<int:id>")
def game(id):
    #just one game based on the id
    sql = """SELECT * FROM SteamGames
    JOIN Studios ON Studios.StudioID=SteamGames.StudioID
    WHERE SteamGames.GameID = ?;"""
    result = query_db(sql,(id,),True)
    return render_template("game.html", game=result)


if __name__ == "__main__":
    app.run(debug=True)