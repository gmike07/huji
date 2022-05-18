#include "serial_io.h"
#include "cellular.h"
#include "global.h"

#include <stdio.h>
#include <string.h>

#define DEFAULT_BAUD 115200

#define AT_BUF_SIZE 64
#define AT_DELAY 7000

#define CREG_BUF_SIZE 64
#define CREG_DELAY 10000

#define COPS_SET_BUF_SIZE 64
#define COPS_SET_DELAY 10000

#define CSQ_BUF_SIZE 64
#define CSQ_DELAY 10000

#define CCID_BUF_SIZE 64
#define CCID_DELAY 10000


#define GSN_BUF_SIZE 64
#define GSN_DELAY 10000

#define SMONI_BUF_SIZE 4096
#define SMONI_DELAY 10000


#define COPS_GET_BUF_SIZE 4096
#define COPS_GET_DELAY 120000

#define MAX_TRIAL_NUM 4

/*
 * Initialize whatever is needed to start working with the cellular modem (e.g. the serial port).
 * Returns 0 on success, and -1 on failure
 */
int CellularInit(char *port) {
    return SerialInit(port, DEFAULT_BAUD);
}

/*
 * Deallocate / close whatever resources CellularInit() allocated
 */
void CellularDisable(void) {
    SerialDisable();
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
 * This extract the string between 2 given inputs.
 */
int findSubstring(const char *string, const char *substring_begin, const char *substring_end, char **substr,
                  unsigned int *len) {
    char *start_pointer = strstr(string, substring_begin);
    if (start_pointer == NULL) {
        return FAILURE_CODE;
    }
    start_pointer += strlen(substring_begin);
    char *end_pointer = strstr(start_pointer, substring_end);
    if (end_pointer == NULL) {
        return FAILURE_CODE;
    }
    *len = (end_pointer - start_pointer + 1);
    *substr = start_pointer;
    return SUCCESS_CODE;
}

/*
 * Check if the given string contain OK
 */
int checkOKString(const char *s) {
    if (strstr(s, "OK\r\n") == NULL) {
        return FAILURE_CODE;
    }
    return SUCCESS_CODE;
}

/*
 * Checks if the modem is responding to AT commands
 * Return 0 if it does, returns -1 otherwise
 */
int CellularCheckModem(void) {
    char recv_buf[AT_BUF_SIZE];
    if (SendAndReceive("AT\r\n", recv_buf, AT_BUF_SIZE, AT_DELAY) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    return checkOKString(recv_buf);
}

/*
 * Checks if the modem is responding to AT commands
 * Return 0 if it does, returns -1 otherwise
 * Tries multiple times until succeeds or fails
 */
int CellularWaitUntilModemResponds(void) {
    for (int i = 0; i < MAX_TRIAL_NUM; i++) {
        if (CellularCheckModem() == SUCCESS_CODE) {
            return SUCCESS_CODE;
        }
    }
    return FAILURE_CODE;
}


/*
 * Returns -1 if the modem did not respond or respond with an error.
 * Returns 0 if the command was successful and the registration status was obtained from
 * the modem. In that case, the status parameter will be populated with the numeric value
 * of the <regStatus> field of the “+CREG” AT command
 */
int CellularGetRegistrationStatus(int *status) {
    char buf[CREG_BUF_SIZE];
    if (SendAndReceive("AT+CREG?\r\n", buf, CREG_BUF_SIZE, CREG_DELAY) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    // format is +CREG: %d,%d and we need the second number
    int tmp;
    char *pointer = strstr(buf, "+CREG");
    if (pointer == NULL || sscanf(pointer, "+CREG: %d,%d", &tmp, status) != 2) {
        return FAILURE_CODE;
    }
    return SUCCESS_CODE;
}

/*
 * Returns -1 if the modem did not respond or respond with an error or couldn't register.
 * Returns 0 if the command was successful and the registration status was obtained from
 * the modem and the modem is registered (1 or 5).
 */
int CellularWaitUntilRegistered(void) {
    int status;
    for (int i = 0; i < MAX_TRIAL_NUM; i++) {
        if (CellularGetRegistrationStatus(&status) == SUCCESS_CODE) {
            if (status == 1 || status == 5) {
                return SUCCESS_CODE;
            }
        }
    }
    return FAILURE_CODE;
}

unsigned int min(unsigned int a, unsigned int b) {
    if (a <= b) {
        return a;
    }
    return b;
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

    //check that there is an operator that we can connect to
    *numOpsFound = 0;
    char recv_buf[SMONI_BUF_SIZE];
    if (SendAndReceive("AT^SMONI\r\n", recv_buf, SMONI_BUF_SIZE, SMONI_DELAY) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    if (strstr(recv_buf, "SEARCH") != NULL) {
        printf("couldn't find an operator to connect to\n");
        return FAILURE_CODE;
    }

    //if there is an operator
    char buf[COPS_GET_BUF_SIZE];
    if (SendAndReceive("AT+COPS=?\r\n", buf, COPS_GET_BUF_SIZE, COPS_GET_DELAY) == FAILURE_CODE) {
        return FAILURE_CODE;
    }

    char *pointer = strstr(buf, "+COPS: ");
    if (pointer == NULL) {
        printf("failed to find start of cops message\n");
        return FAILURE_CODE;
    }
    int tech_id = -1;
    *numOpsFound = 0;

    char temp[MAX_OPERATOR_NAME];
    char operator_name[MAX_OPERATOR_NAME];

    pointer = strstr(pointer, "(");
    for (int i = 0; i < maxops && pointer != NULL; i++) {
        if (sscanf(pointer, "(%d,%[^,],%[^,],\"%d\",%d)", &(opList[i].operator_status),
                   operator_name, temp, &(opList[i].operator_code), &tech_id) != 5) {
            pointer = strstr(pointer + 1, "(");
            continue;
        }

        // Remove the "" frome the name.
        unsigned int len = min(MAX_OPERATOR_NAME, strlen(operator_name + 1));
        strncpy(opList[i].operator_name, operator_name + 1, len - 1);
        opList[i].operator_name[len - 1] = '\0';

        // Set the "access_technology" according to the given tech_id.
        if (tech_id == 0) // GSM
        {
            strcpy(opList[i].access_technology, "2G");
        } else if (tech_id == 2) // UTRAN
        {
            strcpy(opList[i].access_technology, "3G");
        } else {
            pointer = strstr(pointer + 1, "(");
            continue;
        }
        *numOpsFound += 1;
        pointer = strstr(pointer + 1, "(");
    }

    if (*numOpsFound != 0) {
        return SUCCESS_CODE;
    }
    return FAILURE_CODE;
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
    if (mode == SET_OPT_MODE_AUTO || mode == SET_OPT_MODE_DEREG) {
        char send_buf[COPS_SET_BUF_SIZE], recv_buf[COPS_SET_BUF_SIZE];
        memset(recv_buf, 0, COPS_SET_BUF_SIZE);

        sprintf(send_buf, "AT+COPS=%d\r\n", mode);
        if (SendAndReceive(send_buf, recv_buf, COPS_SET_BUF_SIZE, COPS_SET_DELAY) == FAILURE_CODE) {
            return FAILURE_CODE;
        }
        return checkOKString(recv_buf);
    } else if (mode == SET_OPT_MODE_MANUAL) {
        char send_buf[COPS_SET_BUF_SIZE], recv_buf[COPS_SET_BUF_SIZE];
        memset(recv_buf, 0, COPS_SET_BUF_SIZE);
        int format = 2;
        sprintf(send_buf, "AT+COPS=%d,%d,\"%d\"\r\n", mode, format, operatorCode);
        if (SendAndReceive(send_buf, recv_buf, COPS_SET_BUF_SIZE, COPS_SET_DELAY) == FAILURE_CODE) {
            return FAILURE_CODE;
        }
        return checkOKString(recv_buf);
    }
    return FAILURE_CODE;
}

/*
 * Returns -1 if the modem did not respond or respond with an error (note, CSQ=99 is also an error!)
 * Returns 0 if the command was successful and the signal quality was obtained from
 * the modem. In that case, the csq parameter will be populated with the numeric
 * value between -113dBm and -51dBm
 */
int CellularGetSignalQuality(int *csq) {
    char buf[CSQ_BUF_SIZE];
    if (SendAndReceive("AT+CSQ\r\n", buf, CSQ_BUF_SIZE, CSQ_DELAY) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    ///format is +CSQ: $d,%d\r\n and we need the first message
    int rssi = 0;


    char *pointer = strstr(buf, "+CSQ:");
    if (sscanf(pointer, "+CSQ: %d", &rssi) != 1) {
        return FAILURE_CODE;
    }
    if (rssi == 99) {
        return FAILURE_CODE;
    }
    *csq = -113 + 2 * rssi;
    return SUCCESS_CODE;
}

/*
 * Returns -1 if the modem did not respond or respond with an error.
 * Returns 0 if the command was successful and the ICCID was obtained from the modem.
 * iccid is a pointer to a char buffer, which is allocated by the caller of this function.
 * The buffer size is maxlen chars.
 * The obtained ICCID will be placed into the iccid buffer as a null-terminated string
 */
int CellularGetICCID(char *iccid, int maxlen) {
    char recv_buf[CCID_BUF_SIZE];
    if (SendAndReceive("AT+CCID?\r\n", recv_buf, CCID_BUF_SIZE, CCID_DELAY) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    char *pointer;
    unsigned int len;
    ///format is +CCID: %s\r\n and we need %s
    if (findSubstring(recv_buf, "+CCID: ", "\r\n", &pointer, &len) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    len = min(maxlen, len);
    if (len == 0) {
        return FAILURE_CODE;
    }
    memcpy(iccid, pointer, len - 1);
    iccid[len - 1] = '\0';
    return SUCCESS_CODE;
}

/*
 * Returns -1 if the modem did not respond or respond with an error.
 * Returns 0 if the command was successful and the IMEI was obtained from the modem.
 * imei is a pointer to a char buffer, which is allocated by the caller of this function.
 * The buffer size is maxlen chars.
 * The obtained IMEI will be placed into the imei buffer as a null-terminated string
 */
int CellularGetIMEI(char *imei, int maxlen) {

    char recv_buf[GSN_BUF_SIZE];
    if (SendAndReceive("AT+GSN\r\n", recv_buf, GSN_BUF_SIZE, GSN_DELAY) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    char *pointer;
    unsigned int len;
    ///format is \r\n%s\r\n and we want %s
    if (findSubstring(recv_buf, "\r\n", "\r\n", &pointer, &len) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    len = min(maxlen, len);
    if (len == 0) {
        return FAILURE_CODE;
    }
    memcpy(imei, pointer, len - 1);
    imei[len - 1] = '\0';
    return SUCCESS_CODE;
}

/*
 * This function receive a string with $skip_str's and find the n's skip_str.
 */
char* skip_str_n_times(char* string, const char* skip_str, int n)
{
    for(int i = 0; i < n && string != NULL; i++)
    {
        string = strstr(string, skip_str);
        if(string == NULL)
        {
            return NULL;
        }
        string += strlen(skip_str);
    }
    return string;
}

/*
 * Returns -1 if the modem did not respond, respond with an error, respond with SEARCH or NOCONN.
 * Returns 0 if the command was successful and the signal info was obtained from the modem.
 * sigInfo is a pointer to a struct, which is allocated by the caller of this function.
 * The obtained info will be placed into the sigInfo struct
 */
//TODO: check this works for 2G
int CellularGetSignalInfo(SIGNAL_INFO *sigInfo) {
    char recv_buf[SMONI_BUF_SIZE];
    if (SendAndReceive("AT^SMONI\r\n", recv_buf, SMONI_BUF_SIZE, SMONI_DELAY) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    ///format is ^SMONI: %s, to get the signal technology
    char *pointer;
    unsigned int len;
    if (findSubstring(recv_buf, "^SMONI: ", ",", &pointer, &len) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    len = min(MAX_TECH_SIZE, len);
    memcpy(sigInfo->access_technology, pointer, len - 1);
    sigInfo->access_technology[len - 1] = '\0';

    //if search exists then we cant find the db
    if (strstr(recv_buf, "SEARCH") != NULL) {
        return FAILURE_CODE;
    }

    if (strncmp(sigInfo->access_technology, "2G", strlen("2G")) == 0) {
        //if search or noconn exists then we cant find the db
        if (strstr(recv_buf, "NOCONN") != NULL) {
            return FAILURE_CODE;
        }
        pointer = skip_str_n_times(recv_buf, ",",15);
        //in the 16'th place there is the power signal
        if (pointer == NULL || sscanf(pointer, "%d", &(sigInfo->signal_power)) != 1) {
            return FAILURE_CODE;
        }
        return SUCCESS_CODE;
    } else if (strncmp(sigInfo->access_technology, "3G", strlen("3G")) == 0) {
        pointer = skip_str_n_times(recv_buf, ",",3);
        //in the 3,4 place there is the power signal
        if (pointer == NULL || sscanf(pointer, "%d", &(sigInfo->EC_n0)) != 1)
        {
            return FAILURE_CODE;
        }
        pointer = skip_str_n_times(pointer, ",",1);
        if (pointer == NULL || sscanf(pointer, "%d", &(sigInfo->signal_power)) != 1)
        {
            return FAILURE_CODE;
        }
        return SUCCESS_CODE;
    }
    return FAILURE_CODE;
}

