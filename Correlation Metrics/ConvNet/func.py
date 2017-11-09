__author__ = 'wangyi'
import numpy as np

# created on 6th Jun 2017, by Wang Yi
# logistic REGRESSION
def _sigmoid(z):
    return np.divide(1, 1+np.exp(-z))

def  sigmoid(w, X):
    if hasattr(X, "dot"):
        z = X.dot(w)
    elif hasattr(X, "__len__"):
        temp = map(lambda (i, mat): w[i] * mat, enumerate(X))
        z = reduce(lambda pre, curr: pre + curr, temp)
    else:
        z = X*w
    return _sigmoid(z)

def hypo_func(w, X):
    return _sigmoid(X.dot(w))

def hypo_mesh(w, X):
    temp = map(lambda (i, mesh): w[i] * mesh, enumerate(X))
    z = reduce(lambda pre, curr: pre + curr, temp)
    return _sigmoid(z)