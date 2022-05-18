//
// Created by Mike Greenbaum on 12/14/2019.
//

#ifndef EX1_DENSE_H
#define EX1_DENSE_H

#include "Matrix.h"
#include "Activation.h"
/**
 * @class Dense
 * @brief the class represents a layer in the network
 */
class Dense
{
public:
    /**
     * @param weights the weights of this layer
     * @param bias the bias of this layer
     * @param activationType the activation type for this layer
     */
    Dense(const Matrix& weights, const Matrix& bias, ActivationType activationType);

    /**
     * @return the weights of this layer
     */
    const Matrix& getWeights() const;

    /**
     * @return the bias of this layer
     */
    const Matrix& getBias() const;

    /**
     * @return the activation of this layer
     */
    const Activation& getActivation() const;

    /**
     * @param input the input to this layer
     * @return the output matrix of this layer
     */
    Matrix& operator()(Matrix& input) const;
private:
    //the weights of this layer
    const Matrix& _weights;
    //the bias of this layer
    const Matrix& _bias;
    //the activation of this layer
    const Activation _activation;
};
#endif //EX1_DENSE_H
