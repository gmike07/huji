#include "HTTP_client.h"
#include "socket.h"
#include <stdio.h>
#include <strings.h>
#include <string.h>
#include <stdlib.h>
#include "global.h"

#define HTTP_CLIENT_MAX_PAYLOAD_LEN 8192
#define HTTP_CLIENT_TIMEOUT_MS 5000
#define HTTP_CLIENT_CONTENT_LEN_BUF 16

static const char *_get_request = "GET %s HTTP/1.1\r\n"
                                  "Host: %s:%d\r\n\r\n";

static const char *_post_request = "POST %s HTTP/1.1\r\n"
                                   "Host: %s:%d\r\n"
                                   "Content-Type: text/plain\r\n"
                                   "User-Agent: IoTWorkshop\r\n"
                                   "Cache-Control: no-cache\r\n"
                                   "Content-Length: %d\r\n"
                                   "Connection: keep-alive\r\n\r\n"
                                   "%s";

static const char *_payload_delimiter = "\r\n\r\n";

static const char *_content_length_header = "Content-Length: ";
static const char *line_end_del = "\r\n";

static char *g_host;
static int g_port;

int HTTPClientInit(char *host, int port) {
    printf("HTTP: Initializing HTTP\n");

    g_host = host;
    g_port = port;
    if (SocketInit(host, port) < 0) {
        printf("HTTP: Failed initializing HTTP\n");
        return FAILURE_CODE;
    }

    printf("------- HTTP: Initialized HTTP successfully --------\n");
    return SUCCESS_CODE;
}

int HTTPClientSendHTTPGetDemoRequest(char *url, char *response, int response_max_len) {
    int n, resp_len;
    char *payload_loc, *content_len_loc, *cont_len_end_loc;
    static char payload[HTTP_CLIENT_MAX_PAYLOAD_LEN];
    static char content_len[HTTP_CLIENT_CONTENT_LEN_BUF];

    bzero(payload, HTTP_CLIENT_MAX_PAYLOAD_LEN);
    bzero(content_len, HTTP_CLIENT_CONTENT_LEN_BUF);
    bzero(response, response_max_len);

    printf("------ HTTP: Starting HTTPClientSendHTTPGetDemoRequest -------\n");

    if (SocketConnect() < 0) {
        printf("HTTP: Failed connecting to socket\n");
        return FAILURE_CODE;
    }

    if (sprintf(payload, _get_request, url, g_host, g_port) < 0) {
        printf("HTTP: Failed assembling HTTP request\n");
        return FAILURE_CODE;
    }

    n = strlen(payload);
    printf("HTTP: Sending the following message:\n%.*s\n", n, payload);

    if (SocketWrite(payload, n) < n) {
        printf("HTTP: Failed writing to socket\n");
        return FAILURE_CODE;
    }

    bzero(payload, HTTP_CLIENT_MAX_PAYLOAD_LEN);

    n = SocketRead(payload, HTTP_CLIENT_MAX_PAYLOAD_LEN, HTTP_CLIENT_TIMEOUT_MS);
    if (n < 0) {
        printf("HTTP: Failed reading from socket\n");
        return FAILURE_CODE;
    }

    if (SocketClose() < 0) {
        printf("HTTP: Failed closing socket\n");
        return FAILURE_CODE;
    }

    printf("HTTP: Successfully read %d bytes from socket, received the following message:\n%s\n", n, payload);

    content_len_loc = strstr(payload, _content_length_header);
    if (content_len_loc == NULL) {
        printf("HTTP: Invalid response payload\n");
        return FAILURE_CODE;
    }

    cont_len_end_loc = strstr(content_len_loc, line_end_del);
    if (cont_len_end_loc == NULL) {
        printf("HTTP: Invalid response payload\n");
        return FAILURE_CODE;
    }

    strncpy(content_len, content_len_loc + strlen(_content_length_header),
            cont_len_end_loc - content_len_loc - strlen(_content_length_header));

    payload_loc = strstr(payload, _payload_delimiter);
    if (payload_loc == NULL) {
        printf("HTTP: Failed receiving response payload\n");
        return FAILURE_CODE;
    }

    resp_len = atoi(content_len);
    if (response_max_len < resp_len) {
        resp_len = response_max_len;
    }

    strncpy(response, payload_loc + strlen(_payload_delimiter), resp_len);
    n = strlen(response);

    printf("HTTP: Finished HTTPClientSendHTTPGetDemoRequest successfully\n");
    return n;
}

int HTTPClientSendHTTPPostDemoRequest(char *url, char *message, unsigned int message_len, char *response,
                                      int response_max_len) {
    int n, len, resp_len;
    char *payload_loc, *content_len_loc, *cont_len_end_loc;
    static char trimmed_message[HTTP_CLIENT_MAX_PAYLOAD_LEN];
    static char payload[HTTP_CLIENT_MAX_PAYLOAD_LEN];
    static char content_len[HTTP_CLIENT_CONTENT_LEN_BUF];

    bzero(payload, HTTP_CLIENT_MAX_PAYLOAD_LEN);
    bzero(content_len, HTTP_CLIENT_CONTENT_LEN_BUF);
    bzero(trimmed_message, HTTP_CLIENT_MAX_PAYLOAD_LEN);
    bzero(response, response_max_len);
    len = HTTP_CLIENT_MAX_PAYLOAD_LEN;

    printf("HTTP: Starting HTTPClientSendHTTPPostDemoRequest\n");

    if (SocketConnect() < 0) {
        printf("HTTP: Failed connecting to socket\n");
        return FAILURE_CODE;
    }

    if (message_len < HTTP_CLIENT_MAX_PAYLOAD_LEN) {
        len = message_len;
    }

    strncat(trimmed_message, message, len);
    if (sprintf(payload, _post_request, url, g_host, g_port, message_len, trimmed_message) < 0) {
        printf("HTTP: Failed assembling HTTP request\n");
        return FAILURE_CODE;
    }

    n = (int) strlen(payload);
    printf("HTTP: Sending the following message:\n%.*s\n", n, payload);

    if (SocketWrite(payload, n) < n) {
        printf("HTTP: Failed writing to socket\n");
        return FAILURE_CODE;
    }

    bzero(payload, HTTP_CLIENT_MAX_PAYLOAD_LEN);

    n = SocketRead(payload, HTTP_CLIENT_MAX_PAYLOAD_LEN, HTTP_CLIENT_TIMEOUT_MS);
    if (n < 0) {
        printf("HTTP: Failed reading from socket\n");
        return FAILURE_CODE;
    }

    if (SocketClose() < 0) {
        printf("HTTP: Failed closing socket\n");
        return FAILURE_CODE;
    }

    printf("HTTP: Successfully read %d bytes from socket, received the following message:\n%s\n", n, payload);

    content_len_loc = strstr(payload, _content_length_header);
    if (content_len_loc == NULL) {
        printf("HTTP: Invalid response payload\n");
        return FAILURE_CODE;
    }

    cont_len_end_loc = strstr(content_len_loc, line_end_del);
    if (cont_len_end_loc == NULL) {
        printf("HTTP: Invalid response payload\n");
        return FAILURE_CODE;
    }

    strncpy(content_len, content_len_loc + strlen(_content_length_header),
            cont_len_end_loc - content_len_loc - strlen(_content_length_header));

    payload_loc = strstr(payload, _payload_delimiter);
    if (payload_loc == NULL) {
        printf("HTTP: Failed receiving response payload\n");
        return FAILURE_CODE;
    }

    resp_len = atoi(content_len);
    if (response_max_len < resp_len) {
        resp_len = response_max_len;
    }

    strncpy(response, payload_loc + strlen(_payload_delimiter), resp_len);
    n -= strlen(response);

    printf("HTTP: Finished HTTPClientSendHTTPGetDemoRequest successfully\n");
    return n;
}

void HTTPClientDeInit() {
    printf("HTTP: Starting HTTPClientDeInit\n");
    g_host = NULL;
    g_port = 0;
    SocketDeInit();
    printf("HTTP: Finished HTTPClientDeInit successfully\n");
}