import inspect
import os
from core.db import dbtool
import fbdbconfig

__author__ = 'holynoob'

class PredictionFBDB(object):
    def __init__(self, fbdb_config):
        self._fbdb_config = fbdb_config
        self._db = dbtool.connectDatabase(self._fbdb_config.db_path)

    def calculate(self):
        pass

    def getTotalGoalsScoreHome(self, team):
        query = 'select sum(home_score), count(*) from MATCH, TEAM \
                where MATCH.home_id = TEAM.team_id and TEAM.name like ?'
        return dbtool.executeQueryFirst(self._db, query, ['%'+team+'%'])

    def getTotalGoalsScoreAway(self, team):
        query = 'select sum(away_score), count(*) from MATCH, TEAM \
                where MATCH.away_id = TEAM.team_id and TEAM.name like ?'
        return dbtool.executeQueryFirst(self._db, query, ['%'+team+'%'])

    def getTotalGoalsConcededHome(self, team):
        query = 'select sum(away_score), count(*) from MATCH, TEAM \
                where MATCH.home_id = TEAM.team_id and TEAM.name like ?'
        return dbtool.executeQueryFirst(self._db, query, ['%'+team+'%'])

    def getTotalGoalsConcededAway(self, team):
        query = 'select sum(home_score), count(*) from MATCH, TEAM \
                where MATCH.away_id = TEAM.team_id and TEAM.name like ?'
        return dbtool.executeQueryFirst(self._db, query, ['%'+team+'%'])

    def getAllTeam(self, league_name):
        query = 'select TEAM.name from TEAM, LEAGUE \
                where TEAM.league_id = LEAGUE.league_id and LEAGUE.name like ?'
        return dbtool.executeQueryAll(self._db, query, ['%'+league_name+'%'])

    def getTotalGoalsAll(self):
        pass


    def calculateAvgScoredConceded(self):
        all_team = self.getAllTeam('Premier League')
        total_games_home = 0
        total_score_home = 0
        total_conceded_home = 0
        total_avg_score_home = 0
        total_avg_conceded_home = 0
        list_score_home =[]
        list_avg_score_home = []
        list_conceded_home =[]
        list_avg_conceded_home = []

        total_games_away = 0
        total_score_away = 0
        total_conceded_away = 0
        total_avg_score_away = 0
        total_avg_conceded_home = 0
        list_score_away =[]
        list_conceded_away =[]
        list_avg_score_away = []
        list_avg_conceded_away = []

        for current_team in all_team:
            #HOME
            current_team = current_team[0]
            score_home = self.getTotalGoalsScoreHome(current_team)
            games_home = score_home[1]
            score_home = score_home[0]
            conceded_home = self.getTotalGoalsConcededHome(current_team)[0]
            avg_score_home = float(score_home)/games_home
            avg_conceded_home = float(conceded_home)/games_home

            total_games_home += games_home
            list_score_home.append(score_home)
            list_avg_score_home.append(avg_score_home)
            list_conceded_home.append(conceded_home)
            list_avg_conceded_home.append(avg_conceded_home)

            #AWAY
            score_away = self.getTotalGoalsScoreAway(current_team)
            games_away = score_away[1]
            score_away = score_away[0]
            conceded_away = self.getTotalGoalsConcededAway(current_team)[0]
            avg_score_away = float(score_away)/games_away
            avg_conceded_away = float(conceded_away)/games_away

            total_games_away += games_away
            list_score_away.append(score_away)
            list_conceded_away.append(conceded_away)
            list_avg_score_away.append(avg_score_away)
            list_avg_conceded_away.append(avg_conceded_away)

            print current_team, '\t', games_home, '\t',score_home, '\t',avg_score_home, '\t',conceded_home, '\t',avg_conceded_home

        total_score_home = sum(list_score_home)
        total_avg_score_home = float(total_score_home) / total_games_home
        total_conceded_home = sum(list_conceded_home)
        total_avg_conceded_home = float(total_conceded_home) / total_games_home

        total_score_away = sum(list_score_away)
        total_avg_score_away = float(total_score_away) / total_games_away
        total_conceded_away = sum(list_conceded_away)
        total_avg_conceded_away = float(total_conceded_away) / total_games_away

        print 'Total', '\t', total_games_home, '\t', total_score_home, '\t', total_avg_score_home, '\t', total_conceded_home, '\t', total_avg_conceded_home




class QueryFBDB (object):
    def __init__(self, fbdb_config):
        self._fbdb_config = fbdb_config
        self._db = dbtool.connectDatabase(self._fbdb_config.db_path)

    def getQueryFile(self, with_path=True):
        if with_path:
            return os.getcwd() + '/db/' + inspect.stack()[1][3] + '.sql'
        else:
            return inspect.stack()[1][3] + '.sql'

    def readQuery(self):
        query_file_path = os.getcwd() + '/db/' + inspect.stack()[1][3] + '.sql'
        file = open(query_file_path, 'r')
        return file.read()

    def runQuerySeasonTeam(self, season, team):
        query_file_path = os.getcwd() + '/db/' + inspect.stack()[1][3] + '.sql'
        file = open(query_file_path, 'r')
        query_sentence = file.read()
        return dbtool.executeQueryFirst(self._db, query_sentence,[season, "%"+team+"%", season, "%"+team+"%"])

    def runQuerySeasonTeamCategory (self, season, team, force):
        query_file_path = os.getcwd() + '/db/' + inspect.stack()[1][3] + '.sql'
        file = open(query_file_path, 'r')
        query_sentence = file.read()
        return dbtool.executeQueryFirst(self._db, query_sentence,[season, "%"+team+"%", season, "%"+team+"%"])


    def queryOver25Category (self, season, team, force):
        query_sentence = self.readQuery()
        return dbtool.executeQueryFirst(self._db, query_sentence,[force, force, season, "%"+team+"%", season, "%"+team+"%"])


    def queryOver25 (self, season, team):           return self.runQuerySeasonTeam(season, team)
    def queryUnder25 (self, season, team):          return self.runQuerySeasonTeam(season, team)
    def queryOver25Home (self, season, team):       return self.runQuerySeasonTeam(season, team)
    def queryOver25Away (self, season, team):       return self.runQuerySeasonTeam(season, team)
    def queryUnder25Home (self, season, team):      return self.runQuerySeasonTeam(season, team)
    def queryUnder25Away (self, season, team):      return self.runQuerySeasonTeam(season, team)
    def query2ndOver1st (self, season, team):       return self.runQuerySeasonTeam(season, team)
    def query1stOver2nd (self, season, team):       return self.runQuerySeasonTeam(season, team)
    def queryScoreMinute (self, season, team, m_from, m_to):
        query_sentence = self.readQuery()
        return dbtool.executeQueryFirst(self._db, query_sentence, [season, "%"+team+"%", m_from, m_to, m_from, m_to, season, "%"+team+"%"])
    def queryReceiveMinute (self, season, team, m_from, m_to):
        query_sentence = self.readQuery()
        return dbtool.executeQueryFirst(self._db, query_sentence, [season, "%"+team+"%", m_from, m_to, m_from, m_to, season, "%"+team+"%"])
    def queryGoalMinute (self, season, team, m_from, m_to):
        query_sentence = self.readQuery()
        return dbtool.executeQueryFirst(self._db, query_sentence, [season, "%"+team+"%", m_from, m_to, season, "%"+team+"%"])
    def queryPerformance (self, team):
        query_sentence = self.readQuery()
        return dbtool.executeQueryFirst(self._db, query_sentence, ["%"+team+"%", "%"+team+"%"])



    def queryMatchOver25 (self, season, team_1, team_2):
        print inspect.stack()[0][3], "\t", team_1, self.queryOver25(season, team_1), "vs", team_2, self.queryOver25(season, team_2)
    def queryMatchUnder25 (self, season, team_1, team_2):
        print inspect.stack()[0][3], "\t", team_1, self.queryUnder25(season, team_1), "vs", team_2, self.queryUnder25(season, team_2)
    def queryMatchOver25HomeAway (self, season, team_1, team_2):
        print inspect.stack()[0][3], "\t", team_1, self.queryOver25Home(season, team_1), "vs", team_2, self.queryOver25Away(season, team_2)
    def queryMatchUnder25HomeAway (self, season, team_1, team_2):
        print inspect.stack()[0][3], "\t", team_1, self.queryUnder25Home(season, team_1), "vs", team_2, self.queryUnder25Away(season, team_2)
    def queryMatchOver25Category(self, season, team_1, team_2):
        force_1 = dbtool.getTeamForce(self._db, team_1)
        force_2 = dbtool.getTeamForce(self._db, team_2)
        print inspect.stack()[0][3], "\t", team_1, self.queryOver25Category(season, team_1, force_2), "vs", team_2, self.queryOver25Category(season, team_2, force_1)

    def queryMatch2ndOver1st (self, season, team_1, team_2):
        print inspect.stack()[0][3], "\t", team_1, self.query2ndOver1st(season, team_1), "vs", team_2, self.query2ndOver1st(season, team_2)
    def queryMatch1stOver2nd (self, season, team_1, team_2):
        print inspect.stack()[0][3], "\t", team_1, self.query1stOver2nd(season, team_1), "vs", team_2, self.query1stOver2nd(season, team_2)
    def query1stScore2ndReceive (self, season, team_1, team_2):
        for m_from in [0, 15, 30, 45, 60, 75]:
            m_to = m_from + 15
            if m_to == 90:
                m_to = 100
            print inspect.stack()[0][3], "\t", team_1, self.queryScoreMinute(season, team_1, m_from, m_to), "vs", team_2, self.queryReceiveMinute(season, team_2, m_from, m_to), "\t", m_from, m_to

    def query2ndScore1stReceive (self, season, team_1, team_2):
        for m_from in [0, 15, 30, 45, 60, 75]:
            m_to = m_from + 15
            if m_to == 90:
                m_to = 100
            print inspect.stack()[0][3], "\t", team_1, self.queryReceiveMinute(season, team_1, m_from, m_to), "vs", team_2, self.queryScoreMinute(season, team_2, m_from, m_to), "\t", m_from, m_to

    def queryMatchGoalMinute (self, season, team_1, team_2):
        for m_from in [0, 15, 30, 45, 60, 75]:
            m_to = m_from + 15
            if m_to == 90:
                m_to = 100
            print inspect.stack()[0][3], "\t", team_1, self.queryGoalMinute(season, team_1, m_from, m_to), "vs", team_2, self.queryGoalMinute(season, team_2, m_from, m_to), "\t", m_from, m_to


    def queryMatchTeamPerformance (self, season, team_1, team_2):
        print inspect.stack()[0][3], "\t", team_1, self.queryPerformance(team_1);
        print inspect.stack()[0][3], "\t", team_2, self.queryPerformance(team_2);


    def queryUpNextMatches (self):
        for match in dbtool.queryUpNextMatches(self._db):
            self.queryMatchOver25("1415", match[0], match[1])
            self.queryMatchUnder25("1415", match[0], match[1])
            self.queryMatchOver25HomeAway("1415", match[0], match[1])
            self.queryMatchUnder25HomeAway("1415", match[0], match[1])
            self.queryMatch2ndOver1st("1415", match[0], match[1])
            self.queryMatch1stOver2nd("1415", match[0], match[1])
            self.query1stScore2ndReceive("1415", match[0], match[1])
            self.query2ndScore1stReceive("1415", match[0], match[1])
            self.queryMatchGoalMinute("1415", match[0], match[1])
            self.queryMatchTeamPerformance("1415", match[0], match[1])

    def queryUpNextMatchesTest (self):
        for match in dbtool.queryUpNextMatches(self._db):
            self.queryMatchOver25Category("1415", match[0], match[1])


def TestCalculate():
    x = PredictionFBDB(fbdbconfig.FBDBConfig('fbdb.conf'))
    x.calculateAvgScoredConceded()

if __name__ == '__main__':
    TestCalculate()