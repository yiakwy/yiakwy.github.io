//
//  probtests.hpp
//  searching tlabe algorithm in probability theory. (KMP & Boyer Moore)
//
//  This is material together with course CS3001 in our school. In this tutorial, we want to build a common sense
//  of industry envrionment W.R.T random varialbes among students. We define this course material for subject `Computing Random Variables`, as it focuses on using computers to apply stochastic methods on mass data. This is usually the first stage for data scientists, or machine learning engineers.
//
//  As a very important aspect both for academic research and industry IT product, `Computing Random Variables`(in subcourse "probabiity and sampling from mass data" for people specialised in data science., is widely neglected. We also notice that a lot problems regarding to `Computing Random Variables`) are raised quickly both in ACM and other IT technicial interviews.
//
//  Principles: examples, easy -> hard;
//              data structure, native format -> STL standard
//              codes structure, test driven or `bug` driven development
//
//  Created by Wang Yi on 7/3/17.
//  Copyright © 2017 Wang Yi@yiak.co. All rights reserved.
//

#ifndef probtests_hpp
#define probtests_hpp

#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <iostream>
#include <random>

#include "boyerMoore.h"
#include "exceptions.hpp"
#include "api.hpp"

#include <string>
using std::string;
// We will use glog for our tutorial
#ifdef HAVE_LIB_GFLAGS
#include <gflags/gflags.h>
using namespace gflags;
#endif

#include <cmath>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <boost/format.hpp>

#include <glog/logging.h>

#define CACHE(type, length, name) type _cache_##name[length];
typedef unsigned char bytes;

// This tutorial uses Non-deterministic Uniform Random Number Generator, defined in
// Boot boot_random framework: http://www.boost.org/doc/libs/1_50_0/doc/html/boost_random/reference.html#boost_random.reference.concepts.non_deterministic_uniform_random_number_generator
using std::random_device;
/** standard codes **
 * std::random_device device;
 * std::mt19937 gen(device());
 * std::bernoulli_distribution coin_flip(0.5);
 * bool outcome = coin_flip(gen);
 */
// a simple implementation about bernoulli: http://www.boost.org/doc/libs/1_35_0/libs/math/doc/sf_and_dist/html/math_toolkit/dist/dist_ref/dists/bernoulli_dist.html
using std::bernoulli_distribution;

template <typename  _Ar, typename _Tp, class _BinaryOperation>
_Tp
reduce_array(_Ar __array, int len, _Tp __init, _BinaryOperation __binary_op)
{
    int curr=0;
    for (; curr < len; curr++){
        __init = __binary_op(__init, *__array++);
    }
    return __init;
}

// caution, memory manipulation
template <typename _Ar, typename _Tp, class UnaryPredicate>
_Ar
filter_array(_Ar __array, int len, _Tp __default, UnaryPredicate __pred)
{
    int i, j;
    _Ar ret = Malloc(_Tp, len);
    FOR(i, len)
    ret[i] = __default;
    END
    
    i = 0;
    FOR(j, len)
    if (__pred(__array[j]))
        ret[i++] = __array[j];
    END
    
    return ret;
}

// prepare sampling space and output data results for validation
// according to "rule 3", we define 3 class members together
// this class uses "old methods"; we will use smart pointer like "shared_ptr" in the next chapter
#define COPY_MEM(dest, src, len) \
    dest = Malloc(int, len); \
    int  dest## _ptr; \
    FOR( dest## _ptr, len) \
    dest[dest## _ptr] = src[dest## _ptr]; \
    END

class alphabet_distribution
{
public:
    typedef alphabet_distribution alphabet_type;
    // used for index of probs of characters
#define ALPHABET_LEN 256
    explicit alphabet_distribution(const int weights[], int l, int vals_range): m_weights(nullptr),
                                                                         m_vals_range(-1),
                                                                         compact_seq(nullptr)
    {
        this->m_vals_range = vals_range;
        this->m_size = l;
        
        if (weights == nullptr || l <= 0)
            return;
        
        if ((vals_range) / ALPHABET_LEN < m_threshold){
            compact_seq = Malloc(int, vals_range);
            int i;
            
            FOR(i, vals_range)
            compact_seq[i] = 0;
            END
        }
        
        if (l > ALPHABET_LEN && ((double) vals_range / ALPHABET_LEN > m_threshold))
        {
            int alloc_size = l;
            this->m_weights = Malloc(int, alloc_size);
            if (this->m_weights == nullptr)
            {
                NotEnoughMemory e = NotEnoughMemory("weights");
                LOG(INFO) << e.what();//glog or something else
            }
            
            memcpy(this->m_weights, weights, l);
            this->allocated = alloc_size;
        } else {
            // l > 0
            // memcpy(this->_cache_pb, weights, l);
            int i = 0, j=0;
            FOR(i, l)
            this->_cache_pb[i] = weights[i];
            if (compact_seq != nullptr && weights[i] > 0)
            {
                compact_seq[j++] = i;
            }
            END
        }
        
    };
    
    ~alphabet_distribution()
    {
        if (m_weights != nullptr) {
            free(m_weights);
            m_weights = nullptr;
        }
        
        if (compact_seq != nullptr){
            free(compact_seq);
            compact_seq = nullptr;
        }
    };
    
    alphabet_distribution(const alphabet_type& ins)
    {
        if (this != &ins)
        {
            coding = ins.coding;
            m_vals_range = ins.m_vals_range;
            m_size = ins.m_size;
            m_threshold = ins.m_threshold;
            
            // very important
            if (ins.compact_seq != nullptr)
            {
                COPY_MEM(compact_seq, ins.compact_seq, m_vals_range)
            }
            
            if (ins.m_weights != nullptr)
            {
                allocated = ins.allocated;
                COPY_MEM(m_weights, ins.m_weights, allocated)
            }
            
        }
    };
    
    alphabet_type& operator = (const alphabet_type& ins)
    {
        if (this != &ins)
        {
            coding = ins.coding;
            m_vals_range = ins.m_vals_range;
            m_size = ins.m_size;
            m_threshold = ins.m_threshold;
            
            // very important
            if (ins.compact_seq != nullptr)
            {
                COPY_MEM(compact_seq, ins.compact_seq, m_vals_range)
            } else { compact_seq = nullptr;}
            
            if (ins.m_weights != nullptr)
            {
                allocated = ins.allocated;
                COPY_MEM(m_weights, ins.m_weights, allocated)
            }
        }
        return *this;
    };
    
    bool test_uniform_checking(int test_cases=10000);
    
    
    // bytes to unicode conversion and the opposite, should call unicode routines.
    // later we will do a specific encoding and decoding project for `Sequence And Literals`.
    bytes operator()(void);
    
    template <typename _Tp>
    const char* histogram(_Tp hist=nullptr, const char* fmt = "<%1%>: ", char32_t symbol='#');
    
private:
    string coding="ascii";
    int m_vals_range;
    int m_size;
    double m_threshold = 0.8;
    int* compact_seq;
    union {
        CACHE(int, ALPHABET_LEN, pb)
        struct {
            int* m_weights; //  this works as a mask
            int allocated;
        };
    };
};


// executing experiments
template<class distribution> class random_experiment_engine
{
public:
    random_experiment_engine(distribution& random_range):m_random_alphabet(random_range){};
    ~random_experiment_engine(){};
    
    bool single_experiment(char const * pttn, int pttn_len, int l);
    string templestr_gen(int l);
    double run_ex(const char * pttn, int pttn_len, int l, int ex_num);

private:
    distribution m_random_alphabet;
};


template<class distribution>
string
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
    
    while (i++ < l){
        bytes ch_dec = this->m_random_alphabet();
        templestr +=((char)ch_dec);
    }
    return templestr;
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
    const char* templestr = this->templestr_gen(l).c_str();
    size_t ret = boyer_moore(templestr, l, pttn, pttn_len, false); // or use KMP instead
    if (ret != NOT_FOUND)
        return true;
    return false;
}


template<class distribution>
double
random_experiment_engine<distribution>::run_ex(const char * pttn, int pttn_len, int l, int ex_num)
{
    int i, success=0;
    FOR(i, ex_num)
    if (this->single_experiment(pttn, pttn_len, l))
        success++;
    END
    return success / (double) ex_num;
}


#endif /* probtests_hpp */
