// Matrix.h

#ifndef MATRIX_H
#define MATRIX_H
#include <iostream>
#include <fstream>
#define EXIT 1
/**
 * @struct MatrixDims
 * @brief Matrix dimensions container
 */
typedef struct MatrixDims
{
    int rows, cols;
} MatrixDims;


/**
 * @class Matrix
 * @brief the class represents a matrix
 */
class Matrix
{
public:
    /**
     * @param rows the amount of rows in the matrix
     * @param cols the amount of cols in the matrix
     */
    Matrix(const int rows, const int cols);

    /**
     * create a matrix of 1 row and 1 col
     */
    Matrix();

    /**
     * @param m the matrix to copy, copy ctor
     */
    Matrix(const Matrix &m);

    /**
     * the dtor of the class
     */
    ~Matrix();

    /**
     * @return the rows of the matrix
     */
    int getRows() const;

    /**
     * @return the cols of the matrix
     */
    int getCols() const;

    /**
     * @return the matrix itself after changing it to a vector from a matrix (1D)
     */
    Matrix& vectorize();

    /**
     * prints the values of matrix to cout
     */
    void plainPrint() const;

    /**
     * @param other other matrix
     * @return itself after setting itself's data to be other's data
     */
    Matrix& operator=(const Matrix& other);

    /**
     * @param other other matrix
     * @return self * other
     */
    Matrix operator*(const Matrix& other) const;

    /**
     * @param c the scalar
     * @param matrix the matrix
     * @return matrix * c without changing matrix
     */
    Matrix operator*(const float& c) const;

    /**
     * @param c the scalar
     * @param matrix the matrix
     * @return matrix * c without changing matrix
     */
    friend Matrix operator*(const float& c, const Matrix& matrix);

    /**
     * @param other other matrix
     * @return adds other to itself and returns the new matrix if was correct, else TERMINATE
     */
    Matrix operator+(const Matrix& other) const;

    /**
     * @param other other matrix
     * @return adds other to itself and returns a reference to self if was correct, else TERMINATE
     */
    Matrix& operator+=(const Matrix& other);

    /**
     * @param index the index
     * @return the matrix in index if the index is correct, else TERMINATE
     */
    float& operator[](const int index);
    /**
     * @param index the index
     * @return the matrix in index if the index is correct, else TERMINATE
     */
    float operator[](const int index) const;

    /**
     * @param i the row index
     * @param j the col index
     * @return the matrix in i,j if the indexes are correct, else TERMINATE
     */
    float& operator()(const int i, const int j);

    /**
     * @param i the row index
     * @param j the col index
     * @return the matrix in i,j if the indexes are correct, else TERMINATE
     */
    float operator()(const int i, const int j) const;

    /**
     * this function reads from the stream to the matrix
     * @param in the input stream
     * @param matrix the matrix to read into
     * @return the stream in
     */
    friend std::istream& operator>>(std::istream& in, Matrix& matrix);

    /**
     * the function adds the matrix to the stream as image
     * @param os the output stream
     * @param matrix the matrix to add to the stream
     * @return the stream os
     */
    friend std::ostream& operator<<(std::ostream& os, const Matrix& matrix);

private:
    //the dims of the matrix
    MatrixDims _dims{};
    //a pointer to the matrix array
    float* _matrix;
    /**
     * @param m the matrix to store the Relu in
     * @param matrix the matrix to apply Relu to
     * @return the m matrix after Relu
     */
    friend Matrix& _applyRelu(Matrix &m, const Matrix& matrix);

    /**
      * @param m the matrix to store the Softmax in
      * @param matrix the matrix to apply Softmax to
      * @return the m matrix after Softmax
      */
    friend Matrix& _applySoftmax(Matrix &m, const Matrix& matrix);
};
#endif //MATRIX_H
