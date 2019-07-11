__author__ = 'wangyi'
__emails__ = ['lwang11@mtu.edu',
              'L.WANG@ntu.edu.sg', #staff email address
              'lwang019@e.ntu.edu.sg',
              'yiak.wy@gmail.com']

# Created on 1st Nov 2017
# Updated on 5th July 2019:
#  Modified:
#       costimpl.ConvNet.layers.Layer
#       costimpl.common.Node
#       costimpl.common.Graph
#       costimpl.common.Tensor
#       costimpl.common.Device
#       costimpl.common.Protocol
#       costimpl.common.Randomness.Distribution
#       costimpl.common.Randomness.IncrDistribution
#       costimpl.common.Randomness.SparseDistribution
#       costimpl.common.Randomness.IncrSparseDistribution
#       tests.test_conv_net
#       tests.test_kdtree
#       tests.test_kmean_plus_plus
#       tests.test_svm
#  Added:
#       costimpl.ConvNet.layers.ReluActivation
#       costimpl.ConvNet.layers.BatchNorm
#       costimpl.ConvNet.layers.MaxPooling
#       costimpl.ConvNet.layers.UpSampling
#       costimpl.ConvNet.layers.Dropout
#       costimpl.KMenas++.model
#       costimpl.KdTree.model
#       costimpl.SVM.model

from ..common.node import Node
from ..common.device import CPUDevice
from .vol import Vol
import math
import numpy as np

class ImproperType(Exception):pass
class NotImplemented( Exception):pass
class UnSupportedDevice( Exception):pass
class UnSupportedAlgorithm( Exception):pass

# @todo: TODO Device instance factory
def Device(device_type):
    pass

# @todo: TODO Device plural instances factory
def Device_plura(device_list):
    return []


_c = {
    'device_types': 'cpu',
    'device_list': ['cpu://all'], # ${device_protocol}://, see Protocol parser implementation
}

class Layer(Node):

    def __init__(self, inp, Theta, in_num, out_num, name='Layer', device_types=_c['device_types'], device_list=_c['device_list']):

        # input data might be batch_size * col_size, where a col_size*1 vector isomorphic to input
        self.in_nm = in_num
        self.out_nm = out_num

        # dynamic binding
        self._forward_call = self.forward1

        # check devices
        self._devices = Device_plura(device_list) if self.isSupported(device_types) else None
        if self._devices is None:
            raise UnSupportedDevice("%s not supported yet!" % device_types)

        super(Layer, self).__init__(name, (inp, Theta, (self.out_nm, self.in_nm+1)))

    def forward(self, inp):
        if inp.batch_size == 1:
            inp.w = inp.w[np.newaxis, ...]
            inp.grad = inp.grad[np.newaxis, ...]
        return self._forward_call(inp)

    def forward1(self, inp):
        """
        Vallina implementation, without further optimization and mainly running in CPU mode

        :param inp: Vol
        :return: Vol
        """
        raise NotImplementedError("Not Implemented. Should be implemented in subclass of Layer")

    def forward2(self, inp):
        """

        Used for a real assigned device, may be called underlying libraries of implementation to achieve that goal

        :param inp:
        :return:
        """
        raise NotImplementedError("Not Implemented. Should be implemented in the subclass of Layer")

    def fn_call_forward_all(self, inp):
        if isinstance(inp, Layer):
            inp.add_child(self)
            return self
        elif isinstance(inp, Vol):
            out_vol = self.forward(inp)

            if len(self.children) == 0:
               # if no children, return numeric value directly
                return out_vol

            rets = []
            for childOp in self.children:
                # bottom-up implementation
                ret = childOp.fn_call_forward_all(out_vol)
                rets.append(ret)

            if len(rets) == 1:
                # reduce the dimension
                return rets[0]
            return rets

        else:
            raise ImproperType("Improper type to pass into the layer. Only accept Vol and Layer types!")


    __call__ = fn_call_forward_all

    def bp(self, top_layer):
        """
        :param top_layer: subclasses of Layer
        :return: (nparray, nparray | None, nparray | None)
        """
        raise NotImplementedError("Not Implemented. Should be implemented in subclass of Layer!")

    def bp_all(self, top_layer):
        inp_grad, dW, db = self.bp(top_layer)
        if self.father is not None:
            return self.father.bp_all(self)
        else:
            return inp_grad, dW, db


    # This method is not efficient and need to be optimized in the future
    def img2col(self, vol):
        # img to col: (n, channel, in_nm_h, in_nm_w) => (n, channel * kernel_h * kernel_w, out_nm_h * out_nm_w)
        X = vol.w
        convs = self.filters
        _, kernel_depth, kernel_h, kernel_w = convs.shape
        l = kernel_depth*kernel_h*kernel_w
        size1 = (vol.batch_size, self.channel * kernel_h * kernel_w, self.out_nm_h * self.out_nm_w)
        ret = np.zeros(size1)

        pad_default_val = 0
        try:
            pad_default_val = self.padding_default_val
        except:
            pass

        # loop through samples
        for i in range(vol.batch_size):
            for w0 in range(0, self.out_nm_w): # col first
                pad_left, pad_right = 0, 0
                w1 = -self.pad + w0 * self.strip
                w2 = w1 + kernel_w
                if w1 < 0: w1, pad_left= 0, -w1
                if w1 >= self.in_nm_w:
                    continue
                if w2 < 0:
                    continue
                if w2 > self.in_nm_w:
                    pad_right = w2 - self.in_nm_w
                for h0 in range(0, self.out_nm_h):
                    pad_top, pad_bottom = 0, 0
                    h1 = -self.pad + h0 * self.strip
                    h2 = h1 + kernel_h
                    if h1 < 0: h1, pad_top = 0, -h1
                    if h1 >= self.in_nm_h:
                        continue
                    if h2 < 0:
                        continue
                    if h2 > self.in_nm_h:
                        pad_bottom = h2 - self.in_nm_h

                    kernel_conlv = X[i,:, h1:h2, w1:w2]
                    col = np.pad(kernel_conlv, [(0,0), (pad_top, pad_bottom), (pad_left, pad_right)],
                                 mode='constant',
                                 constant_values=pad_default_val).flatten() # row-major (C-style) order
                    if len(col) != l:
                        raise Exception("Wrong Padding")

                    ret[i,:,h0 * self.out_nm_w + w0] = col[:]

        return ret

    @property
    def grad(self):
        return self.filters.grad

    # @todo : TODO
    def isSupported(self, device_types):
        return True


class FackedConvLayer(Layer):

    def __init__(self, inp, Theta):
        self.inp = inp
        self.Theta = Theta


# The convolution is intensively used for image alike input data. Hence we might have multi-dimensional data.
# For the most use cases, three dimensional filters of size P*P*K are applied on multi dimensional input source.
# For the input layer , the dimension might range from 2 dimensions to 5 dimensions (LiDar depth info added).
# Operation required : (( img2col -> conv -> col2img ) Repeated 2 ~ 3 times -> Pooling -> dropout) Repeated many
# times > (upsampling mirror)
class ConvLayer(Layer):

    def __init__(self, spatial_shape, convs, pad=0, strip=2,
                 lr=1.0,  bias=None, **kw):

        # input Vol instance
        self.inp = None
        self.channel, self.in_nm_h, self.in_nm_w = spatial_shape
        # Please refer to this post for details of conv filter paramter definition
        # Conv optimization: http://mp.weixin.qq.com/s/GKZeTrfTgRXmj29c_XouOQ
        self.filters = convs # Vol
        self.pad = pad
        self.strip = strip
        self.LAYER_TYPE = 'conv'
        self.lr = lr

        K, kernel_depth, kernel_h, kernel_w = convs.shape
        self.bias = bias # Vol

        self.out_nm_d = K
        self.out_nm_w = int(math.floor((self.in_nm_w + self.pad*2 - kernel_w) / self.strip + 1))
        self.out_nm_h = int(math.floor((self.in_nm_h + self.pad*2 - kernel_h) / self.strip + 1))

        # padding defaults to 0
        self.padding_default_val = 0

        # output Vol instance
        self.out = None

        super(ConvLayer, self).__init__(None, convs, self.channel*self.in_nm_h*self.in_nm_w,
                                                     K*(kernel_h*kernel_w + 1),
                                                     name='ConvLayer')

    # using nested For-Loop to implement raw ConvNet forward.
    # This is not efficient and left to be improved in the near future
    # See: https://github.com/karpathy/convnetjs/blob/master/src/convnet_layers_dotproducts.js
    #      https://github.com/costapt/cs231n/blob/master/assignment2/cs231n/im2col.py
    def forward1(self, inp):
        """

        By applying `img2col` borrowed from caffe, we implemented shared parameters convolution with respect the input.
        The parameters consist in the layer are K * (kernel_depth * kernel_h * kernel_w + 1). To reduce parameters, we could
        apply (kernel_h * kernel_w) on original input shifting window and repeated the computation 3 times and sum them into
        an `aggregated ` super pixel value. We will use this concept in our `SpatialDetectron` algorithm for arbiturary 3d points
        convolution.


        :param inp: Vol
        :return: Vol
        """
        self.inp = inp # Vol
        n = inp.batch_size
        # might need to check here
        convs = self.filters
        K, kernel_depth, kernel_h, kernel_w = convs.shape
        size1 = (n, K, self.out_nm_h, self.out_nm_w)
        ret = np.zeros(size1)

        # filters to row
        W_row = convs.w.reshape(K, kernel_depth * kernel_h * kernel_w) # -1

        # img to col: (n, channel, in_nm_h, in_nm_w) => (n, kernel_depth * kernel_h * kernel_w, out_nm_h * out_nm_w)
        X_col = self.img2col(inp)
        self.X_col = X_col
        # loop through samples
        for i in range(n):
            # (K, kd*kh*kw) mul (kd*kh*hw, oh*ow)
            out = np.matmul(W_row, X_col[i,:]) + self.bias.w
            # col2img
            out.resize(K, self.out_nm_h, self.out_nm_w)
            ret[i,:] = out[:]
        self.out = Vol(n, (K, self.out_nm_h, self.out_nm_w), init_gen=ret)
        return self.out

    def bp(self, top_layer):
        """

        The algorithm implemented here based on my mathematical interpretation by partial derivatives on both input data and input parameters.
        By partial derivatives of filters, we concluded that each parameter at (i, kd, kh, kw) is determined by:
            - X[p, kd, kh + q*strip_h, kw + s*strip_w] : input convolution window box
            - top_layer.inp.grad[:, i, q, s], where (p, q, s) loop through (K0, out_nm_h, out_nm_w), i loop through K1:

        Simply put, when (q,s) loop through (out_nm_h, out_nm_w), we actually apply `an altrous conv` to the last layer grad to get the
        gradient of this conv layer parameters:



        By partial derivatives with respect to input data -- `self.inp.w`, bp resets `self.inp.grad`. To compute the derivative of
        self.inp.grad[:, channel, in_nm_h, in_nm_w] denoted as grad[:,k,i,j], first apply algebra replacement to forward convolution index:
            - i <- kh + q*strip_h
            - j <- kw + s*strip_w
        Suppose our `filters = self.convs` which is denoted as W,
        we derived that perception field `W(kh,kw)` is equal to `W(i-q*strip_h, j-s*strip_w)`, we acutually got a fliped version of original convs
        In our implementation, we also check whether we the padded index if out of the filter W boundaries.

        Simply put, when (i,j) loop through (in_nm_h, in_nm_w), we actually apply `a flipped conv` to the last layer grad to get the
         gradient of input data, and use transposed convolution to update input data.



        :param top_layer: Layer
        :return: (nparray, nparray, nparray)
        """
        # bias_grad, partial derivatives of biases

        # dW, partial derivatives of filters
        # convol top_layer.grad with inp
        top_grad = top_layer.inp.grad # work as filters
        W = self.filters.w
        K0, kernel_depth, kernel_h, kernel_w = self.filters.shape
        n, K1, out_nm_h, out_nm_w = top_grad.shape

        # Partial derivatives of filters:
        # A naive explanation:
        # for i in range(K1):
        #     f = top_grad[:,i]
        #     # convolute with inp:
        #     # (n, oh, ow) conv (n, kd*kh*kw, oh, ow) => (K, kd, kh, kw):
        #     for kw in range(kernel_w):
        #         for kh in range(kernel_h):
        #             for kd in range(kernel_depth):
        #                 # self.filters_grad[i, kd, kh, kw] += 1/n *
        # sum_(p,q,s){ X[p, kd, kh + q*strip_h, kw + s*strip_w] * f[q,s] } # pay attention to indice
        #
        # Parameters:
        # i: output data channel index, equal to self.inp.shape[0], denoted as K1
        # p: original input batch sample index, equal to top, denoted as K0
        # q: out_nm_h index
        # s: out_nm_w index
        # Rearrange above loop:
        self.filters.grad[:] = 0.0
        for k in range(K1):
            f = top_grad[:, k]
            for kd in range(kernel_depth):
                for kh in range(kernel_h):
                    for kw in range(kernel_w):
                        uid = (kd*kernel_h+kh)*kernel_w+kw
                        self.filters.grad[k, kd, kh, kw] += np.sum(self.X_col[:,uid] * f.reshape(-1, out_nm_h * out_nm_w))

        # partial derivatives of inp
        # opposite to forward , inp computed in flipped direction
        # (n, channel, in_nm_h, in_nm_w) <= (n, K , oh, ow) conv flipped(filter)
        self.inp.grad[:] = 0.0
        for k in range(self.channel):
            for i in range(self.in_nm_h):
                for j in range(self.in_nm_w):

                    # grad (n, K, oh, ow) conlv flipped(f) (K, kernel_depth, kernel_h, kernel_w)
                    self.conlv(self.inp.grad, top_grad, W, (k,i,j))

        # partial derivatives of bias
        for d in range(K1):
            f = top_grad[:, d]
            self.bias.grad[d] = np.sum(f)

        return self.inp.grad, self.filters.grad, self.bias.grad

    # Transposed convolution
    def conlv(self, target, grad, convs, index):
        '''
        Transposed Convolution

        :param target: np.array, destination
        :param grad: np.array, top_diff
        :param convs: np.array, original convolution
        :param index: tuple, destination index
        :return:
        '''
        K0, kernel_depth, kernel_h, kernel_w = convs.shape
        k,i,j = index
        for h in range(self.out_nm_h):
            for w in range(self.out_nm_w):
                if i-h*self.strip+self.pad < 0 or i-h*self.strip+self.pad >= kernel_h or \
                   j-w*self.strip+self.pad < 0 or j-w*self.strip+self.pad >= kernel_w:
                    continue
                try:
                    target[:,k,i,j] += np.matmul(grad[:,:,h,w], convs[:, k, i-h*self.strip+self.pad, j-w*self.strip+self.pad])
                except Exception as e:
                    raise(e)


class FullyCnnLayer(Layer):
    """
    See a naive implementation inspired from my solution submitted to Andrew N.G's coursera deeplearning course in 2014 and 2015 where I passed
    server tests with 100% scores!

    logistic implementation with L1, L2 normalization experiments solution provided:
    fully connected neural network implementation solution provided:

    """
    pass


class AtrousConvLayer(Layer):
    """
    AtrousConv (also called Dilate Convolution) correspond to the backpropogation algorithm with respect to filters or
    gradient of them being applied to the input in a forward process.
    """
    pass


class BatchNorm(Layer):

    def __init__(self, frazed=False, gamma=1, beta=0, bn_params={}, mode='trainning'):
        # input vol instance
        self.inp = None
        self.LAYER_TYPE = 'batch_norm'
        # Not used for the moment TODO
        self.frazed = frazed # Mask RCNN implementation for details

        # parameters
        self.spatial_size = None
        self.gamma = gamma
        self.beta = beta

        # the defaul values borrow from cs231n, I didnt find out reasons why it is good, maybe it is not.
        self.epilon = bn_params.get('epilon', 1e-5)
        self.stat_momentum = bn_params.get('stat_momentum', 0.9)

        # parameters used inside forward operation, needed to be persistent
        self.running_mean = bn_params.get('running_mean', None)
        self.running_var = bn_params.get('running_var' , None)

        # learnable parameters
        # to make a reasonable difference, W and bias should have the same size of gradient spatial shape
        # where parital gamma_0 (scalar) = sum_(i) { partial J over partial y_i0 * partial y_i0 over partial gamma_0 }
        # which means y_i0 can only be computed from gamma_i0 values. Hence if gamma is a scalar equal to gamma_0, that does
        # not make sense

        self._param_initialized = False
        self.W = Vol(1, (1,), init_gen=np.array([self.gamma,])) if np.isscalar(self.gamma) \
            else Vol(1, (1,), init_gen=None) # params
        self.bias = Vol(1, (1,), init_gen=np.array([self.beta,])) if np.isscalar(self.beta) \
            else Vol(1, (1,), init_gen=None) # params

        # bn_params
        # algorithm
        # despite sample mean and variance suggested in original paper, cs231n also suggests torch7 batch norm implementation
        # algorithm "RunningAverages"
        self.algorithm = bn_params.get("algorithm", "SampleStat")
        self.supported_algorithms = [
            "SampleStat",
            "RunningAverages" # see Torch7 batch norm implementation
        ]

        self.mode = mode
        # output Vol instance
        self.out = None

        super(BatchNorm, self).__init__(None, None, 1, 1, name='BatchNorm')

    def forward1(self, inp):
        self.inp = inp
        X = inp.w
        n = inp.batch_size
        spatial_size = inp.spatial_size
        self.spatial_size = spatial_size

        if self.algorithm not in self.supported_algorithms:
            raise UnSupportedAlgorithm("Does not support %s. We only support %s" % (self.algorithm, self.supported_algorithms))

        if self._param_initialized is False:
            identity = np.ones(spatial_size)

            self.W.reset_spatial_size(spatial_size, fill=identity * self.gamma)
            self.bias.reset_spatial_size(spatial_size, fill=identity * self.beta)

            self._param_initialized = True

        W = self.W.w
        bias = self.bias.w

        if self.mode == 'validation':
            shifted = X - self.running_mean
            std = np.sqrt(self.running_var + self.epilon)
            normalized = shifted * 1.0 / std
            affine = normalized * W + bias
            self.out = Vol(n, spatial_size, init_gen=affine)
            return self.out

        if self.mode is not 'trainning':
            raise ValueError("Invalide forward batchnorm mode <%s>" % self.mode)

        # stat computation
        miu = np.mean(X, axis=0)
        shifted = X - miu
        variance = np.sum(shifted**2, axis=0) / n
        std = np.sqrt(variance + self.epilon)
        normalized = shifted * 1.0 / std
        affine = normalized * W + bias

        self.normalized = normalized
        self.shifted = shifted
        self.variance = variance

        if self.algorithm is "SampleStat":
            self.out = Vol(n, inp.spatial_size, init_gen=affine)
            return self.out
        # see cs231n implementation for reference
        if self.algorithm is "RunningAverages":
            """
            The running_mean and running_var are used in inference mode where we have no idea of what statistics should be used from input.
            Hence we turn to running batch of data to gather statistic information.
            """
            self.running_mean = self.running_mean or np.zeros(spatial_size, dtype=X.dtype)
            self.running_var  = self.running_var or np.zeros(spatial_size, dtype=X.dtype)

            self.running_mean = self.momentum * self.running_mean + (1-self.momentum) * miu
            self.running_var  = self.momentum * self.running_var + (1-self.momentum) * variance

            self.out = Vol(n, spatial_size, init_gen=affine)
            return self.out
        else:
            raise NotImplementedError("%s not implemented yet!" % self.algorithm)

    def bp(self, top_layer):
        grad = top_layer.inp.grad
        spatial_size = self.spatial_size or grad.spatial_size

        if self._param_initialized is False:
            identity = np.ones(spatial_size)

            self.W.reset_spatial_size(spatial_size, fill=identity * self.gamma)
            self.bias.reset_spatial_size(spatial_size, fill=identity * self.beta)

            self._param_initialized = True

        W = self.W.w
        N = grad.shape[0]
        # bias_grad, partial derivatives of biases, no parmeters in this layer
        db = np.sum(grad, axis=0) # the derivative of beta
        self.bias.grad[:] = db[:]
        # dW, no parameters in this layer
        dW = np.sum(self.normalized * grad, axis=0) # the derivative of gamma
        self.W.grad[:] = dW[:]

        # partial derivatives of inp

        dx_bar = grad * W
        inverse_std = 1.0 / np.sqrt(self.variance + self.epilon)
        dvar = np.sum(dx_bar * self.shifted, axis=0) * -0.5 * inverse_std**3
        dmiu_1 = dx_bar * inverse_std
        dmiu_2 = 2 * dvar * np.ones(grad.shape) * self.shifted / N
        dx1 = dmiu_1 + dmiu_2
        dmiu = -1 * np.sum(dx1, axis=0)
        dx2 = dmiu * 1.0 / N
        self.inp.grad[:] = dx1 + dx2
        return self.inp.grad, self.W.grad, self.bias.grad


class ReluActivation(Layer):

    def __init__(self):
        # input Vol instance
        self.inp = None
        self.LAYER_TYPE = 'relu'
        # output Vol instance
        self.out = None

        super(ReluActivation, self).__init__(None, None, 1, 1, name='ReluActivation')

    def forward1(self, inp):
        self.inp = inp
        X = inp.w
        out = np.maximum(0, X)
        self.out = Vol(inp.batch_size, inp.spatial_size, init_gen=out)
        return self.out

    def bp(self, top_layer):
        # bias_grad, partial derivatives of biases, no parameters in this layer
        db = None
        # dW, no parameters in this layer
        dW = None

        # partial derivatives of inp
        top_grad = top_layer.inp.grad
        out = top_layer.inp.w
        self.inp.grad[:] = top_grad * (np.maximum(0, out) > 0)
        return self.inp.grad, dW, db


class MaxPooling(Layer):pass


class UpSampling(Layer):
    """
    Upsampling is for resampling and interpolation of your input up to higher resolution. The terminology comes from Signal
    Processing. In convolution neural network, since maxpooling is non invertible, upsampling is an approximation of
    reverse operation of max pooling, which used commonly by the Feature Pyramid Network (FPN) backbone.

    FPN and ResNet50(101, 152, ...) form the foundation of the state of the art in the network architecture for features extraction
     in the realm of objects detection. FPN makes different scales of the same feature map and composes two stages of layers
     stacking method: bottom-up and top-down. It is top-down where we need `upsampling` from the smaller resolution feature map:

        P_i = Add(Upsampling(P_{i+1}), Conv2D()(Ci)) 2<= i < 5
        P_5 = Conv2D()(C_5)

    There are several implementation for that purpose:

        - Unpooling: Unlike MaxPooling, Unpooling repeats nearest neighbor. From [keras documentation](https://github.com/keras-team/keras/blob/master/keras/layers/convolutional.py#L1974),
        we see that upsampling repeats rows and columns data by `factor`. As we can see from our tests, the operation loses details
        in the bigger resampled feature map.

        - Deconvolution: The key idea is that we can perform the reverse of convolution and preserve the connectivity to obtain the original
        input resolution. We have implemented convolution layer and we know that the input data could be updated using
        `transposed convolution`[1] if stride is equal to 1 and `dilate`[2][3] for Bilinear Convolution Kernel[4][5].

        - BilinearInterpolation: see [scikit-image implementation](https://scikit-image.org/docs/dev/api/skimage.transform.html#skimage.transform.rescale),
        it uses interpolation to upsample feature maps, and performs well both in details and overall effects.



    In this implementation, I provide you with additional methods and test codes used for unit tests. I also recommand you to
    read this article to understand it better:

        - http://warmspringwinds.github.io/tensorflow/tf-slim/2016/11/22/upsampling-and-image-segmentation-with-tensorflow-and-tf-slim/

    [Maximum Sampling Theorem](http://avisynth.nl/index.php/Resampling):

            - The sampling rate of samples should be double the maximum of frequences.

    This implementation will compute best upsampling rates and automatically inference sampling factor. The original upsampling factor
    corresponds to sampling frequency. By Maximum Sampling Theorem, we could derive a cheap size for convolution kernel maintaining
    the maximum information of original signals or feature maps.

    The terminology of factor may come from the [scikit-image implementaiton](https://github.com/scikit-image/scikit-image/blob/master/skimage/transform/_warps.py#L187),
    is the compression rate from an unsampled over its downsampled feature map.

    [1] https://www.tensorflow.org/api_docs/python/tf/nn/conv2d_transpose
    [2] https://datascience.stackexchange.com/questions/6107/what-are-deconvolutional-layers
    [3] https://github.com/yiakwy/conv_arithmetic
    [4] https://dsp.stackexchange.com/questions/53200/bilinear-interpolation-implemented-by-convolution
    [5] http://www.sfu.ca/~gchapman/e895/e895l11.pdf
    """

    def __init__(self, factor=1, target_channels=None, algorithm='BilinearInterpolation', conlv_transpose=0):
        """

        :param factor: inverse of the cmpr ratio, used in Deconlv algorithm
        :param target_channels:
        :param algorithm:
        :return:
        """
        # used in BiliearInterpolation
        self.factor = factor
        # used Deconlv
        self.stride = factor
        self.target_channels = target_channels

        # filters used for upsampling with transposed convolution algorithm
        self.filters = None
        self.pad = None
        self.strip = self.stride
        self.LAYER_TYPE="Upsampling"

        # algorithms
        self.algorithm = algorithm
        self.conlv_transpose = conlv_transpose
        # see discussion on implementation of deconvolution in https://github.com/tensorflow/tensorflow/issues/256#issuecomment-162257789
        self.supported_conlv_transpose = {
            "Rot90Conv": 0,
            "DilatedConv":1, # https://datascience.stackexchange.com/questions/6107/what-are-deconvolutional-layers
        }
        self.supported_algorithms = {
            "Conlv": (0,1),
            "BilinearInterpolation": 2
        }

        # output Vol instance
        self.out = None
        # by default, the layer is eliminated from trainning process.
        self.frazed = True

        # padding defaults
        self.padding_default_val = 0.0

        super(UpSampling, self).__init__(None, None, 1, 1, name='UpSampling')

    def Deconlv(self, inp):
        self.inp = inp # update reference
        n = inp.batch_size
        self.channel, self.in_nm_h, self.in_nm_w = inp.spatial_size

        # adapted codes of tensorflow implementation from http://warmspringwinds.github.io/tensorflow/tf-slim/2016/11/22/upsampling-and-image-segmentation-with-tensorflow-and-tf-slim/
        def _get_kernel_size(stride):
            """
            :param stride: the stride of the transposed convolution
            :return: kernel_size
            """
            return 2 * stride - stride % 2

        def get_kernel_weights(kernel_size):
            """
            :param kernel_size: higher resolution size
            :return: 2D bilinear convolution kernel
            """
            x_axis, y_axis = np.ogrid[:kernel_size, :kernel_size]
            factor = int((kernel_size + 1) / 2)
            centre = factor - 1 if kernel_size % 2 == 1 else factor - 0.5
            return (1-np.abs(x_axis-centre)/float(factor)) * \
                   (1-np.abs(y_axis-centre)/float(factor))

        def get_upsample_kernels(stride, filters, channels):
            kernel_size = _get_kernel_size(stride)
            convs = np.zeros((filters, channels, kernel_size, kernel_size), dtype=np.float32)

            kernel_weights = get_kernel_weights(kernel_size)

            for i in xrange(filters):
                kernel = np.repeat(kernel_weights[np.newaxis, ...], 3, 0)
                convs[i, :] = kernel[:]

            return convs

        # compute filters
        self.target_channels = self.target_channels or self.channel

        # make this layer non-trainable, and compute the best sampling rates
        convs = get_upsample_kernels(self.stride, self.target_channels, self.channel)

        K, kernel_depth, kernel_h, kernel_w = convs.shape
        self.filters = Vol(K, (kernel_depth, kernel_h, kernel_w), init_gen=convs)

        # compute out_nm
        self.out_nm_d = K
        # see tf.layers.conv2d_transpose, when  padding='SAME'
        self.out_nm_w = self.in_nm_h * self.factor
        self.out_nm_h = self.in_nm_w * self.factor

        self.pad = int(((self.in_nm_h - 1) * self.strip + kernel_h - self.out_nm_h) / float(2))

        res = np.zeros((n, K, self.out_nm_h, self.out_nm_w))
        # transposed filters to row
        if self.conlv_transpose == self.supported_conlv_transpose["Rot90Conv"]:
            self.pad = int(((self.out_nm_h - 1) * self.strip + kernel_h - self.in_nm_h) / float(2))
            W_row = convs.transpose((0, 1, 3, 2)).reshape(K, kernel_depth * kernel_h * kernel_w) # -1

            # img to col: (n, channel, in_nm_h, in_nm_w) => (n, kernel_depth * kernel_h * kernel_w, out_nm_h * out_nm_w)
            X_col = self.img2col(inp)

            # perform 2d transposed convolution
            for i in range(n):
                # (K, kd*kh*kw) mul (kd*kh*hw, oh*ow)
                out = np.matmul(W_row, X_col[i,:])
                # col2img
                out.resize(K, self.out_nm_h, self.out_nm_w)
                res[i,:] = out[:]

        elif self.conlv_transpose == self.supported_conlv_transpose["DilatedConv"]:
            # (n, channel, oh, ow) <= (n, K , in_nm_h, in_nm_w) conv flipped(convs)
            X = inp.w
            W = convs
            for k in range(self.channel):
                for i in range(self.out_nm_h):
                    for j in range(self.out_nm_w):

                        # (n, K, ih, iw) conlv flipped(f) (K, kernel_depth, kernel_h, kernel_w)
                        self.conlv(res, X, W, (k,i,j))

        else:
            raise UnSupportedAlgorithm("%s is not supported!" % self.algorithm)

        self.out = Vol(n, (K, self.out_nm_h, self.out_nm_w), init_gen=res)
        return self.out

    # @todo : TODO
    def Unpooling(self, inp):
        pass

    def BilinearInterpolation(self, inp):
        self.inp = inp
        n = inp.batch_size
        self.channel, self.in_nm_h, self.in_nm_w = inp.spatial_size

        # compute out_nm
        self.out_nm_w = self.in_nm_h * self.factor
        self.out_nm_h = self.in_nm_w * self.factor

        # adapted codes from https://github.com/keras-team/keras/blob/master/keras/layers/convolutional.py#L1974
        # see Keras.backend.resize_image for details
        X = inp.w
        out = X

        out = np.repeat(out, self.factor, axis=-2)
        out = np.repeat(out, self.factor, axis=-1)

        self.out = Vol(n, (self.channel, self.out_nm_h, self.out_nm_w), init_gen=out)
        return self.out

    def forward1(self, inp):
        self.inp = inp
        if self.algorithm is "Conlv":
            return self.Deconlv(inp)
        elif self.algorithm is "BilinearInterpolation":
            return self.BilinearInterpolation(inp)
        else:
            raise NotImplementedError("%s Not Implemented Yet!" % self.algorithm)

    # frazed in trainning process, This will be excluded from backpropogation, compute derivatives with respect to the latest
    # non-frazed layer
    def bp(self, inp):
        pass

    # Transposed convolution
    def conlv(self, target, grad, convs, index):
        '''
        Transposed Convolution

        :param target: np.array, destination
        :param grad: np.array, top_diff
        :param convs: np.array, original convolution
        :param index: tuple, destination index
        :return:
        '''
        K0, kernel_depth, kernel_h, kernel_w = convs.shape
        k,i,j = index
        for h in range(self.in_nm_h):
            for w in range(self.in_nm_w):
                if i-h*self.strip+self.pad < 0 or i-h*self.strip+self.pad >= kernel_h or \
                   j-w*self.strip+self.pad < 0 or j-w*self.strip+self.pad >= kernel_w:
                    continue
                try:
                    target[:,k,i,j] += np.matmul(grad[:,:,h,w], convs[:, k, i-h*self.strip+self.pad, j-w*self.strip+self.pad])
                except Exception as e:
                    raise(e)