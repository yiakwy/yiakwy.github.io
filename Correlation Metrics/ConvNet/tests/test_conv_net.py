__author__ = 'wangyi'
import os, sys
root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root)

import unittest
import logging
from ConvNet.utils.log import LoggerAdaptor, configure_loggings
_logger = logging.getLogger("ConvLayer")

from ConvNet.cs231n.data_utils import get_CIFAR10_data
from ConvNet.costImpl.ConvNet.layers import ConvLayer, FackedConvLayer
from ConvNet.costImpl.ConvNet.vol import Vol
import numpy as np

# data = get_CIFAR10_data()

def rel_error(x, y):
  """ returns relative error """
  return np.max(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))


# please see https://stackoverflow.com/questions/8518043/turn-some-print-off-in-python-unittest
class MyTestResult(unittest.TextTestResult):

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        self.stream.write("An Error Found!\n\n\r")

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        self.stream.write("An Failure Found!\n\n\r")


# see http://python.net/crew/tbryan/UnitTestTalk/slide30.html
class MyTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return MyTestResult(self.stream, self.descriptions, self.verbosity)

class ConvLayerTestCase(unittest.TestCase):

    logger = LoggerAdaptor("tests/test_conv_net.ConvLayerTestCase", _logger)

    @classmethod
    def setUpClass(cls):
        pass

    def test_forward(self):
        x_shape = (2, 3, 4, 4)
        w_shape = (3, 3, 4, 4)
        x = np.linspace(-0.1, 0.5, num=np.prod(x_shape)).reshape(x_shape)
        w = np.linspace(-0.2, 0.3, num=np.prod(w_shape)).reshape(w_shape)
        b = np.linspace(-0.1, 0.2, num=3)
        conv_param = {'strip': 2, 'pad': 1}

        # test here
        b.resize(3,1)
        bias = Vol(1, (3,1), init_gen=b)
        inp = Vol(2, (3,4,4,), init_gen=x)
        convs = Vol(3, (3,4,4), init_gen=w)
        conv_param['bias'] = bias
        layer = ConvLayer(x_shape[1:], convs, **conv_param)
        vol = layer.forward(inp)
        # the original data form cs321 has been trimmed.
        # before that, 'layer.forward' passed the test.
        correct_out = np.array([[[[[-0.088, -0.110],
                                   [-0.184, -0.211]],
                                  [[ 0.210,  0.217],
                                   [ 0.228,  0.230]],
                                  [[ 0.508,  0.543],
                                   [ 0.641,  0.671]]],
                                 [[[-0.980, -1.031],
                                   [-1.191, -1.247]],
                                  [[ 0.691,  0.667],
                                   [ 0.595,  0.568]],
                                  [[ 2.363,  2.369],
                                   [ 2.381,  2.382]]]]])

        self.logger.info('I have trimmed the test data, hence, epilon as 1.0e-2 is correct. The original data can achieve 1.0e-6 precision')
        self.logger.info('Testing layer.forward')
        err = rel_error(vol.w, correct_out)
        self.logger.info('Difference: %s' % err)
        assert(err < 1.0e-2)

    def test_bp(self):
        import time

        # check using numeric gradient
        x = np.random.randn(4, 3, 5, 5)
        w = np.random.randn(2, 3, 3, 3)
        b = np.random.randn(2,)
        top_diff = np.random.randn(4, 2, 5, 5)
        conv_param = {'strip': 1, 'pad': 1}

        # check eval_numerical_gradient_array implementation
        from ConvNet.cs231n.gradient_check import eval_numerical_gradient_array, eval_numerical_gradient
        b.resize(2,1)
        bias = Vol(1, (2,1), init_gen=b)
        inp = Vol(4, (3,5,5,), init_gen=x)
        convs = Vol(2, (3,3,3), init_gen=w)
        conv_param['bias'] = bias
        layer = ConvLayer((3,5,5), convs, **conv_param)

        # to fit cs231 numeric difference scheme
        def forward_layer_by_arg1(x):
            b.resize(2,1)
            bias = Vol(1, (2,1), init_gen=b)
            inp = Vol(4, (3,5,5), init_gen=x)
            convs = Vol(2, (3,3,3), init_gen=w)
            conv_param['bias'] = bias
            layer = ConvLayer((3,5,5), convs, **conv_param)
            return layer.forward(inp)

        def forward_layer_by_arg2(w):
            b.resize(2,1)
            bias = Vol(1, (2,1), init_gen=b)
            inp = Vol(4, (3,5,5), init_gen=x)
            convs = Vol(2, (3,3,3), init_gen=w)
            conv_param['bias'] = bias
            layer = ConvLayer((3,5,5), convs, **conv_param)
            return layer.forward(inp)

        def forward_layer_by_arg3(b):
            b.resize(2,1)
            bias = Vol(1, (2,1), init_gen=b)
            inp = Vol(4, (3,5,5), init_gen=x)
            convs = Vol(2, (3,3,3), init_gen=w)
            conv_param['bias'] = bias
            layer = ConvLayer((3,5,5), convs, **conv_param)
            return layer.forward(inp)

        start = time.time()
        dx_numeric = eval_numerical_gradient_array(forward_layer_by_arg1, x, top_diff)
        dw_numeric = eval_numerical_gradient_array(forward_layer_by_arg2, w, top_diff)
        db_numeric = eval_numerical_gradient_array(forward_layer_by_arg3, b, top_diff)
        elapsed = time.time() - start

        self.logger.info("Finish numeric computation with elapsed time %s" % elapsed)

        vol = layer.forward(inp)
        top_layer = FackedConvLayer(vol, None)
        top_layer.inp.grad = top_diff
        start = time.time()
        inp_grad, filters_grad, bias_grad = layer.bp(top_layer)
        elapsed = time.time() - start

        self.logger.info("Finish ConvLayer.bp computation with elapsed time %s" % elapsed)

        self.logger.info('Testing layer.bp(top_layer) inp_grad')
        err = rel_error(inp_grad, dx_numeric)
        self.logger.info('Difference: %s' % err)
        assert(err < 1.0e-6)

        self.logger.info('Testing layer.bp(top_layer) filters_grad')
        err = rel_error(filters_grad, dw_numeric)
        self.logger.info('Difference: %s' % err)
        assert(err < 1.0e-6)

        self.logger.info('Testing layer.bp(top_layer) bias_grad')
        err = rel_error(bias_grad, db_numeric)
        self.logger.info('Difference: %s' % err)
        assert(err < 1.0e-6)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=u"%(asctime)s [%(levelname)s]:%(filename)s, %(name)s, in line %(lineno)s >> %(message)s".encode('utf-8'))
    unittest.main(testRunner=MyTestRunner)