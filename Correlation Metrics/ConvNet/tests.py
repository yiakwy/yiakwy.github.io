__author__ = 'wangyi'
import os, sys
root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root)

from ConvNet.cs231n.data_utils import get_CIFAR10_data
from ConvNet.costImpl.ConvNet.layers import ConvLayer
from ConvNet.costImpl.ConvNet.vol import Vol
import numpy as np

# data = get_CIFAR10_data()

def rel_error(x, y):
  """ returns relative error """
  return np.max(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))

def test_ConvLayer_forward():
    x_shape = (2, 3, 4, 4)
    w_shape = (3, 3, 4, 4)
    x = np.linspace(-0.1, 0.5, num=np.prod(x_shape)).reshape(x_shape)
    w = np.linspace(-0.2, 0.3, num=np.prod(w_shape)).reshape(w_shape)
    b = np.linspace(-0.1, 0.2, num=3)
    conv_param = {'strip': 2, 'pad': 1}

    # test here
    convs = Vol(3, (3,4,4), init_gen=w)
    b.resize(3,1)
    bias = Vol(1, (3,1), init_gen=b)
    inp = Vol(2, (3,4,4,), init_gen=x)
    conv_param['bias'] = bias
    layer = ConvLayer(x_shape[1:], convs, **conv_param)
    out = layer.forward(inp)
    correct_out = np.array([[[[[-0.08759809, -0.10987781],
                               [-0.18387192, -0.2109216 ]],
                              [[ 0.21027089,  0.21661097],
                               [ 0.22847626,  0.23004637]],
                              [[ 0.50813986,  0.54309974],
                               [ 0.64082444,  0.67101435]]],
                             [[[-0.98053589, -1.03143541],
                               [-1.19128892, -1.24695841]],
                              [[ 0.69108355,  0.66880383],
                               [ 0.59480972,  0.56776003]],
                              [[ 2.36270298,  2.36904306],
                               [ 2.38090835,  2.38247847]]]]])

    print 'Testing conv_forward_naive'
    print 'difference: ', rel_error(out, correct_out)

def test_ConvLayer_bp():
    pass

if __name__ == "__main__":
    test_ConvLayer_forward()