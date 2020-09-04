"""
File name: train.py
Author: David Lin
"""

import os

import click
import numpy as np
import pandas as pd
from joblib import dump

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

from ffmdl.features.build_features import build_features
from ffmdl.common import get_logger, skill_pos, pos_target_map
from ffmdl.models.mdl_utils import create_model, models

logger = get_logger(__name__)


def prepare_df(df):
    """
    Returns training features as data and labels are the players' performance
    in the following season. For example, if the training example was for year 2015,
    the label would be the fantasy performance in 2016 (avg per game).
    """
    train_dfs = []

    for pos in skill_pos:
        target = pos_target_map[pos]
        logger.info(f"target: {target} pos: {pos}")

        # get all seasons except for last one which we use for inference
        dataframe = df.loc[df["position"] == pos]
        past_ssn = dataframe.season_year.unique()[:-1]
        logger.info(f"dataframe.shape={dataframe.shape}")
        logger.info(f"preparing data in range: {np.min(past_ssn)} - {np.max(past_ssn)}")

        train_data = dataframe.loc[
            (dataframe.season_year >= np.min(past_ssn)) &
            (dataframe.season_year <= np.max(past_ssn))]

        train_df = pd.DataFrame()

        for year in past_ssn:
            train_df = train_df.append(train_data
            .loc[train_data.season_year == year]
            .merge(
                dataframe.loc[
                    dataframe.season_year == year + 1,
                    (target, "player_id")],
                on="player_id"))

        train_df.dropna(inplace=True)
        train_df.rename(columns={f"{target}_y": "y", f"{target}_x": target}, inplace=True)
        train_dfs.append(train_df)

    train_df = pd.concat(train_dfs)
    return train_df.drop("y", axis=1), train_df["y"]


def generate_rb_df(df):
    pos = "RB"
    target = pos_target_map[pos]
    logger.info(f"target: {target} pos: {pos}")

    # get all seasons except for last one which we use for inference
    dataframe = df.loc[df["position"] == pos]
    past_ssn = dataframe.season_year.unique()[:-1]
    logger.info(f"dataframe.shape={dataframe.shape}")
    logger.info(f"preparing data in range: {np.min(past_ssn)} - {np.max(past_ssn)}")

    train_data = dataframe.loc[dataframe.season_year <= np.max(past_ssn)]

    train_df = pd.DataFrame()

    for year in past_ssn:
        train_df = pd.concat([train_df,
        train_data
        .loc[train_data.season_year == year]
        .merge(
            dataframe.loc[
                dataframe.season_year == year + 1,
                (target, "player_id")],
            on="player_id")])

    train_df.dropna(inplace=True)
    train_df.rename(columns={f"{target}_y": "y", f"{target}_x": target}, inplace=True)

    return train_df.drop("y", axis=1), train_df["y"]


# pylint: disable=no-value-for-parameter
@click.command()
@click.option("-n", "--normalize", is_flag=True, default=False, help="Normalize features before training")
@click.option("--output-dir", default="models/trained_models")
def train(normalize, output_dir):
    """
    Method to train a model. Requires an output directory and model_name. See models.py
    for a list of accepted models.
    """

    interim_data_filepath = "data/interim"
    base_df_filepath = "/".join([interim_data_filepath, "base_fantasy_df.csv"])

    if not os.path.exists(base_df_filepath):
        build_features()

    # TODO: save the x_train and x_val splits so the dataset is consistent
    # if not os.path.exists("data/train/train.csv") or not os.path.exists("data/val/val.csv"):
    data, labels = generate_rb_df(pd.read_csv(base_df_filepath))

    # train test split, first remove player identification columns (first 5)
    x_train, x_val, y_train, y_val = train_test_split(data.iloc[:, 6:], labels, test_size=0.33)

    best_score = float('inf')
    best_mdl = None

    logger.info(x_train.shape)

    if normalize:
        scl = StandardScaler()
        scl.fit(x_train)
        x_train = scl.transform(x_train)
        x_val = scl.transform(x_val)

    for mdl_name, mdl in models.items():
        mdl.fit(x_train, y_train)
        y_pred = mdl.predict(x_val)
        mse = mean_squared_error(y_pred, y_val)
        logger.info(f"{mdl_name} -- {mse}")

        if mse < best_score:
            logger.info(f"Best score: {mse} best model: {mdl_name}")
            best_score = mse
            best_mdl = mdl

        mdl_output_dir = output_dir + "/" + mdl_name
        os.makedirs(mdl_output_dir, exist_ok=True)
        mdl_out = "/".join([mdl_output_dir, "final_mdl.joblib"])
        logger.info(f"Saving model to: {mdl_out}")
        dump(best_mdl, mdl_out)

    # save model
    if normalize:
        scl_output_dir = "/".join([output_dir, "scaler"])
        os.makedirs(scl_output_dir, exist_ok=True)
        logger.info(f"Saving scaler to: {scl_output_dir}/scaler.joblib")
        dump(scl, scl_output_dir + "/scaler.joblib")


if __name__ == '__main__':
    train()
