ConvNet
=======

## Caffe Similar Achitecture in Pure Python for Scientific Research

The project implements some of core component of neural network and provides
test programs from different angles.

Before 2014, many researchers are interested high level optimization solution for neural netowrk, such as fully connected neural network.

As the neural netowrk envolves into a dynamic computing graph, different operators are proposed from 2015 to 2017

Nowadays, more research work focuses on the construction of network with different backbones. This project gives us opportunities to rethink about core operators implemented in popular neural netowrk framework.

## An Usage Example

```python
bias = Vol(1, size1, init_gen=b)
inp = Vol(2, size2, init_gen=X)
convs = Vol(3, size3, init_gen=Theta)
conv_param = {'strip':2, 'pad':1}
conv_param['bias'] = bias

layer = ConvNet(X.shape[1:], convs, **conv_param)
vol_output = layer.forward(inp)
inp_grad, filters_grad, bias_grad = layer.bp(vol_output)
```

## Benchmark Test

> The benchmark borrows techniques from Numeric Computing Mathematics and utilizes utilities
provided by Stanford University

```
/anaconda/bin/python /Applications/PyCharm.app/Contents/helpers/pydev/pydevd.py --multiproc --client 127.0.0.1 --port 49974 --file "/Users/wangyi/GitHub/yiak.github.io/Correlation Metrics/ConvNet/tests/test_conv_net.py"
/anaconda/lib/python2.7/site-packages/IPython/utils/traitlets.py:5: UserWarning: IPython.utils.traitlets has moved to a top-level traitlets package.
  warn("IPython.utils.traitlets has moved to a top-level traitlets package.")
pydev debugger: process 70855 is connecting

Connected to pydev debugger (build 139.1001)
2019-07-07 17:43:16,408 [INFO]:test_conv_net.py, ConvNet, in line 295 >> tests/test_conv_net.BatchNormTestCase Finish numeric computation with elapsed time 0.0188329219818
2019-07-07 17:43:16,408 [INFO]:test_conv_net.py, ConvNet, in line 306 >> tests/test_conv_net.BatchNormTestCase Finish BatchNorm.bp computation with elapsed time 0.000133037567139
2019-07-07 17:43:16,409 [INFO]:test_conv_net.py, ConvNet, in line 308 >> tests/test_conv_net.BatchNormTestCase Testing layer.bp(top_layer) inp_grad
2019-07-07 17:43:16,409 [INFO]:test_conv_net.py, ConvNet, in line 310 >> tests/test_conv_net.BatchNormTestCase Difference: 3.2186236349141194e-10
2019-07-07 17:43:16,409 [INFO]:test_conv_net.py, ConvNet, in line 313 >> tests/test_conv_net.BatchNormTestCase Testing layer.bp(top_layer) dW~Difference w.r.t. gamma
2019-07-07 17:43:16,409 [INFO]:test_conv_net.py, ConvNet, in line 315 >> tests/test_conv_net.BatchNormTestCase Difference: 2.770052941835114e-08
2019-07-07 17:43:16,410 [INFO]:test_conv_net.py, ConvNet, in line 318 >> tests/test_conv_net.BatchNormTestCase Testing layer.bp(top_layer) db~Difference w.r.t. beta
2019-07-07 17:43:16,410 [INFO]:test_conv_net.py, ConvNet, in line 320 >> tests/test_conv_net.BatchNormTestCase Difference: 3.275657729593016e-12
Successful with <BatchNormTestCase.test_bp>!

Successful with <BatchNormTestCase.test_forward>!

2019-07-07 17:43:29,999 [INFO]:test_conv_net.py, ConvNet, in line 142 >> tests/test_conv_net.ConvLayerTestCase Finish numeric computation with elapsed time 13.5871639252
2019-07-07 17:43:30,025 [INFO]:test_conv_net.py, ConvNet, in line 151 >> tests/test_conv_net.ConvLayerTestCase Finish ConvLayer.bp computation with elapsed time 0.00559186935425
2019-07-07 17:43:30,025 [INFO]:test_conv_net.py, ConvNet, in line 153 >> tests/test_conv_net.ConvLayerTestCase Testing layer.bp(top_layer) inp_grad
2019-07-07 17:43:30,025 [INFO]:test_conv_net.py, ConvNet, in line 155 >> tests/test_conv_net.ConvLayerTestCase Difference: 1.4249806831849532e-08
2019-07-07 17:43:30,026 [INFO]:test_conv_net.py, ConvNet, in line 158 >> tests/test_conv_net.ConvLayerTestCase Testing layer.bp(top_layer) filters_grad
2019-07-07 17:43:30,026 [INFO]:test_conv_net.py, ConvNet, in line 160 >> tests/test_conv_net.ConvLayerTestCase Difference: 6.165459855631704e-10
2019-07-07 17:43:30,026 [INFO]:test_conv_net.py, ConvNet, in line 163 >> tests/test_conv_net.ConvLayerTestCase Testing layer.bp(top_layer) bias_grad
2019-07-07 17:43:30,026 [INFO]:test_conv_net.py, ConvNet, in line 165 >> tests/test_conv_net.ConvLayerTestCase Difference: 5.1677473106768316e-11
Successful with <ConvLayerTestCase.test_bp>!

2019-07-07 17:43:30,029 [INFO]:test_conv_net.py, ConvNet, in line 83 >> tests/test_conv_net.ConvLayerTestCase I have trimmed the test data, hence, epilon as 1.0e-2 is correct. The original data can achieve 1.0e-6 precision
2019-07-07 17:43:30,029 [INFO]:test_conv_net.py, ConvNet, in line 84 >> tests/test_conv_net.ConvLayerTestCase Testing layer.forward
2019-07-07 17:43:30,030 [INFO]:test_conv_net.py, ConvNet, in line 86 >> tests/test_conv_net.ConvLayerTestCase Difference: 0.002288828337874726
Successful with <ConvLayerTestCase.test_forward>!

2019-07-07 17:43:47,510 [INFO]:test_conv_net.py, ConvNet, in line 207 >> tests/test_conv_net.ReluActivationTestCase Finish numeric computation with elapsed time 17.4793348312
2019-07-07 17:43:47,554 [INFO]:test_conv_net.py, ConvNet, in line 225 >> tests/test_conv_net.ReluActivationTestCase Finish stacked layer (ConvLayer -> ReluActivation).bp_all computation with elapsed time 0.0232589244843
2019-07-07 17:43:47,555 [INFO]:test_conv_net.py, ConvNet, in line 227 >> tests/test_conv_net.ReluActivationTestCase Testing layer.bp_all(top_layer) inp_grad
2019-07-07 17:43:47,555 [INFO]:test_conv_net.py, ConvNet, in line 229 >> tests/test_conv_net.ReluActivationTestCase Difference: 2.4689621312297805e-09
Successful with <ReluActivationTestCase.test_bp_all>!


----------------------------------------------------------------------
Ran 5 tests in 31.167s

OK

Process finished with exit code 0
```
