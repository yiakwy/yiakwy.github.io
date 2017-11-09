//
//  array.hpp
//  ConvNet.array
//
//  Created by Wang Yi on 1/11/17.
//  Copyright © 2017 Wang Lei. All rights reserved.
//

#ifndef array_hpp
#define array_hpp

#include <Python.h>
#include <stdlib.h>
#include <boost/python.hpp>
#include <boost/python/tuple.hpp>
#include <boost/python/list.hpp>
#include <boost/python/slice.hpp>

#include <stdio.h>
#include <limits.h>

#include <vector>
using std::vector;
#include <cmath>

#define Malloc(t, l) \
    t* malloc(sizeof(t)*l)

typedef long long ll;
// see http://www.sgi.com/tech/stl/complexity.html complexity specification
// see also my test report gen module ConvNet.test_array,
typedef vector<PyObject*> list;
namespace python = boost::python;

namespace matrix_array {
    
    typedef struct _seq_gen_func {
        ll index;
        
        _seq_gen_func():index(0){};
        ll next(){return (ll)(index*index);};
        ll operator()(ll seed){ index = next() + seed; return index;};
    } func_seq_gen;
    
    class Matrix {
    public:
        Matrix(ll size);
        virtual ~Matrix();
        
        // core input and output methods
        // for more info from historical design, please refer to the research project created in 2014 PyMatrix:
        // https://testpypi.python.org/pypi/matrix_array/0.1.0 The project has been deprecated since benchmark tests show the "deep search" in primitive python is 100 times slower than python builtin list.
        // usage example: mtx[N:M,[a,b,c, ... ],x,:,'?',...]
        // boost::python provides a wrapper for PyObject*. But for the moment, let us just focus on PyObject*
        PyObject* getitem(ll i);
        PyObject* getitem_multi(python::tuple inp);
        Matrix& setitem(ll i, PyObject* val);
        Matrix& setitem_multi(python::tuple inp, Matrix& mtx);
        
    private:
        list m_array;
        ll capacity=0;
        ll length=0;
        func_seq_gen seq_generate;
    };
    
}

#endif /* array_hpp */
