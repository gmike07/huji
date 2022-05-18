#include "utils.h"
#include "global.h"
#include <ctype.h>

int isnumber(unsigned char *candidate, int len)
{
    int i;
    for (i = 0; i < len; i++)
    {
        if(!isdigit(candidate[i]))
        {
            return FALSE;
        }
    }

    return TRUE;
}