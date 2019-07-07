__author__ = 'wangyi'
import numpy as np

class Vol:

    def __init__(self, batch_size, spatial_size, init_gen=None):
        self.batch_size = batch_size
        self.spatial_size = spatial_size

        self._init(batch_size, spatial_size, init_gen)

    @property
    def shape(self):
        return (self.batch_size,) + self.spatial_size

    def copy(self, only='weights'):
        if only is 'weights':
            # for cs231 tests grad_numeric_computation
            return self.w.copy()
        else:
            raise NotImplementedError("Not Implemented Yet!")

    def _init(self, batch_size, spatial_size, init_gen):
        if batch_size > 1:
            self.w = np.zeros((batch_size,)+spatial_size)
            self.grad = np.zeros((batch_size,)+spatial_size)
        else:
            self.w = np.zeros(spatial_size)
            self.grad = np.zeros(spatial_size)

        if hasattr(init_gen, "__len__"):
            self.w[:] = init_gen[:]

    # C-Style uid computing routine
    def uid(self, argc, argv, dims):
        ret = 1
        i = 0
        factor = 1

        while i < argc:
            factor *= dims[i]
            i += 1

        i = 0
        while i < argc:
            ret += (argv[i]) * factor
            factor /= dims[argc-1-i]
            i += 1

        return ret

    def reset_spatial_size(self, spatial_size, fill=None):
        self.spatial_size = spatial_size
        self._init(self.batch_size, spatial_size, init_gen=fill)