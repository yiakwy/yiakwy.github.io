"author: Lei Wang(lwang019@e.ntu.edu)"

from __future__ import division
from math import *
from sklearn import metrics

import numpy as np

SIM_FA = -1
SIM_FA_L = 0
TRAPEZOIDAL_FA = 1
SIMPSON_FA = 2

ALGO_FA = None  
EPILON = 1.0e-8
POSITIVE = 1

import logging
from utils.log import LoggerAdaptor
_logger = logging.getLogger("test.metrics")

def logLoss(samples):
    """
    shanno info entopy
     E(a subset) = sum p_i * log (1/p_i) from i upto N
     
    Hence we define K-L distance to measure E_1 of set a_1 and E_2 of set a_2:
    D_KL(P||Q) = sum p_i * log (1/q_i) - p_i * log(1/p_i) from i upto N
                      p_i * log (p_i / q_i)
            or = sum p_i * log (1/q_i) from i upto N - const
    
    When our KL-Distance is determined, we derived our LogLoss function
    """
    
    # -1.0/impression * (click * log(pctr) + (click-impression) * log(1-pctr))
    loss = 0.0
    l = len(samples)
    for sample in samples:
        if sample['click'] == 1:
            loss += -log(sample['pctr'])
        else:
            loss += -log(1-sample['pctr'])
    return loss / l      

def logregobj(preds, dtrain):
    """ xgboost example
    y is real belongs to {0, 1}
    L(real, pred) = log(1+exp(real)) - real * pred
    L_pred = 1/(1+exp(-pred)) - real
    L_pred^2 = (1-1/(1+exp(-pred)))*1/(1+exp(-pred))
    
    """
    labels = dtrain.get_label()
    preds = 1.0 / (1.0 + np.exp(-preds))
    grad = preds - labels
    hess = preds * (1.0-preds)
    return grad, hess

def smooth_abolute_factory(alpha=None):
    
    if alpha is None:
        alpha = 1
    
    def wrapped(preds, dtrain):
        labels = dtrain.get_label()
        err = labels - preds
        grad = 1/(1+np.exp(alpha * (err))) - 1/(1+np.exp(alpha * (-err)))
        hess = 2 * alpha * np.exp(alpha * err) / ((1 + np.exp(alpha * err)) ** 2)
        logger = LoggerAdaptor("xgboost", _logger)
        logger.info("<grad: \n%s>" % grad)
        logger.info("<hess: \n%s>" % hess)
        from config import settings
        import os
        with open(os.path.join(settings.BASE_DIR, "obj_track.log"), 'w') as f:
            f.write("<grad: \n%s>" % grad)
            f.write("<hess: \n%s>" % hess)
        return grad, hess
    return wrapped


def numer_equal(one, other, eplion=None):
    if eplion is None: eplion = EPILON
    return True if abs(one - other) < eplion else False

class RocBase(object):
    
    @staticmethod
    def auc(x, y, algo):
        """
        Area Under ROC:
        tps, fps: matrix of vals
        numeric alglorithms
        """
        if algo == SIMPSON_FA:
            """
            simpson method:
            """
        
        elif algo == TRAPEZOIDAL_FA:
            """
            trapezoidal method
            """
            
        else:
            raise Exception("Not implemented!")

class RocAdv(RocBase):

    @staticmethod
    def auc(samples, pctr, algo=SIM_FA):
        """
        used for prediction
        """
        l = len(samples)
        
        if l < 2:
            raise ValueError("At least 2 samples are needed for area computing!")
        
        if algo == SIM_FA:
            """
            considering the area under curve as a family of rectangules
            we will derive:
            
            """
            area = 0.0 
            tp = 0, 0
            fp, fp_pre = 0, 0
            
            last_point = samples[0]['pctr']
            
            for sample in samples:
                if sample['label'] == POSITIVE:
                    tp += 1 # y axis
                else:
                    fp += 1 # x axis
                    
                # add area
                if  not numer_equal(last_point, sample['pctr']):
                    area += (fp - fp_pre) * tp
                    fp_pre = fp
                    last_point = sample['pctr']
                
            return area / tp * fp

        elif algo == SIM_FA_L:
            """
            considering the area under curve as a family of trapzoids
            we will derive:
            """
            
            area = 0.0
            tp, tp_pre = 0, 0
            fp, fp_pre = 0, 0
            
            last_point = samples[0]['pctr']
            
            for sample in samples:
                if sample['label'] == POSITIVE:
                    tp += 1
                else:
                    fp += 1
                
                if not numer_equal(last_point, sample['pctr']):    
                    # add area
                    area += (fp - fp_pre) * (tp + tp_pre) / 2
                    tp_pre, fp_pre = tp, fp
                    last_point = sample['pctr']
                    
            return area / tp * fp
            
        else:
            """
            before call 
             super(self.__class__, self).auc(samples, pctr, algo)
             
            we need to make sure : one fp correspond to one tp
            """
            raise Exception("Not implemented!")
    
    
    
    
    