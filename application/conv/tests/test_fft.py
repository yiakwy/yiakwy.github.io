import sys
sys.path.append("../build")
sys.path.append("../lib")
import fft
from fft import *

def test_method1_dft():
    print("Method 1:")
    print("dft:")
    x = doubleVec()
    x[:] = [1., 2., 1., -1.]
    y = dft_recursive(x)

    for i in y:
        print(i)

def test_method1_idft():
    print("Method 1:")
    print("idft:")
    x = complexVec()
    x[:] = [3.+0.j, 0.-3.j, 1.+0.j, 0.+3.j]
    y = idft_recursive(x)

    for i in y:
        print(i)

if __name__ == "__main__":
    test_method1_dft()
    test_method1_idft()
