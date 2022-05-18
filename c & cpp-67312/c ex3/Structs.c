//
// Created by Mike Greenbaum on 11/30/2019.
//
#include <string.h>
#include <stdlib.h>
#include "Structs.h"
#include <math.h>
#define ERROR 0
#define SUCCESS 1

/**
 * CompFunc for strings (assumes strings end with "\0")
 * @param a - char* pointer
 * @param b - char* pointer
 * @return equal to 0 iff a == b. lower than 0 if a < b. Greater than 0 iff b < a. (lexicographic
 * order)
 */
int stringCompare(const void *a, const void *b)
{
    if(a == NULL || b == NULL)
    {
        return 0;
    }
    char *string1 = (char*)a;
    char *string2 = (char*)b;
    int length1 = (int)strlen(string1);
    int length2 = (int)strlen(string2);
    int minimumLength = length1 <= length2 ? length1 : length2;
    for(int i = 0; i < minimumLength; i++)
    {
        if(string1[i] != string2[i])
        {
            return string1[i] - string2[i];
        }
    }
    return length1 - length2;
}

/**
 * ForEach function that concatenates the given word to pConcatenated. pConcatenated is already allocated with
 * enough space.
 * @param word - char* to add to pConcatenated
 * @param pConcatenated - char*
 * @return 0 on failure, other on success
 */
int concatenate(const void *word, void *pConcatenated)
{
    if(word == NULL || pConcatenated == NULL)
    {
        return ERROR;
    }
    char *string1 = (char*)pConcatenated;
    char *string2 = (char*)word;
    int length1 = (int)strlen(string1);
    int length2 = (int)strlen(string2);
    for(int i = 0; i < length2; i++)
    {
        string1[length1 + i] = string2[i];
    }
    string1[length1 + length2] = '\n';
    string1[length1 + length2 + 1] = '\0';
    return SUCCESS;
}

/**
 * FreeFunc for strings
 */
void freeString(void *s)
{
    if(s != NULL)
    {
        free((char*) s);
    }
}

/**
 * CompFunc for Vectors, compares element by element, the vector that has the first larger
 * element is considered larger. If vectors are of different lengths and identify for the length
 * of the shorter vector, the shorter vector is considered smaller.
 * @param a - first vector
 * @param b - second vector
 * @return equal to 0 iff a == b. lower than 0 if a < b. Greater than 0 iff b < a.
 */
int vectorCompare1By1(const void *a, const void *b)
{
    if(a == NULL || b == NULL)
    {
        return ERROR;
    }
    Vector *v1 = (Vector*)a;
    Vector *v2 = (Vector*)b;
    if(v1->vector == NULL || v2->vector == NULL)
    {
        return 0;
    }
    int length = v1->len <= v2->len ? v1->len : v2->len;
    for(int i = 0; i < length; i++)
    {
        if(v1->vector[i] > v2->vector[i])
        {
            return 1;
        }
        if(v1->vector[i] < v2->vector[i])
        {
            return -1;
        }
    }
    return v1->len - v2->len;
}

/**
 * FreeFunc for vectors
 */
void freeVector(void *pVector)
{
    if(pVector != NULL)
    {
        Vector *v = (Vector *)pVector;
        free(v->vector);
        free(v);
    }
}

/**
 * @param vector the vector to calculate
 * @return the norm of the vector, if an error occured -1
 */
static double calculateNorm(Vector *vector)
{
    if(vector == NULL || vector->vector == NULL)
    {
        return -1;
    }
    double sum = 0;
    for(int i = 0; i < vector->len; i++)
    {
        sum += (vector->vector[i] * vector->vector[i]);
    }
    return sqrt(sum);
}

/**
 * copy pVector to pMaxVector if : 1. The norm of pVector is greater then the norm of pMaxVector.
 * 								   2. pMaxVector == NULL.
 * @param pVector pointer to Vector
 * @param pMaxVector pointer to Vector
 * @return 1 on success, 0 on failure (if pVector == NULL: failure).
 */
int copyIfNormIsLarger(const void *pVector, void *pMaxVector)
{
    if(pVector == NULL || pMaxVector == NULL || ((Vector*)pVector)->vector == NULL)
    {
        return ERROR;
    }
    Vector *v1 = (Vector *)pVector;
    Vector *v2 = (Vector *)pMaxVector;
    if(calculateNorm(v1) <= calculateNorm(v2))
    {
        return SUCCESS;
    }
    v2->len = v1->len;
    if(v2->vector != NULL)
    {
        free(v2->vector);
    }
    v2->vector = malloc(v2->len * sizeof(double));
    if(v2->vector == NULL)
    {
        return ERROR;
    }
    for(int i = 0; i < v2->len; i++)
    {
        v2->vector[i] = v1->vector[i];
    }
    return SUCCESS;
}

/**
 * @param tree a pointer to a tree of Vectors
 * @return pointer to a *copy* of the vector that has the largest norm (L2 Norm).
 */
Vector *findMaxNormVectorInTree(RBTree *tree)
{
    if(tree == NULL)
    {
        return NULL;
    }
    Vector *v = malloc(sizeof(Vector));
    v->len = 0;
    v->vector = NULL;
    if(forEachRBTree(tree, copyIfNormIsLarger, v) == ERROR)
    {
        freeVector(v);
        return NULL;
    }
    return v;
}