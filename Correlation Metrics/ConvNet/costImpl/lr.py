__author__ = 'wangyi'

import numpy as np
from ..optimizer import cost_adaptor
from ..func import sigmoid
from ..settings import EPILON
from ..DATA.simple import X0, X1, X2, Z # sample data
# lrCostFunc
# created at 14/12/15, 11:40 AM by WANG YI, lwang019@e.ntu.edu.sg
# updated on 6th Jun, 2017 by WANG YI, lwang11@mtu.edu
#   1. add line search
#   2. support corr supervised learning
# ALL RIGHTS RESERVED

def logloss(p, q):
    return np.sum(cross_entropy(p, q), axis=0)

def cross_entropy(p, q):
    print("q(sigmoid): %s" % np.array2string(q, formatter={'float_kind':'{0:6.3f}'.format}))
    print("p(y): %s" % np.array2string(p, formatter={'float_kind':'{0:6.3f}'.format}))
    print("entropy: %s" % np.array2string(-p * np.log(q) - (1-p) * np.log(1-q), formatter={'float_kind':'{0:6.3f}'.format}))
    return -p * np.log(q) - (1-p) * np.log(1-q)

def lasso(theta):
    ret = np.abs(theta)
    if hasattr(theta, "__len__"):
        ret[0] = 0
    return ret

# You might also want to use approximate function here
# for more information please refer to Proximal Gradient Methods, the following equation is equivalent to Proximal Gradient Methods
def lasso_pxm(theta, epilon=EPILON):
    if hasattr(theta, "__len__"):
        p = len(theta)
        ret = np.array(map(lambda i: np.sign(theta[i]) if np.abs(theta[i]) >= epilon else 0, np.arange(p)))
    else:
        ret = np.sign(theta) if np.abs(theta) >= epilon else 0
    return ret

learning_rate = 0.1
@cost_adaptor(np.column_stack([X0, X1, X2]), Z, sigmoid, learning_rate, lasso, lasso_pxm)
def lrCostFunc(theta, X, y, hypo, _lambda, reg_f, reg_G):
    n, p = X.shape
    if reg_G is not None and reg_f is not None:
        reg = reg_f(theta)
        # grad = 1.0/n * (X.T).dot(sigmoid(theta, X) - y) + 1.0/(2*n) * _lambda * reg_G(reg, epilon=_lambda)
        grad = np.array(map(lambda i: 1.0/n * X[:,i].dot(sigmoid(theta, X) - y) +  1.0/n * _lambda * reg_G(reg[i], epilon=_lambda), np.arange(p)))
        J = 1.0/n * logloss(y, sigmoid(theta, X)) + _lambda/(2*n) * np.sum(reg)
    else:
        # grad = 1.0/n * (X.T).dot(sigmoid(theta, X) - y)
        grad = np.array(map(lambda i: 1.0/n * X[:,i].dot(sigmoid(theta, X) - y), np.arange(p)))
        J = 1.0/n * logloss(y, sigmoid(theta, X))
        # grad = np.array(map(lambda i: 1.0/n * np.sum(sigmoid(y, X.dot(theta))*y*X[:,i]), np.arange(p)))
        # J = 1.0/n * np.sum(np.log(1 + np.exp(-y * X.dot(theta))))
    return (J, grad)

# derived from max likelyhood
@cost_adaptor(np.column_stack([X0, X1, X2]), Z, sigmoid, learning_rate, lasso, None)
def lr_entropy(theta, X, y, hypo, _lambda, reg_f, reg_g):
    n, p = X.shape
    temp_err = np.divide(1, 1 + np.exp(y * X.dot(theta)))
    grad = np.array(map(lambda i: np.average(temp_err * (-y * X[:, i])), np.arange(p)))
    J = 1.0/n * np.sum( np.divide(1, 1 + np.exp(y * X.dot(theta))) )
    return (J, grad)

# X0 will be replaced by a step func
@cost_adaptor(np.column_stack([X1, X2]), Z, sigmoid, learning_rate, lasso, None)
def corr(theta, X, y, hypo, V, _lambda, reg_f, reg_g):
    pass
