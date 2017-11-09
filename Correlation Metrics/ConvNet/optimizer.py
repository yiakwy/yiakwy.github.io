__author__ = 'wangyi'
import numpy as np
from .settings import EPILON

# decoratorLib from PEP 318 standard
def accepts(*types):
    def check_accepts(f):
        assert len(types) == f.func_code.co_argcount
        def new_f(*args, **kwds):
            for (a, t) in zip(args, types):
                assert isinstance(a, t), \
                       "arg %r does not match %s" % (a,t)
            return f(*args, **kwds)
        new_f.func_name = f.func_name
        return new_f
    return check_accepts

def returns(rtype):
    def check_returns(f):
        def new_f(*args, **kwds):
            result = f(*args, **kwds)
            assert isinstance(result, rtype), \
                   "return value %r does not match %s" % (result,rtype)
            return result
        new_f.func_name = f.func_name
        return new_f
    return check_returns

# add cost adaptor for fmin_cg
def cost_adaptor(*args, **kw):
    def wrapper(f):
        def adaptor(theta):
            return f(theta, *args, **kw)
        return adaptor
    return wrapper

def wolf_powell(f, fk, xk, lr, g, p=None):
    c1 = 0.1 # 0.01
    c2 = 0.8
    EPILON = 0.01
    p = p or - g
    alpha = 1.0
    MAX = 5
    LOWER_Bound, UPPER_Bound = 0.0, MAX

    maxIter = 4
    i = 0
    flag1 = True
    flag2 = True
    print("begin line search")
    while (flag1 or flag2) and i < maxIter:
        fkplus = f(xk + alpha * p)
        temp1 = fkplus[0] - fk - c1 * alpha * g.dot(p)
        flag1 = temp1 > 0 ## cond1 does not hold
        temp2 = fkplus[1].dot(p) - c2 * g.dot(p)
        flag2 = temp2 < 0 and np.abs(temp2) < EPILON ## cond2 does not hold
        print(" f(xk + alpha*p)  =%6.2f %2s  fk+c1*alpha*g@p=%6.2f" % (fkplus[0], '>' if flag1 else '<=', fk + c1 * alpha * g.dot(p)))
        print("df(xk + alpha*p)*p=%6.2f %2s           c2*g@p=%6.2f" % (fkplus[1].dot(p), '<' if flag2 else '>=', c2 * g.dot(p)))
        if flag1:
            UPPER_Bound = alpha
        elif flag2:
            LOWER_Bound = alpha
        alpha = (LOWER_Bound + UPPER_Bound) / 2
        # alpha = alpha*(1.0 - alpha / 2)
        i += 1
    print("end line search")
    print("step ratio %6.2f" % alpha)
    return alpha

def fmin_cg(cost, init_param, options={}):
    gifseq = options['gifseq']
    maxIter = options['maxIter']
    weights = init_param
    lr = options['learning_rate']
    line_search = options['line_search']
    alpha = int(1)
    user_call = options['user_call']
    hypo = options['hypo']
    i = 0
    J0 = 10
    while i < maxIter:
        J1, grad = cost(weights)
        print("Iteration %s, error %s" % (i, J1))
        print("grad %s" % grad)
        if np.abs(J0 - J1) < EPILON and grad.dot(grad) < EPILON:
            print("convergent! at iteration %s" % i)
            print("with weights %s" % weights)
            print("grad %s" % grad)
            break
        # linear search here
        if line_search:
            # you can also pass p computed from L-BFGSh
            alpha = wolf_powell(cost, J1, weights, lr, grad)
            weights = weights - alpha * grad
        else:
            weights = weights - lr * grad

        if user_call and i in gifseq: user_call(weights)
        J0 = J1
        i += 1
    return weights

def batch(mat, ratio=1.0):
    r, _ = mat.shape
    return randperm(mat)[:int(r*ratio) + 1]

def randperm(mat):
    return np.random.permutation(mat) # for truely randomly shuffling, please refer to

def InitalizWeights(*size):
    return np.random.rand(*size)

