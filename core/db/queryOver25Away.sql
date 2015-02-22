Select count(*) as sub_total, total
from MATCH, TEAM
left join (Select count(*) as total
           from MATCH, TEAM
           where (MATCH.season_id = ?)
           and (TEAM.team_id = MATCH.away_id)
           and TEAM.name like ?)
where (MATCH.season_id = ?)
      and (TEAM.team_id = MATCH.away_id)
      and TEAM.name like ?
      and MATCH.home_score + MATCH.away_score > 2.5