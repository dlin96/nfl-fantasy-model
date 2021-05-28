import argparse
import numpy as np
import pandas as pd
from joblib import dump

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# models
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.metrics import mean_squared_error


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


def train(output_dir):
    x, y = prepare_df(pd.read_pickle("../../data/processed/base_fantasy_df.pkl"))

    # train test split
    x_train, x_val, y_train, y_val = train_test_split(x.iloc[:, 5:], y, test_size=0.33)

    scl = StandardScaler()
    scl.fit(x_train)

    final_mdl = None
    min_mse = float('inf')
    models = [DecisionTreeRegressor(max_depth=50),
              RandomForestRegressor(n_estimators=100),
              AdaBoostRegressor(base_estimator=None, n_estimators=50, loss="square")]

    for model in models:
        model.fit(scl.transform(x_train), y_train)
        y_pred = model.predict(scl.transform(x_val))
        mse = mean_squared_error(y_val, y_pred)
        print(model.__class__, mse)
        if mse < min_mse:
            min_mse = mse
            final_mdl = model
    dump(final_mdl, output_dir + "/final_mdl.joblib")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output-dir", help="output directory for trained model")
    args = parser.parse_args()

    train(args.output_dir)
