__author__ = 'wangyi'
# Created on 1st Nov 2017

from ..common.node import Node
import math
import numpy as np

class Layer(Node):

    def __init__(self, input, Theta, in_num, out_num):

        # input data might be batch_size * col_size, where a col_size*1 vector isomorphic to input
        self.in_nm = in_num
        self.out_nm = out_num

        # parsing data
        data = None
        # parsing name
        name = None
        super(Layer, self).__init__(name, data)

    def forward(self):
        pass

    def bp(self):
        pass

    def img2col(self, vol):
        return vol.flatten()

# The convolution is intensively used for image alike input data. Hence we might have multi-dimensional data.
# For the most use cases, three dimensional filters of size P*P*K are applied on multi dimensional input source.
# For the input layer , the dimension might range from 2 dimensions to 5 dimensions (LiDar depth info added).
# Operation required : (( img2col -> conv -> col2img ) Repeated 2 ~ 3 times -> Pooling -> dropout) Repeated many
# times > (upsampling mirror)
class ConvLayer(Layer):

    def __init__(self, inp, n, spatial_shape, convs, K, pad=0, strip=2,
                 lr=1.0, default_conv="Gaussion", bias=None, **kw):
        self.inp = inp # of size (n,<spatial dim>)
        self.out = None
        self.grad = None
        self.n = n
        # assert(inp, np.array)
        self.in_nm_w, self.in_nm_h, self.channel = spatial_shape
        # Please refer to this post for details of conv filter paramter definition
        # Conv optimization: http://mp.weixin.qq.com/s/GKZeTrfTgRXmj29c_XouOQ
        self.filters = convs
        self.K = K
        self.pad = pad
        self.strip = strip
        self.LAYER_TYPE = 'conv'
        self.lr = lr
        self.default_conv = default_conv
        self.bias = bias or 1

        cout, kernel_w, kernel_h, kernel_depth = self.filters.shape
        # check dim
        if kernel_w is not self.in_nm_h or \
            kernel_h is not self.in_nm_w or \
            kernel_depth is not self.channel:
            raise Exception("inp dims do not match the conv size")
        self.P = None
        if kernel_w == kernel_h:
            self.p = kernel_w
        self.out_nm_w = math.floor((self.in_nm_w + self.pad*2 - kernel_w) / self.strip + 1)
        self.out_nm_h = math.floor((self.in_nm_h + self.pad*2 - kernel_h) / self.strip + 1)

        # TO DO:
        # Initialize filters

    def uid(self, argc, key, dims):
        ret = 1.0
        i = 0
        factor = 1

        while i < argc:
            factor *= dims[i]
            i += 1

        i = 0
        while i < argc:
            ret += (key[i]) * factor
            factor /= dims[argc-1-i]
            i += 1

        return ret

    def diff(self, inp, W_col, filters):
        pass

    def convolute1(self, inp, W_col, filters):
        cout, kernel_w, kernel_h, kernel_depth = filters.shape
        size1 = (self.n, self.out_nm_w*self.out_nm_h)
        ret = np.zeros(size1)
        for i, X in enumerate(inp):

            j = 0
            for w in range(-self.pad, kernel_w+self.pad, self.strip):
                for h in range(-self.pad, kernel_h+self.pad, self.strip): # column first

                    # conv
                    start, end = 0, -1
                    w0, w1, w2 = w, w + self.strip, 0
                    if w0 < 0:
                        w0 = 0
                        if w1 < 0:
                            continue
                        w2 = -w
                    h0, h1, h2 = h, h + self.strip, 0
                    if h0 < 0:
                        h0 = 0
                        if h1 < 0:
                            continue
                        h2 = -h

                    delta = self.uid(3, (w2, h2, 0), (kernel_w, kernel_h, kernel_depth))
                    start += delta
                    end -= delta
                    # fft might be used here
                    ret[i,j] = np.dot(X[w0:w1, h0:h1, :], W_col[start:end])
                    j += 1

        return ret

    # using four nested For-Loop to implement raw ConvNet forward.
    # This is not efficient and left to be improved in the near future
    def forward1(self, inp):
        self.inp = inp
        # assuming shape does not change
        cout, kernel_w, kernel_h, kernel_depth = self.filters.shape
        size1 = (self.n, self.out_nm_w*self.out_nm_h, cout)
        ret = np.zeros(size1)
        # depth  * cout
        for i, f in enumerate(self.convs):
            # img2col
            W_col = self.img2col(f) # 1 dimensional vec
            out = self.convolute1(self.inp, W_col, self.filters)
            ret[:,i] = out[:]

        # the val of size (self.n,out_nm_w*out_nm_h,cout)
        # col2img
        ret.resize(self.n, self.out_nm_w, self.out_nm_h, cout)
        self.out = ret
        return ret


    def bp(self, top_layer):
        # back propagation in practice
        # return cost, grad of weights; the grad of weights will be stored in the
        # based on chain rule and observation of conv, the partial derivatives are given
        # another spatial flipped convolution over gradients from top node
        size1 = (len(self.filters), self.kernel_w*self.kernel_h*self.kernel_depth) # cout * p * j * k
        ret = np.zeros(size1)
        # top_layer.grad: of size eq to (n, h, w, d) functions as a family of filters (h,w,d) == (out_nm_w, out_nm_h, cout)
        # self.inp: of size eq to (self.n, self.in_nm_w, self.in_nm_h, self.channel)
        for i, f in enumerate(top_layer.grad):
            # img2col
            W_col = self.img2col(f)
            out = self.diff(self.inp, W_col, top_layer.grad)
            ret[:,i] = out[:]

        # the val of size (self.n, l)
        pass





