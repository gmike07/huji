#include "utils.h"
#include "global.h"
#include <ctype.h>
#include "sl_sleeptimer.h"

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

void sleep(unsigned int ms_time)
{
    sl_sleeptimer_delay_millisecond(ms_time);
}