import inspect
import os
from core.db import dbtool
import fbdbconfig
import mytool

__author__ = 'holynoob'

class SeasonPerformanceData(object):
    def __init__(self):
        self.total_games = 0
        self.total_score = 0
        self.total_conceded = 0
        self.total_avg_score = 0
        self.total_avg_conceded = 0
        self.list_score =[]
        self.list_avg_score = []
        self.list_conceded =[]
        self.list_avg_conceded = []


    def calculate(self):
        self.total_score = sum(self.list_score)
        self.total_avg_score = float(self.total_score) / self.total_games
        self.total_conceded = sum(self.list_conceded)
        self.total_avg_conceded = float(self.total_conceded) / self.total_games

    def toString(self):
        return str(self.total_games) + '\t' + str(self.total_score) + '\t' + str(self.total_avg_score) \
               + '\t' + str(self.total_conceded) + '\t' + str(self.total_avg_conceded)



class PredictionFBDB(object):
    def __init__(self, fbdb_config):
        self._fbdb_config = fbdb_config
        self._db = dbtool.connectDatabase(self._fbdb_config.db_path)
        self.home_perf = SeasonPerformanceData()
        self.away_perf = SeasonPerformanceData()
        self.dict_team = {}

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

        for i in range(0, len(all_team)):
            #HOME
            current_team = all_team[i][0]
            self.dict_team[current_team] = i

            score_home = self.getTotalGoalsScoreHome(current_team)
            games_home = score_home[1]
            score_home = score_home[0]
            conceded_home = self.getTotalGoalsConcededHome(current_team)[0]
            avg_score_home = float(score_home)/games_home
            avg_conceded_home = float(conceded_home)/games_home

            self.home_perf.total_games += games_home
            self.home_perf.list_score.append(score_home)
            self.home_perf.list_avg_score.append(avg_score_home)
            self.home_perf.list_conceded.append(conceded_home)
            self.home_perf.list_avg_conceded.append(avg_conceded_home)

            #AWAY
            score_away = self.getTotalGoalsScoreAway(current_team)
            games_away = score_away[1]
            score_away = score_away[0]
            conceded_away = self.getTotalGoalsConcededAway(current_team)[0]
            avg_score_away = float(score_away)/games_away
            avg_conceded_away = float(conceded_away)/games_away

            self.away_perf.total_games += games_away
            self.away_perf.list_score.append(score_away)
            self.away_perf.list_conceded.append(conceded_away)
            self.away_perf.list_avg_score.append(avg_score_away)
            self.away_perf.list_avg_conceded.append(avg_conceded_away)

            print current_team, '\t', games_home, '\t',score_home, '\t',avg_score_home, '\t',conceded_home, '\t',avg_conceded_home
            print current_team, '\t', games_away, '\t',score_away, '\t',avg_score_away, '\t',conceded_away, '\t',avg_conceded_away

        self.home_perf.calculate()
        self.away_perf.calculate()

        print 'Total Home', '\t', self.home_perf.toString()
        print 'Total Away', '\t', self.away_perf.toString()


    def predictNextGames(self):
        home_team = 'Chelsea FC'
        away_team = 'Burnley FC'

        self.calculateAvgScoredConceded()
        home_att_str = self.home_perf.list_avg_score[self.dict_team[home_team]] / self.home_perf.total_avg_score
        home_def_str = self.home_perf.list_avg_conceded[self.dict_team[home_team]] / self.home_perf.total_avg_conceded

        away_att_str = self.away_perf.list_avg_score[self.dict_team[away_team]] / self.away_perf.total_avg_score
        away_def_str = self.away_perf.list_avg_conceded[self.dict_team[away_team]] / self.away_perf.total_avg_conceded

        home_goal_exp = home_att_str * away_def_str * self.home_perf.total_avg_score
        away_goal_exp = away_att_str * home_def_str * self.away_perf.total_avg_score

        print home_att_str, home_def_str
        print away_att_str, away_def_str
        print home_goal_exp, away_goal_exp

        print "My Poisson", mytool.poisson_probability(2, home_goal_exp)
        #print "SciPy Poisson", poisson._pmf(2, home_goal_exp)



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
    x.predictNextGames()

if __name__ == '__main__':
    TestCalculate()