from flask import Flask, render_template, blueprints, request, redirect
from AnimeWebsiteProject import app, user, admin
import sqlite3
from funcs import table_form, genre_list

#home directory, main page where random anime genres will be displayed

@user.route("/")
@user.route("/home")
def index():
    return render_template("main_page.html")

#Anime Table, showing all the anime in the database

@user.route("/anime_list")
def anime_list():
    table_form()
    return render_template("anime_table.html", rows = table_form())

#admin page, for modifying the database

@admin.route("/admin")
def CRUD():
    table_form()
    return render_template("CRUD.html", rows = table_form())

@admin.route("/admin/create")
def create_entry():
    return render_template("create.html", genres = genre_list())

@admin.route("/create", methods = ["GET", "POST"])
def create():
    if request.method == "POST":
        req = request.form
        title = req["title"]
        number_eps = req["numepisodes"]
        rating = req["rating"]
        genre = req.getlist("genres")
        return str("%s, %s, %s, %s" % (title, number_eps, rating, genre))
    return render_template("main_page.html")
#Runnning the server

if __name__ == "__main__":
    app.register_blueprint(user) # register blueprint
    app.register_blueprint(admin) # register blueprint
    #app.config.from_pyfile("settingslocal.py") #config file
    #app.config["EXPLAIN_TEMPLATE_LOADING"] = True #debug in the command line, tells you where it searches for the templates and static files
    app.run(debug = False, port = 6969, use_reloader=False)
