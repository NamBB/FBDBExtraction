Select count(*) as sub_total, total
from    (Select MATCH.match_id
        from MATCH, TEAM
        where (MATCH.season_id = ?)
            and (TEAM.team_id = MATCH.home_id or TEAM.team_id = MATCH.away_id)
            and TEAM.name like ?
            and home_score - home_score_1st + away_score - away_score_1st < home_score_1st + away_score_1st
        group by MATCH.match_id)
left join   (Select count(*) as total
            from MATCH, TEAM
            where (MATCH.season_id = ?)
                and (TEAM.team_id = MATCH.home_id or TEAM.team_id = MATCH.away_id)
                and TEAM.name like ?)