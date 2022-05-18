#include <fstream>

#include "Matrix.h"
#include "Activation.h"
#include "Dense.h"
#include "MlpNetwork.h"

#define QUIT "q"
#define INSERT_IMAGE_PATH "Please insert image path:"
#define ERROR_INAVLID_PARAMETER "Error: invalid Parameters file for layer: "
#define ERROR_INVALID_INPUT "Error: Failed to retrieve input. Exiting.."
#define ERROR_INVALID_IMG "Error: invalid image path or size: "
#define USAGE_MSG "Usage:\n" \
                  "\t./mlpnetwork w1 w2 w3 w4 b1 b2 b3 b4\n" \
                  "\twi - the i'th layer's weights\n" \
                  "\tbi - the i'th layer's biases"


#define ARGS_START_IDX 1
#define ARGS_COUNT (ARGS_START_IDX + (MLP_SIZE * 2))
#define WEIGHTS_START_IDX ARGS_START_IDX
#define BIAS_START_IDX (ARGS_START_IDX + MLP_SIZE)




/**
 * Prints program usage to stdout.
 */
void usage()
{
    std::cout << USAGE_MSG << std::endl;
}

/**
 * Given a binary file path and a matrix,
 * reads the content of the file into the matrix.
 * file must match matrix in size in order to read successfully.
 * @param filePath - path of the binary file to read
 * @param mat -  matrix to read the file into.
 * @return boolean status
 *          true - success
 *          false - failure
 */
bool readFileToMatrix(const std::string &filePath, Matrix &mat)
{
    std::ifstream is;
    is.open(filePath, std::ios::in | std::ios::binary | std::ios::ate);
    if(!is.is_open())
    {
        return false;
    }

    long int matByteSize = (long int) mat.getCols() * mat.getRows() * sizeof(float);
    if(is.tellg() != matByteSize)
    {
        is.close();
        return false;
    }

    is.seekg(0, std::ios_base::beg);
    is >> mat;
    is.close();
    return true;
}

/**
 * Loads MLP parameters from weights & biases paths
 * to Weights[] and Biases[].
 * Exits (code == 1) upon failures.
 * @param paths array of programs arguments, expected to be mlp parameters
 *        path.
 * @param weights array of matrix, weigths[i] is the i'th layer weights matrix
 * @param biases array of matrix, biases[i] is the i'th layer bias matrix
 *          (which is actually a vector)
 */
void loadParameters(char *paths[ARGS_COUNT], Matrix weights[MLP_SIZE], Matrix biases[MLP_SIZE])
{
    for(int i = 0; i < MLP_SIZE; i++)
    {
        weights[i] = Matrix(weightsDims[i].rows, weightsDims[i].cols);
        biases[i] = Matrix(biasDims[i].rows, biasDims[i].cols);

        std::string weightsPath(paths[WEIGHTS_START_IDX + i]);
        std::string biasPath(paths[BIAS_START_IDX + i]);

        if(!(readFileToMatrix(weightsPath, weights[i]) &&
           readFileToMatrix(biasPath, biases[i])))
        {
            std::cerr << ERROR_INAVLID_PARAMETER << (i + 1) << std::endl;
            exit(EXIT_FAILURE);
        }

    }
}

/**
 * This programs Command line interface for the mlp network.
 * Looping on: {
 *                  Retrieve user input
 *                  Feed input to mlpNetwork
 *                  print image & netowrk prediction
 *             }
 * Exits (code == 1) on fatal errors: unable to read user input path.
 * @param mlp MlpNetwork to use in order to predict img.
 */
void mlpCli(MlpNetwork &mlp)
{
    Matrix img(imgDims.rows, imgDims.cols);
    std::string imgPath;

    std::cout << INSERT_IMAGE_PATH << std::endl;
    std::cin >> imgPath;
    if(!std::cin.good())
    {
        std::cout << ERROR_INVALID_INPUT << std::endl;
        exit(EXIT_FAILURE);
    }

    while(imgPath != QUIT)
    {
        if(readFileToMatrix(imgPath, img))
        {
            Matrix imgVec = img;
            Digit output = mlp(imgVec.vectorize());
            std::cout << "Image processed:" << std::endl
                      << img << std::endl;
            std::cout << "Mlp result: " << output.value <<
                      " at probability: " << output.probability << std::endl;
        }
        else
        {
            std::cout << ERROR_INVALID_IMG << imgPath << std::endl;
        }

        std::cout << INSERT_IMAGE_PATH << std::endl;
        std::cin >> imgPath;
        if(!std::cin.good())
        {
            std::cout << ERROR_INVALID_INPUT << std::endl;
            exit(EXIT_FAILURE);
        }
    }
}

/**
 * Program's main
 * @param argc count of args
 * @param argv args values
 * @return program exit status code
 */
int main(int argc, char **argv)
{
    if(argc != ARGS_COUNT)
    {
        usage();
        exit(EXIT_FAILURE);
    }

    Matrix weights[MLP_SIZE];
    Matrix biases[MLP_SIZE];
    loadParameters(argv, weights, biases);

    MlpNetwork mlp(weights, biases);

    mlpCli(mlp);


    return EXIT_SUCCESS;
}
