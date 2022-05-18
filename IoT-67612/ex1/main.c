#include <stdio.h>
#include "HTTP_client.h"
#include <string.h>

int main() {

    HTTPClientInit("en8wtnrvtnkt5.x.pipedream.net", 80);

    // Send GET request, and save the response data.
    char getResult[17];
    HTTPClientSendHTTPGetDemoRequest("/", getResult, 16);

    // Send POST request, and save the response data.
    char postResult[17];
    HTTPClientSendHTTPPostDemoRequest("/", "hello cellular world!",
                                      strlen("hello cellular world!"),
                                      postResult, 16);

    // NULL terminate the responses
    getResult[16] = NULL;
    postResult[16] = NULL;

    // Print the given responses.
    printf("\n***** RESULTS: *****\n\n");
    printf("Get response: %s\n", getResult);
    printf("Post response: %s\n\n", postResult);

    HTTPClientDeInit();
    return 0;
}
