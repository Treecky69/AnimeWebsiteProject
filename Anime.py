from flask import Flask, render_template, blueprints, request, redirect
from AnimeWebsiteProject import app, user, admin
import sqlite3
from funcs import table_form, genre_list, Database_entry

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

#Admin page, for modifying the database

@admin.route("/admin")
def CRUD():
    table_form()
    return render_template("admin.html", rows = table_form())

#The html for inserting info about a new entry

@admin.route("/admin/create")
def create_entry():
    return render_template("create.html", genres = genre_list())

#Where the request is made and the title is inserted in the database

@admin.route("/create", methods = ["GET", "POST"])
def create():
    if request.method == "POST":
        req = request.form
        entries = Database_entry(req["title"], req["numepisodes"], req["rating"], req.getlist("genres"))
        return str("%s" % (entries.Main_data()))
    return render_template("admin.html")

#Runnning the server

if __name__ == "__main__":
    app.register_blueprint(user) # register blueprint
    app.register_blueprint(admin) # register blueprint
    #app.config["EXPLAIN_TEMPLATE_LOADING"] = True #debug in the command line, tells you where it searches for the templates and static files
    app.run(debug = True, port = 6969, use_reloader=False)
