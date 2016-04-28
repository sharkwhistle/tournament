#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches;")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""

    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players;")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""

    db = connect()
    c = db.cursor()
    c.execute("SELECT COUNT(player_id) FROM players;")
    rows = c.fetchall()
    db.close()
    return int(rows[0][0])

def registerPlayer(name):
    """Adds a player to the tournament database."""

    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)",(name,))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins."""

    db = connect()
    c = db.cursor()
    c.execute("SELECT player_id, name, wins, matches FROM standings ORDER BY \
    wins DESC;")
    rows = c.fetchall()
    db.close()
    return rows

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players."""

    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO matches (player1,player2, result) VALUES(%s, %s, 1)",
    (winner, loser,))
    c.execute("INSERT INTO matches (player1,player2, result) VALUES(%s, %s, 0)",
    (loser, winner))
    db.commit()
    db.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match."""

    db = connect()
    c = db.cursor()
    c.execute("SELECT player_id, wins FROM standings ORDER BY wins DESC;")
    rows = c.fetchall()
    db.close()
    i=0
    pairings = []
    while i < len(rows):
        id1 = rows[i][0]
        name1 = rows[i][1]
        id2 = rows[i+1][0]
        name2 = rows[i+1][1]
        pairings.append((id1,name1,id2,name2))
        i = i+2

    return pairings
