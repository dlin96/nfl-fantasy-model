"""
Module name: feats_prod_per_pos
Author: David Lin
Purpose: feature generation of advanced statistics (those that don't have a direct
effect on the fantasy score, but could help predict next year's)
"""

def time_of_pos(): # team, season_year, season_type='regular'):
    """
    Get the average time of possession per game for given team, season year and type
    """

    # query = "select SUM(CAST(regexp_replace(CAST(pos_time as TEXT), '\(|\)', '', 'g') as INT))\
    #         as time_of_possession, a.gsis_id, result, pos_team\
    #         from (select gsis_id, season_year, season_type, home_team, away_team\
    #                     from game where (home_team='NE' or away_team='NE')\
    #                     and season_year=2009 and season_type='Regular') as a join drive\
    #                     on a.gsis_id = drive.gsis_id where pos_team='NE'\
    #                     group by a.gsis_id, pos_team, result;"
    return


def pts_per_pos(): # team, season_year, season_type='regular'):
    """
    points per possession.
    """
    return ""
