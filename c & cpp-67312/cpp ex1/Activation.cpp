//
// Created by Mike Greenbaum on 12/15/2019.
//
#include "Activation.h"
#include <math.h>
#include "Matrix.h"
#define ERROR_WRONG_TYPE "Error: wrong activation type was given"
#define ERROR_DIVISION_ZERO "Error: tried to divide by 0 in soft max"

/**
 * @param type the type of this activation
 */
Activation::Activation(ActivationType type): _type(type)
{
    _printWrongType();
}

/**
 * @return the activation type of this object
 */
ActivationType Activation::getActivationType() const
{
    return this->_type;
}

/**
 * @param m the matrix to store the Relu in
 * @param matrix the matrix to apply Relu to
 * @return the m matrix after Relu
 */
Matrix& _applyRelu(Matrix &m, const Matrix& matrix)
{
    for(int i = 0; i < matrix.getRows() * matrix.getCols(); i++)
    {
        m._matrix[i] = (matrix._matrix[i] < 0) ? 0 : matrix._matrix[i];
    }
    return m;
}

/**
 * @param m the matrix to store the Softmax in
 * @param matrix the matrix to apply Softmax to
 * @return the m matrix after Softmax
 */
Matrix& _applySoftmax(Matrix &m, const Matrix& matrix)
{
    float sum = 0;
    float value = 0;
    for(int i = 0; i < matrix.getRows() * matrix.getCols(); i++)
    {
        value = (float) std::exp(matrix._matrix[i]);
        sum += value;
        m[i] = value;
    }
    if(sum == 0)
    {
        std::cerr << ERROR_DIVISION_ZERO << std::endl;
        exit(EXIT);
    }
    m = m * (1 / sum);
    return m;
}

/**
 * @param matrix the input matrix, doesn't change matrix
 * @return a new matrix after activation on the input
 */
Matrix Activation::operator()(const Matrix& matrix) const
{
    _printWrongType();
    Matrix m(matrix.getRows(), matrix.getCols());
    if(this->_type == Relu)
    {
        return _applyRelu(m, matrix);
    }
    else if(this->_type == Softmax)
    {
        return _applySoftmax(m, matrix);
    }
    return m;
}

/**
 * @param type the type of input function
 * @return exits if the type is wrong
 */
void Activation::_printWrongType() const
{
    if(this->_type != Relu && this->_type != Softmax)
    {
        std::cerr << ERROR_WRONG_TYPE << std::endl;
        exit(EXIT);
    }
}

