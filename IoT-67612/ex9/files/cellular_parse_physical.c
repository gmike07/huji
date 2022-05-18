#include "cellular_parse_physical.h"
#include "global.h"
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include "utils.h"
#include "my_printf_lib.h"
#define CSQ_BUF 4

#define CSQ_ERR_CODE 99

static char iccid_response_prefix[] = "+CCID: ";
static char imei_response_prefix[] = "\r\n";
static char csq_response_prefix[] = "+CSQ: ";

/////// Public Functions ///////

int ParseICCID(unsigned char *buf, char* iccid, int maxlen)
{
    char *ret;
    int i;

    ret = strstr(buf, iccid_response_prefix);

    if (ret == NULL)
    {
        return FAILURE_CODE;
    }

    ret = ret + strlen(iccid_response_prefix);

    for (i = 0; i < maxlen; i++)
    {
        if (isdigit(ret[i]))
        {
            iccid[i] = ret[i];
        }
        else
        {
            break;
        }
    }

    return SUCCESS_CODE;
}

int ParseIMEI(unsigned char *buf, char* imei, int maxlen)
{
    char *ret;
    int i;

    ret = strstr(buf, imei_response_prefix);

    if (ret == NULL)
    {
        return FAILURE_CODE;
    }

    ret = ret + strlen(imei_response_prefix);

    for (i = 0; i < maxlen; i++)
    {
        if (isdigit(ret[i]))
        {
            imei[i] = ret[i];
        }
        else
        {
            break;
        }
    }
    return SUCCESS_CODE;
}

int ParseSignalQuality(unsigned char *buf, int *signal)
{
    char *ret;
    static char csq_str[CSQ_BUF];
    int csq;

    memset(csq_str, 0, CSQ_BUF);

    ret = strstr(buf, csq_response_prefix);

    if (ret == NULL)
    {
        return FAILURE_CODE;
    }

    ret = ret + strlen(csq_response_prefix);

    if (isdigit(*ret) && isdigit(*(ret + 1)))
    {
        csq_str[0] = *ret;
        csq_str[1] = *(ret + 1);
        csq = atoi(csq_str);
    }
    else if (isdigit(*ret) && *(ret + 1) == ',')
    {
        csq = (int)((*ret) - '0');
    }
    else
    {
        *signal = csq;
        return FAILURE_CODE;
    }

    if (csq == CSQ_ERR_CODE)
    {
        return FAILURE_CODE;
    }

    *signal =-113 + csq * 2;

    return SUCCESS_CODE;
}