import argparse
# import logging
import numpy as np
import os
import pandas as pd
from joblib import dump

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import mean_squared_error

import models


def prepare_df(df):
    """
    Returns training features as data and labels are the players' performance in the following season. For example,
    if the training example was for year 2015, the label would be the fantasy performance in 2016 (avg per game).
    """

    # get all seasons except for last one which we use for inference
    past_ssn = df["season_year"].unique()[:-1]
    train_data = df.loc[(df["season_year"] >= np.min(past_ssn)) & (df["season_year"] <= np.max(past_ssn))]
    train_df = pd.DataFrame()
    for year in past_ssn:
        train_df = train_df.append(train_data
                                   .loc[train_data["season_year"] == year]
                                   .merge(df.loc[df["season_year"] == year + 1, ("avg_fantasy", "player_id")],
                                          on="player_id"))
    train_df.rename(columns={"avg_fantasy_y": "y", "avg_fantasy_x": "avg_fantasy"}, inplace=True)
    train_df.dropna(inplace=True)

    labels, data = train_df["y"], train_df.drop("y", axis=1)
    return data, labels


def train(args):
    output_dir = args.mdl_output_dir
    model_name = args.model_type

    x, y = prepare_df(pd.read_pickle("../../data/interim/base_fantasy_df.pkl"))

    # train test split, first remove player identification columns (first 5)
    x_train, x_val, y_train, y_val = train_test_split(x.iloc[:, 5:], y, test_size=0.33)

    scl = StandardScaler()
    scl.fit(x_train)

    model = models.create_model(model_name)
    model.fit(scl.transform(x_train), y_train)
    y_pred = model.predict(scl.transform(x_val))
    print("Mean squared error: %5f" % mean_squared_error(y_pred, y_val))

    mdl_output_dir = output_dir + "/" + model_name
    os.makedirs(mdl_output_dir, exist_ok=True)

    # save model
    dump(model, "/".join([mdl_output_dir, "final_mdl.joblib"]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--mdl-output-dir", required=True)
    parser.add_argument("-t", "--model-type", help="Type of model", required=True)
    args = parser.parse_args()
    train(args)
