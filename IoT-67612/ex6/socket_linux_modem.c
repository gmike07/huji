#include "socket.h"
#include "cellular.h"
#include "global.h"

#include <stdio.h>
#include <netdb.h>	//hostent
#include <arpa/inet.h>
#include <string.h>

#define COM_PORT "/dev/ttyUSB0"

#define CONN_INACTIVE_TIMEOUT 60
#define CONN_KEEPINTVL 40

#define NUM_OF_OPERATORS 30
#define ICCID_BUF_LEN 30
#define IMEI_BUF_LEN 30
#define IPv4_BUF_LEN 16

#define FIND_COPS_ATTEMPTS 3

static char *g_host;
static int g_port;
OPERATOR_INFO ops[NUM_OF_OPERATORS] = { 0 };
char imei[IMEI_BUF_LEN] = { 0 };
int ops_found;

int hostname_to_ip(char *hostname , char* ip)
{
    struct hostent *he;
    struct in_addr **addr_list;
    int i;

    if ( (he = gethostbyname( hostname ) ) == NULL)
    {
        // get the host info
        herror("gethostbyname");
        return 1;
    }

    addr_list = (struct in_addr **) he->h_addr_list;

    for(i = 0; addr_list[i] != NULL; i++)
    {
        //Return the first one
        strcpy(ip , inet_ntoa(*addr_list[i]) );
        return 1;
    }

    return 0;
}

/////// Public Functions ///////

int SocketInit(char *host, int port)
{
    char iccid[ICCID_BUF_LEN] = { 0 };

    if (CellularInit(COM_PORT) < 0)
    {
        return FAILURE_CODE;
    }

    if (CellularWaitUntilModemResponds() < 0)
    {
        return FAILURE_CODE;
    }

    if (CellularGetIMEI(imei, IMEI_BUF_LEN) < 0)
    {
        return FAILURE_CODE;
    }

    printf("Socket: IMEI: %s\n", imei);

    if (CellularGetICCID(iccid, ICCID_BUF_LEN) < 0)
    {
        return FAILURE_CODE;
    }

    printf("Socket: ICCID: %s\n", iccid);

    if (CellularWaitUntilRegistered() < 0)
    {
        return FAILURE_CODE;
    }

    g_host = host;
    g_port = port;

    return SUCCESS_CODE;
}

int SocketConnect(void)
{
    int i, signal;
    char ipv4[IPv4_BUF_LEN] = { 0 };
    char ops_available = FALSE;
    char selectOpt = FALSE;

#ifndef AUTO_OPT
    for (i = 0; i < FIND_COPS_ATTEMPTS; i++)
    {
        if (CellularGetOperators(ops, NUM_OF_OPERATORS, &ops_found) < 0)
        {
            if (CellularWaitUntilModemResponds() < 0)
            {
                return FAILURE_CODE;
            }
        }
        else
        {
            ops_available = TRUE;
            break;
        }
    }

    if (!ops_available)
    {
        return FAILURE_CODE;
    }

    printf("Socket: ops found: %d\n", ops_found);
    for (i = 0; i < ops_found; i++)
    {
        printf("Socket: op name: %s\n", ops[i].operator_name);
        printf("Socket: operator code: %d\n", ops[i].operator_code);
        printf("Socket: access tech: %s\n", ops[i].access_technology);
        printf("Socket: op status: %d\n", ops[i].operator_status);
    }

    for (i = 0; i < ops_found; i++)
    {
        printf("Socket: registering to op %s with code %d\n", ops[i].operator_name, ops[i].operator_code);

        if (ops[i].operator_status != CURRENT_OPERATOR && ops[i].operator_status != OPERATOR_AVAILABLE)
        {
            printf("op is not available, skipping\n");
            continue;
        }

        if (CellularSetOperator(SET_OPT_MODE_MANUAL, ops[i].operator_code) < 0)
        {
            printf("Socket: Failed selecting op\n");
            continue;
        }

        printf("Socket: op selected\n");
        selectOpt = TRUE;
        break;
    }

    if (!selectOpt)
    {
        printf("Socket: No opt selected\n");
        return FAILURE_CODE;
    }
#else
    if (CellularSetOperator(SET_OPT_MODE_AUTO, 0) < 0)
    {
        printf("Socket: Failed registering\n");
        return FAILURE_CODE;
    }
#endif

    printf("Socket: selected operator successfully\n");

    if (CellularGetSignalQuality(&signal) < 0)
    {
        return FAILURE_CODE;
    }

    printf("Socket: signal is: %d\n", signal);

    if (CellularSetupInternetConnectionProfile(CONN_INACTIVE_TIMEOUT) < 0)
    {
        printf("Socket: Failed setting internet connection profile\n");
        return FAILURE_CODE;
    }

    if (!hostname_to_ip(g_host, ipv4))
    {
        return FAILURE_CODE;
    }

    if (CellularSetupInternetServiceProfile(ipv4, g_port, CONN_KEEPINTVL) < 0)
    {
        printf("Socket: Failed setting internet service profile\n");
        return FAILURE_CODE;
    }

    if (CellularConnect() < 0)
    {
        return FAILURE_CODE;
    }

    return SUCCESS_CODE;
}

int SocketWrite(unsigned char *payload, unsigned int len)
{
    return CellularWrite(payload, len);
}

int SocketRead(unsigned char *buf, unsigned int max_len, unsigned int timeout_ms)
{
    return CellularRead(buf, max_len, timeout_ms);
}

int SocketClose(void)
{
    return CellularClose();
}

void SocketDeInit(void)
{
    CellularDisable();
}

int get_num_ops()
{
    return ops_found;
}

OPERATOR_INFO* get_ops()
{
    return ops;
}

char* get_imei()
{
    return imei;
}