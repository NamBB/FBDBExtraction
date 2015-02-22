ManCity hay ghi bàn sau phut 75: 34/53 tran (2 muà giai gan nhat) và 10/15 trong mua 2014/2015
ManCity tren 2.5 bàn: 34/53 tran, 9/15 trong muà 2014/2015

(kha stable)
MU tren 2.5 bàn: 10/15 trong muà 2014/2015
Liverpool tren 2.5 bàn: 9/15 trong muà 2014/2015

ManCity tren 2.5 bàn: 9/15 trong muà 2014/2015
  sau 75: 9/15
Leicester tren 2.5 bàn: 6/15
  sau 75: 6/15

Swansea 8/15
Tottenham 10/15

Chelsea 9/15
  ghi bàn sau 75: 10/15
Hull 7/15


SELECT CASE
          WHEN home_score > away_score
              THEN 'W'
          WHEN home_score = away_score
              THEN 'D'
          ELSE 'L'
      END as result, "home" as side, round_id
FROM MATCH, TEAM
WHERE (TEAM.team_id = MATCH.home_id)
      AND TEAM.name LIKE ?
UNION
SELECT CASE
          WHEN home_score < away_score
              THEN 'W'
          WHEN home_score = away_score
              THEN 'D'
          ELSE 'W'
      END as result, "away" as side, round_id
FROM MATCH, TEAM
WHERE (TEAM.team_id = MATCH.away_id)
      AND TEAM.name LIKE ?
ORDER BY round_id DESC
LIMIT 10


// hiep 2 nhieu ban hon hiep 1
Select count(*) as sub_total, total
from    (Select MATCH.match_id
        from MATCH, TEAM
        where (MATCH.season_id = "1415")
            and (TEAM.team_id = MATCH.home_id or TEAM.team_id = MATCH.away_id)
            and TEAM.name like "%Manchester City%"
            and home_score - home_score_1st + away_score - away_score_1st > home_score_1st + away_score_1st
        group by MATCH.match_id)
left join   (Select count(*) as total
            from MATCH, TEAM
            where (MATCH.season_id = "1415")
                and (TEAM.team_id = MATCH.home_id or TEAM.team_id = MATCH.away_id)
                and TEAM.name like "%Manchester City%")



// so ban thang hiep 1 be hon 1.5
Select count(*) as sub_total, total
from (Select MATCH.match_id
      from MATCH, TEAM, GOAL
      where MATCH.match_id = GOAL.match_id
            and (MATCH.season_id = "1415")
            and (TEAM.team_id = MATCH.home_id or TEAM.team_id = MATCH.away_id)
            and TEAM.name like "%Manchester City%"
            and home_score_1st + away_score_1st < 1.5
      group by MATCH.match_id)
left join (Select count(*) as total
           from MATCH, TEAM
           where (MATCH.season_id = "1415")
                  and (TEAM.team_id = MATCH.home_id or TEAM.team_id = MATCH.away_id)
                  and TEAM.name like "%Manchester City%")


// so ban thang hiep 1 be hon 1.5
Select count(*) as sub_total, total
from (Select MATCH.match_id
      from MATCH, TEAM, GOAL
      where MATCH.match_id = GOAL.match_id
            and (MATCH.season_id = "1415")
            and (TEAM.team_id = MATCH.home_id or TEAM.team_id = MATCH.away_id)
            and TEAM.name like "%Manchester City%"
            and home_score - home_score_1st + away_score - away_score_1st < 1.5
      group by MATCH.match_id)
left join (Select count(*) as total
           from MATCH, TEAM
           where (MATCH.season_id = "1415")
                  and (TEAM.team_id = MATCH.home_id or TEAM.team_id = MATCH.away_id)
                  and TEAM.name like "%Manchester City%")


Select count(*) as sub_total, total
from MATCH, TEAM
left join (Select count(*) as total
           from MATCH, TEAM
           where (MATCH.season_id = "1415")
           and (TEAM.team_id = MATCH.home_id)
           and TEAM.name like "%Manchester City%")
where (MATCH.season_id = "1415")
      and (TEAM.team_id = MATCH.home_id)
      and TEAM.name like "%Manchester City%"
      and MATCH.home_score + MATCH.away_score > 2.5


Select count(*) as sub_total, total
from (Select MATCH.match_id
      from MATCH, TEAM, GOAL
      where MATCH.match_id = GOAL.match_id
            and (MATCH.season_id = "1415")
            and TEAM.name like "%Manchester City%"
            and ((TEAM.team_id = MATCH.home_id and GOAL.minute >= 0 and GOAL.minute<=15 and GOAL.side = 0)
                or (TEAM.team_id = MATCH.away_id and GOAL.minute >= 0 and GOAL.minute<=15 and GOAL.side = 1))
      group by MATCH.match_id)
left join (Select count(*) as total
           from MATCH, TEAM
           where (MATCH.season_id = "1415")
                  and (TEAM.team_id = MATCH.home_id or TEAM.team_id = MATCH.away_id)
                  and TEAM.name like "%Manchester City%")



Select count(*) as sub_total, total
from (Select MATCH.match_id
      from MATCH, TEAM, GOAL
      where MATCH.match_id = GOAL.match_id
            and (MATCH.season_id = "1415")
            and TEAM.name like "%Manchester City%"
            and (TEAM.team_id = MATCH.home_id or TEAM.team_id = MATCH.away_id)
            and GOAL.minute >= 0 and GOAL.minute<=15
      group by MATCH.match_id)
left join (Select count(*) as total
           from MATCH, TEAM
           where (MATCH.season_id = "1415")
                  and (TEAM.team_id = MATCH.home_id or TEAM.team_id = MATCH.away_id)
                  and TEAM.name like "%Manchester City%")



Select count(*) as sub_total, total
from MATCH, TEAM
left join (Select count(*) as total
           from MATCH, TEAM
           where (MATCH.season_id = "1415" or MATCH.season_id = "1314")
           and (TEAM.team_id = MATCH.home_id or TEAM.team_id = MATCH.away_id)
           and TEAM.name like "%Manchester City%")
where (MATCH.season_id = "1415" or MATCH.season_id = "1314")
      and (TEAM.team_id = MATCH.home_id or TEAM.team_id = MATCH.away_id)
      and TEAM.name like "%Manchester City%"
      and MATCH.home_score + MATCH.away_score >=3




Select TEAM1.name, TEAM2.name
from UPNEXT
left join TEAM as TEAM1, TEAM as TEAM2
on (TEAM1.team_id = UPNEXT.home_id)
      and (TEAM2.team_id = UPNEXT.away_id)