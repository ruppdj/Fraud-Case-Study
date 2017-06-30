"""
Module containing model fitting code implements a random forest classification model on fraud data.



When run as a module, this will load a json dataset, train a classification
model, and then pickle the resulting model object to disk.
"""
import cPickle as pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from DataCleaner import DataCleaner


class FraudModel(object):
    """A fraud classifier model:
        - Cleans input data to desired format
        - Fit a model to the resulting features.
    """

    def __init__(self):
        self._dataclean = DataCleaner()
        self._model = RandomForestClassifier()

    def fit(self, X):
        """Fit a  model.

        Parameters
        ----------
        X: A pandas or numpy array of features, to be used as predictors. (processing will be done to clean the data and the label column 'fraud' will be split off and returned)


        Returns
        -------
        self: The fit model object.
        """
        # Code to fit the model.

        #need a one size fit all cleaning function

        X_train, y_train = self._dataclean.clean(X)
        self._model.fit(X_train,y_train)


        return self

    def predict_proba(self, X):
        """Make probability predictions on new data. After preprocessing the input.
        Currently we are modeling on 3 possable classifications so output must be in a 3 column format for the rest of teh system to work.
        column 0 = probability of NOT fraud
        column 1 = probability of possable fraud
        column 2 = probability of fraud"""

        X_predict = self._dataclean.clean(X)
        result = self._model.predict_proba(X_predict)
        return result
        pass

    def predict(self, X):
        """Make predictions on new data."""
        X_predict = self._dataclean.clean(X)
        result = self._model.predict(X_predict)

        return result
        pass

    def score(self, X, y):
        """Return a classification accuracy score on new data."""
        X_predict = self._dataclean.clean(X)
        result = self._model.score(X_predict,y)

        return result
        pass

def add_fraud_value(df):
    '''Data we get does not have a label column. One is created baised off field 'acct_type' for model fitting.'''
    if 'fraud' not in df.columns.values:
        df['fraud']= 1
        df.loc[df['acct_type'] == 'fraudster', 'fraud'] = 2
        df.loc[df['acct_type'] == 'fraudster_event', 'fraud'] = 2
        df.loc[df['acct_type'] == 'premium', 'fraud'] = 0

    return df

def get_data(filename):
    """Load raw data from a file and return training data.

    Parameters
    ----------
    filename: The path to a json file containing the data.

    Returns
    -------
    X: A pandas array with the 'fraud' column.

    """
    df = pd.read_json(filename)

    if 'fraud' not in df.columns.values:
        df = add_fraud_value(df)

    return df
    pass


if __name__ == '__main__':
    '''Main: runs when build_model is called creating the model and pickeling it'''
    X= get_data("data.json")
    tc = FraudModel()
    tc.fit(X)
    with open('model.pkl', 'w') as f:
        pickle.dump(tc, f)
