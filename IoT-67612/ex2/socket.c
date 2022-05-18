//
// Created by osboxes on 10/13/21.
//
#include <sys/socket.h>
#include <netinet/in.h>
#include "socket.h"
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <netdb.h>


#define MS_TO_SECOND 1000
#define MS_TO_US 1000

static int sockId = -1;
static struct sockaddr_in server_adder;


/*
 * Initializes the socket.
 * Host: The destination address
 * as DNS: en8wtnrvtnkt5.x.pipedream.net,
 * or as IPv4: 35.169.0.97.
 * Port: The communication endpoint, int, e.g.: 80.
 * Returns 0 on success, -1 on failure
 */
int SocketInit(char *host, int port) {
    //AF_INET = internet ipv4, sock_stream = tcp
    print_debugger("*** initializing socket...\n");
    sockId = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    if (sockId < 0) {
        print_debugger("ERROR: socket couldn't be created...:(\n");
        return FAILURE;
    }

    struct hostent *host_info = gethostbyname(host);
    if (host_info == NULL) {
        print_debugger("ERROR: failed to resolve ip...\n");
        return FAILURE;
    }

    struct in_addr *address = (struct in_addr *) (host_info->h_addr);

    server_adder.sin_family = AF_INET;
    server_adder.sin_addr.s_addr = inet_addr(inet_ntoa(*address));
    server_adder.sin_port = htons(port);

    return SUCCESS;
}

/*
 * Connects to the socket
 * (establishes TCP connection to the pre-defined host and port).
 * Returns 0 on success, -1 on failure
 */
int SocketConnect(void) {
    if (connect(sockId, (struct sockaddr *) &server_adder, sizeof(server_adder)) < 0) {
        print_debugger("ERROR: couldn't connect to socket...:(\n");
        return FAILURE;
    }

    return SUCCESS;
}

/*
 * Writes len bytes from the payload buffer
 * to the established connection.
 * Returns the number of bytes written on success, -1 on failure
 */
int SocketWrite(unsigned char *payload, unsigned int len) {
    print_debugger("*** writing to socket, msg: \n");
    print_debugger((char *) payload);
    print_debugger("\n");
    return send(sockId, payload, len, 0);
}

/*
 * Reads up to max_len bytes from the established connection
 * to the provided buf buffer,
 * for up to timeout_ms (doesn’t block longer than that,
 * even if not all max_len bytes were received).
 * Returns the number of bytes read on success, -1 on failure
 */
int SocketRead(unsigned char *buf, unsigned int max_len, unsigned int timeout_ms) {
    print_debugger("*** reading socket...\n");

    // the time to wait before giving up the message
    struct timeval tv;
    tv.tv_sec = timeout_ms / MS_TO_SECOND;
    tv.tv_usec = (timeout_ms % MS_TO_SECOND) * MS_TO_US;
    if (setsockopt(sockId, SOL_SOCKET, SO_RCVTIMEO, (const char *) &tv, sizeof(tv)) < 0) {
        return FAILURE;
    }
    return read(sockId, buf, max_len);
}

/*
 * Closes the established connection.
 * Returns 0 on success, -1 on failure
 */
int SocketClose(void) {
    print_debugger("*** closing socket...\n");
    return close(sockId);
}

/*
 * Frees any resources that were allocated by SocketInit
 */
void SocketDeInit(void) {
    print_debugger("*** de-initializing socket...\n");
    sockId = -1;
}