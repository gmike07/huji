#ifndef SOCKET_H
#define SOCKET_H

int SocketInit(char *host, int port);
int SocketConnect(void);
int SocketWrite(unsigned char *payload, unsigned int len);
int SocketRead(unsigned char *buf, unsigned int max_len, unsigned int timeout_ms);
int SocketClose(void);
void SocketDeInit(void);

#endif //SOCKET_H