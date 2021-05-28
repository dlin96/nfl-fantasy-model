import pandas as pd
import sqlalchemy
from dotenv import load_dotenv
import os
import scipy.stats as st
from src.common import skill_pos


def build_base_df():
    load_dotenv()
    db_user = os.getenv("user")
    db_pass = os.getenv("pass")
    db_port = os.getenv("port")

    # connect to nfldb
    db_uri = "postgresql://{username}:{password}@localhost:{port}/nfldb"
    engine = sqlalchemy.create_engine(
        db_uri.format(username=db_user, password=db_pass, port=db_port))
    conn = engine.connect()

    fantasy_stats = \
        """
        select g.player_id, team, season_year, full_name, position,
        games_played, total_passing_twopt, total_rushing_twopt,
        total_rushing_yds, total_rushing_tds, total_fum_lost, total_rushing_att,
        total_passing_att, total_passing_yds, total_passing_tds, total_ints,
        total_rec_yds, total_rec_tds, total_recs, total_targets
        from (select player_id, season_year, count(distinct(play_player.gsis_id)) as games_played,
            sum(passing_twoptm) as total_passing_twopt, sum(rushing_twoptm) as total_rushing_twopt,
            sum(rushing_yds) as total_rushing_yds, sum(rushing_tds) as total_rushing_tds,
            sum(receiving_yds) as total_rec_yds, sum(receiving_tds) as total_rec_tds, sum(receiving_rec) as total_recs,
            sum(passing_yds) as total_passing_yds, sum(passing_tds) as total_passing_tds,
            sum(fumbles_lost) as total_fum_lost, sum(passing_int) as total_ints,
            sum(rushing_att) as total_rushing_att,
            sum(receiving_tar) as total_targets,
            sum(passing_att) as total_passing_att
            from play_player
            join game on play_player.gsis_id = game.gsis_id 
            where season_type=\'Regular\'
            group by season_year, player_id) as g join player on player.player_id = g.player_id
            where position in {};
        """
    skill_pos_stats = fantasy_stats.format(skill_pos)

    query = conn.execute(skill_pos_stats)
    qb_agg = pd.DataFrame(query)
    qb_agg.columns = query.keys()

    # initialize tables and metadata for sqlalchemy expression language
    metadata = sqlalchemy.MetaData(bind=None)
    player = sqlalchemy.Table("player", metadata, autoload=True, autoload_with=engine)
    game = sqlalchemy.Table("game", metadata, autoload=True, autoload_with=engine)
    play_player = sqlalchemy.Table("play_player", metadata, autoload=True, autoload_with=engine)

    # calculate "big passing games" of >300 and >400 yards passing
    # TODO: >100, >200 receiving/rushing
    ypg = sqlalchemy.sql.select([player.c.player_id, game.c.season_year,
                                 sqlalchemy.func.sum(play_player.c.passing_yds).label('total_passing_yds_game')])\
        .select_from(
        game.join(play_player, game.c.gsis_id == play_player.c.gsis_id)
        .join(player, player.c.player_id == play_player.c.player_id)
    ).where(
        sqlalchemy.and_(player.c.player_id.in_(qb_agg["player_id"].unique()),
                        game.c.season_type == 'Regular'))\
        .group_by(game.c.gsis_id, game.c.season_year, player.c.player_id)

    ypg_subq = ypg.alias()
    over_300 = sqlalchemy.sql.select([
        sqlalchemy.sql.column("player_id"),
        sqlalchemy.sql.column("season_year"),
        sqlalchemy.func.count(sqlalchemy.case([
            (sqlalchemy.sql.column("total_passing_yds_game").between(300, 399), 1)
        ])).label("over_300"),
        sqlalchemy.func.count(sqlalchemy.case([
            (sqlalchemy.sql.column("total_passing_yds_game") >= 400, 1)
        ])).label("over_400")
    ])\
        .select_from(ypg_subq)\
        .group_by(sqlalchemy.sql.column("player_id"), sqlalchemy.sql.column("season_year"))

    result = conn.execute(over_300)
    big_passing_games = result.fetchall()
    big_passing_games = pd.DataFrame(big_passing_games)
    big_passing_games.columns = result.keys()

    rpg = sqlalchemy.sql.select([player.c.player_id, game.c.season_year,
                                 sqlalchemy.func.sum(play_player.c.receiving_yds).label('total_receiving_yds_game')]) \
        .select_from(game.join(play_player, game.c.gsis_id == play_player.c.gsis_id)
                     .join(player, player.c.player_id == play_player.c.player_id))\
        .where(sqlalchemy.and_(player.c.player_id.in_(qb_agg["player_id"].unique()),
                               game.c.season_type == 'Regular'))\
        .group_by(game.c.gsis_id, game.c.season_year, player.c.player_id)

    rpg_subq = rpg.alias()
    over_100 = sqlalchemy.sql.select([
        sqlalchemy.sql.column("player_id"),
        sqlalchemy.sql.column("season_year"),
        sqlalchemy.func.count(sqlalchemy.case([
            (sqlalchemy.sql.column("total_receiving_yds_game").between(100, 199), 1)
        ])).label("over_100"),
        sqlalchemy.func.count(sqlalchemy.case([
            (sqlalchemy.sql.column("total_receiving_yds_game") >= 200, 1)
        ])).label("over_200")
    ])\
        .select_from(rpg_subq)\
        .group_by(sqlalchemy.sql.column("player_id"), sqlalchemy.sql.column("season_year"))

    result = conn.execute(over_100)
    big_rec_games = result.fetchall()
    big_rec_games = pd.DataFrame(big_rec_games)
    big_rec_games.columns = result.keys()

    rupg = sqlalchemy.sql.select([player.c.player_id, game.c.season_year,
                                  sqlalchemy.func.sum(play_player.c.rushing_yds).label('total_rushing_yds_game')]) \
                         .select_from(game.join(play_player, game.c.gsis_id == play_player.c.gsis_id)
                                          .join(player, player.c.player_id == play_player.c.player_id))\
                         .where(sqlalchemy.and_(player.c.player_id.in_(qb_agg["player_id"].unique()),
                                game.c.season_type == 'Regular'))\
                         .group_by(game.c.gsis_id, game.c.season_year, player.c.player_id)

    rupg_subq = rupg.alias()
    over_100_rush = sqlalchemy.sql.select([
        sqlalchemy.sql.column("player_id"),
        sqlalchemy.sql.column("season_year"),
        sqlalchemy.func.count(sqlalchemy.case([
            (sqlalchemy.sql.column("total_rushing_yds_game").between(100, 199), 1)
        ])).label("over_100_rush"),
        sqlalchemy.func.count(sqlalchemy.case([
            (sqlalchemy.sql.column("total_rushing_yds_game") >= 200, 1)
        ])).label("over_200_rush")
    ])\
        .select_from(rupg_subq)\
        .group_by(sqlalchemy.sql.column("player_id"), sqlalchemy.sql.column("season_year"))

    result = conn.execute(over_100_rush)
    big_rush_games = result.fetchall()
    big_rush_games = pd.DataFrame(big_rush_games)
    big_rush_games.columns = result.keys()
    for extra_pts_df in [big_passing_games, big_rec_games, big_rush_games]:
        qb_agg = qb_agg.merge(extra_pts_df, on=["player_id", "season_year"])

    # 2pt pass, 2pt rush, rush yds, rush td, pass yd, pass td, fumble lost, int, >300, >400
    # TODO: >100, >200 receiving/rushing
    pt_multipliers = (2, 2, 0.1, 6, 0.1, 6, 0.04, 4, -2, -2, 1, 2)

    qb_agg["avg_fantasy"] = (qb_agg.loc[:, ("total_passing_twopt", "total_rushing_twopt",
                                            "total_rushing_yds", "total_rushing_tds",
                                            "total_rec_yds", "total_rec_tds",
                                            "total_passing_yds", "total_passing_tds", "total_fum_lost",
                                            "total_ints", "over_300", "over_400")] * pt_multipliers).sum(axis=1)\
                            / qb_agg["games_played"]

    return qb_agg


def zp_scores(position, df):
    if position not in ("QB", "RB", "WR", "TE"):
        raise ValueError("Position needs to be QB, RB, WR, or TE")
    pos_df = df.loc[df["position"] == position].sort_values(by="y", ascending=False)
    pos_df["z_score"] = (pos_df["y"] - pos_df["y"].mean()) / pos_df["y"].std()
    pos_df["p-score"] = st.norm.cdf(pos_df["z_score"])
    return pos_df.rename(columns={"y": "pred_avg_pts"})


if __name__ == '__main__':
    build_base_df().to_pickle("../../data/processed/base_fantasy_df.pkl")
