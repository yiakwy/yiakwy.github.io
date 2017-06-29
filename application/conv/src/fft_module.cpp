//
//  fft_module.cpp
//  Op_conv
//
//  Created by Wang Yi on 27/6/17.
//  Copyright © 2017 Wang Lei. All rights reserved.
//

#include "fft_module.hpp"

#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
// #include <boost/python/stl_iterator.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

typedef vector<double> doubleVec;
typedef vector<complex<double>> complexVec;

/*
// https://stackoverflow.com/questions/15842126/feeding-a-python-list-into-a-function-taking-in-a-vector-with-boost-python
struct iterable_converter
{
    template <typename Container>
    iterable_converter&
    from_python()
    {
        boost::python::converter::registry::push_back(
                                                      &iterable_converter::convertible,
                                                      &iterable_converter::construct<Container>,
                                                      boost::python::type_id<Container>()
                                                      );
        return *this;
    }
    
    static void* convertible(PyObject* obj)
    {
        return PyObject_GetIter(obj) ? obj : NULL;
    }
    
    template<typename Container>
    static void construct(PyObject* obj,
                          boost::python::converter::rvalue_from_python_stage1_data* data)
    {
        namespace py = boost::python;
        py::handle<> handle(py::borrowed(obj));
        
        typedef py::converter::rvalue_from_python_storage<Container> storage_type;
        void* storage = reinterpret_cast<storage_type*>(data)->storage.bytes;
        typedef py::stl_input_iterator<typename Container::value_type> it;
        
        new (storage) Container(
                                it(py::object(handle)),
                                it()
                                );
        data->convertible = storage;
    }
};
*/

BOOST_PYTHON_MODULE(fft)
{
    using namespace boost::python;
    
    // iterable_converter().from_python<std::vector<double>>();
    
	class_<std::vector<double>>("doubleVec")
        .def(vector_indexing_suite<vector<double>>());
    
    class_<std::vector<complex<double>>>("complexVec")
        .def(vector_indexing_suite<vector<complex<double>>>());

    def( "dft_recursive", dft_recursive);
    def("idft_recursive", idft_recursive);
}
