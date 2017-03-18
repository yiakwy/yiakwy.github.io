//
//  main.cpp
//  boyerMoore
//
//  Created by Wang Yi on 30/10/16.
//  Copyright (c) 2016 Wang Yi. All rights reserved.
//

#include <iostream>
#include <sstream>
#include <string>
#include "boyerMoore.h"
#include "logging.hpp"
#include "probtests.hpp"

#include <glog/logging.h>

int main(int argc, const char * argv[])
{
    
    // globalInit(argc, argv);
    
    std::string pttn;
    int l = 30;
    // std::getline(std::cin, pttn);
    // std::cin >> l;
    pttn = "AAB";

    // init weights
#define ALPHABET_LEN 256
    int weights[ALPHABET_LEN] = {0,};
    weights['A'] = 1;
    weights['B'] = 1;
    alphabet_distribution random_alphabet(weights, 256, 2);
    
    // random_alphabet checking
//    LOG(INFO) << "random_alphabet distribution, uniform checking ...";
    random_alphabet.test_uniform_checking();
    
    // specify a test case
    random_experiment_engine<alphabet_distribution> ex_engine(random_alphabet);
//    ex_engine.run_ex(pttn.c_str(),
//                               (int)pttn.length(),
//                               l,
//                               10000);
    return 0;

}
