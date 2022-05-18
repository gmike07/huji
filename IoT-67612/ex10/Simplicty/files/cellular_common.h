#ifndef EX4_CELLULAR_COMMON_H
#define EX4_CELLULAR_COMMON_H

#define BAUD_RATE 115200

#define SERIAL_BUF_SIZE 2048

#define SHORT_TIMEOUT 2000
#define MEDIUM_TIMEOUT 8000
#define LONG_TIMEOUT 140000

#define SHORT_RESPONSE_BUF_SIZE 10
#define MEDIUM_RESPONSE_BUF_SIZE 50
#define LARGE_RESPONSE_BUF_SIZE 2048

#define ECHO_MODE_OFF 0
#define ECHO_MODE ON 1

extern char serial_buf[SERIAL_BUF_SIZE]; // buffer for storing RXed data

void CleanResvBuf(void);

int HasOK(unsigned char *buf);

int HasNoCarrier(unsigned char *buf);

int SendCmdRecvResp(unsigned char *cmd, unsigned char *resp_buf, unsigned int resp_max_size, unsigned int timeout_ms);

void DefineRequiredEchoMode(char mode);

void VerifyEchoMode(void);

int SetSettingsConfiguration(char *config_name, char *config_values);

int SendCmdRecvRespWithWait(unsigned char *cmd, unsigned char *resp_buf, unsigned int resp_max_size, unsigned int timeout_ms);

#endif //EX4_CELLULAR_COMMON_H
