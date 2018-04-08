__author__ = 'wangyi'
# Created on 1st Nov 2017

from ..common.node import Node
from .vol import Vol
import math
import numpy as np

class Layer(Node):

    def __init__(self, inp, Theta, in_num, out_num, name='Layer'):

        # input data might be batch_size * col_size, where a col_size*1 vector isomorphic to input
        self.in_nm = in_num
        self.out_nm = out_num

        super(Layer, self).__init__(name, (inp, Theta, (self.out_nm, inp.nm+1)))

    def forward(self, inp):
        return self.forward1(inp)

    def bp(self):
        pass

    def img2col(self, vol):
        # img to col: (n, channel, in_nm_h, in_nm_w) => (n, channel * kernel_h * kernel_w, out_nm_h * out_nm_w)
        X = vol.w
        convs = self.filters
        _, kernel_depth, kernel_h, kernel_w = convs.shape
        l = kernel_depth*kernel_h*kernel_w
        size1 = (vol.batch_size, self.channel * kernel_h * kernel_w, self.out_nm_h * self.out_nm_w)
        ret = np.zeros(size1)
        # loop through samples
        for i in range(vol.batch_size):
            for w0 in range(0, self.out_nm_w): # col first
                pad_left, pad_right = 0, 0
                w1 = -self.pad + w0 * self.strip
                w2 = w1 + kernel_w
                if w1 < 0: w1, pad_left= 0, -w1
                if w2 < 0:
                    continue
                if w2 > self.in_nm_w:
                    pad_right = w2 - self.in_nm_w
                for h0 in range(0, self.out_nm_h):
                    pad_top, pad_bottom = 0, 0
                    h1 = -self.pad + h0 * self.strip
                    h2 = h1 + kernel_h
                    if h1 < 0: h1, pad_top = 0, -h1
                    if h2 < 0:
                        continue
                    if h2 > self.in_nm_h:
                        pad_bottom = h2 - self.in_nm_h

                    kernel_conlv = X[i,:, h1:h2, w1:w2]
                    col = np.pad(kernel_conlv, [(0,0), (pad_top, pad_bottom), (pad_left, pad_right)],
                                 mode='constant',
                                 constant_values=0).flatten()
                    if len(col) != l:
                        raise Exception("Wrong Padding")

                    ret[i,:,h0 * self.out_nm_w + w0] = col[:]

        return ret

    @property
    def grad(self):
        return self.filters.grad

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
        # output Vol instance
        self.out = None

    # using nested For-Loop to implement raw ConvNet forward.
    # This is not efficient and left to be improved in the near future
    # See: https://github.com/karpathy/convnetjs/blob/master/src/convnet_layers_dotproducts.js
    #      https://github.com/costapt/cs231n/blob/master/assignment2/cs231n/im2col.py
    def forward1(self, inp):
        self.inp = inp # Vol
        n = inp.batch_size
        # might need to check here
        convs = self.filters
        K, kernel_depth, kernel_h, kernel_w = convs.shape
        size1 = (n, K, self.out_nm_h, self.out_nm_w)
        ret = np.zeros(size1)

        # filters to row
        W_row = convs.w.reshape(K, kernel_depth * kernel_h * kernel_w) # -1

        # img to col: (n, channel, in_nm_h, in_nm_w) => (n, kernel_channel * kernel_h * kernel_w, out_nm_h * out_nm_w)
        X_col = self.img2col(inp)
        self.X_col = X_col
        # loop through samples
        for i in range(n):
            # (K, kc*kh*kw) mul (kc*kh*hw, oh*ow)
            out = np.matmul(W_row, X_col[i,:]) + self.bias.w
            # col2img
            out.resize(K, self.out_nm_h, self.out_nm_w)
            ret[i,:] = out[:]
        self.out = Vol(n, (K, self.out_nm_h, self.out_nm_w), init_gen=ret)
        return self.out

    def bp(self, top_layer):
        # bias_grad, partial derivatives of biases

        # dW, partial derivatives of filters
        # convol top_layer.grad with inp
        filters = top_layer.inp.grad
        convs = self.filters
        K0, kernel_depth, kernel_h, kernel_w = convs.shape
        n, K1, out_nm_h, out_nm_w = filters.shape

        # partial dirivatives of filters:
        # a naive explanation:
        # for i in range(K1):
        #     f = filters[:,i]
        #     # convol with inp
        #     # (n, oh, ow) conv (n, kd*kh*kw, oh, ow) => (K, kd, kh, kw):
        #     for kw in range(kernel_w):
        #         for kh in range(kernel_h):
        #             for kd in range(kernel_depth):
        #                 # self.filters_grad[i, kw, kh, kd] += 1/n *
        # sum_(p,q,s){ X[p, kd, kh + q*kernel_h, kw + s*kernel_w] * f[p,q,s] } # pay attention to indice
        # p: batch sample index
        # q: out_nm_h index
        # s: out_nm_w index
        # Rearrange above loop:
        self.filters.grad[:] = 0.0
        for k in range(K1):
            f = filters[:, k]
            for kd in range(kernel_depth):
                for kh in range(kernel_h):
                    for kw in range(kernel_w):
                        uid = (kd*kernel_h+kh)*kernel_w+kw
                        self.filters.grad[k, kd, kh, kw] += np.sum(self.X_col[:,uid] * f.reshape(-1, out_nm_h * out_nm_w))

        # partial derivatives of inp
        # opposite to forward , inp computed in flipped direction
        # (n, channel, in_nm_h, in_nm_w) <= (n, K , oh, ow) conv flipped(filter) dot g(inp)
        self.inp.grad[:] = 0.0
        for k in range(self.channel):
            for i in range(self.in_nm_h):
                for j in range(self.in_nm_w):

                    # grad (n, K, oh, ow) conlv flipped(f) (K, kernel_depth, kernel_h, kernel_w)
                    self.conlv(self.inp.grad, filters, convs.w, (k,i,j))

        # partial derivatives of bias
        for d in range(K1):
            f = filters[:, d]
            self.bias.grad[d] = np.sum(f)

        return self.inp.grad, self.filters.grad, self.bias.grad

    def conlv(self, target, grad, convs, index):
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

class FullyCnnLayer(Layer):pass
class AtrousConvLayer(Layer):pass
class BatchNormLayer(Layer):pass

class ReluActivation(Layer):

    def __init__(self, spatial_shape):
        # input Vol instance
        self.inp = None
        self.channel, self.in_nm_h, self.in_nm_w = spatial_shape
        self.LAYER_TYPE = 'relu'
        self.out_nm_d, self.out_nm_h, self.out_nm_w = self.channel, self.in_nm_h, self.in_nm_w
        # output Vol instance
        self.out = None

    def forward1(self, inp):
        pass

    def bp(self, top_layer):
        pass