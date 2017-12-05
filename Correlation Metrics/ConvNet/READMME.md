ConvNet
=======

## Caffe Similar Achitecture in Pure Python

bias = Vol(1, size1, init_gen=b)
inp = Vol(2, size2, init_gen=X)
convs = Vol(3, size3, init_gen=Theta)
conv\_param = {'strip':2, 'pad':1}
conv\_param['bias'] = bias

layer = ConvNet(X.shape[1:], convs, \*\*conv\_param)
vol\_output = layer.forward(inp)
inp\_grad, filters\_grad, bias\_grad = layer.bp(vol\_output)

## Benchmark Test

```
/anaconda/bin/python "/Users/wangyi/GitHub/yiak.github.io/Correlation Metrics/ConvNet/tests/test_conv_net.py"
2017-12-05 20:58:19,736 [INFO]:test_conv_net.py, ConvLayer, in line 141 >> tests/test_conv_net.ConvLayerTestCase Finish numeric computation with elapsed time 4.31141901016
2017-12-05 20:58:19,748 [INFO]:test_conv_net.py, ConvLayer, in line 150 >> tests/test_conv_net.ConvLayerTestCase Finish ConvLayer.bp computation with elapsed time 0.0062530040741
2017-12-05 20:58:19,748 [INFO]:test_conv_net.py, ConvLayer, in line 152 >> tests/test_conv_net.ConvLayerTestCase Testing layer.bp(top_layer) inp_grad
2017-12-05 20:58:19,748 [INFO]:test_conv_net.py, ConvLayer, in line 154 >> tests/test_conv_net.ConvLayerTestCase Difference: 1.64026257505e-09
2017-12-05 20:58:19,748 [INFO]:test_conv_net.py, ConvLayer, in line 157 >> tests/test_conv_net.ConvLayerTestCase Testing layer.bp(top_layer) filters_grad
2017-12-05 20:58:19,749 [INFO]:test_conv_net.py, ConvLayer, in line 159 >> tests/test_conv_net.ConvLayerTestCase Difference: 1.30125156197e-09
2017-12-05 20:58:19,749 [INFO]:test_conv_net.py, ConvLayer, in line 162 >> tests/test_conv_net.ConvLayerTestCase Testing layer.bp(top_layer) bias_grad
2017-12-05 20:58:19,749 [INFO]:test_conv_net.py, ConvLayer, in line 164 >> tests/test_conv_net.ConvLayerTestCase Difference: 5.81767207296e-12
2017-12-05 20:58:19,750 [INFO]:test_conv_net.py, ConvLayer, in line 82 >> tests/test_conv_net.ConvLayerTestCase I have trimmed the test data, hence, epilon as 1.0e-2 is correct. The original data can achieve 1.0e-6 precision
2017-12-05 20:58:19,750 [INFO]:test_conv_net.py, ConvLayer, in line 83 >> tests/test_conv_net.ConvLayerTestCase Testing layer.forward
2017-12-05 20:58:19,750 [INFO]:test_conv_net.py, ConvLayer, in line 85 >> tests/test_conv_net.ConvLayerTestCase Difference: 0.00228882833787

----------------------------------------------------------------------
Ran 2 tests in 4.326s

OK

Process finished with exit code 0
```
