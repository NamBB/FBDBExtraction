SELECT GROUP_CONCAT(result,'')
FROM (SELECT CASE
                WHEN home_score > away_score
                    THEN 'W'
                WHEN home_score = away_score
                    THEN 'D'
                ELSE 'L'
            END as result, round_id
      FROM MATCH, TEAM
      WHERE (TEAM.team_id = MATCH.home_id)
            AND TEAM.name LIKE ?
      UNION
      SELECT CASE
                WHEN home_score > away_score
                    THEN 'L'
                WHEN home_score = away_score
                    THEN 'D'
                ELSE 'W'
            END as result, round_id
      FROM MATCH, TEAM
      WHERE (TEAM.team_id = MATCH.away_id)
            AND TEAM.name LIKE ?
      ORDER BY round_id DESC
      LIMIT 10)