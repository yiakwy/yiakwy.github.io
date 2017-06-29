//
//  main.cpp
//  Op_conv
//
//  Created by Wang Yi on 26/6/17.
//  Copyright © 2017 Wang Lei. All rights reserved.
//

#include <iostream>
#include <iomanip>
#include "fft.hpp"

int main(int argc, const char * argv[]) {
    vector<double> a = {1., 2., 1., -1.};
    vector<complex<double>> ft = fft::dft_recursive(a);
    for (auto el : ft){
        std::cout << el << std::setprecision(4) << ' ';
    }
    std::cout << std::endl;
    
    vector<complex<double>> b = {
        {3.,  0.},
        {0., -3.},
        {1.,  0.},
        {0.,  3.}
    };
    vector<complex<double>> ift = fft::idft_recursive(b);
    for (auto el : ift){
        std::cout << el << std::setprecision(4) << ' ';
    }
    std::cout << std::endl;
    return 0;
}
