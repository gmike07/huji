#ifndef EX4_CELLULAR_PARSE_OPERATORS_H
#define EX4_CELLULAR_PARSE_OPERATORS_H

#include "cellular.h"
/*
 * Returns the list of operators as appears in the AT+COPS=? response
 * Assumes that "OK" is contained in buf
 * If empty response is received, i.e.: +COPS: ,,(0,1,2,3,4),(0,1,2,90,91)
 * then -1 is returned
 */
int ParseOperators(unsigned char *buf, OPERATOR_INFO *opList, int maxops, int *numOpsFound);

#endif //EX4_CELLULAR_PARSE_OPERATORS_H
