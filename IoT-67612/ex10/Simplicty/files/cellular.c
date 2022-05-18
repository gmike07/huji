#include "cellular.h"
#include "serial_io.h"
#include "cellular_common.h"
#include "cellular_parse_physical.h"
#include "cellular_parse_operators.h"
#include "cellular_internet.h"
#include "global.h"
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>
#include "utils.h"
#include "my_printf_lib.h"


#ifdef TEST_COPS
#include "test_cellular.h"
#endif

#define AT_TEST_ATTEMPTS 20
#define AT_TEST_SLEEP_SEC 10

#define REG_ATTEMPTS 20
#define REG_SLEEP_SEC 10

#define SET_OPT_BUF 40

#define SET_INTERNET_CONN_PROF_BUF 100
#define SET_INTERNET_SERV_PROF_BUF 100

static char cmd_AT[] = "AT\r\n";
static char cmd_check_reg[] = "AT+CREG?\r\n";
static char cmd_check_ops[] = "AT+COPS=?\r\n";
static char cmd_check_iccid[] = "AT+CCID\r\n";
static char cmd_check_imei[] = "AT+GSN\r\n";
static char cmd_set_opt_auto_or_dereg[] = "AT+COPS=%d\r\n";
static char cmd_set_opt_manual[] = "AT+COPS=%d,2,\"%d\"\r\n";
static char cmd_check_signal_quality[] = "AT+CSQ\r\n";

static char creg_response_prefix[] = "+CREG: ";

static char scfg_tcpWithUrc[] = "\"Tcp/WithURCs\"";

static char set_internet_conn = FALSE;
static char connected = FALSE;

int parseRegistrationStatus(unsigned char *buf, int *status);

/*
 * Returns the status of the AT+CREG? response
 * For example, if +CREG: 0,5 is returned, then status will be 5
 * Assumes that "OK" is contained in buf
 */
int parseRegistrationStatus(unsigned char *buf, int *status)
{
    char *ret;

    ret = strstr(buf, creg_response_prefix);

    if (ret == NULL)
    {
        return FAILURE_CODE;
    }

    // take the digit after "0,"
    ret = ret + strlen(creg_response_prefix) + 2;

    if (isdigit(*ret))
    {
        *status = (int)((*ret) - '0');
        return SUCCESS_CODE;
    }

    return FAILURE_CODE;
}

/////// Public Functions ///////

/*
 * Initialize whatever is needed to start working with the cellular modem (e.g. the serial port).
 * Returns 0 on success, and -1 on failure
 */
int CellularInit(char *port)
{
    CleanResvBuf();
    SerialFlushInputBuff();

    DefineRequiredEchoMode(ECHO_MODE_OFF);

    return SerialInit(port, BAUD_RATE);
}

/*
 * Deallocate / close whatever resources CellularInit() allocated
 */
void CellularDisable()
{
    SerialDisable();
}

/*
 * Checks if the modem is responding to AT commands
 * Return 0 if it does, returns -1 otherwise
 */
int CellularCheckModem(void)
{
    int n;

    CleanResvBuf();

    my_printf("Cellular: Sending AT\n");
    n = SendCmdRecvResp(cmd_AT, serial_buf, SHORT_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf))
    {
        my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    my_printf("Cellular: AT test passed\n");

    VerifyEchoMode();
    return SUCCESS_CODE;
}

/*
 * Checks if the modem is responding to AT commands
 * Return 0 if it does, returns -1 otherwise
 * Tries multiple times until succeeds or fails
 */
int CellularWaitUntilModemResponds(void)
{
    int i;

    for (i = 0; i < AT_TEST_ATTEMPTS; i++)
    {
        my_printf("Cellular: Checking if modem responds\n");

        if (CellularCheckModem() < 0)
        {
            my_printf("Cellular: Modem didn't respond\n");

            // wait until some/any response is received
            sleep(AT_TEST_SLEEP_SEC);
            continue;
        }

        my_printf("Cellular: Modems has responded\n");

        VerifyEchoMode();
        return SUCCESS_CODE;
    }

    my_printf("Cellular: Modem didn't respond for too long - failing\n");
    return FAILURE_CODE;
}

/*
 * Returns -1 if the modem did not respond or respond with an error.
 * Returns 0 if the command was successful and the registration status was obtained from
 * the modem. In that case, the status parameter will be populated with the numeric value
 * of the <regStatus> field of the “+CREG” AT command
 */
int CellularGetRegistrationStatus(int *status)
{
    int n;

    CleanResvBuf();

    VerifyEchoMode();

    my_printf("Cellular: Checking registration status\n");
    n = SendCmdRecvResp(cmd_check_reg, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf))
    {
        my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    my_printf("Cellular: Received registration status: %s\n", serial_buf);

    return parseRegistrationStatus(serial_buf, status);
}

/*
 * Returns -1 if the modem did not respond or respond with an error or couldn't register.
 * Returns 0 if the command was successful and the registration status was obtained from
 * the modem and the modem is registered (1 or 5).
 */
int CellularWaitUntilRegistered()
{
    int i, status;

    VerifyEchoMode();

    for (i = 0; i < REG_ATTEMPTS; i++) {

        my_printf("Cellular: Checking if modem registered\n");
        if (CellularGetRegistrationStatus(&status) < 0)
        {
            my_printf("Cellular: Registration error\n");
            return FAILURE_CODE;
        }

        if (status == MODEM_REG_HOME || status == MODEM_REG_ROAM)
        {
            my_printf("Cellular: Modem registered\n");
            return SUCCESS_CODE;
        }

        if (status == MODEM_REG_NOT_SEARCHING)
        {
            my_printf("Cellular: Modem is not searching for network\n");
            return FAILURE_CODE;
        }

        sleep(REG_SLEEP_SEC);
    }

    return FAILURE_CODE;
}

/*
 * Forces the modem to search for available operators (see “+COPS=?” command). Returns -1
 * if an error occurred or no operators found. Returns 0 and populates opList and opsFound if
 * the command succeeded.
 * opList is a pointer to the first item of an array of type OPERATOR_INFO, which is allocated
 * by the caller of this function. The array contains a total of maxops items. numOpsFound is
 * allocated by the caller and set by the function. numOpsFound will contain the number of
 * operators found and populated into the opList
 */
int CellularGetOperators(OPERATOR_INFO *opList, int maxops, int *numOpsFound)
{
    int n;

    CleanResvBuf();

    VerifyEchoMode();

    my_printf("Cellular: Checking available operators\n");
#if TEST_COPS == 1
    n = SendCmdRecvResp_TestCops_1(cmd_check_ops, serial_buf, LARGE_RESPONSE_BUF_SIZE, LONG_TIMEOUT);
#elif TEST_COPS == 2
    n = SendCmdRecvResp_TestCops_2(cmd_check_ops, serial_buf, LARGE_RESPONSE_BUF_SIZE, LONG_TIMEOUT);
#elif TEST_COPS == 3
    n = SendCmdRecvResp_TestCops_3(cmd_check_ops, serial_buf, LARGE_RESPONSE_BUF_SIZE, LONG_TIMEOUT);
#else
    n = SendCmdRecvResp(cmd_check_ops, serial_buf, LARGE_RESPONSE_BUF_SIZE, LONG_TIMEOUT);
#endif

    if (n <= 0 || !HasOK(serial_buf))
    {
        my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    my_printf("Cellular: Received the following operators: %s\n", serial_buf);

    return ParseOperators(serial_buf, opList, maxops, numOpsFound);
}

/*
 * Returns -1 if the modem did not respond or respond with an error.
 * Returns 0 if the command was successful and the ICCID was obtained from the modem.
 * iccid is a pointer to a char buffer, which is allocated by the caller of this function.
 * The buffer size is maxlen chars.
 * The obtained ICCID will be placed into the iccid buffer as a null-terminated string
 */
int CellularGetICCID(char* iccid, int maxlen)
{
    int n;

    CleanResvBuf();

    VerifyEchoMode();

    my_printf("Cellular: Checking ICCID\n");
    n = SendCmdRecvResp(cmd_check_iccid, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf))
    {
        my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    my_printf("Cellular: Received ICCID: %s\n", serial_buf);

    return ParseICCID(serial_buf, iccid, maxlen);
}

/*
 * Returns -1 if the modem did not respond or respond with an error.
 * Returns 0 if the command was successful and the IMEI was obtained from the modem.
 * imei is a pointer to a char buffer, which is allocated by the caller of this function.
 * The buffer size is maxlen chars.
 * The obtained IMEI will be placed into the imei buffer as a null-terminated string
 */
int CellularGetIMEI(char* imei, int maxlen)
{
    int n;

    CleanResvBuf();

    VerifyEchoMode();

    my_printf("Cellular: Checking IMEI\n");
    n = SendCmdRecvResp(cmd_check_imei, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf))
    {
        my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    my_printf("Cellular: Received IMEI: %s\n", serial_buf);

    return ParseIMEI(serial_buf, imei, maxlen);
}

/*
 * Forces the modem to register/deregister with a network. Returns 0 if the
 * command was successful, returns -1 otherwise.
 * If mode=0, sets the modem to automatically register with an operator (ignores the
 * operatorCode parameter).
 * If mode=1, forces the modem to work with a specific operator, given in operatorCode.
 * If mode=2, deregisters from the network (ignores the operatorCode parameter).
 * See the “+COPS=<mode>,…” command for more details
 */
int CellularSetOperator(int mode, int operatorCode)
{
    int n;
    static char cmd[SET_OPT_BUF];

    memset(cmd, 0, SET_OPT_BUF);

    CleanResvBuf();

    VerifyEchoMode();

    my_printf("Cellular: Setting registration mode to %d\n", mode);
    if (mode == SET_OPT_MODE_AUTO || mode == SET_OPT_MODE_DEREG)
    {
        if (sprintf(cmd, cmd_set_opt_auto_or_dereg, mode) < 0)
        {
            return FAILURE_CODE;
        }
    }
    else if (mode == SET_OPT_MODE_MANUAL)
    {
        if (sprintf(cmd, cmd_set_opt_manual, mode, operatorCode) < 0)
        {
            return FAILURE_CODE;
        }
    }
    else
    {
        return FAILURE_CODE;
    }

    n = SendCmdRecvResp(cmd, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, LONG_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf))
    {
        my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    return SUCCESS_CODE;
}

/*
 * Returns -1 if the modem did not respond or respond with an error (note, CSQ=99 is also an error!)
 * Returns 0 if the command was successful and the signal quality was obtained from
 * the modem. In that case, the csq parameter will be populated with the numeric
 * value between -113dBm and -51dBm
 */
int CellularGetSignalQuality(int *csq)
{
    int n;

    CleanResvBuf();

    VerifyEchoMode();

    my_printf("Cellular: Checking signal quality\n");
    n = SendCmdRecvResp(cmd_check_signal_quality, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf))
    {
        my_printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    my_printf("Cellular: Received csq: %s\n", serial_buf);

    return ParseSignalQuality(serial_buf, csq);
}

/*
 * Initialize an internet connection profile (AT^SICS)
 * with inactTO=inact_time_sec and
 * conType=GPRS0 and apn="postm2m.lu". Return 0 on success, and -1 on failure.
 */
int CellularSetupInternetConnectionProfile(int inact_time_sec)
{
    static char cmd[SET_INTERNET_CONN_PROF_BUF];

    memset(cmd, 0, SET_INTERNET_CONN_PROF_BUF);

    CleanResvBuf();

    VerifyEchoMode();

    if (SetupInternetConnectionProfileConnType(cmd) < 0)
    {
        return FAILURE_CODE;
    }

    memset(cmd, 0, SET_INTERNET_CONN_PROF_BUF);

    if (SetupInternetConnectionProfileApn(cmd) < 0)
    {
        return FAILURE_CODE;
    }

    memset(cmd, 0, SET_INTERNET_CONN_PROF_BUF);

    if (SetupInternetConnectionProfileInactTimeout(cmd, inact_time_sec) < 0)
    {
        return FAILURE_CODE;
    }

    set_internet_conn = TRUE;

    my_printf("Cellular: Completed setting internet connection profile\n");
    return SUCCESS_CODE;
}

/*
 * Initialize an internal service profile (AT^SISS)
 * with SrvType=Socket
 * and conId=<CellularSetupInternetConnectionProfile_id>
 * (if CellularSetupInternetConnectionProfile is already initialized. Return error, -1, otherwise)
 * and Address=socktcp://IP:port;etx;time=keepintvl_sec.
 * Return 0 on success, and -1 on failure.
 */
int CellularSetupInternetServiceProfile(char *IP, int port, int keepintvl_sec)
{
    static char cmd[SET_INTERNET_SERV_PROF_BUF];

    my_printf_clear();
    if (!set_internet_conn)
    {
        my_printf("Cellular: CellularSetupInternetConnectionProfile hasn't been called yet\n");
        return FAILURE_CODE;
    }

    memset(cmd, 0, SET_INTERNET_SERV_PROF_BUF);

    CleanResvBuf();

    VerifyEchoMode();
    if (SetupInternetServiceProfileSrvType(cmd) < 0)
    {
        return FAILURE_CODE;
    }

    memset(cmd, 0, SET_INTERNET_SERV_PROF_BUF);
    if (SetupInternetServiceProfileConId(cmd) < 0)
    {
        return FAILURE_CODE;
    }

    memset(cmd, 0, SET_INTERNET_SERV_PROF_BUF);

    if (SetupInternetServiceProfileAddr(cmd, IP, port, keepintvl_sec) < 0)
    {
        return FAILURE_CODE;
    }

    my_printf("Cellular: Completed setting internet service profile\n");

    return SUCCESS_CODE;
}

/*
 * Connects to the socket (establishes TCP connection to the pre-defined host and port).
 * Returns 0 on success, -1 on failure.
 */
int CellularConnect()
{
    CleanResvBuf();

    VerifyEchoMode();

    my_printf("Cellular: Setting configuration: tcpWithUrc to off\n");
    if (SetSettingsConfiguration(scfg_tcpWithUrc, "\"off\"") < 0)
    {
        my_printf("Cellular: Failed turning off URCs\n");
        return FAILURE_CODE;
    }

    if (OpenInternetConnection() < 0)
    {
        my_printf("Cellular: Failed opening connection\n");
        CellularClose();
        return FAILURE_CODE;
    }

    if (WaitUntilServiceProfileIsUp() < 0)
    {
        my_printf("Cellular: Failed opening connection\n");
        CellularClose();
        return FAILURE_CODE;
    }

    if (OpenTransparentSocket() < 0)
    {
        my_printf("Cellular: Failed opening connection\n");
        CellularClose();
        return FAILURE_CODE;
    }

    connected = TRUE;

    return SUCCESS_CODE;
}

/*
 * Closes the established connection.
 * Returns 0 on success, -1 on failure.
 */
int CellularClose()
{
    CleanResvBuf();

    VerifyEchoMode();

    if (connected)
    {
        ExitTransparentSocket();
    }

    if (CloseInternetConnection() < 0)
    {
        return FAILURE_CODE;
    }

    connected = FALSE;

    SerialFlushInputBuff();

    return SUCCESS_CODE;
}

/*
 * Writes len bytes from payload buffer to the established connection
 * Returns the number of bytes written on success, -1 on failure
 */
int CellularWrite(unsigned char *payload, unsigned int len)
{
    if (!connected)
    {
        return FAILURE_CODE;
    }

    return SerialSend(payload, len);
}

/*
 * Reads up to max_len bytes from the established connection
 * to the provided buf buffer, for up to timeout_ms
 * (doesn’t block longer than that, even
 * if not all max_len bytes were received).
 * Returns the number of bytes read on success, -1 on failure.
 */
int CellularRead(unsigned char *buf, unsigned int max_len, unsigned int timeout_ms)
{
    if (!connected)
    {
        return FAILURE_CODE;
    }

    return SerialRecv(buf, max_len, timeout_ms);
}
