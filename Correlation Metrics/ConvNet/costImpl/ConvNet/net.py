__author__ = 'wangyi'

from ..common.node import Node


class Net(Node):

    def __init__(self, model_weights, model_def):

        # parsing data
        data = None
        # parsing name
        name = None
        super(Net, self).__init__(name, data)
        pass

    def forward(self):
        pass

    def bp(self):
        pass