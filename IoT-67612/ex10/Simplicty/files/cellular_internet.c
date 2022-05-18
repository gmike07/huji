#include "cellular_internet.h"
#include "global.h"
#include "cellular_common.h"
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include "utils.h"
#include "my_printf_lib.h"

#define SET_INTERNET_CONN_PROF_TIMEOUT_BUF 10
#define SET_INTERNET_SERV_PROF_ADDR_BUF 60

#define INT_SERV_UP_ATTEMPTS 20
#define INT_SERV_UP_ATTEMPT_SEC 2


static char cmd_set_internet_conn_profile[] = "AT^SICS=0,%s,%s\r\n";
static char cmd_set_internet_serv_profile[] = "AT^SISS=1,%s,%s\r\n";

static char conn_profile_conn_type_cmd[] = "conType";
static char conn_profile_conn_type[] = "\"GPRS0\"";
static char conn_profile_apn_cmd[] = "apn";
static char conn_profile_apn[] = "\"postm2m.lu\"";
static char conn_profile_inactto_cmd[] = "inactTO";
static char conn_profile_inactto_format[] = "\"%d\"";

static char serv_profile_srv_type_cmd[] = "SrvType";
static char serv_profile_srv_type[] = "\"Socket\"";
static char serv_profile_srv_con_id_cmd[] = "conId";
static char serv_profile_srv_con_id[] = "\"0\"";
static char serv_profile_srv_addr_cmd[] = "address";
static char serv_profile_srv_addr_format[] = "\"socktcp://%s:%d;etx;timer=%d\"";

static char cmd_open_internet_connection[] = "AT^SISO=1\r\n";
static char cmd_close_internet_connection[] = "AT^SISC=1\r\n";

static char cmd_check_internet_service[] = "AT^SISI?\r\n";
static char cmd_open_transparent_socket[] = "AT^SIST=1\r\n";

static char cmd_exit_transparent_socket[] = "+++";

static char sisi_response_prefix[] = "^SISI: ";
static char sisi_inner_delimiter[] = ",";

static char connect_resp[] = "CONNECT";

typedef enum __internet_service_state {
    Allocated = 2,
    Connecting = 3,
    Up_Listening = 4,
    Closing = 5,
    Down = 6,
    Alerting = 7,
    Connected = 8,
    Released = 9
} internetServiceState;

int internetServiceStateValid(int state);
int parseInternetServiceState(unsigned char *buf, internetServiceState *srvState);
int hasConnect(unsigned char *buf);

int internetServiceStateValid(int state)
{
    int valid = 0;

    switch(state) {
        case Allocated:
        case Connecting:
        case Up_Listening:
        case Closing:
        case Down:
        case Alerting:
        case Connected:
        case Released:
            valid = 1;
    }

    return valid;
}

int parseInternetServiceState(unsigned char *buf, internetServiceState *srvState)
{
    char *ret, *delimiter;

    ret = strstr(buf, sisi_response_prefix);

    if (ret == NULL)
    {
        return FAILURE_CODE;
    }

    ret += strlen(sisi_response_prefix);

    // check the first digit until the "," it's the profile
    delimiter = strstr(ret, sisi_inner_delimiter);

    if (delimiter == NULL)
    {
        return FAILURE_CODE;
    }

    // we expect a single digit (0-9) for the profile number
    if (delimiter - ret != 1)
    {
        return FAILURE_CODE;
    }

    if (!isdigit(*ret))
    {
        return FAILURE_CODE;
    }

    if (*ret != '1')
    {
        return FAILURE_CODE;
    }

    ret = delimiter + strlen(sisi_inner_delimiter);

    // check the number after the first delimiter, it's the srvState
    if (!isdigit(*ret))
    {
        return FAILURE_CODE;
    }

    if(!internetServiceStateValid((int)(*ret - '0')))
    {
        return FAILURE_CODE;
    }

    *srvState = (int)((*ret) - '0');

    return SUCCESS_CODE;
}

int hasConnect(unsigned char *buf)
{
    if (strstr(buf, connect_resp) == NULL)
    {
        return FALSE;
    }

    return TRUE;
}

/////// Public Functions ///////

int SetupInternetConnectionProfileConnType(char *cmd_buf)
{
    int n;

    CleanResvBuf();

    my_printf("Cellular: Setting conType\n");
    if (sprintf(cmd_buf, cmd_set_internet_conn_profile, conn_profile_conn_type_cmd, conn_profile_conn_type) < 0)
    {
        my_printf("Cellular: Failed assembling internet connection profile\n");
        return FAILURE_CODE;
    }

    n = SendCmdRecvResp(cmd_buf, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf))
    {
        my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    return SUCCESS_CODE;
}

int SetupInternetConnectionProfileApn(char *cmd_buf)
{
    int n;

    CleanResvBuf();

    my_printf("Cellular: Setting apn\n");
    if (sprintf(cmd_buf, cmd_set_internet_conn_profile, conn_profile_apn_cmd, conn_profile_apn) < 0)
    {
        my_printf("Cellular: Failed assembling internet connection profile\n");
        return FAILURE_CODE;
    }

    n = SendCmdRecvResp(cmd_buf, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf))
    {
        my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    return SUCCESS_CODE;
}

int SetupInternetConnectionProfileInactTimeout(char *cmd_buf, int inact_time_sec)
{
    int n;
    static char inact_time_sec_str[SET_INTERNET_CONN_PROF_TIMEOUT_BUF];

    memset(inact_time_sec_str, 0, SET_INTERNET_CONN_PROF_TIMEOUT_BUF);

    CleanResvBuf();

    printf("Cellular: Setting inactive timeout\n");
    if (sprintf(inact_time_sec_str, conn_profile_inactto_format, inact_time_sec) < 0)
    {
        my_printf("Cellular: Failed assembling internet connection profile\n");
        return FAILURE_CODE;
    }

    if (sprintf(cmd_buf, cmd_set_internet_conn_profile, conn_profile_inactto_cmd, inact_time_sec_str) < 0)
    {
        my_printf("Cellular: Failed assembling internet connection profile\n");
        return FAILURE_CODE;
    }

    n = SendCmdRecvResp(cmd_buf, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf))
    {
        my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    return SUCCESS_CODE;
}

int SetupInternetServiceProfileSrvType(char *cmd_buf)
{
    int n;

    CleanResvBuf();

    my_printf("Cellular: Setting SrvType\n");
    if (sprintf(cmd_buf, cmd_set_internet_serv_profile, serv_profile_srv_type_cmd, serv_profile_srv_type) < 0)
    {
        my_printf("Cellular: Failed assembling internet service profile\n");
        return FAILURE_CODE;
    }

    n = SendCmdRecvResp(cmd_buf, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf))
    {
        my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    return SUCCESS_CODE;
}

int SetupInternetServiceProfileConId(char *cmd_buf)
{
    int n;

    CleanResvBuf();

    my_printf("Cellular: Setting conId\n");
    if (sprintf(cmd_buf, cmd_set_internet_serv_profile, serv_profile_srv_con_id_cmd, serv_profile_srv_con_id) < 0)
    {
        my_printf("Cellular: Failed assembling internet service profile\n");
        return FAILURE_CODE;
    }

    n = SendCmdRecvResp(cmd_buf, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf))
    {
        my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    return SUCCESS_CODE;
}

int SetupInternetServiceProfileAddr(char *cmd_buf, char *IP, int port, int keepintvl_sec)
{
    int n;
    static char addr_cmd[SET_INTERNET_SERV_PROF_ADDR_BUF];

    memset(addr_cmd, 0, SET_INTERNET_SERV_PROF_ADDR_BUF);

    CleanResvBuf();

    my_printf("Cellular: Setting address\n");
    if (sprintf(addr_cmd, serv_profile_srv_addr_format, IP, port, keepintvl_sec) < 0)
    {
        my_printf("Cellular: Failed assembling internet service profile\n");
        return FAILURE_CODE;
    }

    if (sprintf(cmd_buf, cmd_set_internet_serv_profile, serv_profile_srv_addr_cmd, addr_cmd) < 0)
    {
        my_printf("Cellular: Failed assembling internet connection profile\n");
        return FAILURE_CODE;
    }

    n = SendCmdRecvResp(cmd_buf, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || (!HasOK(serial_buf) && strstr(serial_buf, "ERROR") != NULL))
    {
        my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    return SUCCESS_CODE;
}

int OpenInternetConnection()
{
    int n;

    CleanResvBuf();

    my_printf("Cellular: Opening internet connection\n");
    n = SendCmdRecvResp(cmd_open_internet_connection, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf))
    {
        my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    my_printf("Cellular: Opening internet connection result: %s\n", serial_buf);

    return SUCCESS_CODE;
}

int CloseInternetConnection()
{
    int n;

    CleanResvBuf();

    my_printf("Cellular: Closing internet connection\n");
    n = SendCmdRecvResp(cmd_close_internet_connection, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf))
    {
        my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    my_printf("Cellular: Closing internet connection result: %s\n", serial_buf);

    return SUCCESS_CODE;
}

int WaitUntilServiceProfileIsUp()
{
    int n, i;
    internetServiceState state;

    for (i = 0; i < INT_SERV_UP_ATTEMPTS; i++)
    {
        CleanResvBuf();

        n = SendCmdRecvResp(cmd_check_internet_service, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

        my_printf("Cellular: Internet service response: %s\n", serial_buf);

        if (n <= 0 || !HasOK(serial_buf))
        {
            my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
            sleep(INT_SERV_UP_ATTEMPT_SEC);
            continue;
        }

        if (parseInternetServiceState(serial_buf, &state) < 0)
        {
            my_printf("Cellular: Internet service is not up, yet\n");
            sleep(INT_SERV_UP_ATTEMPT_SEC);
            continue;
        }

        if (state == Up_Listening)
        {
            my_printf("Cellular: Internet service is up. State: %d\n", state);
            return SUCCESS_CODE;
        }

        my_printf("Cellular: Internet service is not up, yet. Current state: %d\n", state);

        if (i != INT_SERV_UP_ATTEMPTS - 1)
        {
            sleep(INT_SERV_UP_ATTEMPT_SEC);
        }
    }

    my_printf("Cellular: Internet service is not up. Failed connecting\n");

    return FAILURE_CODE;
}

int OpenTransparentSocket()
{
    int n;

    CleanResvBuf();

    my_printf("Cellular: Opening transparent socket\n");
    n = SendCmdRecvResp(cmd_open_transparent_socket, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !hasConnect(serial_buf))
    {
        printf("Cellular: Not CONNECT response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    my_printf("Cellular: Opening internet connection result: %s\n", serial_buf);

    return SUCCESS_CODE;
}

int ExitTransparentSocket()
{
    int n;

    CleanResvBuf();

    my_printf("Cellular: Exiting transparent socket\n");
    n = SendCmdRecvRespWithWait(cmd_exit_transparent_socket, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, MEDIUM_TIMEOUT);
    if (n <= 0)
    {
        my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }
    if(!HasOK(serial_buf))
    {
        if (HasNoCarrier(serial_buf))
        {
            my_printf("Cellular: NO CARRIER response received\n");
            return SUCCESS_CODE;
        }
        my_printf("Cellular: Not valid response received. Expected: OK or NO CARRIER. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    my_printf("Cellular: Exiting internet connection result: %s\n", serial_buf);

    return SUCCESS_CODE;
}
