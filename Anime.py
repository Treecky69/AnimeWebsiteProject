from flask import Flask, render_template, blueprints
from AnimeWebsiteProject import app, home_view
import sqlite3

#home directory, main page where random anime genres will be displayed

@home_view.route("/")
@home_view.route("/home")
def index():
    return render_template("main_page.html")

#Anime Table, showing all the anime in the database

@home_view.route("/anime_list")
def anime_list():
    con = sqlite3.connect("anime_mock.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""select anime.name as anime_name, anime.numepisodes as numepisodes, anime.rating as rating, genres.genre as anime_genre from anime_genre
    inner join anime on anime.ID = anime_genre.animeID inner join genres on genres.ID = anime_genre.genreID""")
    rows = cur.fetchall()
    return render_template("anime_table.html", rows = rows)

#Runnning the server

if __name__ == "__main__":
    app.register_blueprint(home_view) # register blueprint
    app.config.from_pyfile("settingslocal.py") #config file
    #app.config["EXPLAIN_TEMPLATE_LOADING"] = True #debug in the command line, tells you where it searches for the templates and static files
    app.run(debug = True, port = 6969)
