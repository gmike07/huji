//Activation.h
#ifndef ACTIVATION_H
#define ACTIVATION_H

#include "Matrix.h"
/**
 * @enum ActivationType
 * @brief Indicator of activation function.
 */
enum ActivationType
{
    Relu,
    Softmax
};

/**
 * @class Activation
 * @brief the class represents an abstraction to activation functions
 */
class Activation
{
public:
    /**
     * @param type the type of this activation
     */
    Activation(ActivationType type);

    /**
     * @return the activation type of this object
     */
    ActivationType getActivationType() const;

    /**
     * @param matrix the input matrix, doesn't change matrix
     * @return a new matrix after activation on the input
     */
    Matrix operator()(const Matrix& matrix) const;
private:
    //the type of this activation
    const ActivationType _type;

    /**
     * @param type the type of input function
     * @return exits if the type is wrong
     */
    void _printWrongType() const;
};

#endif //ACTIVATION_H
