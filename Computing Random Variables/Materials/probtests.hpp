//
//  probtests.hpp
//  searching tlabe algorithm in probability theory. (KMP & Boyer Moore)
//
//  This is material together with course CS3001 in our school. In this tutorial, we want to build a common sense
//  of industry envrionment W.R.T random varialbes among students. We define this course material for subject `Computing Random Variables`, as it focuses on using computers to apply stochastic methods on mass data. This is usually the first stage for data scientists, or machine learning engineers.
//
//  As a very important aspect both for academic research and industry IT product, `Computing Random Variables`(in subcourse "probabiity and sampling from mass data" for people specialised in data science., is widely neglected. We also notice that a lot problems regarding to `Computing Random Variables`) are raised quickly both in ACM and other IT technicial interviews.
//
//  Created by Wang Yi on 7/3/17.
//  Copyright © 2017 Wang Yi@yiak.co. All rights reserved.
//

#ifndef probtests_hpp
#define probtests_hpp

#include <stdio.h>
#include <stdlib.h>
#include <random>

// We will use glog for our tutorial
#ifdef HAVE_LIB_GFLAGS
#include <gflags/gflags.h>
using namespace gflags;
#endif


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

class alphabet_distribution
{
public:
// used for index of probs of characters
#define ALPHABET_LEN 256
    

    ;
private:

};

class random_experiment_engine
{
public:
    typedef class _distribution {
    } distribution_param;
    
    bool single_experiment(const char * pttn, int l);
    const char* templestr_gen(int l);

private:
    distribution_param m_distrpb;
};

#endif /* probtests_hpp */
