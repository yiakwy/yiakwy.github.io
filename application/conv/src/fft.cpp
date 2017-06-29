//
//  fft.cpp
//  Op_conv
//
//  Created by Wang Yi on 26/6/17.
//  Copyright © 2017 Wang Lei. All rights reserved.
//

#include "fft.hpp"
#include "functional.hpp"

unsigned int
fft::bit_overloop_reverse(unsigned int n)
{
    unsigned int len = ByteWidth * sizeof(unsigned int);
    unsigned int i, ret=0, bit;
    
    for (i=0; i < len; i++) {
        bit = get_bit(n, i);
        if (bit==1) {
            set_bit(&n, len-1-i);
        }
    }

    return ret;
}

vector<complex<double>>
fft::dft_recursive(vector<double> inp)
{
    unsigned int n = inp.size(), k;
    vector<complex<double>> ret(n), A0, A1;
    
    if (n == 1)
    {
        ret[0] = complex<double>(inp[0]);
        return ret;
    }
    
    complex<double> wn =std::polar(1., -2. * M_PI / n);
    complex<double> w(1.), t;
    
    vector<double> inp_even = filter_vec(inp, [](size_t index){return index % 2 == 0 ? true:false;});
    vector<double> inp_odd  = filter_vec(inp, [](size_t index){return index % 2 == 1 ? true:false;});
    
    A0 = dft_recursive(inp_even);
    A1 = dft_recursive(inp_odd);
    
    for (k=0; k < n/2; k++)
    {
        t = w * A1[k];
        ret[k] = A0[k] + t;
        ret[k + n/2] = A0[k] - t;
        w = w * wn;
    }
    
    return ret;
}

vector<complex<double>>
fft::_dft_recursive(vector<complex<double>> inp)
{
    unsigned int n = inp.size(), k;
    vector<complex<double>> ret(n), A0, A1;
    
    if (n == 1)
    {
        ret[0] = complex<double>(inp[0].real(), inp[0].imag());
        return ret;
    }
    
    complex<double> wn =std::polar(1., 2. * M_PI / n);
    complex<double> w(1.), t;
    
    vector<complex<double>> inp_even = filter_vec(inp, [](size_t index){return index % 2 == 0 ? true:false;});
    vector<complex<double>> inp_odd  = filter_vec(inp, [](size_t index){return index % 2 == 1 ? true:false;});
    
    A0 = _dft_recursive(inp_even);
    A1 = _dft_recursive(inp_odd);
    
    for (k=0; k < n/2; k++)
    {
        t = w * A1[k];
        ret[k] = (A0[k] + t);
        ret[k + n/2] = (A0[k] - t);
        w = w * wn;
    }
    
    return ret;
}

vector<complex<double>>
fft::idft_recursive(vector<complex<double>> inp)
{
    unsigned int n = inp.size(), k;
    for (k=0; k < n; k++)
    {
        inp[k] = inp[k] / complex<double>(n);
    }
    
    return fft::_dft_recursive(inp);
}


