"""
filename: inference.py
author: David Lin
"""

import click
from joblib import load
import os
import pandas as pd
from sklearn.metrics import mean_squared_error

from ffmdl.common import get_logger


logger = get_logger(__name__)


def zp_scores(position, stats_df):
    """
    fn_name: zp_scores
    purpose: to calculate the z-scores and p-values of players. Z-scores represent how far they
    are from their position mean, and p-values should indicate how statistically significant it is.
    """
    if position not in ("QB", "RB", "WR", "TE"):
        raise ValueError("Position needs to be QB, RB, WR, or TE")
    pos_df = stats_df.loc[stats_df["position"] == position].sort_values(by="y", ascending=False)
    pos_df["z_score"] = (pos_df["y"] - pos_df["y"].mean()) / pos_df["y"].std()
    return pos_df


# pylint: disable=no-value-for-parameter
@click.command()
@click.option("--model-dir", default="models/trained_models")
@click.option("--model-name", default="lin_reg")
@click.option("--output-dir", default="output")
def inference(model_dir, model_name, output_dir):
    """
    Actual inference function using the new model for prediction by position.
    Right now, only uses the last season where data was available for (2019).
    """

    pos = "RB"

    model = load("/".join([model_dir, model_name, "final_mdl.joblib"]))
    scaler = load("/".join([model_dir, "scaler", "scaler.joblib"]))

    # load test_data
    test_df = pd.read_csv("data/interim/base_fantasy_df.csv")
    curr_season = test_df.season_year.max()
    y_real = test_df.loc[(test_df.position == pos) & (test_df.season_year == curr_season)]

    print(f"Predicting fantasy stats for {curr_season}")
    test_df = test_df.loc[(test_df.position == pos) & (test_df.season_year == curr_season - 1)]

    # first 5 cols are player metadata
    y_pred = model.predict(scaler.transform(test_df.iloc[:, 6:]))
    test_df.loc[:, "y"] = y_pred

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    # save predictions
    test_df.to_csv("/".join([output_dir, "predictions.csv"]))

    # grade predictions
    grade_df = pd.merge(
        y_real[["player_id", "total_rushing_yds"]],
        test_df[["player_id", "y"]],
        on="player_id")

    logger.info(f"Mean Squared Error: %s " % mean_squared_error(grade_df.total_rushing_yds, grade_df.y))

    cols = ["player_id", "full_name", "y", "z_score", "season_year"]

    ref_df = pd.merge(
        zp_scores(pos, test_df)[cols],
        y_real[["player_id", "total_rushing_yds"]],
        on="player_id"
    )
    ref_df.to_csv("/".join([output_dir, f"{pos}_{curr_season}_prediction.csv"]))
    print(ref_df.sort_values(by="total_rushing_yds", axis=0, ascending=False)[:10])


if __name__ == '__main__':
    inference()
