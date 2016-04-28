-- Table definitions for the tournament project.
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

/* These lines will drop the DATABASE, any TABLES and/or VIEWS if they have
already been created*/
DROP DATABASE IF EXISTS tournament;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS matches;
DROP VIEW IF EXISTS match_count;
DROP VIEW IF EXISTS wins;
DROP VIEW IF EXISTS standings;

-- This will create our DATABASE
CREATE DATABASE tournament;

\c tournament;

/*This query will create a TABLE in our DATABASE for players who will
participate in our tournament*/
CREATE TABLE players (
	player_id serial PRIMARY KEY,
	name varchar(255)
);

/*This query will create a TABLE in our DATABASE to keep track of player
matches in our tournament*/
CREATE TABLE matches (
	match_id serial PRIMARY KEY,
	player1 int REFERENCES players(player_id),
	player2 int REFERENCES players(player_id),
	result int
);

/*This query will create a VIEW to keep track of matches that take place
between players in our tournament*/
CREATE VIEW match_count AS
	SELECT players.player_id, COUNT(matches.player2) AS n
	FROM players
	LEFT JOIN matches ON players.player_id = matches.player1
	GROUP BY players.player_id;

/*This query will create a VIEW to keep track of player match wins*/
CREATE VIEW wins AS
	SELECT players.player_id, COUNT(matches.player2) AS n
	FROM players
	LEFT JOIN (SELECT * FROM matches where result > 0) as matches
	ON players.player_id = matches.player1
	GROUP BY players.player_id;

/*This query will create a VIEW to keep track of player tournament standings
(i.e. wins and losses)*/
CREATE VIEW standings AS
	SELECT players.player_id, players.name, wins.n AS wins, match_count.n as matches
	FROM players, match_count, wins
	WHERE players.player_id = wins.player_id AND wins.player_id = match_count.player_id;
