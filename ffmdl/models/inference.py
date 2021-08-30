import argparse
# import models
import pandas as pd
from joblib import load, dump


def inference(season_year):
    """
    :param season_year: the year we want to predict stats for. For example, if current season is 20-21, then this is 20
    :return: no return value, but should write player predictions to disk
    """

    model = load("../../models/final_mdl.joblib")

    # load test_data
    test_df = pd.read_pickle("../../data/processed/base_fantasy_df.pkl")
    test_df = test_df.loc[test_df["season_year"] == season_year-1]
    y_pred = model.predict(test_df.iloc[:, 5:])  # first 5 cols are player metadata
    test_df.loc[:, "y"] = y_pred
    dump(test_df, "../../output/predictions.pkl")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--season-year", type=int)
    args = parser.parse_args()
    inference(args.season_year)
