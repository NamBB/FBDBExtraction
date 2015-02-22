__author__ = 'holynoob'

import dbtool


class TransactionFBDB (object):
    def __init__(self, db_path):
        self._db = dbtool.connectDatabase(db_path)


    def searchTeam (self, team_name):
        with dbtool.cursor(self._db) as cur:
            cur.execute('select team_id from TEAM where name = ?', (team_name,))
            return cur.fetchone()

    def searchLeague (self, league_name):
        with dbtool.cursor(self._db) as cur:
            cur.execute('select league_id from LEAGUE where name = ?', (league_name,))
            return cur.fetchone()