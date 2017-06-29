//
//  fft.hpp
//  Op_conv
//
//  Created by Wang Yi on 26/6/17.
//  Copyright © 2017 Wang Lei. All rights reserved.
//

#ifndef fft_hpp
#define fft_hpp

#include <stdio.h>
#include <limits.h>

#include <vector>
using std::vector;
#include <complex>
using std::complex;
#include <cmath>

#ifndef M_PI
#define M_PI 3.1415926535897932384
#endif

#define ByteWidth 8

namespace fft {
    inline unsigned int get_bit(unsigned int n, unsigned int pos)
    {
        return n  & (1 << pos);
    }

    inline void set_bit(unsigned int *n, unsigned int pos)
    {
              *n |= (1 << pos);
    }

    unsigned int
    bit_overloop_reverse(unsigned int n);
    
    vector<complex<double>>
     dft_recursive(vector<double> inp);
    
    vector<complex<double>>
    _dft_recursive(vector<complex<double>> inp);
    
    vector<complex<double>>
    idft_recursive(vector<complex<double>> inp);
    // butterfly_op
    // dft
    // idft
    
}
#endif /* fft_hpp */
