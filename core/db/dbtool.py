import sqlite3
import time
from contextlib import contextmanager

__author__ = 'holynoob'


#====================================================================================
# CURSOR CONTEXT
#====================================================================================
@contextmanager
def cursor(db):
    try:
        cur = db.cursor()
        yield(cur)
    except:
        db.rollback()
        raise
    finally:
        cur.close()



def commitData (db):
    pass


def connectDatabase(db_path):
    return sqlite3.connect(db_path)

def createDatabase ():
    DB = sqlite3.connect("../db/fbdata_sample.db", 10)
    pass


def executeQueryFirst(db, sentence, listParam):
    with cursor(db) as cur:
        cur.execute(sentence, listParam)
        query_result = cur.fetchone()
        return query_result


def searchTeam (db, team_name):
    with cursor(db) as cur:
        cur.execute('select team_id from TEAM where name = ?', (team_name,))
        return cur.fetchone()


def searchLeague (db, league_name):
    with cursor(db) as cur:
        cur.execute('select league_id from LEAGUE where name = ?', (league_name,))
        return cur.fetchone()



def archiveTeam (db, team_name):
    with cursor(db) as cur:
        cur.execute('select team_id from TEAM where name = ?', (team_name,))
        team = cur.fetchone()
        if team == None:
            cur.execute('insert into TEAM (name) values (?)', (team_name,))
            db.commit()
            return cur.lastrowid
        else:
            return team[0]

def updateTeamForce (db, team_name, force_value):
    with cursor(db) as cur:
        cur.execute('update TEAM set force=? where name = ?', (force_value, team_name,))
        db.commit()

def getTeamForce (db, team_name):
    with cursor(db) as cur:
        cur.execute('select force from TEAM where name = ?', (team_name,))
        force = cur.fetchone()
        return force[0]


def archiveLeague (db, league_name):
    with cursor(db) as cur:
        cur.execute('select league_id from LEAGUE where name = ?', (league_name,))
        league = cur.fetchone()
        if league == None:
            cur.execute('insert into LEAGUE (name) values (?)', (league_name,))
            db.commit()
            return cur.lastrowid
        else:
            return league[0]


def archivePlayer (db, player_name, team_id):
    with cursor(db) as cur:
        cur.execute('select player_id from PLAYER where name = ?', (player_name,))
        player = cur.fetchone()
        if player == None:
            cur.execute('insert into PLAYER (name, team_id) values (?, ?)', (player_name, team_id))
            db.commit()
            return cur.lastrowid
        else:
            return player[0]


def archiveGoal (db, match, goal):
    if goal[1] == 0 or goal[1] == 3:
        player_id = archivePlayer(db, goal[0], match.home_id)
    else:
        player_id = archivePlayer(db, goal[0], match.away_id)

    #id, player, side, minute
    with cursor(db) as cur:
        cur.execute('insert into GOAL values(?, ?, ?, ?)', (match.match_id, player_id, goal[1], goal[2]))
        db.commit()



def archiveMatch (db, match):
    match.home_id = archiveTeam(db, match.home)
    match.away_id = archiveTeam(db, match.away)

    with cursor(db) as cur:
        cur.execute('insert into MATCH (home_id, away_id, home_score, away_score, home_score_1st, away_score_1st, match_date, league_id, season_id, round_id) '\
                    'values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (match.home_id, match.away_id, match.home_score, match.away_score, match.home_score_1st, match.away_score_1st, time.strftime("%Y-%m-%d", match.match_date), match.league_id, match.season_id, match.round)
                    )
        db.commit()
        match.match_id = cur.lastrowid

    #print "Archive goal "
    for goal in match.l_goal:
        #print goal
        archiveGoal(db, match, goal)


def archiveNextMatch (db, next_match):
    next_match.home_id = archiveTeam(db, next_match.home)
    next_match.away_id = archiveTeam(db, next_match.away)


    with cursor(db) as cur:
        cur.execute('insert into UPNEXT (home_id, away_id, match_date, league_id, season_id, round_id) '\
                    'values (?, ?, ?, ?, ?, ?)',
                    (next_match.home_id, next_match.away_id, time.strftime("%Y-%m-%d", next_match.match_date), next_match.league_id, next_match.season_id, next_match.round)
                    )
        db.commit()



def queryUpNextMatches (db):
    with cursor(db) as cur:
        cur.execute('Select TEAM1.name, TEAM2.name, UPNEXT.league_id, UPNEXT.round_id, UPNEXT.Match_date '
                    'from UPNEXT '
                    'left join TEAM as TEAM1, TEAM as TEAM2 '
                    'on (TEAM1.team_id = UPNEXT.home_id)'
                    '    and (TEAM2.team_id = UPNEXT.away_id)')
        return cur.fetchall()