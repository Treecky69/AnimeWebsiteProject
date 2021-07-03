import sqlite3

#function to fetch the info for the table for the user side

def table_form():
    con = sqlite3.connect("anime_mock.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("""select anime.ID as ID, anime.name as anime_name, anime.numepisodes as numepisodes, anime.rating as rating, genres.genre as anime_genre from anime_genre
    inner join anime on anime.ID = anime_genre.animeID inner join genres on genres.ID = anime_genre.genreID""")

    rows = cur.fetchall()
    return rows

def id_entry(id):
    con = sqlite3.connect("anime_mock.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("""select anime.ID as ID, anime.name as anime_name, anime.numepisodes as numepisodes, anime.rating as rating, genres.genre as anime_genre from anime_genre
    inner join anime on anime.ID = anime_genre.animeID inner join genres on genres.ID = anime_genre.genreID
    where anime.ID == :id""", {"id": id})

    rows = cur.fetchall()
    return rows

#function for displaying the genres

def genre_list():
    con = sqlite3.connect("anime_mock.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from genres")
    rows = cur.fetchall()
    return rows

#class for the form request and database entry

class Database_entry:
    def __init__(self, title, NumEpisodes, rating, genres):
        self.title = title
        self.episodes = NumEpisodes
        self.rating = rating
        self.genres = genres

    def Main_data(self):
        con = sqlite3.connect("anime_mock.db")
        con.row_factory = sqlite3.Row
        #con = sqlite3.connect("anime_mock - Copy.db")
        cur = con.cursor()
        cur.execute("select name from anime")
        rows = cur.fetchall()

        #capitalizing the first letter of each word in the anime title and comparing with existing titles
        self.title = self.title.title()
        for row in rows:
            if self.title in row["name"]:
                message = "This anime is already in the database"
                return message

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
        message = "Change commited to the database"
        return message

#function for updating anime info

def update_db(id, attrib, query, genres):
    con = sqlite3.connect("anime_mock.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

#delete all the exsiting genre IDs associated with the anime ID in the anime_genre database
#then inserts the new ones

    if attrib == "genres":
        cur.execute("delete from anime_genre where animeid = :id", {"id": id})
        for genre in genres:
            cur.execute("insert into anime_genre(animeID, genreID) values(:anime_ID, :genre_ID)", {"anime_ID": int(id), "genre_ID": int(genre)})

#updates the name
    elif attrib == "name":
        query = query.title()
        cur.execute("update anime set name = :query where id == :id", {"id": id, "query": query})

#updates the number of episodes
    elif attrib == "numepisodes":
        cur.execute("update anime set numepisodes = :query where id == :id", {"id": id, "query": query})

#updates the rating
    elif attrib == "rating":
        cur.execute("update anime set rating = :query where id == :id", {"id": id, "query": query})

    con.commit()
    return "update commited"
