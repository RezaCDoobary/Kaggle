from scipy.stats import ks_2samp
from sklearn import metrics
from sklearn.metrics import precision_recall_curve,roc_curve
from sklearn.metrics import precision_score, recall_score, f1_score, \
accuracy_score, balanced_accuracy_score, roc_auc_score,average_precision_score
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_validate, StratifiedKFold
from tqdm import tqdm_notebook

def KolmogorovSmirnov(data1, data2, alpha):

    res = ks_2samp(data1,data2)
    if res.pvalue < alpha:
        reject_H0 = True
    else:
        reject_H0 = False

    return res.statistic, res.pvalue, reject_H0

def panel_of_tests(y_pred, y_observed, y_score):
    tests = [precision_score, recall_score, f1_score,average_precision_score,accuracy_score, balanced_accuracy_score, roc_auc_score]
    name = ['Precision','Recall', 'F1','AUPRC',  'Accuracy','Balanced Accuracy','ROC_AUC']
    res = {}
    for i,t in enumerate(tests):
        if name[i] == 'AUPRC':
            res[name[i]] = t(y_observed, y_score)
        else:
            res[name[i]] = t(y_observed, y_pred)
    return res