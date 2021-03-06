PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE anime(ID integer primary key autoincrement, name text not null, NumEpisodes integer, rating real);
CREATE TABLE genres(ID integer primary key autoincrement, genre text not null);
CREATE TABLE anime_genre(animeID integer, genreID integer);
DELETE FROM sqlite_sequence;
COMMIT;