#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <stdlib.h>
#include "cellular.h"
#include "global.h"
#include "HTTP_client.h"

# define HTTP_BUFFER_SIZE 500
#define PORT 80
#define ADDRESS "en8wtnrvtnkt5.x.pipedream.net"


/*
 * This function called when ^c is pressed.
 */
void sig_handler(int signum) {
    printf("trl+C, why did you press it?!!!\n");
    CellularDisable();
    exit(FAILURE_CODE);
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

    if (CellularWaitUntilModemResponds() < 0)
    {
        return FAILURE_CODE;
    }

    if (HTTPClientInit(ADDRESS, PORT) == FAILURE_CODE) {
        return FAILURE_CODE;
    }

    char buf[HTTP_BUFFER_SIZE];
    if(HTTPClientSendHTTPGetDemoRequest("/", buf, HTTP_BUFFER_SIZE) == FAILURE_CODE)
    {
        return FAILURE_CODE;
    }
    printf("got response %s\n", buf);
    char *msg = "hello cellular world!";
    if(HTTPClientSendHTTPPostDemoRequest("/", msg, strlen(msg),buf, HTTP_BUFFER_SIZE-1) == FAILURE_CODE)
    {
        return FAILURE_CODE;
    }

    printf("got response %s\n", buf);
    HTTPClientDeInit();
    return SUCCESS_CODE;
}
