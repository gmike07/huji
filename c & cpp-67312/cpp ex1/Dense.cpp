
// Created by Mike Greenbaum on 12/14/2019.
//
#include "Dense.h"

/**
 * @param weights the weights of this layer
 * @param bias the bias of this layer
 * @param activationType the activation type for this layer
 */
Dense::Dense(const Matrix& weights, const Matrix& bias, ActivationType activationType)
: _weights(weights), _bias(bias), _activation(activationType)
{
}

/**
 * @return the weights of this layer
 */
const Matrix& Dense::getWeights() const
{
    return this->_weights;
}

/**
 * @return the bias of this layer
 */
const Matrix& Dense::getBias() const
{
    return this->_bias;
}

/**
 * @return the activation of this layer
 */
const Activation& Dense::getActivation() const
{
    return this->_activation;
}

/**
 * @param input the input to this layer
 * @return the output matrix of this layer
*/
Matrix& Dense::operator()(Matrix& input) const
{
    input = this->_weights * input;
    input += this->_bias;
    input = this->_activation(input);
    return input;
}


