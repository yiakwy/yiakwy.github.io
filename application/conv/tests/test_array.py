import sys
sys.path.append("../build")
import matrix_array
from matrix_array import *

def test_array_getitem():
    print("test getitem func")
    import random
    import time
    N = 1000000
    M = 1000000
    index = long(random.uniform(0, N))
    mtx = Matrix(N)
    print("Initialing a matrix of %ld elements, defaults value to null" % N)
    print("Randomly acccess an elemtn at positon %ld : %s" % (index, type(mtx.getitem(index))))
    i = 0
    start = time.time()
    while i < M:
        mtx.getitem(index)
        i+=1
    elapse = time.time() - start
    print("\"Get\" test for C++ wrapped vector at Random Position %ld" % index)
    print("        Elapse:%s" % elapse)
    import numpy as np
    mtx2 = np.array([None]*N)
    i=0
    start = time.time()
    while i < M:
        mtx2[index]
        i+=1
    elapse = time.time() - start
    print("\"Get\" test for np.array at Random Position %ld" % index)
    print("       Elapse:%s" % elapse)
	
def test_array_setitem():
    print("test setitem func")
    import random
    import time
    N = 1000000
    M = 1000000
    index = long(random.uniform(0, N))
    mtx = Matrix(N)
    print("Initialing a matrix of %ld elements, defaults value to null" % N)
    print("Randomly set an element at positon %ld : %s" % (index, type(mtx.setitem(index, object()))))
    i = 0
    start = time.time()
    while i < M:
        mtx.setitem(index, object())
        i+=1
    elapse = time.time() - start
    print("\"Get\" test for C++ wrapped vector at Random Position %ld" % index)
    print("        Elapse:%s" % elapse)
    import numpy as np
    mtx2 = np.array([None]*N)
    i=0
    start = time.time()
    while i < M:
        mtx2[index] = object()
        i+=1
    elapse = time.time() - start
    print("\"Get\" test for np.array at Random Position %ld" % index)
    print("       Elapse:%s" % elapse)

if __name__ == "__main__":
    test_array_getitem()
    test_array_setitem()
