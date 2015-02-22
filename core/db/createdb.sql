CREATE TABLE [GOAL] (
[match_id] INTEGER  NOT NULL,
[player_id] INTEGER  NOT NULL,
[side] INTEGER  NULL,
[minute] INTEGER  NOT NULL,
PRIMARY KEY ([match_id],[player_id],[side],[minute])
);

CREATE TABLE [LEAGUE] ([league_id] INTEGER PRIMARY KEY AUTOINCREMENT, [name] TEXT (50));

CREATE TABLE [MATCH] (
[match_id] INTEGER  PRIMARY KEY AUTOINCREMENT NULL,
[home_id] INTEGER  NULL,
[away_id] INTEGER  NULL,
[home_score] INTEGER  NULL,
[away_score] INTEGER  NULL,
[match_date] DATE  NULL,
[league_id] INTEGER  NULL,
[season_id] INTEGER  NULL,
[round_id] INTEGER  NULL
);

CREATE TABLE [PLAYER] (
[player_id] INTEGER  PRIMARY KEY NOT NULL,
[name] TEXT (50) DEFAULT 'null' NULL,
[team_id] INTEGER DEFAULT 'team_id' NULL
);

CREATE TABLE [ROUND] ([round_id] INTEGER PRIMARY KEY, [name] TEXT (12));

CREATE TABLE [SEASON] ([season_id] INTEGER PRIMARY KEY);

CREATE TABLE [TEAM] ([team_id] INTEGER PRIMARY KEY, [name] TEXT (50), [league_id] INTEGER REFERENCES [LEAGUE] ([league_id]));