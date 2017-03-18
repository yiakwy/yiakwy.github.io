//
//  probtests.cpp
//  KMP
//
//  Created by Wang Yi on 7/3/17.
//  Copyright © 2017 Wang Yi@yiak.co. All rights reserved.
//

#include "probtests.hpp"
#include "boyerMoore.h"

#include <cmath>
#include <iostream>
#include <boost/format.hpp>
using std::accumulate;

template <class _Ar, class _Tp, class _BinaryOperation>
_Tp
reduce_array(_Ar __array, int len, _Tp __init, _BinaryOperation __binary_op)
{
    int curr=0;
    for (; curr < len; curr++)
        __init = __binary_op(__init, *__array++);
    return __init;
}


bool is_alphabet(bytes ch_dec)
{
    if ((ch_dec >= 'a' && ch_dec <= 'z') ||
        (ch_dec >= 'A' && ch_dec <= 'Z'))
        return true;
    return false;
}


typedef unsigned char bytes;
bytes
alphabet_distribution::operator()(void)
{
    bytes ch;
    int ch_dec;
    int* weights=nullptr;
    
    std::random_device device;
    std::mt19937 gen(device());
    weights = this->m_weights != nullptr ? this->m_weights : this->_cache_pb;
    
    // refuse sampling has a problem:
    // if there are too much choices to be refused, the programme has a
    // large probability to be blocked. Hence we need to narrow donw the sampling space
    
    
    if ((double)m_vals_range / ALPHABET_LEN > m_threshold)
    {
        std::uniform_int_distribution<unsigned int> random_range(0, ALPHABET_LEN);
        ch_dec = random_range(gen);
        while (not is_alphabet(ch_dec) || weights[ch_dec] <= 0)
        {
            ch_dec = random_range(gen);
        }
    } else {
        // another algorithm
        std::uniform_int_distribution<unsigned int> random_range(0, this->m_vals_range);
        // linear mapping
        ch_dec = random_range(gen);
        ch_dec = compact_seq[ch_dec];
    }

    ch = bytes(ch_dec);
    return ch;
}


// checking whether it is a uniform sampling
// google test for unity testing
bool
alphabet_distribution::test_uniform_checking()
{
    bytes ch;
    int test_cases = 10000, i;
    double avg=0.0, _stds=0.0;
    int* symbol_Table = Malloc(int, this->m_vals_range);
    if (symbol_Table == NULL)
        ;
    FOR(i, this->m_vals_range)
    symbol_Table[ch] = 0;
    END
    
    for(i=0; i < test_cases; i++){
        ch = (*this)();
        symbol_Table[ch] += 1;
    }
    
    // computing variance and average to verify whether they are uniform numerically.
    avg = reduce_array(symbol_Table, this->m_vals_range, 0,
                    [](int pre, int curr){return pre + curr;}) / this->m_vals_range;
    
    // or you can write in this way
//    std::vector<int> _symbol_Table(symbol_Table, symbol_Table + this->m_vals_range);
//    avg = sum_array(_symbol_Table, [](int pre, int curr){return pre + curr;}) / this->m_vals_range;
    
    _stds = reduce_array(symbol_Table, this->m_vals_range, 0,
                         [](int pre, int curr){return pre*pre + curr*curr;}) / this->m_vals_range;
    _stds = sqrt(_stds);

    
//    std::cout << "running test cases <" << test_cases << "> : "
//                               << "avg:" << avg << " , " << "std:" << _stds
//                               << std::endl;
//    LOG(INFO) << boost::format("running test cases <%1%> :"
//                               "avg: %1%, "
//                               "std: %1%, "
//                               ) % test_cases % avg % _stds << std::endl;
    
    // google test , asserts ...
    free(symbol_Table);
    symbol_Table = nullptr;
    return true;
}


template<class distribution>
const char*
random_experiment_engine<distribution>::templestr_gen(int l)
{
    string templestr = "";
    int i = 0;
    
/*
 *
#define ALPHABET_LEN 256
 int weights[ALPHABET_LEN] = {1};
 alphabet_distribution random_alphabet(weights, 256, 52);
 *
 */
    
    while (i < l){
        bytes ch_dec = this->m_random_alphabet();
        templestr +=((char)ch_dec);
    }
    return templestr.c_str();
}


// aka given a template string, calc the possibility to find the string in the template
// e.g: AAB, ABB

/*
 *
#define ALPHABET_LEN 256
 int weights[ALPHABET_LEN] = {0};
 weights['A'] = 1;
 weights['B'] = 1;
 alphabet_distribution random_alphabet(weights, 256, 2);
 *
 */

template<class distribution>
bool
random_experiment_engine<distribution>::single_experiment(char const * pttn,
                                                          int pttn_len,
                                                          int l) {
    const char* templestr = this->templestr_gen(l);
    size_t ret = boyer_moore(templestr, l, pttn, pttn_len); // or use KMP instead
    if (ret != NOT_FOUND)
        return true;
    return false;
}


template<class distribution>
double
random_experiment_engine<distribution>::run_ex(const char * pttn,
                                               int pttn_len,
                                               int l,
                                               int ex_num)
{
    int i = 0;
    int success = 0;
    FOR(i, ex_num)
        if (this->single_experiment(pttn, pttn_len, l))
            success++;
    END
    return success / (double) ex_num;
}



