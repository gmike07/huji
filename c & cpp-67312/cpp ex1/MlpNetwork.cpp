//
// Created by Mike Greenbaum on 12/14/2019.
//

#include "MlpNetwork.h"
#include <iostream>
#include "Matrix.h"
#define ERROR_IM_DIMS  "Error: wrong dims of image"
#define ERROR_WEIGHTS_BIAS "Error: wrong dims of weights or biases"

/**
 * @param weights the weights of the network
 * @param biases the biases of the network
 */
MlpNetwork::MlpNetwork(const Matrix (&weights)[MLP_SIZE], const Matrix (&biases)[MLP_SIZE]) :_layers(
{
    Dense(weights[0], biases[0], Relu),
    Dense(weights[1], biases[1], Relu),
    Dense(weights[2], biases[2], Relu),
    Dense(weights[3], biases[3], Softmax)
})
{
    for(int i = 0; i < MLP_SIZE; i++)
    {
        if(weightsDims[i].cols != weights[i].getCols() || weightsDims[i].rows != weights[i].getRows()
          || biasDims[i].cols != biases[i].getCols() || biasDims[i].rows != biases[i].getRows())
        {
            std::cerr << ERROR_WEIGHTS_BIAS << std::endl;
            exit(EXIT);
        }
    }
}

/**
 * @param input the input to the network
 * @return the output of the network
 */
Digit MlpNetwork::operator()(Matrix& input) const
{

    if(input.getCols() != 1 || input.getRows() != imgDims.cols * imgDims.rows)
    {
        std::cerr << ERROR_IM_DIMS << std::endl;
        exit(EXIT);
    }
    for(int i = 0; i < MLP_SIZE; i++)
    {
        input = _layers[i](input);
    }
    int bestGuess = 0;
    float bestGuessValue = 0;
    float value = 0;
    for(int i = 0; i < input.getRows() * input.getCols(); i++)
    {
        value = input[i];
        if(value > bestGuessValue)
        {
            bestGuess = i;
            bestGuessValue = value;
        }
    }
    Digit d;
    d.value = bestGuess;
    d.probability = bestGuessValue;
    return d;
}
