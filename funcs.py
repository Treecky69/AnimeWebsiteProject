import sqlite3

def table_form():
    con = sqlite3.connect("anime_mock.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""select anime.ID as ID, anime.name as anime_name, anime.numepisodes as numepisodes, anime.rating as rating, genres.genre as anime_genre from anime_genre
    inner join anime on anime.ID = anime_genre.animeID inner join genres on genres.ID = anime_genre.genreID""")
    rows = cur.fetchall()
    return rows

def genre_list():
    con = sqlite3.connect("anime_mock.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from genres")
    rows = cur.fetchall()
    return rows