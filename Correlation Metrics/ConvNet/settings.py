__author__ = 'wangyi'

# according to IEEE numeric model, we don't have precise == in computer. We use abs() < EPILON to replace floated equivalence
EPILON = 1.0e-8