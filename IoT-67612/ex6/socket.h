#ifndef SOCKET_H
#define SOCKET_H
#include "cellular.h"

int SocketInit(char *host, int port);
int SocketConnect(void);
int SocketWrite(unsigned char *payload, unsigned int len);
int SocketRead(unsigned char *buf, unsigned int max_len, unsigned int timeout_ms);
int SocketClose(void);
void SocketDeInit(void);
int get_num_ops();
OPERATOR_INFO* get_ops();
char* get_imei();
#endif //SOCKET_H