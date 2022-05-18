//Digit.h
#ifndef DIGIT_H
#define DIGIT_H

/**
 * @struct Digit
 * @brief Identified (by Mlp network) Digit with
 *        the associated probability.
 * @var value - Identified digit value
 * @var probability - identification probability
 */
typedef struct Digit
{
    unsigned int value;
    float probability;
} Digit;

#endif //DIGIT_H
