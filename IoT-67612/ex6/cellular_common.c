#include "cellular_common.h"
#include "global.h"
#include "serial_io.h"
#include <string.h>
#include <stdio.h>
#include <zconf.h>

#define SET_SCFG_BUF 100

char serial_buf[SERIAL_BUF_SIZE]; // buffer for storing RXed data

static char successful_resp[] = "OK";

static char cmd_turn_off_echo[] = "ATE0\r\n";
static char cmd_set_settings_configuration[] = "AT^SCFG=%s,%s\r\n";

static char turn_off_echo = FALSE;
static char echo_off = FALSE;

void turnOffEcho(void);

/*
 * Turns off echo mode by sending ATE0 command
 * Leaves the receive buffer clean
 */
void turnOffEcho()
{
    int n;

    CleanResvBuf();

    printf("Cellular: Turning off echo\n");
    n = SendCmdRecvResp(cmd_turn_off_echo, serial_buf, SHORT_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0)
    {
        printf("Cellular: Failed turning off echo\n");
        echo_off = FALSE;
    }

    if (!HasOK(serial_buf))
    {
        printf("Cellular: Failed turning off echo\n");
        echo_off = FALSE;
    }

    printf("Cellular: Turned off echo\n");
    echo_off = TRUE;

    CleanResvBuf();
}

/////// Public Functions ///////

void CleanResvBuf()
{
    memset(serial_buf, 0, SERIAL_BUF_SIZE);
}

int HasOK(unsigned char *buf)
{
    if (strstr(buf, successful_resp) == NULL)
    {
        return FALSE;
    }

    return TRUE;
}

/*
 * Send cmd to the serial port, and waits for timeout_ms for a response.
 * Response with site up to rest_max_size is stored in resp_buf.
 * Assumes cmd is null terminated.
 * Assumes resp_buf is of size resp_max_size+1 or more, and rest_buf[resp_max_size] = '\0'
 * Returns -1 is sending failed, and the number of received bytes on success
 */
int SendCmdRecvResp(unsigned char *cmd, unsigned char *resp_buf, unsigned int resp_max_size, unsigned int timeout_ms)
{
    SerialFlushInputBuff();

    if (SerialSend(cmd, strlen(cmd)) < 0)
    {
        printf("Cellular: Failed sending command\n");
        return FAILURE_CODE;
    }

    memset(serial_buf, 0, resp_max_size);
    return SerialRecv(resp_buf, resp_max_size, timeout_ms);
}


int SendCmdRecvRespWithWait(unsigned char *cmd, unsigned char *resp_buf, unsigned int resp_max_size, unsigned int timeout_ms)
{
    SerialFlushInputBuff();

    sleep(2);

    if (SerialSend(cmd, strlen(cmd)) < 0)
    {
        printf("Cellular: Failed sending command\n");
        return FAILURE_CODE;
    }

    sleep(2);

    memset(serial_buf, 0, resp_max_size);
    return SerialRecv(resp_buf, resp_max_size, timeout_ms);
}


void DefineRequiredEchoMode(char mode)
{
    if (!mode)
    {
        turn_off_echo = TRUE;
    }
    else
    {
        turn_off_echo = FALSE;
    }
}

void VerifyEchoMode()
{
    if (turn_off_echo && !echo_off)
    {
        turnOffEcho();
    }
}

int SetSettingsConfiguration(char *config_name, char *config_values)
{
    int n;
    static char cmd[SET_SCFG_BUF];

    memset(cmd, 0, SET_SCFG_BUF);

    CleanResvBuf();

    if (sprintf(cmd, cmd_set_settings_configuration, config_name, config_values) < 0)
    {
        printf("Cellular: Failed assembling configuration change\n");
        return FAILURE_CODE;
    }

    n = SendCmdRecvResp(cmd, serial_buf, LARGE_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

    if (n <= 0 || !HasOK(serial_buf))
    {
        printf("Cellular: Not OK response received. Received: %s\n", serial_buf);
        return FAILURE_CODE;
    }

    return SUCCESS_CODE;
}