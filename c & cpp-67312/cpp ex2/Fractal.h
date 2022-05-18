//
// Created by Mike Greenbaum on 12/29/2019.
//

#ifndef EX2_FRACTAL_H
#define EX2_FRACTAL_H

#include <vector>
#include <iostream>
#include <string>
#include <cmath>
#define MIN_FRACTAL_DIM 1
#define MAX_FRACTAL_DIM 6

#define CARPET_FRACTAL_SQUARE_LENGTH 3
#define TRIANGLE_FRACTAL_SQUARE_LENGTH 2
#define VICSEK_FRACTAL_SQUARE_LENGTH 3
#define FILLED '#'
#define EMPTY ' '

/**
 * @class this class represents a abstract fractal
 */
class Fractal
{
public:
    /**
     * @param fractalDim the amount of recursion in the fractal
     * @param baseCase the baseCase of the fractal
     */
    Fractal(int fractalDim, int baseCase);
    /**
     * a function that draws the fractals, uses drawFractalHelper which is an abstract method!
     */
    virtual void drawFractal() const;

    /**
     * a function inits the fractal to be printed
     */
    virtual void initFractal();

    /**
     * the default dtor
     */
    virtual ~Fractal();

private:
    // the amount of recursion in the fractal
   int _fractalDim;
   // the length of every induction in the fractal
   int _baseCase;
    // output to the user, a matrix of the fractal in point i,j is filled or empty
    std::vector<std::vector<char>> _fractal;
    /**
     * @param fractal the fractal to fill
     * @param row the row to fill with the fractal
     * @param col the col to fill with the fractal
     * @param squareLength the length of the fractal to fill
     * fills the fractal in place (row, col) up to (row + squareLength, col + squareLength)
     */
    virtual void _initFractalHelper(std::vector<std::vector<char>>& fractal, int row, int col, int squareLength) = 0;
};

/**
 * @class a class that represents the SierpinskiCarpetFractal
 */
class SierpinskiCarpetFractal : public Fractal
{
public:
    /**
     * @param fractalDim the amount of recursion in the fractal
     */
    SierpinskiCarpetFractal(int fractalDim);

private:
    /**
     * @param fractal the fractal to fill
     * @param row the row to fill with the fractal
     * @param col the col to fill with the fractal
     * @param squareLength the length of the fractal to fill
     * fills the SierpinskiCarpetFractal in place (row, col) up to (row + squareLength, col + squareLength)
     */
    void _initFractalHelper(std::vector<std::vector<char>>& fractal, int row, int col, int squareLength) override;
};

/**
 * @class a class that represents the SierpinskiTriangleFractal
 */
class SierpinskiTriangleFractal : public Fractal
{
public:
    /**
     * @param fractalDim the amount of recursion in the fractal
     */
    SierpinskiTriangleFractal(int fractalDim);

private:
    /**
     * @param fractal the fractal to fill
     * @param row the row to fill with the fractal
     * @param col the col to fill with the fractal
     * @param squareLength the length of the fractal to fill
     * fills the SierpinskiTriangleFractal in place (row, col) up to (row + squareLength, col + squareLength)
     */
    void _initFractalHelper(std::vector<std::vector<char>>& fractal, int row, int col, int squareLength) override;
};

/**
 * @class a class that represents the VicsekFractal
 */
class VicsekFractal : public Fractal
{
public:
    /**
     * @param fractalDim the amount of recursion in the fractal
     */
    VicsekFractal(int fractalDim);

private:
    /**
     * @param fractal the fractal to fill
     * @param row the row to fill with the fractal
     * @param col the col to fill with the fractal
     * @param squareLength the length of the fractal to fill
     * fills the VicsekFractal in place (row, col) up to (row + squareLength, col + squareLength)
     */
    void _initFractalHelper(std::vector<std::vector<char>>& fractal, int row, int col, int squareLength) override;
};

/**
 * @class a class that creates fractals if the inputs are correct else nullptr
 */
class FractalFactory
{
public:
    /**
     * @brief this enum represents the different types of fractals
     */
    enum FractalType
    {
        SierpinskiCarpetType = 1,
        SierpinskiTriangleType = 2,
        VicsekFractalType = 3
    };
    /**
     * @param type the type of the fractal
     * @param n the amount of recursion in the fractal
     * @return the fractal created if could and input is correct, else nullptr
     */
    static Fractal* createFractal(FractalType type, int n);
};
#endif //EX2_FRACTAL_H
