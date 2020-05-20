from sklearn import metrics
from sklearn.metrics import precision_recall_curve,roc_curve
from sklearn.metrics import precision_score, recall_score, f1_score, \
accuracy_score, balanced_accuracy_score, roc_auc_score
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_validate, StratifiedKFold
from tqdm import tqdm_notebook
from tests import *

import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.naive_bayes import GaussianNB

class cv_modelling(object):
    def __init__(self,xx,yy, folds, sampling_function = None, outlier_function = None):
        """
        Will require an api to a model that can be refit without using previous parameters
        """
        self.xx = xx
        self.yy = yy
        self.folds = folds
        self.sampling_function = sampling_function
        self.outlier_function = outlier_function
        
    def _create_result_df(self):
        model_performance = pd.DataFrame(columns = ['Precision','Recall', 'F1','AUPRC',  'Accuracy','Balanced Accuracy','ROC_AUC'],\
                                    index = np.arange(self.folds))
        
        return model_performance
    
    def _create_model_instance(self, model_string):
        model_string = model_string.split(' ')
        if model_string[0] == 'logistic':
            return LogisticRegression(max_iter = 1000, C = float(model_string[1]), n_jobs = -1)
        elif model_string[0] == 'randomforest':
            n_estimators, max_depth = int(model_string[1]), int(model_string[2])
            return RandomForestClassifier(n_estimators = n_estimators, max_depth = max_depth)
        elif model_string[0] == 'NBGaussian':
            return GaussianNB()
        elif model_string[0] == 'SVC':
            return SVC()
        elif model_string[0] == 'xgboost':
            n_estimators, max_depth = int(model_string[1]), int(model_string[2])
            return XGBClassifier(n_estimators = n_estimators, max_depth = max_depth)
        else:
            raise NotImplementedError
    
    def fit(self, model_string, verbose = True):
        models = []
        skf = StratifiedKFold(n_splits = self.folds, shuffle=True)
        skf.get_n_splits(self.xx, self.yy)
        model_performance = self._create_result_df()
        
        for i,indices in enumerate(skf.split(self.xx, self.yy)):
            if verbose:
                print('\r', 'Fold [{}/{}]'.format(i+1,self.folds), end='')
            train_index, test_index = indices
            X_train, X_test = self.xx[train_index], self.xx[test_index]
            y_train, y_test = self.yy[train_index], self.yy[test_index]

            if self.sampling_function is not None:
                X_train, y_train = self.sampling_function(X_train, y_train)

            if self.outlier_function is not None:
                X_train, y_train = self.outlier_function(X_train, y_train)

            model = self._create_model_instance(model_string)
            model.fit(X_train, y_train)


            y_pred = model.predict(X_test)
            y_score = model.predict_proba(X_test)[:,1]
            tests = panel_of_tests(y_pred, y_test, y_score)
            model_performance.iloc[i] = tests
            models.append(model)
        
        model_performance.loc['mean'] = model_performance.mean()
        
        return model_performance, models