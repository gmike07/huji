//
// Created by Mike Greenbaum on 12/14/2019.
//
#include "Matrix.h"
#include <string>
#define READ_ERROR "Error: read into matrix didn't read everything"
#define ERROR_WRONG_INDICES "Error: trying to access invalid indexes i, j in matrix"
#define ERROR_WRONG_INDEX "Error: trying to access invalid index in matrix"
#define ERROR_MEMORY_EQ "Error: couldn't allocate memory in = in matrix"
#define ERROR_NEGATIVE_DIMS "Error: the cols or the rows are negative"
#define ERROR_MEMORY_CTOR "Error: couldn't allocate memory in ctor"
#define ERROR_PLUS_EQ_DIMS "Error: the += of 2 matrices are of wrong dims!"
#define ERROR_PLUS_DIMS "Error: the sum of 2 matrices are of wrong dims!"
#define ERROR_MUL_DIMS "Error: the multiplication of 2 matrices are of wrong dims!"
#define FULL_CELL "**"
#define EMPTY_CELL "  "
#define PROBABILITY 0.1f

/**
 * @param s the string to print if an error occured and then TERMINATE
 * @param errorOccured true iff an error
 */
void printError(const std::string &s, bool errorOccured)
{
    if(!errorOccured)
    {
        return;
    }
    std::cerr << s << std::endl;
    exit(EXIT);
}

/**
 * @param rows the amount of rows in the matrix
 * @param cols the amount of cols in the matrix
 */
Matrix::Matrix(const int rows, const int cols): _dims({rows, cols})
{
    printError(ERROR_NEGATIVE_DIMS, cols <= 0 || rows <= 0);
    this->_matrix = new (std::nothrow) float[cols * rows];
    printError(ERROR_MEMORY_CTOR, this->_matrix == nullptr);
    for(int i = 0; i < cols * rows; i++)
    {
        this->_matrix[i] = 0;
    }
}

/**
 * create a matrix of 1 row and 1 col
 */
Matrix::Matrix(): Matrix(1, 1)
{
}

/**
 * @param m the matrix to copy, copy ctor
 */
Matrix::Matrix(const Matrix &m): Matrix(m.getRows(), m.getCols())
{
    for(int i = 0; i < m.getRows() * m.getCols(); i++)
    {
        this->_matrix[i] = m._matrix[i];
    }
}

/**
 * the dtor of the class
 */
Matrix::~Matrix()
{
    delete[] this->_matrix;
}

/**
 * @return the rows of the matrix
 */
int Matrix::getRows() const
{
    return this->_dims.rows;
}
/**
 * @return the cols of the matrix
 */
int Matrix::getCols() const
{
    return this->_dims.cols;
}

/**
 * @return the matrix itself after changing it to a vector from a matrix (1D)
 */
Matrix& Matrix::vectorize()
{
    this->_dims.rows *= this->_dims.cols;
    this->_dims.cols = 1;
    return *this;
}

/**
 * prints the values of matrix to cout
 */
void Matrix::plainPrint() const
{
    for(int i = 0; i < this->getRows(); i++)
    {
        for(int j = 0; j < this->getCols(); j++)
        {
            std::cout << this->_matrix[i * this->getCols() + j] << ' ';
        }
        std::cout << std::endl;
    }
}

/**
 * @param other other matrix
 * @return self * other
 */
Matrix Matrix::operator*(const Matrix& other) const
{
    printError(ERROR_MUL_DIMS, this->getCols() != other.getRows());
    Matrix m(this->getRows(), other.getCols());
    for(int i = 0; i < this->getRows(); i++)
    {
        for(int j = 0; j < other.getCols(); j++)
        {
            float sum = 0;
            for(int k = 0; k < this->getCols(); k++)
            {
                sum += this->_matrix[i * this->getCols() + k] * other._matrix[k * other.getCols() + j];
            }
            m._matrix[i * m.getCols() + j] = sum;
        }
    }
    return m;
}

/**
 * @param c the scalar
 * @param matrix the matrix
 * @return matrix * c without changing matrix
 */
Matrix Matrix::operator*(const float& c) const
{
    Matrix m(this->getRows(), this->getCols());
    for(int i = 0; i < this->getRows() * this->getCols(); i++)
    {
        m._matrix[i] = c * this->_matrix[i];
    }
    return m;
}

/**
 * @param c the scalar
 * @param matrix the matrix
 * @return matrix * c without changing matrix
 */
Matrix operator*(const float& c, const Matrix& matrix)
{
    return matrix * c;
}

/**
 * @param other other matrix
 * @return adds other to itself and returns the matrix if was correct, else TERMINATE
 */
Matrix Matrix::operator+(const Matrix& other) const
{
    printError(ERROR_PLUS_DIMS, this->getCols() != other.getCols() || this->getRows() != other.getRows());
    Matrix m(this->getRows(), this->getCols());
    for(int i = 0; i < this->getRows() * this->getCols(); i++)
    {
        m._matrix[i] = other._matrix[i] + this->_matrix[i];
    }
    return m;
}

/**
 * @param other other matrix
 * @return adds other to itself and returns a reference to self if was correct, else TERMINATE
 */
Matrix& Matrix::operator+=(const Matrix& other)
{
    printError(ERROR_PLUS_EQ_DIMS, this->getCols() != other.getCols() || this->getRows() != other.getRows());
    for(int i = 0; i < getRows() * getCols(); i++)
    {
        this->_matrix[i] += other._matrix[i];
    }
    return *this;
}

/**
 * @param other other matrix
 * @return itself after setting itself's data to be other's data
 */
Matrix& Matrix::operator=(const Matrix& other)
{
    if(other.getCols() * other.getRows() != this->getCols() * this->getRows())
    {
        delete[] this->_matrix;
        this->_matrix = new (std::nothrow) float[other._dims.cols * other._dims.rows];
        printError(ERROR_MEMORY_EQ, this->_matrix == nullptr);
    }
    this->_dims.cols = other._dims.cols;
    this->_dims.rows = other._dims.rows;
    for(int i = 0; i < getRows() * getCols(); i++)
    {
        this->_matrix[i] = other._matrix[i];
    }
    return *this;
}

/**
 * @param index the index
 * @return the matrix in index if the index is correct, else TERMINATE
 */
float& Matrix::operator[](const int index)
{
    printError(ERROR_WRONG_INDEX, index < 0 || index >= getRows() * getCols());
    return this->_matrix[index];
}

/**
 * @param index the index
 * @return the matrix in index if the index is correct, else TERMINATE
 */
float Matrix::operator[](const int index) const
{
    printError(ERROR_WRONG_INDEX, index < 0 || index >= getRows() * getCols());
    return this->_matrix[index];
}

/**
 * @param i the row index
 * @param j the col index
 * @return the matrix in i,j if the indexes are correct, else TERMINATE
 */
float& Matrix::operator()(const int i, const int j)
{
    printError(ERROR_WRONG_INDICES, i < 0 || i >= this->getRows() || j < 0 || j >= this->getCols());
    return this->_matrix[i * getCols() + j];
}

/**
 * @param i the row index
 * @param j the col index
 * @return the matrix in i,j if the indexes are correct, else TERMINATE
 */
float Matrix::operator()(const int i, const int j) const
{
    printError(ERROR_WRONG_INDICES, i < 0 || i >= this->getRows() || j < 0 || j >= this->getCols());
    return this->_matrix[i * getCols() + j];
}

/**
 * this function reads from the stream to the matrix
 * @param in the input stream
 * @param matrix the matrix to read into
 * @return the stream in
 */
std::istream& operator>>(std::istream& in, Matrix& matrix)
{
    int i = 0;
    while (in.good() && in.read((char*)(&matrix._matrix[i]), sizeof(float)))
    {
        i++;
    }
    printError(READ_ERROR, i != matrix.getRows() * matrix.getCols() || !in.eof());
    return in;
}

/**
 * the function adds the matrix to the stream as image
 * @param os the output stream
 * @param matrix the matrix to add to the stream
 * @return the stream os
*/
std::ostream& operator<<(std::ostream& os, const Matrix& matrix)
{
    for(int i = 0; i < matrix.getRows(); i++)
    {
        for(int j = 0; j < matrix.getCols(); j++)
        {
            if(matrix._matrix[i * matrix.getCols() + j] <= PROBABILITY)
            {
                os << EMPTY_CELL;
            }
            else
            {
                os << FULL_CELL;
            }
        }
        os << std::endl;
    }
    return os;
}
