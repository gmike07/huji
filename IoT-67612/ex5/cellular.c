#include "serial_io.h"
#include "cellular.h"
#include "global.h"

#include <stdio.h>
#include <string.h>



#include "cellular_common.h"
#include "cellular_parse_physical.h"
#include "cellular_parse_operators.h"
#include <unistd.h>
#include <ctype.h>

#ifdef TEST_COPS
#include "test_cellular.h"
#endif

#define AT_TEST_ATTEMPTS 20
#define AT_TEST_SLEEP_SEC 10

#define REG_ATTEMPTS 10
#define REG_SLEEP_SEC 5

#define SET_OPT_BUF 40

#define MODEM_REG_HOME 1
#define MODEM_REG_ROAM 5
#define MODEM_REG_NOT_SEARCHING 0

#define CON_PROFILE_BUF_SIZE 64
#define CON_PROFILE_DELAY 10000

#define CONNECT_BUF_SIZE 64
#define CONNECT_DELAY 10000

#define CLOSE_BUF_SIZE 64
#define CLOSE_DELAY 10000

#define WRITE_BUF_SIZE 1024
#define WRITE_DELAY 10000

#define READ_BUF_SIZE 2048

#define SERV_PROFILE_BUF_SIZE 256
#define SERV_PROFILE_DELAY 10000

#define SICS_LIST_BUF_SIZE 256
#define SICS_LIST_DELAY 10000

#define SISS_LIST_BUF_SIZE 512
#define SISS_LIST_DELAY 10000

#define SISO_LIST_BUFFER 256
#define SISO_LIST_DELAY 10000

#define MAX_READ_SIZE 1024
#define MAX_WRITE_SIZE 1024


static char cmd_AT[] = "AT\r\n";
static char cmd_check_reg[] = "AT+CREG?\r\n";
static char cmd_check_ops[] = "AT+COPS=?\r\n";
static char cmd_check_iccid[] = "AT+CCID\r\n";
static char cmd_check_imei[] = "AT+GSN\r\n";
static char cmd_set_opt_auto_or_dereg[] = "AT+COPS=%d\r\n";
static char cmd_set_opt_manual[] = "AT+COPS=%d,2,\"%d\"\r\n";
static char cmd_check_signal_quality[] = "AT+CSQ\r\n";

static char creg_response_prefix[] = "+CREG: ";

int parseRegistrationStatus(unsigned char *buf, int *status);

/*
 * Returns the status of the AT+CREG? response
 * For example, if +CREG: 0,5 is returned, then status will be 5
 * Assumes that "OK" is contained in buf
 */
int parseRegistrationStatus(unsigned char *buf, int *status) {
    char *ret;

    ret = strstr(buf, creg_response_prefix);

    if (ret == NULL) {
        return FAILURE_CODE;
    }

    // take the digit after "0,"
    ret = ret + strlen(creg_response_prefix) + 2;

    if (isdigit(*ret)) {
        *status = (int) ((*ret) - '0');
        return SUCCESS_CODE;
    }

    return FAILURE_CODE;
}

/////// Public Functions ///////

/*
 * Initialize whatever is needed to start working with the cellular modem (e.g. the serial port).
 * Returns 0 on success, and -1 on failure
 */
int CellularInit(char *port) {
    CleanResvBuf();

    SerialFlushInputBuff();
    DefineRequiredEchoMode(ECHO_MODE_OFF);

    return SerialInit(port, BAUD_RATE);
}

/*
 * Deallocate / close whatever resources CellularInit() allocated
 */
void CellularDisable() {
    SerialDisable();
}

/*
 * Checks if the modem is responding to AT commands
 * Return 0 if it does, returns -1 otherwise
 */
int CellularCheckModem(void) {
    int n;

    CleanResvBuf();

    printf("Cellular: Sending AT\n");
    n = SendCmdRecvResp(cmd_AT, serial_buf, SHORT_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf)) {
        printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    printf("Cellular: AT test passed\n");

    VerifyEchoMode();
    return SUCCESS_CODE;
}

/*
 * Checks if the modem is responding to AT commands
 * Return 0 if it does, returns -1 otherwise
 * Tries multiple times until succeeds or fails
 */
int CellularWaitUntilModemResponds(void) {
    int i;

    for (i = 0; i < AT_TEST_ATTEMPTS; i++) {
        printf("Cellular: Checking if modem responds\n");

        if (CellularCheckModem() < 0) {
            printf("Cellular: Modem didn't respond\n");

            // wait until some/any response is received
            sleep(AT_TEST_SLEEP_SEC);
            continue;
        }

        printf("Cellular: Modems has responded\n");

        VerifyEchoMode();
        return SUCCESS_CODE;
    }

    printf("Cellular: Modem didn't respond for too long - failing\n");
    return FAILURE_CODE;
}

/*
 * Returns -1 if the modem did not respond or respond with an error.
 * Returns 0 if the command was successful and the registration status was obtained from
 * the modem. In that case, the status parameter will be populated with the numeric value
 * of the <regStatus> field of the “+CREG” AT command
 */
int CellularGetRegistrationStatus(int *status) {
    int n;

    CleanResvBuf();

    VerifyEchoMode();

    printf("Cellular: Checking registration status\n");
    n = SendCmdRecvResp(cmd_check_reg, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf)) {
        printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    printf("Cellular: Received registration status: %s\n", serial_buf);

    return parseRegistrationStatus(serial_buf, status);
}

/*
 * Returns -1 if the modem did not respond or respond with an error or couldn't register.
 * Returns 0 if the command was successful and the registration status was obtained from
 * the modem and the modem is registered (1 or 5).
 */
int CellularWaitUntilRegistered() {
    int i, status;

    VerifyEchoMode();

    for (i = 0; i < REG_ATTEMPTS; i++) {

        printf("Cellular: Checking if modem registered\n");
        if (CellularGetRegistrationStatus(&status) < 0) {
            printf("Cellular: Registration error\n");
            return FAILURE_CODE;
        }

        if (status == MODEM_REG_HOME || status == MODEM_REG_ROAM) {
            printf("Cellular: Modem registered\n");
            return SUCCESS_CODE;
        }

        if (status == MODEM_REG_NOT_SEARCHING) {
            printf("Cellular: Modem is not searching for network\n");
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
int CellularGetOperators(OPERATOR_INFO *opList, int maxops, int *numOpsFound) {
    int n;

    CleanResvBuf();

    VerifyEchoMode();

    printf("Cellular: Checking available operators\n");
#if TEST_COPS == 1
    n = SendCmdRecvResp_TestCops_1(cmd_check_ops, serial_buf, LARGE_RESPONSE_BUF_SIZE, LONG_TIMEOUT);
#elif TEST_COPS == 2
    n = SendCmdRecvResp_TestCops_2(cmd_check_ops, serial_buf, LARGE_RESPONSE_BUF_SIZE, LONG_TIMEOUT);
#elif TEST_COPS == 3
    n = SendCmdRecvResp_TestCops_3(cmd_check_ops, serial_buf, LARGE_RESPONSE_BUF_SIZE, LONG_TIMEOUT);
#else
    n = SendCmdRecvResp(cmd_check_ops, serial_buf, LARGE_RESPONSE_BUF_SIZE, LONG_TIMEOUT);
#endif

    if (n <= 0 || !HasOK(serial_buf)) {
        printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    printf("Cellular: Received the following operators: %s\n", serial_buf);

    return ParseOperators(serial_buf, opList, maxops, numOpsFound);
}

/*
 * Returns -1 if the modem did not respond or respond with an error.
 * Returns 0 if the command was successful and the ICCID was obtained from the modem.
 * iccid is a pointer to a char buffer, which is allocated by the caller of this function.
 * The buffer size is maxlen chars.
 * The obtained ICCID will be placed into the iccid buffer as a null-terminated string
 */
int CellularGetICCID(char *iccid, int maxlen) {
    int n;

    CleanResvBuf();

    VerifyEchoMode();

    printf("Cellular: Checking ICCID\n");
    n = SendCmdRecvResp(cmd_check_iccid, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf)) {
        printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    printf("Cellular: Received ICCID: %s\n", serial_buf);

    return ParseICCID(serial_buf, iccid, maxlen);
}

/*
 * Returns -1 if the modem did not respond or respond with an error.
 * Returns 0 if the command was successful and the IMEI was obtained from the modem.
 * imei is a pointer to a char buffer, which is allocated by the caller of this function.
 * The buffer size is maxlen chars.
 * The obtained IMEI will be placed into the imei buffer as a null-terminated string
 */
int CellularGetIMEI(char *imei, int maxlen) {
    int n;

    CleanResvBuf();

    VerifyEchoMode();

    printf("Cellular: Checking IMEI\n");
    n = SendCmdRecvResp(cmd_check_imei, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf)) {
        printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    printf("Cellular: Received IMEI: %s\n", serial_buf);

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
int CellularSetOperator(int mode, int operatorCode) {
    int n;
    static char cmd[SET_OPT_BUF];

    memset(cmd, 0, SET_OPT_BUF);

    CleanResvBuf();

    VerifyEchoMode();

    printf("Cellular: Setting registration mode to %d\n", mode);
    if (mode == SET_OPT_MODE_AUTO || mode == SET_OPT_MODE_DEREG) {
        if (sprintf(cmd, cmd_set_opt_auto_or_dereg, mode) < 0) {
            return FAILURE_CODE;
        }
    } else if (mode == SET_OPT_MODE_MANUAL) {
        if (sprintf(cmd, cmd_set_opt_manual, mode, operatorCode) < 0) {
            return FAILURE_CODE;
        }
    } else {
        return FAILURE_CODE;
    }

    n = SendCmdRecvResp(cmd, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, MEDIUM_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf)) {
        printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
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
int CellularGetSignalQuality(int *csq) {
    int n;

    CleanResvBuf();

    VerifyEchoMode();

    printf("Cellular: Checking signal quality\n");
    n = SendCmdRecvResp(cmd_check_signal_quality, serial_buf, MEDIUM_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf)) {
        printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    printf("Cellular: Received csq: %s\n", serial_buf);

    return ParseSignalQuality(serial_buf, csq);
}

/*
 * This function send the given message and print the result.
 */
int SendAndReceive(const char *msg, char *recv_buf, unsigned int recv_buf_size,
                   unsigned int timeout_ms) {
    memset(recv_buf, 0, recv_buf_size);
    printf("-----------------------------------\nsending %s\n", msg);
    if (SerialSend(msg, strlen(msg)) == FAILURE_CODE) {
        printf("failed to write\n");
        return FAILURE_CODE;
    }
    if (SerialRecv(recv_buf, recv_buf_size - 1, timeout_ms) == FAILURE_CODE) {
        printf("failed to read\n");
        return FAILURE_CODE;
    }
    printf("got: ");
    recv_buf[recv_buf_size - 1] = '\0';
    printf("%s\n", recv_buf);
    return SUCCESS_CODE;
}


/*
 * Check if the given string contain OK
 */
int checkOKString(const char *s) {
    if (strstr(s, "OK") == NULL) {
        return FAILURE_CODE;
    }
    return SUCCESS_CODE;
}


unsigned int min(unsigned int a, unsigned int b) {
    if (a <= b) {
        return a;
    }
    return b;
}

/*
 * This function send AT command to the modem, and save&print the response in the given buffer.
 * Return SUCCESS_CODE if the response contains "OK", FAILURE_CODE otherwise.
 */
int SendAndReceiveOk(const char *msg, char *recv_buf, unsigned int recv_buf_size, unsigned int timeout_ms) {
    if (SendAndReceive(msg, recv_buf, recv_buf_size, timeout_ms) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    return checkOKString(recv_buf);
}

/*
* Initialize an internet connection profile (AT^SICS)
* with inactTO=inact_time_sec and
* conType=GPRS0 and apn="postm2m.lu". Return 0 on success,
* and -1 on failure.
*/
int CellularSetupInternetConnectionProfile(int inact_time_sec) {
    char recv_buf[CON_PROFILE_BUF_SIZE];
    char intact_msg[CON_PROFILE_BUF_SIZE];
    memset(intact_msg, 0, CON_PROFILE_BUF_SIZE);
    sprintf(intact_msg, "AT^SICS=0,inactTO,\"%d\"\r\n", inact_time_sec);
    char *messages[3] = {"AT^SICS=0,conType,\"GPRS0\"\r\n", "AT^SICS=0,apn,\"postm2m.lu\"\r\n", intact_msg};
    for (int i = 0; i < 3; i++) {
        if (SendAndReceiveOk(messages[i], recv_buf, CON_PROFILE_BUF_SIZE, CON_PROFILE_DELAY) == FAILURE_CODE) {
            return FAILURE_CODE;
        }
    }
    return SUCCESS_CODE;
}

/*
 * This function check if the connection profile is initialize as needed.
 */
int checkInitOfConnectionProfile() {
    char recv_buf[SICS_LIST_BUF_SIZE];
    if (SendAndReceive("AT^SICS?\r\n", recv_buf, SICS_LIST_BUF_SIZE, SICS_LIST_DELAY) == FAILURE_CODE) {
        return FAILURE_CODE;
    }

    if (strstr(recv_buf, "^SICS: 0,\"conType\",\"GPRS0\"") != NULL &&
        strstr(recv_buf, "^SICS: 0,\"inactTO\"") != NULL &&
        strstr(recv_buf, "^SICS: 0,\"apn\",\"postm2m.lu\"") != NULL) {
        return SUCCESS_CODE;
    }
    printf("Error: cannot find the desired connection profile.\n");
    return FAILURE_CODE;
}

/*
 * This function check if the connection profile is initialize as needed.
 */
int checkInitOfServiceProfile() {
    char recv_buf[SISS_LIST_BUF_SIZE];
    if (SendAndReceive("AT^SISS?\r\n", recv_buf, SISS_LIST_BUF_SIZE, SISS_LIST_DELAY) == FAILURE_CODE) {
        return FAILURE_CODE;
    }

    if (strstr(recv_buf, "^SISS: 1,\"srvType\",\"Socket\"") != NULL &&
    strstr(recv_buf, "^SISS: 1,\"conId\",\"0\"") != NULL &&
    strstr(recv_buf, "^SISS: 1,\"address\",\"socktcp://") != NULL) {
        return SUCCESS_CODE;
    }
    printf("Error: cannot find the desired service profile.\n");
    return FAILURE_CODE;
}


/*
* Initialize an internal service profile (AT^SISS)
* with keepintvl=keepintvl_sec (the timer)
* and SrvType=Socket
* and conId=<CellularSetupInternetConnectionProfile_id>
* (if CellularSetupInternetConnectionProfile is already initialized.
* Return error, -1, otherwise)
* and Address=socktcp://IP:port;etx;time=keepintvl_sec.
* Return 0 on success, and -1 on failure.
*/
int CellularSetupInternetServiceProfile(char *IP, int port, int keepintvl_sec) {
    // Check if the connection profile is already set:
    if (checkInitOfConnectionProfile() == FAILURE_CODE) {
        return FAILURE_CODE;
    }

    // Set the service profile:
    char recv_buf[SERV_PROFILE_BUF_SIZE];
    char address_msg[SERV_PROFILE_BUF_SIZE];
    memset(address_msg, 0, SERV_PROFILE_BUF_SIZE);
    sprintf(address_msg, "AT^SISS=1,\"address\",\"socktcp://%s:%d;timer=%d\"\r\n", IP, port, keepintvl_sec);
    char *messages[4] = {"AT^SISS=1,\"srvType\",\"Socket\"\r\n", "AT^SISS=1,\"conId\",\"0\"\r\n", address_msg,
                         "AT^SCFG=\"Tcp/WithURCs\",\"on\"\r\n"};
    for (int i = 0; i < 4; i++) {
        if (SendAndReceiveOk(messages[i], recv_buf, SERV_PROFILE_BUF_SIZE, SERV_PROFILE_DELAY) == FAILURE_CODE) {
            return FAILURE_CODE;
        }
    }
    return checkInitOfServiceProfile();
}

/*
* Connects to the socket (establishes TCP connection to the pre-
defined host and port).
* Returns 0 on success, -1 on failure.
*/
int CellularConnect(void) {
    char recv_buf[CONNECT_BUF_SIZE];
    if (SendAndReceiveOk("AT^SISO=1\r\n", recv_buf, CONNECT_BUF_SIZE, CONNECT_DELAY) == FAILURE_CODE) {
        return FAILURE_CODE;
    }

    char list_buffer[SICS_LIST_BUF_SIZE];
    if (SendAndReceive("AT^SISO=1,1\r\n", list_buffer, SISO_LIST_BUFFER, SISO_LIST_DELAY) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    if (strstr(list_buffer, "^SISO: 1,\"Socket\",4") == NULL) {
        return FAILURE_CODE;
    }
    return SUCCESS_CODE;
}

/*
* Closes the established connection.
* Returns 0 on success, -1 on failure.
*/
int CellularClose() {
    char recv_buf[CLOSE_BUF_SIZE];
    return SendAndReceiveOk("AT^SISC=1\r\n", recv_buf, CLOSE_BUF_SIZE, CLOSE_DELAY);
}

int findLenURC(char *recv_msg, const char *urc) {
    char *pointer = strstr(recv_msg, urc);
    if (pointer == NULL) {
        return FAILURE_CODE;
    }
    pointer += strlen(urc);
    int len = FAILURE_CODE;
    if (sscanf(pointer, "%d", &len) != 1) {
        return FAILURE_CODE;
    }
    printf("%d\n", len);
    return len;

}

/*
* Writes len bytes from payload buffer to the established connection
* Returns the number of bytes written on success, -1 on failure
*/
int CellularWrite(unsigned char *payload, unsigned int len) {
    char send_msg[WRITE_BUF_SIZE], recv_msg[WRITE_BUF_SIZE];
    memset(send_msg, 0, WRITE_BUF_SIZE);
    sprintf(send_msg, "AT^SISW=1,%d,0\r\n", min(len, MAX_WRITE_SIZE));
    printf("sending command %s", send_msg);
    if (SendAndReceive(send_msg, recv_msg, WRITE_BUF_SIZE, WRITE_DELAY) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    int val = SerialSend(payload, len);
    if (SerialRecv(recv_msg, WRITE_BUF_SIZE, WRITE_DELAY) == FAILURE_CODE ||
        checkOKString(recv_msg) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    printf("received: %s\n", recv_msg);
    return val;
}

/*
* Reads up to max_len bytes from the established connection
* to the provided buf buffer, for up to timeout_ms
* (doesn’t block longer than that, even
* if not all max_len bytes were received).
* Returns the number of bytes read on success, -1 on failure.
*/
int CellularRead(unsigned char *buf, unsigned int max_len, unsigned int timeout_ms) {
    char send_msg[READ_BUF_SIZE], read_buf[READ_BUF_SIZE];
    memset(send_msg, 0, READ_BUF_SIZE);
    sprintf(send_msg, "AT^SISR=1,%d\r\n", min(max_len, MAX_READ_SIZE));
    printf("reading command %s", send_msg);
    if (SendAndReceive(send_msg, read_buf, READ_BUF_SIZE, timeout_ms) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    int len = (int) min(findLenURC(read_buf, "^SISR: 1,"), max_len);

    if (len == FAILURE_CODE) {
        return FAILURE_CODE;
    }

    char *pointer = strstr(read_buf, "^SISR: 1,");
    pointer = strstr(pointer, "\r\n");
    if (pointer == NULL) {
        return FAILURE_CODE;
    }
    pointer += strlen("\r\n");
    memcpy(buf, pointer, len);
    return len;
}

