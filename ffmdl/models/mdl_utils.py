"""
Module name: models.py
Purpose: Where models are defined with hyperparams, and functions for loading and saving
models.
"""

from sklearn.linear_model import LinearRegression
from sklearn.svm import LinearSVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
# import torch

from ffmdl import common

models = {
    "lin_reg": LinearRegression(),
    "lin_svr": LinearSVR(),
    "dec_tree": DecisionTreeRegressor(max_depth=3),
    "rand_forest": RandomForestRegressor(n_estimators=100),
    "ada_boost": AdaBoostRegressor()
}

def load_model(model_type):
    """
    Load a trained model from disk
    """

    if model_type not in common.model_types:
        raise ValueError(
            "Model type provided hasn't been trained or isn't available. \
            Try one of the following: {common.model_types}")
    return model_type


def create_model(model_type):
    """
    Create a new model based on model_type (model_name).
    """

    return models[model_type]


# def nn_arch():
#     """
#     Neural network model goes here
#     """
#     pass
