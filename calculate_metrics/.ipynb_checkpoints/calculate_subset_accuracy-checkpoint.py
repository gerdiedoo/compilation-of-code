import pandas as pd 
import numpy as np 
from sklearn.metrics import multilabel_confusion_matrix
import pickle as pkl

from sklearn.metrics import f1_score

import warnings

def subset_accuracy(real, pred):
    equalities = (np.all(pred == real, axis=0)).astype(float)
    subset     = np.sum(equalities)
    subset_accuracy = subset / (pred.shape[1])
    return subset_accuracy

warnings.filterwarnings('ignore')

prediction_files = [f'gerd_pkl/prediction_{i}.pkl' for i in range(8)]
real_files = [f'gerd_pkl/real_{i}.pkl' for i in range(8)]

preds = []
reals = []

for idx, (pred, real) in enumerate(zip(prediction_files, real_files)):
    
    with open(pred, 'rb') as f:
        p = pkl.load(f)
        preds.append(p)
    with open(real, 'rb') as f:
        r = pkl.load(f)
        reals.append(r)

    print(f'split {idx}: {subset_accuracy(r.T, p.T)}')

    
    
preds = np.vstack(preds).T
reals = np.vstack(reals).T

print(f'Total subset accuracy: {subset_accuracy(reals, preds)}')