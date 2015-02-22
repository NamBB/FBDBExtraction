__author__ = 'holynoob'

from lxml import html
import time
import requests
from db import dbtool
import fbdbconfig
from model import match
import queryfbdb


class TransferMarktDriver(object):

    def __init__(self, fbdb_config, season):
        self._fbdb_config = fbdb_config

        self._current_league_id = 1
        self._current_season = season
        self._current_league_name = ''

        self._db = dbtool.connectDatabase(self._fbdb_config.db_path)
        print self._fbdb_config.db_path


    #minute: dong = 252 ==>  71-80
    #khoang cach cac dong = 36
    #khoang cach cac cot = 36
    #cot va dong dau tien = 0
    def __convertPositionToMinute (self, col, row):
        return (row / 36) * 10 + (col / 36) + 1



    def test(self, web):
        print self._fbdb_config.db_path


    #----------------------------------------------------------
    # parse page like this http://www.transfermarkt.co.uk/spielbericht/index/spielbericht/2486613
    #----------------------------------------------------------
    def parseMatchDetail (self, web):
        try:
            print web
            page = requests.get(web)
            root = html.document_fromstring(page.text)

            #match summary
            summary = root.xpath("//div[@class='box-content']")[0]
            home = summary.xpath(".//div[@class='sb-team sb-heim hide-for-small']/a")[0].get("title")
            away = summary.xpath(".//div[@class='sb-team sb-gast hide-for-small']/a")[0].get("title")
            round = summary.xpath(".//p[@class='sb-datum show-for-small']//text()")
            result = summary.xpath(".//div[@class='sb-endstand']//text()")[0].strip()
            result_1st = summary.xpath(".//div[@class='sb-halbzeit']")[0].text_content()[1:-1]

            # home, away, result, match_date, league_id, season, round
            match_detail = match.MatchDetail(home, away, result, result_1st, time.strptime(round[1], "%b %d, %Y"), self._current_league_id, self._current_season, round[0].split('.')[0])

            # parse goals
            if result != '0:0' :
                l_detail = root.xpath("//div[@class='row']/div[@class='twelve columns']/div[@class='box']")

                l_goal = l_detail[2].xpath(".//div[@class='sb-aktion-aktion']")
                l_minute = l_detail[2].xpath(".//span[@class='sb-sprite-uhr-klein']")
                l_side = l_detail[2].xpath(".//div[@class='sb-aktion-wappen']")

                for i in xrange(len(l_goal)):
                    scorer = l_goal[i].xpath(".//a")[0].text
                    colrow = l_minute[i].get("style")[22:-1].replace('-','').replace('px','').split(' ')
                    side = l_side[i].xpath(".//a")[0].get("title")
                    score_minute = self.__convertPositionToMinute(int(colrow[0]), int(colrow[1]))
                    #side = 0: home  1: away  2:home own  3:away own
                    is_own = ("Own-goal" in l_goal[i].text_content()) * 2
                    #match_detail.addGoal(scorer, (side!=home) + is_own, score_minute)
                    if (side == home):
                        match_detail.addGoal(scorer, 0 + is_own, score_minute)
                    else:
                        match_detail.addGoal(scorer, 1 + is_own, score_minute)

            match_detail.toConsole()
            dbtool.archiveMatch(self._db, match_detail)

            return match_detail

        except Exception as e:
            print e.message
            return None


    #----------------------------------------------------------
    # parse page like this http://www.transfermarkt.co.uk/premier-league/gesamtspielplan/wettbewerb/GB1?saison_id=2014&spieltagVon=21&spieltagBis=21
    #----------------------------------------------------------
    def parseSeasonFixture (self, web):
        try:
            #file = open('x.txt', 'r')
            #page = file.read()
            #root = html.document_fromstring(page)

            #get season number by last two digits of link
            #digit = int(web[:2])
            #print (digit * 100) + digit + 1

            #get page content
            page = requests.get(web)
            root = html.document_fromstring(page.text)

            #get current league
            self._current_league_name = root.xpath("//div[@class='spielername-profil']")[0].text.strip()
            self._current_league_id = dbtool.archiveLeague(self._db, self._current_league_name)

            #for each round of season, find match link and parse
            round_wrappers = root.xpath("//div[@class='six columns']")
            for round in round_wrappers:
                round_no = round.xpath(".//div[@class='table-header']")
                print round_no[0].text

                match_list = round.xpath(".//table/tbody/tr")
                for match in match_list:
                    try:
                        match_link = "http://www.transfermarkt.co.uk" + match.xpath(".//a[starts-with(@title,'Match')]")[0].get("href")
                        self.parseMatchDetail(match_link)
                    except Exception, e:
                        print e

                    #match_info = match.xpath(".//td//text()")
                    # Match info are under format like this
                    #['\n\t\t\t\t\tSat\t\t\t\t\t', 'Aug 18, 2012', ' \n\t\t\t\t', '\t\n\t\t\t\t\t4:00 PM\t\t\t\t', 'QPR', u'\xa0', '0:5', u'\xa0', 'Swansea City']
                    #from Match day 2, there are some columns more (indicate the current position of team) ==> len = 12 or 13
                    #print match_info

        except Exception as e:
            print "Exception " + e.message



    def parseNextMatchDetail (self, web):
        try:
            print web
            page = requests.get(web)
            root = html.document_fromstring(page.text)

            #match summary
            summary = root.xpath("//div[@class='box-content']")[0]
            home = summary.xpath(".//div[@class='sb-team sb-heim hide-for-small']/a")[0].get("title")
            away = summary.xpath(".//div[@class='sb-team sb-gast hide-for-small']/a")[0].get("title")
            round = summary.xpath(".//p[@class='sb-datum show-for-small']//text()")

            next_match_detail = match.MatchDetail(home, away, "", "", time.strptime(round[1], "%b %d, %Y"), self._current_league_id, self._current_season, round[0].split('.')[0])

            dbtool.archiveNextMatch(self._db, next_match_detail)

            return next_match_detail

        except Exception as e:
            print e.message
            return None

    #----------------------------------------------------------
    # parse page like this http://www.transfermarkt.co.uk/premier-league/gesamtspielplan/wettbewerb/GB1?saison_id=2014&spieltagVon=21&spieltagBis=21
    #----------------------------------------------------------
    def parseNextFixture (self, web):
        try:
            #get page content
            page = requests.get(web)
            root = html.document_fromstring(page.text)

            #get current league
            self._current_league_name = root.xpath("//div[@class='spielername-profil']")[0].text.strip()
            self._current_league_id = dbtool.archiveLeague(self._db, self._current_league_name)

            #for each round of season, find match link and parse
            round_wrappers = root.xpath("//div[@class='six columns']")
            for round in round_wrappers:
                round_no = round.xpath(".//div[@class='table-header']")
                print round_no[0].text

                match_list = round.xpath(".//table/tbody/tr")
                for match in match_list:
                    match_link = "http://www.transfermarkt.co.uk" + match.xpath(".//a[@title='Match preview']")[0].get("href")
                    self.parseNextMatchDetail(match_link)

                    #match_info = match.xpath(".//td//text()")
                    # Match info are under format like this
                    #['\n\t\t\t\t\tSat\t\t\t\t\t', 'Aug 18, 2012', ' \n\t\t\t\t', '\t\n\t\t\t\t\t4:00 PM\t\t\t\t', 'QPR', u'\xa0', '0:5', u'\xa0', 'Swansea City']
                    #from Match day 2, there are some columns more (indicate the current position of team) ==> len = 12 or 13
                    #print match_info

        except Exception as e:
            print "Exception " + e.message





def ParsePremier():
    fbdb_config = fbdbconfig.FBDBConfig('fbdb.conf')
    x = TransferMarktDriver(fbdb_config, '1415')
    web = 'http://www.transfermarkt.co.uk/premier-league/gesamtspielplan/wettbewerb/GB1/saison_id/2014'
    premier = 'http://www.transfermarkt.co.uk/premier-league/gesamtspielplan/wettbewerb/GB1?saison_id=2014&spieltagVon=24&spieltagBis=24'
    x.parseSeasonFixture(premier)


def ParseItaly():
    fbdb_config = fbdbconfig.FBDBConfig('fbdb.conf')
    x = TransferMarktDriver(fbdb_config, '1415')
    italy = 'http://www.transfermarkt.co.uk/serie-a/gesamtspielplan/wettbewerb/IT1?saison_id=2014&spieltagVon=22&spieltagBis=22'
    x.parseSeasonFixture(italy)


def ParseMatch():
    x = TransferMarktDriver(fbdbconfig.FBDBConfig('fbdb.conf'), '1415')
    web = 'http://www.transfermarkt.co.uk/spielbericht/index/spielbericht/2478801'
    x.parseMatchDetail(web)

def ParseNextFixture():
    fbdb_config = fbdbconfig.FBDBConfig('fbdb.conf')
    x = TransferMarktDriver(fbdb_config, '1415')
    web = 'http://www.transfermarkt.co.uk/premier-league/gesamtspielplan/wettbewerb/GB1?saison_id=2014&spieltagVon=25&spieltagBis=25'
    italy = 'http://www.transfermarkt.co.uk/serie-a/gesamtspielplan/wettbewerb/IT1?saison_id=2014&spieltagVon=22&spieltagBis=22'
    #web = 'http://www.transfermarkt.co.uk/spielbericht/index/spielbericht/2486685'
    x.parseNextFixture(web)
    #x.parseNextFixture(italy)


def QueryNextFixture():
    x = queryfbdb.QueryFBDB(fbdbconfig.FBDBConfig('fbdb.conf'))
    print x.queryUpNextMatches()



def ExecuteQuery():
    x = queryfbdb.QueryFBDB(fbdbconfig.FBDBConfig('fbdb.conf'))
    x.queryMatchOver25("1415", "Chelsea", "Swansea")


def Test ():
    fbdb_config = fbdbconfig.FBDBConfig('fbdb.conf')
    x = TransferMarktDriver(fbdb_config, '1415')
    web = 'http://www.transfermarkt.co.uk/spielbericht/index/spielbericht/2486613'
    x.parseMatchDetail(web)

if __name__ == '__main__':
    #ParseNextFixture()
    #ParsePremier()
    #ParseItaly()
    QueryNextFixture()