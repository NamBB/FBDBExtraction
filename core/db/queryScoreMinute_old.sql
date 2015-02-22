Select count(*) as sub_total, total
from (Select MATCH.match_id
      from MATCH, TEAM, GOAL
      where MATCH.match_id = GOAL.match_id
            and (MATCH.season_id = ?)
            and TEAM.name like ?
            and (TEAM.team_id = MATCH.home_id and GOAL.minute > ? and GOAL.minute <= ? and GOAL.side = 0)
      group by MATCH.match_id)
left join (Select count(*) as total
           from MATCH, TEAM
           where (MATCH.season_id = ?)
                  and (TEAM.team_id = MATCH.home_id)
                  and TEAM.name like ?)