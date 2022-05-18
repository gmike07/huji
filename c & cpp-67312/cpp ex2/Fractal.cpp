//
// Created by Mike Greenbaum on 12/29/2019.
//

#include "Fractal.h"

/**
 * @param fractalDim the amount of recursion in the fractal
 * @param baseCase the baseCase of the fractal
 */
Fractal::Fractal(int fractalDim, int baseCase): _fractalDim(fractalDim), _baseCase(baseCase)
{
}

/**
 * a function that draws the fractals, uses drawFractalHelper which is an abstract method!
 */
void Fractal::drawFractal() const
{
    int length = this->_fractal.size();
    for(int i = 0; i < length; i++)
    {
        for(int j = 0; j < length; j++)
        {
            std::cout << this->_fractal[i][j];
        }
        std::cout << std::endl;
    }
}

/**
 * a function inits the fractal to be printed
 */
void Fractal::initFractal()
{
    int squareLength = (int)pow(this->_baseCase, this->_fractalDim);
    std::vector<char> helper(squareLength, EMPTY);
    this->_fractal = std::vector<std::vector<char>>(squareLength, helper);
    this->_initFractalHelper(this->_fractal, 0, 0, squareLength);
}

/**
 * the default dtor
 */
Fractal::~Fractal() = default;

/**
 * @param fractalDim the amount of recursion in the fractal
 */
SierpinskiCarpetFractal::SierpinskiCarpetFractal(int fractalDim): Fractal(fractalDim, CARPET_FRACTAL_SQUARE_LENGTH)
{
}

/**
 * @param fractal the fractal to fill
 * @param row the row to fill with the fractal
 * @param col the col to fill with the fractal
 * @param squareLength the length of the fractal to fill
 * fills the SierpinskiCarpetFractal in place (row, col) up to (row + squareLength, col + squareLength)
 */
void SierpinskiCarpetFractal::_initFractalHelper(std::vector<std::vector<char>>& fractal, int row, int col,
                                                 int squareLength)
{
    if(squareLength == 1)
    {
        fractal[row][col] = FILLED;
        return;
    }
    int newLength = squareLength / CARPET_FRACTAL_SQUARE_LENGTH;
    for(int i = 0; i < CARPET_FRACTAL_SQUARE_LENGTH; i++)
    {
        for(int j = 0; j < CARPET_FRACTAL_SQUARE_LENGTH; j++)
        {
            if(i != 1 || j != 1) //the check that it is not the middle square
            {
                _initFractalHelper(fractal, row + i * newLength, col + j * newLength, newLength);
            }
        }
    }
}

/**
 * @param fractalDim the amount of recursion in the fractal
 */
SierpinskiTriangleFractal::SierpinskiTriangleFractal(int fractalDim): Fractal(fractalDim, TRIANGLE_FRACTAL_SQUARE_LENGTH)
{
}

/**
 * @param fractal the fractal to fill
 * @param row the row to fill with the fractal
 * @param col the col to fill with the fractal
 * @param squareLength the length of the fractal to fill
 * fills the SierpinskiTriangleFractal in place (row, col) up to (row + squareLength, col + squareLength)
 */
void SierpinskiTriangleFractal::_initFractalHelper(std::vector<std::vector<char>>& fractal, int row, int col,
                                                   int squareLength)
{
    if(squareLength == 1)
    {
        fractal[row][col] = FILLED;
        return;
    }
    int newLength = squareLength / TRIANGLE_FRACTAL_SQUARE_LENGTH;
    for(int i = 0; i < TRIANGLE_FRACTAL_SQUARE_LENGTH; i++)
    {
        for(int j = 0; j < TRIANGLE_FRACTAL_SQUARE_LENGTH; j++)
        {
            if(i != 1 || j != 1) //the check that it should be filled in the SierpinskiTriangleFractal
            {
                _initFractalHelper(fractal, row + i * newLength, col + j * newLength, newLength);
            }
        }
    }
}

/**
 * @param fractalDim the amount of recursion in the fractal
 */
VicsekFractal::VicsekFractal(int fractalDim): Fractal(fractalDim, 3)
{
}

/**
 * @param fractal the fractal to fill
 * @param row the row to fill with the fractal
 * @param col the col to fill with the fractal
 * @param squareLength the length of the fractal to fill
 * fills the VicsekFractal in place (row, col) up to (row + squareLength, col + squareLength)
 */
void VicsekFractal::_initFractalHelper(std::vector<std::vector<char>>& fractal, int row, int col, int squareLength)
{
    if(squareLength == 1)
    {
        fractal[row][col] = FILLED;
        return;
    }
    int newLength = squareLength / VICSEK_FRACTAL_SQUARE_LENGTH;
    for(int i = 0; i < VICSEK_FRACTAL_SQUARE_LENGTH; i++)
    {
        for(int j = 0; j < VICSEK_FRACTAL_SQUARE_LENGTH; j++)
        {
            if((i + j) % 2 == 0) //the check that it should be filled in the VicsekFractal
            {
                this->_initFractalHelper(fractal, row + i * newLength, col + j * newLength, newLength);
            }
        }
    }
}

/**
 * @param type the type of the fractal
 * @param n the amount of recursion in the fractal
 * @return the fractal created if could and input is correct, else nullptr
 */
Fractal* FractalFactory::createFractal(FractalType type, int n)
{
    if(n < MIN_FRACTAL_DIM || n > MAX_FRACTAL_DIM)
    {
        return nullptr;
    }
    if(type == FractalType::SierpinskiCarpetType)
    {
        return new (std::nothrow) SierpinskiCarpetFractal(n);
    }
    if(type == FractalType::SierpinskiTriangleType)
    {
        return new (std::nothrow) SierpinskiTriangleFractal(n);
    }
    if(type == FractalType::VicsekFractalType)
    {
        return new (std::nothrow) VicsekFractal(n);
    }
    return nullptr;
}