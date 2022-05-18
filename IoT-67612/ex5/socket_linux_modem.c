#include "socket.h"
#include "cellular.h"
#include "global.h"
#include "stdio.h"
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netdb.h>

#define INACT_SEC 60
#define KEEP_INTVL 40
#define MAX_NETWORKS 15

int connect_to_network(OPERATOR_INFO *list, int len) {
    for (int i = 0; i < len; i++) {
        if (list[i].operator_status == CURRENT_OPERATOR) {
            return i;
        }
    }
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
 * Initializes the socket.
 * Host: The destination address
 * as DNS: en8wtnrvtnkt5.x.pipedream.net,
 * or as IPv4: 35.169.0.97.
 * Port: The communication endpoint, int, e.g.: 80.
 * Returns 0 on success, -1 on failure
 */
int SocketInit(char *host, int port) {
    printf("waiting for model to register...\n");
    if (CellularWaitUntilRegistered() == FAILURE_CODE) {
        return FAILURE_CODE;
    }

    if (CellularSetupInternetConnectionProfile(INACT_SEC) == FAILURE_CODE ||
        CellularSetupInternetServiceProfile(host, port, KEEP_INTVL) == FAILURE_CODE) {
        return FAILURE_CODE;
    }
    return SUCCESS_CODE;
}

/*
 * Connects to the socket
 * (establishes TCP connection to the pre-defined host and port).
 * Returns 0 on success, -1 on failure
 */
int SocketConnect(void) {
    return CellularConnect();
}

/*
 * Writes len bytes from the payload buffer
 * to the established connection.
 * Returns the number of bytes written on success, -1 on failure
 */
int SocketWrite(unsigned char *payload, unsigned int len) {
    return CellularWrite(payload, len);
}

/*
 * Reads up to max_len bytes from the established connection
 * to the provided buf buffer,
 * for up to timeout_ms (doesn’t block longer than that,
 * even if not all max_len bytes were received).
 * Returns the number of bytes read on success, -1 on failure
 */
int SocketRead(unsigned char *buf, unsigned int max_len, unsigned int timeout_ms) {
    return CellularRead(buf, max_len, timeout_ms);
}

/*
 * Closes the established connection.
 * Returns 0 on success, -1 on failure
 */
int SocketClose(void) {
    return CellularClose();
}

/*
 * Frees any resources that were allocated by SocketInit
 */
void SocketDeInit(void) {
    CellularDisable();
}