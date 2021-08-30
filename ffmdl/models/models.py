from joblib import load
import os

from sklearn.linear_model import LinearRegression
from sklearn.svm import LinearSVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
import torch

from ffmdl import common

def load_model(model_type):
    if model_type not in common.model_types:
        raise ValueError(
            "Model type provided hasn't been trained or isn't available. \
            Try one of the following: %s" % common.model_types)
    pass


def create_model(model_type):
    if model_type == 'lin_reg':
        return LinearRegression()
    elif model_type == 'svm':
        pass
    elif model_type == 'nn':
        pass


def nn_arch():
    pass
