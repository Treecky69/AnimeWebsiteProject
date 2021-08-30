import sqlite3
import random

#database variable
database = "./data/anime_mock.db"

#FUNCTION TO FETCH INFO FOR THE TABLE IN THE USER SIDE

def table_form():
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #this sqlite command fetches needed info for the table and merges ID from anime with animeID from anime_genre and ID from genres with genreID from anime_genre
    cur.execute("""select anime.ID as ID, anime.name as anime_name, anime.numepisodes as numepisodes, anime.rating as rating, genres.genre as anime_genre from anime_genre
    inner join anime on anime.ID = anime_genre.animeID inner join genres on genres.ID = anime_genre.genreID""")

    rows = cur.fetchall()
    return rows

def id_entry(id):
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #same as the command on line 11 but this one fetches info based on anime ID
    cur.execute("""select anime.ID as ID, anime.name as anime_name, anime.numepisodes as numepisodes, anime.rating as rating, genres.genre as anime_genre
    from anime_genre inner join anime on anime.ID = anime_genre.animeID inner join genres on genres.ID = anime_genre.genreID 
    where anime.ID == :id""", {"id": id})

    rows = cur.fetchall()
    return rows

#FUNCTION FOR DISPLAYING GENRES

def genre_list():
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #select all genres
    cur.execute("select * from genres")

    rows = cur.fetchall()
    return rows

#CLASS FOR THE NEW DATABASE ENTRY

class Database_entry:
    def __init__(self, title, NumEpisodes, rating, genres):
        self.title = title
        self.episodes = NumEpisodes #number of episodes
        self.rating = rating
        self.genres = genres

    def Main_data(self):
        #boolean variable that only becomes true when the inserted title from the form is already in the database
        check = False

        con = sqlite3.connect(database)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        #select all anime names
        cur.execute("select name from anime")
        rows = cur.fetchall()

        #capitalizing the first letter of each word in the anime title and comparing with existing titles
        self.title = self.title.title()
        for row in rows:
            if self.title in row["name"]:
                check = True
                return check

        #inserting the title, number of episodes and rating in the anime table
        cur.execute("insert into anime(name, NumEpisodes, rating) values(:name, :episodes, :rating)", {"name": self.title, "episodes": self.episodes, "rating": self.rating})

        #fetching the ID of the newly inserted anime
        cur.execute("select id from anime where name = :title", {"title": self.title})
        IDs = cur.fetchone()
        anime_ID = IDs["id"] #anime ID

        #inserting into the anime_genre database where the title and genres are connected
        for genre in self.genres:
            cur.execute("insert into anime_genre(animeID, genreID) values(:anime_ID, :genre_ID)", {"anime_ID": int(anime_ID), "genre_ID": int(genre)})  

        con.commit()
        return check

#FUNCTION FOR UPDATING ANIME INFO

def update_db(id, attrib, query, genres):
    #if there is an error, then its true
    error = False

    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #check if the string is empty or has nothing but whitespaces
    string_check = not query or query.isspace()

    if attrib == "genres" and len(genres) == 0:
        error = True

    elif attrib != "genres" and string_check:
        error = True

    else:
        #delete all the exsiting genre IDs associated with the anime ID in the anime_genre database
        #then insert the new ones
        if attrib == "genres":
            cur.execute("delete from anime_genre where animeid = :id", {"id": id})

            for genre in genres:
                cur.execute("insert into anime_genre(animeID, genreID) values(:anime_ID, :genre_ID)", {"anime_ID": int(id), "genre_ID": int(genre)})

        #update the name
        elif attrib == "name":

            query = query.title()
            cur.execute("update anime set name = :query where id == :id", {"id": id, "query": query})

        #update the number of episodes
        elif attrib == "numepisodes":
            cur.execute("update anime set numepisodes = :query where id == :id", {"id": id, "query": query})

        #update the rating
        elif attrib == "rating":
            cur.execute("update anime set rating = :query where id == :id", {"id": id, "query": query})

    if error == False:
        con.commit()

    return error

#FUNCTION FOR DELETING AN ENTRY

def delete_entry(id):
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #deleting the title and genres that it was connected to using the id
    cur.execute("delete from anime where ID == :id", {"id": id})
    cur.execute("delete from anime_genre where animeID == :id", {"id": id})

    con.commit()

#FUNCTION FOR ENTERING A NEW GENRE

def new_genre(name):
    #boolean variable that only becomes true when the inserted title from the form is already in the database
    check = False

    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #select all genres
    cur.execute("select genre from genres")
    rows = cur.fetchall()

    #capitalizing the first letter of each word in the anime title and comparing with existing titles
    name = name.title()
    for row in rows:
        if name in row:
            check = True
            break

    if check == False:
        cur.execute("insert into genres(genre) values(:name)", {"name": name})
        con.commit()

    return check

#FUNCTION THAT PICKS A RANDOM NUMBER IN THE RANGE BETWEEN ONE AND THE NUMBER OF GENRES IN THE DATABASE
def random_num():
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #select the last ID
    cur.execute("select max(id) from genres")
    rows = cur.fetchone()

    #we add 1 to the number because of the way the randrange function works
    #and this is stored in a separate variable for more readability i guess
    range_limit = rows[0] + 1

    #chooses a number between 1 and the number fetched from the database
    id = random.randrange(1, range_limit)
    return id

#FUNCTION THAT SELECTS THE ANIME FOR THE MAIN PAGE FOR THE RANDOM GENRE
#ID IS THE RANDOM NUMBER FROM THE random_num() FUNCTION
def random_id(id):
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #same command from line 11 but this one selects info based on genre ID
    cur.execute("""select anime.ID as ID, anime.name as anime_name, anime.numepisodes as numepisodes, anime.rating as rating, 
    genres.genre as anime_genre from anime_genre inner join anime on anime.ID = anime_genre.animeID inner join genres on genres.ID = anime_genre.genreID 
    where anime_genre.genreid = :id;""", {"id": id})
    rows = cur.fetchall()

    #if rows is empty, execute the function again but with the id lowered by 1
    #do this until a valid id is fetched
    if len(rows) == 0:
        rows = random_id(id - 1)
    return rows