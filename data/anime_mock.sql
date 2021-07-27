PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE anime(ID integer primary key autoincrement, name text not null, NumEpisodes integer, rating real);
CREATE TABLE genres(ID integer primary key autoincrement, genre text not null);
CREATE TABLE anime_genre(animeID integer, genreID integer);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('anime',8);
INSERT INTO sqlite_sequence VALUES('genres',9);
COMMIT;
