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
    
    globalInit(argc, argv);
    
    std::string pttn;
    int l = 6;
    double pb;
    // std::getline(std::cin, pttn);
    // std::cin >> l;
#define COLOR_OFF "\033[0m";
#define GREEN "\033[0;32m";

    // init weights
#define ALPHABET_LEN 256
    int weights[ALPHABET_LEN] = {0,};
    weights['A'] = 1;
    weights['B'] = 1;
    alphabet_distribution random_alphabet(weights, 256, 2);
    
    // random_alphabet checking
    LOG(INFO) << "random_alphabet distribution, uniform checking ...";
    // multi scale testing
    random_alphabet.test_uniform_checking(10000);
    
    // specify a test case
    random_experiment_engine<alphabet_distribution> ex_engine(random_alphabet);
    
    pttn = "ABB";
    pb = ex_engine.run_ex(pttn.c_str(),
                               (int)pttn.length(),
                               l,
                               10000);
//    std::cout << boost::format("(1) Given a text M of length %1%, the probability of pattern string P : %2% in M is: %3%") % l % pttn % pb << std::endl;
    LOG(INFO) << boost::format("Given a text M of length %1%, the probability of string <P> : %2% in <M> is: %3%") % l % pttn % pb << std::endl;
    
    pttn = "ABA";
    pb = ex_engine.run_ex(pttn.c_str(),
                          (int)pttn.length(),
                          l,
                          10000);
//    std::cout << boost::format("(2) Given a text M of length %1%, the probability of pattern string P : %2% in M is: %3%") % l % pttn % pb << std::endl;
    LOG(INFO) << boost::format("Given a text M of length %1%, the probability of string <P> : %2% in <M> is: %3%") % l % pttn % pb << std::endl;
    return 0;

}