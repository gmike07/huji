//
// Created by evyat on 10/13/2019.
//

#include "RBTree.h"

#ifndef TA_EX3_STRUCTS_H
#define TA_EX3_STRUCTS_H

/**
 * Represents a vector. The double* should be dynamically allocated
 */
typedef struct Vector
{
	int len;
	double *vector;
} Vector;


/**
 * CompFunc for strings (assumes strings end with "\0")
 * @param a - char* pointer
 * @param b - char* pointer
 * @return equal to 0 iff a == b. lower than 0 if a < b. Greater than 0 iff b < a. (lexicographic
 * order)
 */
int stringCompare(const void *a, const void *b); // implement it in Structs.c

/**
 * ForEach function that concatenates the given word to pConcatenated. pConcatenated is already allocated with
 * enough space.
 * @param word - char* to add to pConcatenated
 * @param pConcatenated - char*
 * @return 0 on failure, other on success
 */
int concatenate(const void *word, void *pConcatenated); // implement it in Structs.c

/**
 * FreeFunc for strings
 */
void freeString(void *s); // implement it in Structs.c

/**
 * CompFunc for Vectors, compares element by element, the vector that has the first larger
 * element is considered larger. If vectors are of different lengths and identify for the length
 * of the shorter vector, the shorter vector is considered smaller.
 * @param a - first vector
 * @param b - second vector
 * @return equal to 0 iff a == b. lower than 0 if a < b. Greater than 0 iff b < a.
 */
int vectorCompare1By1(const void *a, const void *b); // implement it in Structs.c

/**
 * FreeFunc for vectors
 */
void freeVector(void *pVector); // implement it in Structs.c

/**
 * copy pVector to pMaxVector if : 1. The norm of pVector is greater then the norm of pMaxVector.
 * 								   2. pMaxVector == NULL.
 * @param pVector pointer to Vector
 * @param pMaxVector pointer to Vector
 * @return 1 on success, 0 on failure (if pVector == NULL: failure).
 */
int copyIfNormIsLarger(const void *pVector, void *pMaxVector); // implement it in Structs.c

/**
 * @param tree a pointer to a tree of Vectors
 * @return pointer to a *copy* of the vector that has the largest norm (L2 Norm).
 */
Vector *findMaxNormVectorInTree(RBTree *tree); // implement it in Structs.c You must use copyIfNormIsLarger in the implementation!


#endif //TA_EX3_STRUCTS_H
