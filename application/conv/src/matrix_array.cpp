//
//  array.cpp
//  ConvNet.array
//
//  Created by Wang Yi on 3/11/17.
//  Copyright © 2017 Wang Lei. All rights reserved.
//

#include "matrix_array.hpp"
using namespace matrix_array;

Matrix::Matrix(ll size)
{
    if (size > 0) {
        capacity = seq_generate(size);
        this->m_array.resize(capacity, nullptr);
        length = size;
    }

}

Matrix::~Matrix()
{
    this->m_array.clear();
    capacity = 0;
    length = 0;
}

PyObject*
Matrix::getitem(ll i) {
    PyObject* ret = nullptr;
    if (i < length and i >= 0)
    {
        ret = this->m_array[i];
    }
    else if (i < 0 and i > -length) {
        ret = this->m_array[(i+length)%length];
    }
    else if (i >= capacity) {
        // In numpy we will throw an error, but I don't think this is good for practice
        ret = nullptr;
    }
    else {
        // not handled
    }
    return ret;
}

// TO DO
PyObject*
Matrix::getitem_multi(python::tuple inp)
{
    PyObject* ret = nullptr;
    return ret;
}

Matrix&
Matrix::setitem(ll i, PyObject* val)
{
    if (i < capacity and i >= 0)
    {
        this->m_array[i] = val;
    }
    else if (i < 0 and i > -length) {
        this->m_array[(i+length)%length] = val;
    }
    else if (i >= capacity) {
        capacity = capacity + seq_generate(i-capacity);
        this->m_array.resize(capacity, nullptr);
        length = i;
        this->m_array[i] = val;
    }
    else {
        // not handled
    }
    return *this;
}

// TO DO
Matrix&
Matrix::setitem_multi(python::tuple inp, Matrix& mtx){
    return *this;
}
