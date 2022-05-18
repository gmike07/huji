#ifndef HTTP_CLIENT_H
#define HTTP_CLIENT_H

/*
 * Initializes the client.
 * Host: The destination address
 * as DNS: en8wtnrvtnkt5.x.pipedream.net,
 * or as IPv4: 35.169.0.97.
 * Port: The communication endpoint, int, e.g.: 80.
 * Returns 0 on success, -1 on failure
 */
int HTTPClientInit(char *host, int port);

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
int HTTPClientSendHTTPGetDemoRequest(char *url, char *response, int response_max_len);

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
                                      int response_max_len);

/*
 * Closes any open connections and cleans all the defined and allocated variables
 */
void HTTPClientDeInit(void);

#endif //HTTP_CLIENT_H