__author__ = 'wangyi'

# see tutorial https://medium.com/@d3lm/understand-tensorflow-by-mimicking-its-api-from-scratch-faa55787170d by Dominic E.
# and this tutorial about autograd.
#
# The layer api implements some important ConvNet structure but leave forward and backpropogration to be implemented
# by users. Autograd techniques are the key for trainning of customer model definition.
#
# We also want to take this opportunity to explore where (which devices) and how (sub common expression elimination) to
# execute a neural network, -- a computation graph.
#

class Graph:

    def __init__(self):
        self.operants = []
        self.operators = []
        self.constants = []
        self.placeholder = []

    def as_default(self):
        global _default_graph
        _default_graph = self
        return self

