////
////  probtests.hpp
////  searching tlabe algorithm in probability theory. (KMP & Boyer Moore)
////
////  This is material together with course CS3001 in our school. In this tutorial, we want to build a common sense
////  of industry envrionment W.R.T random varialbes among students. We define this course material for subject `Computing Random Variables`, as it focuses on using computers to apply stochastic methods on mass data. This is usually the first stage for data scientists, or machine learning engineers.
////
////  As a very important aspect both for academic research and industry IT product, `Computing Random Variables`(in subcourse "probabiity and sampling from mass data" for people specialised in data science., is widely neglected. We also notice that a lot problems regarding to `Computing Random Variables`) are raised quickly both in ACM and other IT technicial interviews.
////
////  Principles: examples, easy -> hard;
////              data structure, native format -> STL standard
////              codes structure, test driven or `bug` driven development
////
////  Created by Wang Yi on 7/3/17.
////  Copyright © 2017 Wang Yi@yiak.co. All rights reserved.
////
//
#ifndef probtests_hpp
#define probtests_hpp

#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <iostream>
#include <random>

#include "exceptions.hpp"
#include "api.hpp"

#include <string>
using std::string;
// We will use glog for our tutorial
#ifdef HAVE_LIB_GFLAGS
#include <gflags/gflags.h>
using namespace gflags;
#endif

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


// prepare sampling space and output data results for validation
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
        }
        
        if (l > ALPHABET_LEN)
        {
            int alloc_size = l;
            this->m_weights = Malloc(int, alloc_size);
            if (this->m_weights == nullptr)
            {
                NotEnoughMemory e = NotEnoughMemory("weights");
                //LOG(INFO) << e.what();//glog or something else
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
                compact_seq[j++] = weights[i];
            }
            END
        }
        
    };
    
    ~alphabet_distribution()
    {
        if (this->m_size > ALPHABET_LEN) {
            free(m_weights);
            m_weights = nullptr;
        }
        
        if (compact_seq != nullptr){
            free(compact_seq);
            compact_seq = nullptr;
        }
    };
    
    bool test_uniform_checking();
    
    
    // bytes to unicode conversion and the opposite, should call unicode routines.
    // later we will do a specific encoding and decoding project for `Sequence And Literals`.
    bytes operator()(void);
    
private:
    string coding="ascii";
    int m_vals_range;
    int m_size;
    int m_threshold = 0.8;
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
    double run_ex(const char * pttn, int pttn_len, int l, int ex_num);
    const char* templestr_gen(int l);

private:
    distribution m_random_alphabet;
};

#endif /* probtests_hpp */
