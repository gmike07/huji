#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "serial_io.h"
#define DEFAULT_BUFFER_SIZE 256
#define DEFAULT_BAUD_RATE 115200

unsigned int MS_TIMES[] = {2000, 10000, 120000};
unsigned int MAX_SIZES[] = {64, 128, 256, 4096};


/**
 * Send single message, and print it's response.
 * @param len Expected response length.
 * @param timeout Expected timeout.
 * @return SUCCESS_CODE on success, FAILURE_CODE on failure.
 */
int read_message(unsigned int len, unsigned int timeout)
{
    char buf[len];
    memset(buf, 0, len);
    if(SerialRecv(buf, len - 1, timeout) == FAILURE_CODE)
    {
        return FAILURE_CODE;
    }
    // make sure that we can easily print it
    buf[len-1] = '\0';
    printf("%s\n", buf);
    return SUCCESS_CODE;
}

/**
 * This function send a single message.
 * @param msg Message to sent.
 */
void send_message(char* msg)
{
    printf("Sending message: %s\n", msg);
    if(SerialSend(msg, strlen(msg)) == FAILURE_CODE)
    {
        exit(FAILURE_CODE);
    }
}

/**
 * This function wait until the modem is ready. (Receiving +PBREADY)
 */
void wait_to_ready(){
    char buf[DEFAULT_BUFFER_SIZE];
    char cum_buf [DEFAULT_BUFFER_SIZE];

    memset(buf, 0, DEFAULT_BUFFER_SIZE);
    memset(cum_buf, 0, DEFAULT_BUFFER_SIZE);

    printf("waiting for +PBREADY...\n");

    int n;

    while (strstr(cum_buf, "\r\n+PBREADY\r\n") == NULL)
    {
        memset(buf, 0, DEFAULT_BUFFER_SIZE);
        n = SerialRecv(buf, DEFAULT_BUFFER_SIZE - 1, MS_TIMES[0]);
        if(n != -1 && n != 0)
        {
            printf("got %s\n", buf);
        }
        strcat(cum_buf, buf);
    }
}

/**
 * Run the example code.
 */
int main()
{
    char *port = "/dev/ttyUSB0";
    SerialInit(port, DEFAULT_BAUD_RATE);
    // clear buffer
    SerialFlushInputBuff();


    wait_to_ready();
    printf("*********** FINISH LOADING ***********\n");

    send_message("AT\r\n");
    read_message(MAX_SIZES[0], MS_TIMES[1]);
    printf("----------------------------------------------\n");
    send_message("AT+CCID\r\n");
    read_message(MAX_SIZES[0], MS_TIMES[1]);
    printf("----------------------------------------------\n");
    send_message("AT+GSN\r\n");
    read_message(MAX_SIZES[0], MS_TIMES[1]);
    printf("----------------------------------------------\n");
    send_message("AT+CREG?\r\n");
    read_message(MAX_SIZES[0], MS_TIMES[1]);
    printf("----------------------------------------------\n");
    send_message("AT+COPS?\r\n");
    read_message(MAX_SIZES[1], MS_TIMES[1]);
    printf("----------------------------------------------\n");
    send_message("AT+COPS=?\r\n");
    read_message(MAX_SIZES[3], MS_TIMES[2]);


    SerialDisable();
    return SUCCESS_CODE;
}
