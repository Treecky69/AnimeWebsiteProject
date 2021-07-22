from flask import Flask, render_template, blueprints, request, redirect
from AnimeWebsiteProject import app, user, admin
import sqlite3
from funcs import table_form, genre_list, Database_entry, update_db, id_entry, delete_entry, new_genre, random_id, random_num

#home directory, main page where random anime genres will be displayed

@user.route("/")
@user.route("/home")
def index():
    return render_template("main_page.html", rows = random_id(random_num()))

#Anime Table, showing all the anime in the database

@user.route("/anime_list")
def anime_list():
    return render_template("anime_table.html", rows = table_form())

#Admin page, for modifying the database

@admin.route("/admin")
def CRUD():
    return render_template("admin.html", rows = table_form())

#The html and logic for the new entry

@admin.route("/admin/create", methods = ["GET", "POST"])
def create():
    if request.method == "POST":
        req = request.form
        entries = Database_entry(req["title"], req["numepisodes"], req["rating"], req.getlist("genres"))
        check = entries.Main_data()

        #if a title is already in the database
        if check:
            return redirect("/failure")

        return redirect("/endpoint")

    if request.method == "GET":
        return render_template("create.html", genres = genre_list())

#The html and logic when updating info about an anime

@admin.route("/admin/update", methods = ["GET", "POST"])
def update():
    if request.method == "GET":
        args = request.args
        return render_template("update.html", rows = id_entry(args["id"]), genres = genre_list())

    if request.method == "POST":
        args = request.args
        forms = request.form
        error = update_db(args["id"], forms["db-attribs"], forms["query"], forms.getlist("genres"))
        if error:
            return redirect("/failure")
        return redirect("/endpoint")

#html and logic for deleting an entry in the database

@admin.route("/admin/delete", methods = ["GET", "POST"])
def delete():
    if request.method == "GET":
        args=request.args
        return render_template("delete.html", rows = id_entry(args["id"]))

    if request.method == "POST":
        args = request.args
        delete_entry(args["id"])
        return redirect("/endpoint")

#html and logic for adding a new genre to the genres table in the database

@admin.route("/admin/new_genre", methods=["GET", "POST"])
def genre():
    if request.method == "POST":
        req = request.form

        #if a title is already in the database
        check = new_genre(req["genre"])
        if check:
            return redirect("/failure")

        return redirect("/endpoint")

    if request.method == "GET":
        return render_template("create_genre.html")

#endpoint for when a change is made

@admin.route("/endpoint")
def endpoint():
    return render_template("endpoint.html")

@admin.route("/failure")
def failure():
    return render_template("failure.html")

#Runnning the server

if __name__ == "__main__":
    app.register_blueprint(user) # register blueprint
    app.register_blueprint(admin) # register blueprint
    #app.config["EXPLAIN_TEMPLATE_LOADING"] = True #debug in the command line, tells you where it searches for the templates and static files
    app.run(debug = True, port = 6969, use_reloader=False)
