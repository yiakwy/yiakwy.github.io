ConvNet
=======

## Caffe Similar Achitecture in Pure Python

> A Usage Example

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

> The benchmark borrow techniques from Numeric Computing Mathematics and utilize functionaility
provided by Stanford University

```
/anaconda/bin/python "/Users/wangyi/GitHub/yiak.github.io/Correlation Metrics/ConvNet/tests/test_conv_net.py"
2017-12-06 12:53:43,126 [INFO]:test_conv_net.py, ConvLayer, in line 142 >> tests/test_conv_net.ConvLayerTestCase Finish numeric computation with elapsed time 4.09476804733
2017-12-06 12:53:43,136 [INFO]:test_conv_net.py, ConvLayer, in line 151 >> tests/test_conv_net.ConvLayerTestCase Finish ConvLayer.bp computation with elapsed time 0.00484800338745
2017-12-06 12:53:43,136 [INFO]:test_conv_net.py, ConvLayer, in line 153 >> tests/test_conv_net.ConvLayerTestCase Testing layer.bp(top_layer) inp_grad
2017-12-06 12:53:43,136 [INFO]:test_conv_net.py, ConvLayer, in line 155 >> tests/test_conv_net.ConvLayerTestCase Difference: 1.45838153378e-09
2017-12-06 12:53:43,137 [INFO]:test_conv_net.py, ConvLayer, in line 158 >> tests/test_conv_net.ConvLayerTestCase Testing layer.bp(top_layer) filters_grad
2017-12-06 12:53:43,137 [INFO]:test_conv_net.py, ConvLayer, in line 160 >> tests/test_conv_net.ConvLayerTestCase Difference: 4.13542299065e-10
2017-12-06 12:53:43,137 [INFO]:test_conv_net.py, ConvLayer, in line 163 >> tests/test_conv_net.ConvLayerTestCase Testing layer.bp(top_layer) bias_grad
2017-12-06 12:53:43,137 [INFO]:test_conv_net.py, ConvLayer, in line 165 >> tests/test_conv_net.ConvLayerTestCase Difference: 2.53413272295e-11
Successful!

2017-12-06 12:53:43,138 [INFO]:test_conv_net.py, ConvLayer, in line 83 >> tests/test_conv_net.ConvLayerTestCase I have trimmed the test data, hence, epilon as 1.0e-2 is correct. The original data can achieve 1.0e-6 precision
2017-12-06 12:53:43,138 [INFO]:test_conv_net.py, ConvLayer, in line 84 >> tests/test_conv_net.ConvLayerTestCase Testing layer.forward
2017-12-06 12:53:43,138 [INFO]:test_conv_net.py, ConvLayer, in line 86 >> tests/test_conv_net.ConvLayerTestCase Difference: 0.00228882833787
Successful!


----------------------------------------------------------------------
Ran 2 tests in 4.108s

OK

Process finished with exit code 0
```
