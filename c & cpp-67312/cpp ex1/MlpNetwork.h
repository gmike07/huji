//MlpNetwork.h

#ifndef MLPNETWORK_H
#define MLPNETWORK_H

#include "Digit.h"
#include "Matrix.h"
#include "Dense.h"

#define MLP_SIZE 4

const MatrixDims imgDims = {28, 28};
const MatrixDims weightsDims[] = {{128, 784}, {64, 128}, {20, 64}, {10, 20}};
const MatrixDims biasDims[]    = {{128, 1}, {64, 1}, {20, 1},  {10, 1}};
/**
 * @class MlpNetwork
 * @brief the class represents the network
 */
class MlpNetwork
{
public:
    /**
     * @param weights the weights of the network
     * @param biases the biases of the network
     */
    MlpNetwork(const Matrix (&weights)[MLP_SIZE], const Matrix (&biases)[MLP_SIZE]);

    /**
     * @param input the input to the network
     * @return the output of the network
     */
    Digit operator()(Matrix& input) const;
private:
    //the layers of this network
    Dense _layers[MLP_SIZE];
};

#endif // MLPNETWORK_H
