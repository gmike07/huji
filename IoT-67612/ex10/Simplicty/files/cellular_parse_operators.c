#include "cellular_parse_operators.h"
#include "utils.h"
#include "global.h"
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include "utils.h"
#include "my_printf_lib.h"

#define OPERATOR_BUF_SIZE 60

#define NUMERIC_NAME_BUF_LEN 10
#define NUMERIC_NAME_MIN_LEN 5
#define NUMERIC_NAME_MAX_LEN 6

static char cops_list_response_prefix[] = "+COPS: ";
static char cops_opt_start[] = "(";
static char cops_opt_end[] = ")";
static char cops_opt_inner_delimiter[] = ",";

static char gsm[] = "2G";
static char umts[] = "3G";

typedef enum __access_technology_code {
    GSM = 0,
    UMTS = 2
} accessTechnologyCode;

int getFirstOperatorString(unsigned char *buf, unsigned char *opt_buf, int *opt_end_len);
unsigned char *parseOperatorStatus(unsigned char *buf, OP_STATUS *op_stat);
unsigned char *parseOperatorName(unsigned char *buf,  char *operator_name);
unsigned char *parseOperatorShortName(unsigned char *buf,  char *operator_short_name);
unsigned char *parseOperatorNumericName(unsigned char *buf, int *operator_code);
int parseOperatorAccessTech(unsigned char *curr, unsigned char *buf_start, char *access_technology);

int getFirstOperatorString(unsigned char *buf, unsigned char *opt_buf, int *opt_end_len)
{
    unsigned char *start, *end;

    start = strstr(buf, cops_opt_start);

    if (start == NULL)
    {
        return FAILURE_CODE;
    }

    end = strstr(start, cops_opt_end);

    if (end == NULL)
    {
        return FAILURE_CODE;
    }

    strncpy(opt_buf, start + 1, end - start - 1);
    *opt_end_len = end - buf;

    return SUCCESS_CODE;
}

unsigned char *parseOperatorStatus(unsigned char *buf, OP_STATUS *op_stat)
{
    unsigned char *ret;
    OP_STATUS op_stat_curr;

    ret = strstr(buf, cops_opt_inner_delimiter);

    if (ret == NULL)
    {
        return NULL;
    }

    if (ret - buf > 1)
    {
        return NULL;
    }

    if (!isdigit(*buf))
    {
        return NULL;
    }

    op_stat_curr = (*buf) - '0';

    switch (op_stat_curr)
    {
        case UNKNOWN_OPERATOR:
        case OPERATOR_AVAILABLE:
        case CURRENT_OPERATOR:
        case OPERATOR_FORBIDDEN:
            *op_stat = op_stat_curr;
            break;
        default:
            return NULL;
    }

    return ret;
}

unsigned char *parseOperatorName(unsigned char *buf,  char *operator_name)
{
    unsigned char *ret;

    ret = strstr(buf, cops_opt_inner_delimiter);

    if (ret - buf < 2) // opt name is at least ""
    {
        return NULL;
    }

    // name starts and ends with "
    if (*buf != '\"' && *(ret - 1) != '\"')
    {
        return NULL;
    }

    strncpy(operator_name, buf + 1, ret - buf - 2);

    return ret;
}

unsigned char *parseOperatorShortName(unsigned char *buf,  char *operator_short_name)
{
    unsigned char *ret;

    ret = strstr(buf, cops_opt_inner_delimiter);

    if (ret - buf < 2) // opt name is at least ""
    {
        return NULL;
    }

    // name starts and ends with "
    if (*buf != '\"' && *(ret - 1) != '\"')
    {
        return NULL;
    }

    strncpy(operator_short_name, buf + 1, ret - buf - 2);

    return ret;
}

unsigned char *parseOperatorNumericName(unsigned char *buf, int *operator_code)
{
    unsigned char *ret;
    static char numeric_name[NUMERIC_NAME_BUF_LEN];

    memset(numeric_name, 0, NUMERIC_NAME_BUF_LEN);

    ret = strstr(buf, cops_opt_inner_delimiter);

    if (ret == NULL)
    {
        return NULL;
    }

    // numeric name is at least "" and MCC and MNC
    if (ret - buf > NUMERIC_NAME_MAX_LEN + 2 || ret - buf < NUMERIC_NAME_MIN_LEN + 2)
    {
        return NULL;
    }

    // name starts and ends with "
    if (*buf != '\"' && *(ret - 1) != '\"')
    {
        return NULL;
    }

    strncpy(numeric_name, buf + 1, ret - buf - 2);

    if (!isnumber(numeric_name, strlen(numeric_name)))
    {
        return NULL;
    }

    *operator_code = atoi(numeric_name);

    return ret;
}

int parseOperatorAccessTech(unsigned char *curr, unsigned char *buf_start, char *access_technology)
{
    if (buf_start + strlen(buf_start) - 1 != curr)
    {
        return FAILURE_CODE;
    }

    if (!isdigit(*curr))
    {
        return FAILURE_CODE;
    }

    if ((int)((*curr) - '0') == GSM)
    {
        strcpy(access_technology, gsm);
    }
    else if ((int)((*curr) - '0') == UMTS)
    {
        strcpy(access_technology, umts);
    }
    else
    {
        return FAILURE_CODE;
    }

    return SUCCESS_CODE;
}

int parseOperator(unsigned char *opt_str, OPERATOR_INFO *opt)
{
    unsigned char *ret;
    unsigned char *start;
    static char operator_name[OPERATOR_BUF_SIZE];
    static char operator_short_name[OPERATOR_BUF_SIZE];
    static char access_technology[MAX_TECH_SIZE];
    int operator_code;
    OP_STATUS op_stat;

    memset(operator_name, 0, OPERATOR_BUF_SIZE);
    memset(operator_short_name, 0, OPERATOR_BUF_SIZE);
    memset(access_technology, 0, MAX_TECH_SIZE);

    start = opt_str;
    ret = parseOperatorStatus(start, &op_stat);

    if (ret == NULL)
    {
        return FAILURE_CODE;
    }

    start = opt_str + (ret - opt_str) + 1;
    ret = parseOperatorName(start, operator_name);

    if (ret == NULL)
    {
        return FAILURE_CODE;
    }

    start = opt_str + (ret - opt_str) + 1;

    ret = parseOperatorShortName(start, operator_short_name);

    if (ret == NULL)
    {
        return FAILURE_CODE;
    }

    start = opt_str + (ret - opt_str) + 1;

    ret = parseOperatorNumericName(start, &operator_code);

    if (ret == NULL)
    {
        return FAILURE_CODE;
    }

    start = opt_str + (ret - opt_str) + 1;

    if (parseOperatorAccessTech(start, opt_str, access_technology) < 0)
    {
        return FAILURE_CODE;
    }

    strcpy(opt->operator_name, operator_name);
    opt->operator_code = operator_code;
    strcpy(opt->access_technology, access_technology);
    opt->operator_status = op_stat;

    my_printf("op short name: %s\n", operator_short_name);

    return SUCCESS_CODE;
}

/////// Public Functions ///////

/*
 * Returns the list of operators as appears in the AT+COPS=? response
 * Assumes that "OK" is contained in buf
 * If empty response is received, i.e.: +COPS: ,,(0,1,2,3,4),(0,1,2,90,91)
 * then -1 is returned
 */
int ParseOperators(unsigned char *buf, OPERATOR_INFO *opList, int maxops, int *numOpsFound)
{
    char *ret, *curr_buf;
    static char operator[OPERATOR_BUF_SIZE];
    OPERATOR_INFO *curr_opt;
    int opt_end_len = 0, got_one = FALSE;

    *numOpsFound = 0;
    curr_opt = opList;

    ret = strstr(buf, cops_list_response_prefix);

    if (ret == NULL)
    {
        return FAILURE_CODE;
    }

    curr_buf = buf;
    do
    {
        memset(operator, 0, OPERATOR_BUF_SIZE);
        if (getFirstOperatorString(curr_buf, operator, &opt_end_len) < 0)
        {
            break;
        }

        curr_buf += opt_end_len;

        my_printf("Cellular: Found operator: %s\n", operator);

        if (parseOperator(operator, curr_opt) >= 0)
        {
            got_one = TRUE;
            curr_opt++;
            (*numOpsFound)++;
        }
    } while (*numOpsFound < maxops);

    if (got_one)
    {
        return SUCCESS_CODE;
    }

    return FAILURE_CODE;
}