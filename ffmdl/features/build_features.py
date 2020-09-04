"""
Module name: build_features.py
Author: David Lin
Purpose: Build features describing player for model training.
"""

import os
import pandas as pd
import sqlalchemy
from dotenv import load_dotenv
from ffmdl.common import skill_pos


def build_base_df():
    """
    Build a base dataframe of players by stats that directly contribute to fantasy score.
    """

    load_dotenv(".env")
    db_user = os.getenv("PG_USER")
    db_pass = os.getenv("NFLDB_PASSWORD")
    db_port = os.getenv("PORT")

    # connect to nfldb
    db_uri = "postgresql://{username}:{password}@{host}:{port}/nfldb"
    engine = sqlalchemy.create_engine(
        db_uri.format(username=db_user, password=db_pass, host='localhost', port=db_port))
    conn = engine.connect()

    # fantasy_stats = \
    #     """
    #     select g.player_id, team, season_year ,full_name, position,
    #     games_played, total_passing_twopt, total_rushing_twopt,
    #     total_rushing_yds, total_rushing_tds, total_fum_lost, total_rushing_att,
    #     total_passing_att, total_passing_yds, total_passing_tds, total_ints,
    #     total_rec_yds, total_rec_tds, total_recs, total_targets
    #     from (select player_id, season_year, count(distinct(play_player.gsis_id)) as games_played,
    #         sum(passing_twoptm) as total_passing_twopt, sum(rushing_twoptm) as total_rushing_twopt,
    #         sum(rushing_yds) as total_rushing_yds, sum(rushing_tds) as total_rushing_tds,
    #         sum(receiving_yds) as total_rec_yds, sum(receiving_tds) as total_rec_tds,
    #         sum(receiving_rec) as total_recs,
    #         sum(passing_yds) as total_passing_yds, sum(passing_tds) as total_passing_tds,
    #         sum(fumbles_lost) as total_fum_lost, sum(passing_int) as total_ints,
    #         sum(rushing_att) as total_rushing_att,
    #         sum(receiving_tar) as total_targets,
    #         sum(passing_att) as total_passing_att
    #         from play_player
    #         join game on play_player.gsis_id = game.gsis_id
    #         where season_type=\'Regular\'
    #         group by season_year, player_id) as g join player on player.player_id = g.player_id
    #         where position in {};
    #     """
    # skill_pos_stats = fantasy_stats.format(skill_pos)

    fantasy_stats = \
        """
        select g.player_id, team, season_year ,full_name, position,
        games_played, 
        total_rushing_twopt,
        total_rushing_yds,
        total_rushing_tds,
        total_fum_lost,
        total_rushing_att
        from (select player_id, season_year, count(distinct(play_player.gsis_id)) as games_played,
            sum(rushing_twoptm) as total_rushing_twopt,
            sum(rushing_yds) as total_rushing_yds, 
            sum(rushing_tds) as total_rushing_tds,
            sum(fumbles_lost) as total_fum_lost,
            sum(rushing_att) as total_rushing_att
            from play_player
            join game on play_player.gsis_id = game.gsis_id
            where season_type=\'Regular\'
            group by season_year, player_id) as g join player on player.player_id = g.player_id
            where position = \'{}\';
        """
    skill_pos_stats = fantasy_stats.format("RB")

    query = conn.execute(skill_pos_stats)
    agg_stats = pd.DataFrame(query)
    agg_stats.columns = query.keys()

    return agg_stats


def save_df(output_dir, fname, dataframe):
    output_loc = "/".join([output_dir, fname])
    print(f"Saving to {output_loc}")
    dataframe.to_csv(output_loc)


def build_features():
    """
    This is a convenience function to build a full-features dataframe. It will be a pipeline
    serving the base DF into the functions to generate the calculated features. Right now,
    it does the same thing as building the base DF.
    """
    output_dir = "data/interim"
    output_filename = "base_fantasy_df.csv"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    save_df(output_dir, output_filename, build_base_df())
