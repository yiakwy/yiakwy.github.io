__author__ = 'wangyi'
import os, sys
root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root)

import unittest
import logging
from ConvNet.utils.log import LoggerAdaptor, configure_loggings
_logger = logging.getLogger("ConvNet")

from ConvNet.cs231n.data_utils import get_CIFAR10_data
from ConvNet.costImpl.ConvNet.layers import ConvLayer, FackedConvLayer, BatchNorm, ReluActivation, UpSampling
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
        self.stream.write("Successful with <%s.%s>!\n\n\r" % (test.__class__.__name__, test._testMethodName))

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
        # before that, 'layer.forward' passed the test with numeric 1e-10 accuracy.
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


class ReluActivationTestCase(unittest.TestCase):

    logger = LoggerAdaptor("tests/test_conv_net.ReluActivationTestCase", _logger)

    @classmethod
    def setUpClass(cls):
        pass

    def test_bp_all(self):
        import time

        # check using numeric gradient
        x = np.random.randn(2, 3, 8, 8)
        w = np.random.randn(3, 3, 3, 3)
        b = np.random.randn(3,)
        top_diff = np.random.randn(2, 3, 8, 8)
        conv_param = {'strip': 1, 'pad': 1}

        b.resize(3,1)

         # to fit cs231 numeric difference scheme
        def forward_layer_by_arg1(x):
            b.resize(3,1)
            bias = Vol(1, (3,1), init_gen=b)
            inp = Vol(2, (3,8,8), init_gen=x)
            convs = Vol(3, (3,3,3), init_gen=w)
            conv_param['bias'] = bias
            conv1_numeric = ConvLayer((3,8,8), convs, **conv_param)(inp)
            relu_numeric = ReluActivation()(conv1_numeric)
            return relu_numeric

         # check eval_numerical_gradient_array implementation
        from ConvNet.cs231n.gradient_check import eval_numerical_gradient_array, eval_numerical_gradient

        start = time.time()
        dx_numeric = eval_numerical_gradient_array(forward_layer_by_arg1, x, top_diff)
        elapsed = time.time() -start

        self.logger.info("Finish numeric computation with elapsed time %s" % elapsed)

        bias = Vol(1, (3,1), init_gen=b)
        inp = Vol(2, (3,8,8), init_gen=x)
        convs = Vol(3, (3,3,3), init_gen=w)
        conv_param['bias'] = bias
        # Keras alike layer stack syntax
        conv_layer = ConvLayer((3,8,8), convs, **conv_param)
        relu_layer = ReluActivation()(conv_layer)

        # test backpropogation conv followed by a relu
        vol = conv_layer(inp)
        top_layer = FackedConvLayer(vol, None)
        top_layer.inp.grad = top_diff
        start = time.time()
        inp_grad, filters_grad, bias_grad = relu_layer.bp_all(top_layer)
        elapsed = time.time() - start

        self.logger.info("Finish stacked layer (ConvLayer -> ReluActivation).bp_all computation with elapsed time %s" % elapsed)

        self.logger.info('Testing layer.bp_all(top_layer) inp_grad')
        err = rel_error(inp_grad, dx_numeric)
        self.logger.info('Difference: %s' % err)
        assert(err < 1.0e-8)


class BatchNormTestCase(unittest.TestCase):

    logger = LoggerAdaptor("tests/test_conv_net.BatchNormTestCase", _logger)

    @classmethod
    def setUpClass(cls):
        pass

    def test_forward(self):
        Batch_Size = 200
        D1, D2, D3 = 50, 60, 3

        X = np.random.randn(Batch_Size, D1)
        W1 = np.random.randn(D1, D2)
        W2 = np.random.randn(D2, D3)
        a = np.maximum(0, X.dot(W1)).dot(W2) # Batch_Size * D3

        # gamma = 1, beta = 0
        inp = Vol(Batch_Size, (D3,), init_gen=a)
        layer = BatchNorm()
        vol = layer.forward(inp)

        mean = np.mean(vol.w, axis=0)
        std = np.std(vol.w, axis=0)

        assert(rel_error(mean, np.zeros(D3)) < 1e-6)
        assert(rel_error(std, np.ones(D3)) < 1e-6)

    def test_bp(self):
        import time

        Batch_Size, D = 4, 5
        a1, a0 = 5, 12
        X = a1 * np.random.randn(Batch_Size, D) + a0
        Gamma = np.random.randn(1)
        Beta = np.random.randn(1)
        top_diff = np.random.randn(Batch_Size, D)

        def forward_layer_by_arg1(x):
            inp = Vol(Batch_Size, (D,), init_gen=x)
            layer = BatchNorm(gamma=Gamma, beta=Beta)
            return layer.forward(inp)

        def forward_layer_by_arg2(gamma):
            inp = Vol(Batch_Size, (D,), init_gen=X)
            layer = BatchNorm(gamma=gamma, beta=Beta)
            return layer.forward(inp)

        def forward_layer_by_arg3(beta):
            inp = Vol(Batch_Size, (D,), init_gen=X)
            layer = BatchNorm(gamma=Gamma, beta=beta)
            return layer.forward(inp)

        # check eval_numerical_gradient_array implementation
        from ConvNet.cs231n.gradient_check import eval_numerical_gradient_array, eval_numerical_gradient

        start = time.time()
        dx_numeric = eval_numerical_gradient_array(forward_layer_by_arg1, X, top_diff)
        dw_numeric = eval_numerical_gradient_array(forward_layer_by_arg2, np.ones((D,)) * Gamma, top_diff)
        db_numeric = eval_numerical_gradient_array(forward_layer_by_arg3, np.ones((D,)) * Beta, top_diff)
        elapsed = time.time() - start

        self.logger.info("Finish numeric computation with elapsed time %s" % elapsed)

        inp = Vol(Batch_Size, (D,), init_gen=X)
        layer = BatchNorm(gamma=Gamma, beta=Beta)
        vol = layer.forward(inp)
        top_layer = FackedConvLayer(vol, None)
        top_layer.inp.grad = top_diff
        start = time.time()
        inp_grad, dW, db = layer.bp(top_layer)
        elapsed = time.time() - start

        self.logger.info("Finish BatchNorm.bp computation with elapsed time %s" % elapsed)

        self.logger.info('Testing layer.bp(top_layer) inp_grad')
        err = rel_error(inp_grad, dx_numeric)
        self.logger.info('Difference: %s' % err)
        assert(err < 1.0e-6)

        self.logger.info('Testing layer.bp(top_layer) dW~Difference w.r.t. gamma')
        err = rel_error(dW, dw_numeric)
        self.logger.info('Difference: %s' % err)
        assert(err < 1.0e-6)

        self.logger.info('Testing layer.bp(top_layer) db~Difference w.r.t. beta')
        err = rel_error(db, db_numeric)
        self.logger.info('Difference: %s' % err)
        assert(err < 1.0e-6)

class UpSamplingTestCase(unittest.TestCase):

    logger = LoggerAdaptor("tests/test_conv_net.UpSamplingTestCase", _logger)

    @classmethod
    def setUpClass(cls):
        pass

    def test_forward(self):
        # see http://warmspringwinds.github.io/tensorflow/tf-slim/2016/11/22/upsampling-and-image-segmentation-with-tensorflow-and-tf-slim/
        # make a 3 by 3 test image
        imsize = 3
        x_axis, y_axis = np.ogrid[:imsize, :imsize]
        # repeat along channels 3 times
        img = np.repeat((x_axis+y_axis)[..., np.newaxis], 3, 2) / float(imsize + imsize)

        import cv2
        # from skimage import io
        import matplotlib
        import matplotlib.pyplot as plt

        def display(im):
            figsize = (9, 9)
            _, ax = plt.subplots(1, figsize=figsize)
            height, width = im.shape[:2]
            size = (width, height)
            ax.set_ylim(height + 2, -2)
            ax.set_xlim(-2, width + 2)
            # ax.axis('off')
            if np.max(im) < 1.0:
                # ax.imshow(im)
                pass
            else:
                # ax.imshow(im.astype(np.uint8))
                pass
            ax.imshow(im)
            plt.show()

        display(img)
        # io.imshow(img, interpolation='none')

        # constructed sample layer
        # algorithm:
        #  - BilinearInterpolation
        #  - Conlv
        # conlv_transpose:
        #  - DilatedConv
        #  - Rot90Conv
        sampled = UpSampling(factor=3, algorithm="BilinearInterpolation", conlv_transpose=0)

        # constructed input volume
        inp = Vol(1, img.shape, init_gen=img.transpose([2,0,1]))

        # upsampling
        vol = sampled.forward(inp)

        sampled_img = vol.w.transpose([1,2,0])
        display(sampled_img)

        # assert computed value with standard libraries by extracting comparing image data.

        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=u"%(asctime)s [%(levelname)s]:%(filename)s, %(name)s, in line %(lineno)s >> %(message)s".encode('utf-8'))
    TEST_ALL = False
    if TEST_ALL:
        unittest.main(testRunner=MyTestRunner)
    else:
        suite = unittest.TestSuite()
        suite.addTest(UpSamplingTestCase("test_forward"))
        runner = MyTestRunner()
        runner.run(suite)