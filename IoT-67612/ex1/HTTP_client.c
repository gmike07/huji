#include "socket.h"
#include "HTTP_client.h"
#include "string.h"

#ifdef DEBUG

#include <stdio.h>

#endif

#define MAX_TIMEOUT_MS 1000
#define MAX_SIZE_RESPONSE_DATA 4096
#define MAX_SIZE_REQUEST_DATA 1024


static char *urlHost = NULL;
static int urlPort = -1;

/*
 * Initializes the client.
 * Host: The destination address
 * as DNS: en8wtnrvtnkt5.x.pipedream.net,
 * or as IPv4: 35.169.0.97.
 * Port: The communication endpoint, int, e.g.: 80.
 * Returns 0 on success, -1 on failure
 */
int HTTPClientInit(char *host, int port) {
    print_debugger("*** initializing HTTPSocket...\n");
    urlPort = port;
    urlHost = host;
    if (SocketInit(host, port) == FAILURE) {
        return FAILURE;
    }
    print_debugger("*** connecting HTTPSocket...\n");
    return SocketConnect();
}

/**
 * Find when the data of the response start.
 * @param httpResponse All response from the server.
 * @param length Length of the response.
 * @return Pointer to the start of the response's data.
 */
char *removeHeaders(char *httpResponse, int length) {
    for (int i = 0; i < length; i++) {
        if (strncmp("\r\n\r\n", httpResponse + i, 4) == 0) {
            return httpResponse + i + 4; //skip the \r\n\r\n
        }
    }
    return NULL;
}

/*
 * Writes a simple HTTP GET request to the given URL (e.g.: “/”),
 * and pre-defined host (appears in HTTP body) and port.
 * Reads up to response_max_len bytes from
 * the received response to the provided response buffer.
 * The response buffer and the provided response_max_len
 * are used only for the payload part
 * (e.g.: {"success":true} – 16 bytes) and not the entire message.
 * i.e. response like HTTP/1.1 200 OK and headers are not included
 * Returns the number of bytes read on success, -1 on failure
 */
int HTTPClientSendHTTPGetDemoRequest(char *url, char *response, int response_max_len) {
    print_debugger("*** starting GET request...\n");
    char requestData[MAX_SIZE_REQUEST_DATA];
    const char *headersDefault = "GET %s HTTP/1.1\r\nHost: %s:%d\r\n\r\n";

    if (sprintf(requestData, headersDefault, url, urlHost, urlPort) < 0) {
        print_debugger("ERROR: OS failed me again (sprintf)...\n");
        return FAILURE;
    }

    SocketWrite(requestData, strlen(requestData));

    char responseData[MAX_SIZE_RESPONSE_DATA];
    int readBytes = SocketRead(responseData, MAX_SIZE_RESPONSE_DATA, MAX_TIMEOUT_MS);

    if (readBytes == FAILURE) {
        return FAILURE;
    }

    // Get only the desire data from thr response.
    char *responsePayload = removeHeaders(responseData, readBytes);

    if (responsePayload == NULL) {
        print_debugger("ERROR: no payload, you lied to me!\n");
        return FAILURE;
    }

    strncpy(response, responsePayload, response_max_len);

    return (int) strlen(responsePayload);
}

/*
 * Writes a simple HTTP POST request to the given URL (e.g.: “/”),
 * and pre-defined host (appears in HTTP body) and port.
 * The POST request sends the provided message_len from the message buffer.
 * Reads up to response_max_len bytes from the
 * received response to the provided response buffer.
 * The response buffer and the provided response_max_len
 * are used only for the payload part
 * (e.g.: {"success":true} – 16 bytes) and not the entire message.
 * i.e. response like HTTP/1.1 200 OK and headers are not included
 * Returns the number of bytes read on success, -1 on failure.
 */
int HTTPClientSendHTTPPostDemoRequest(char *url, char *message, unsigned int message_len, char *response,
                                      int response_max_len) {
    print_debugger("*** starting POST request...\n");
    char postRequestData[MAX_SIZE_REQUEST_DATA];
    const char *headersDefault = "POST %s HTTP/1.1\r\nHost: %s:%d\r\nContent-Type: text/plain\r\n"
                                 "Content-Length: %d\r\n\r\n%s\r\n\r\n";

    if (sprintf(postRequestData, headersDefault, url, urlHost, urlPort, message_len, message) < 0) {
        print_debugger("ERROR: OS failed me again (sprintf)...\n");
        return FAILURE;
    }

    SocketWrite(postRequestData, strlen(postRequestData));

    char responseData[MAX_SIZE_RESPONSE_DATA];
    int readBytes = SocketRead(responseData, MAX_SIZE_RESPONSE_DATA, MAX_TIMEOUT_MS);

    if (readBytes == FAILURE) {
        return FAILURE;
    }

    // Get only the desire data from the response.
    char *responsePayload = removeHeaders(responseData, readBytes);

    if (responsePayload == NULL) {
        print_debugger("ERROR: no payload, you lied to me!\n");
        return FAILURE;
    }

    strncpy(response, responsePayload, response_max_len);

    return (int) strlen(responsePayload);
}

/*
 * Closes any open connections and cleans all the defined and allocated variables
 */
void HTTPClientDeInit(void) {
    print_debugger("*** closing HTTPSocket...\n");
    urlPort = -1;
    urlHost = NULL;
    SocketClose();
    print_debugger("*** de-initializing HTTPSocket...\n");
    SocketDeInit();
}