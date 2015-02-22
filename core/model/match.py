import time


__author__ = 'holynoob'


class Goal(object):
    def __init__(self):
        pass
    def __init__(self, scorer, minute, own_goal=False):
        self.player = scorer
        self.minute = minute
        self.own_goal = own_goal

    def toConsole(self):
        print self.scorer + " " + str(self.minute)



class MatchDetail(object):

    def __init__(self, home, away, result, result_1st, match_date, league_id, season, round):
        self.home = home
        self.away = away
        try:
            self.home_score = result.split(':')[0]
            self.away_score = result.split(':')[1]
            self.home_score_1st = result_1st.split(':')[0]
            self.away_score_1st = result_1st.split(':')[1]
        except:
            self.home_score = ""
            self.away_score = ""
            self.home_score_1st =""
            self.away_score_1st = ""

        self.match_date = match_date

        self.league_id = league_id
        self.season_id = season
        self.round = round

        self.l_goal = []


    def addGoal(self, scorer, side, minute):
        self.l_goal.append([scorer, side, minute])


    def toConsole(self):
        print self.home + " " + self.home_score + ":" + self.away_score + " " + self.away + " " + time.strftime("%Y-%m-%d", self.match_date) + " " + self.round + " " + self.season_id
        for goal in self.l_goal:
            print goal