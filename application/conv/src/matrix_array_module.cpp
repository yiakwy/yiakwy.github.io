//
//  array_module.cpp
//  ConvNet.array
//
//  Created by Wang Yi on 5/11/17.
//  Copyright © 2017 Wang Lei. All rights reserved.
//

#include "matrix_array_module.hpp"
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>


BOOST_PYTHON_MODULE(matrix_array)
{
    using namespace boost::python;
    
    class_<Matrix>("Matrix",
                          "NetConv.array.Matrix is a n-dimensional matrix container based on research 'matrix_array' published in 2014 in PyPi"
                          "The project is aimed to provided easy interactive matrix container for ConvNet project",
                          init<ll>(args("size"), "Row contructor. This will be called by upper layer constructors")
                   )
    .def("getitem", &Matrix::getitem)
    .def("getitem_multi", &Matrix::getitem_multi)
    .def("setitem", &Matrix::setitem, return_internal_reference<>())
    .def("setitem_multi", &Matrix::setitem_multi, return_internal_reference<>())
    ;
}
