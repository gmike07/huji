#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <stdlib.h>
#include "cellular.h"
#include "global.h"
#include "serial_io.h"

#define CCID_LEN 64
#define IMEI_LEN 64
#define MAX_NETWORKS 15

#define ATE0_BUF 20
#define ATE0_DELAY 10000

/*
 * This function called when ^c is pressed.
 */
void sig_handler(int signum) {
    printf("trl+C, why did you press it?!!!\n");
    CellularDisable();
    exit(FAILURE_CODE);
}

/*
 * Iterate over all available networks and connect to the first that we can.
 */
int connect_to_network(OPERATOR_INFO *list, int len) {
    for (int i = 0; i < len; i++) {
        CellularSetOperator(SET_OPT_MODE_DEREG, 0);
        if (list[i].operator_status != OPERATOR_AVAILABLE && list[i].operator_status != CURRENT_OPERATOR) {
            continue;
        }
        if (CellularSetOperator(SET_OPT_MODE_MANUAL, list[i].operator_code) == SUCCESS_CODE) {
            return i;
        }
    }
    return FAILURE_CODE;
}

/*
 * This function send the given message and print the result.
 */
int SendAndReceive1(const char *msg, char *recv_buf, unsigned int recv_buf_size,
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
 * This function turn the echo off by sending "ATE0".
 */
int turn_off_echo() {
    printf("turn echo off\n");
    char buf[ATE0_BUF];
    if (SendAndReceive1("ATE0\r\n", buf, ATE0_BUF, ATE0_DELAY) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    if (strstr(buf, "OK") == NULL) {
        return FAILURE_CODE;
    }
    return SUCCESS_CODE;
}

/*
 * The main?
 */
int main() {
    // Handle ^C
    signal(SIGINT, sig_handler); // Register signal handler

    if (CellularInit("/dev/ttyUSB0") == FAILURE_CODE) {
        printf("failed to init\n");
        return FAILURE_CODE;
    }

    printf("waiting for model to respond...\n");
    if (CellularWaitUntilModemResponds() == FAILURE_CODE) {
    }

    if (turn_off_echo() == FAILURE_CODE) {
        return FAILURE_CODE;
    }

    char ccid[CCID_LEN];
    if (CellularGetICCID(ccid, CCID_LEN) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    printf("got ccid: %s\n", ccid);

    char imei[IMEI_LEN];
    if (CellularGetIMEI(imei, IMEI_LEN) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    printf("got imei: %s\n", imei);


    printf("waiting for model to register...\n");
    while (CellularWaitUntilRegistered() == FAILURE_CODE) {
    }

    OPERATOR_INFO list[MAX_NETWORKS];
    int array_length = -1;
    printf("searching for operators...\n");
    if (CellularGetOperators(list, MAX_NETWORKS, &array_length) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    for (int i = 0; i < array_length; i++) {
        printf("status: %d, name: %s, code: %d, tech: %s\n", list[i].operator_status,
               list[i].operator_name, list[i].operator_code, list[i].access_technology);
    }

    int network_id = connect_to_network(list, array_length);
    if (network_id == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    printf("connected to %s\n", list[network_id].operator_name);

    int csq = -1;
    CellularGetSignalQuality(&csq);
    printf("got quality: %d\n", csq);

    // ---------- BONUS ----------
//    SIGNAL_INFO sigInfo;
//    CellularGetSignalInfo(&sigInfo);
//    printf("tech: %s, dbm: %d, ecn0: %d\n", sigInfo.access_technology, sigInfo.signal_power, sigInfo.EC_n0);

    CellularDisable();
    return 0;
}
