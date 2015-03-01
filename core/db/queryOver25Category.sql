Select count(*) as sub_total, total
from MATCH, TEAM as TEAM1, (Select * from TEAM where force=?) as TEAM2
left join (Select count(*) as total
           from MATCH, TEAM as TEAM1, (Select * from TEAM where force=?) as TEAM2
           where (MATCH.season_id = ?)
           and TEAM1.name like ?
           and ((TEAM1.team_id = MATCH.home_id and TEAM2.team_id = MATCH.away_id)
                  or
                 (TEAM1.team_id = MATCH.away_id and TEAM2.team_id = MATCH.home_id))
           )
where (MATCH.season_id = ?)
      and TEAM1.name like ?
      and ((TEAM1.team_id = MATCH.home_id and TEAM2.team_id = MATCH.away_id)
            or
            (TEAM1.team_id = MATCH.away_id and TEAM2.team_id = MATCH.home_id))
      and MATCH.home_score + MATCH.away_score > 2.5