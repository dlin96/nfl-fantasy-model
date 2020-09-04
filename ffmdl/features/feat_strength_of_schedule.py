# import sqlalchemy

# import ffmdl.common as common

# # strength of schedule
# def get_sched(team_name, year):
#     """
#     Takes in team_name and year of season and returns query for games scheduled and scores
#     if the games have been played
#     """
#     return \
#         sqlalchemy.sql.select([sqlalchemy.column("home_team"), sqlalchemy.column("away_team"),
#                                sqlalchemy.column("home_score"), sqlalchemy.column("away_score")
#                               ])\
#         .select_from(game) \
#         .where(
#             sqlalchemy.and_(
#                 sqlalchemy.column("season_year") == year,
#                 sqlalchemy.or_(sqlalchemy.column("home_team") == team_name, \
#                                sqlalchemy.column("away_team") == team_name),
#                 sqlalchemy.column("season_type") == "Regular"
#             )
#         )


# def get_team_record(team_name, year):
#     """
#     Get the record of a specific team during a specific year (regular season only)

#     Returns wins, losses (16-wins)
#     """

#     a = get_sched(team_name, year).alias()
#     query = sqlalchemy.sql.select([
#         sqlalchemy.func.sum(
#             sqlalchemy.case([(sqlalchemy.column("winner") == team_name, 1)])
#         )
#     ]).select_from(
#         sqlalchemy.sql.select([
#             sqlalchemy.case([(a.c.home_score > a.c.away_score, sqlalchemy.column("home_team"))], \
#                             else_=sqlalchemy.column("away_team")).label("winner")
#         ])\
#         .select_from(a).alias()
#     )
#     wins = conn.execute(query).fetchall()[0][0]
#     return wins, common.TOTAL_GAMES_PER_SEASON - wins


# def team_records(season_year: int) -> dict:
#     """
#     Takes in a season year and returns a dictionary mapping teams to their records for that season
#     """

#     return {team: get_team_record(team, season_year) for team in teams}


# def get_opp_wl(team_name: str, season_year: int) -> tuple:
#     """
#     Get the total W-L record for all teams that team_name played that year.
#     """
#     result = get_sched(team_name, season_year)
#     sched = [row[0] if row[1] == team_name else row[1] for row in conn.execute(result).fetchall()]

#     season_records = team_records(season_year)

#     # TODO replace team_records_2009 with more general dataframe
#     record_totals = [i for i in zip(*[season_records[opp] for opp in sched])]
#     return record_totals[0]
