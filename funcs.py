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

#function for displaying the genres for the genre_list while entering the info for the new entry in the database

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
        #row factory didnt work for some reason
        con = sqlite3.connect("anime_mock.db")
        #con = sqlite3.connect("anime_mock - Copy.db")
        cur = con.cursor()
        cur.execute("select name from anime")
        rows = cur.fetchall()

        #capitalizing the first letter of each word in the anime title and comparing with existing titles
        self.title = self.title.title()
        for row in rows:
            if self.title in row:
                message = "This anime is already in the database"
                return message

        #inserting the title, number of episodes and rating in the anime table
        cur.execute("insert into anime(name, NumEpisodes, rating) values(:name, :episodes, :rating)", {"name": self.title, "episodes": self.episodes, "rating": self.rating})

        #fetching the ID of the newly inserted anime
        cur.execute("select id from anime where name = :title", {"title": self.title})
        IDs = cur.fetchall()
        anime_ID = IDs[0][0] #anime ID

        #inserting into the anime_genre database where the title and genres are connected
        for genre in self.genres:
            cur.execute("insert into anime_genre(animeID, genreID) values(:anime_ID, :genre_ID)", {"anime_ID": int(anime_ID), "genre_ID": int(genre)})

        # cur.execute("select * from anime_genre where animeID = :anime_ID", {"anime_ID": anime_ID})
        # test = cur.fetchall()
        # myList = []
        # for elem in test:
        #     myList.append(elem)
        # return myList

        con.commit()
        message = "Change commited to the database"
        return message