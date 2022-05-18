#include "socket.h"
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <strings.h>
#include <zconf.h>
#include <stdlib.h>
#include "global.h"
#include <errno.h>

static int sockfd, portno;
static struct hostent *server;
static struct sockaddr_in serv_addr;

int SocketInit(char *host, int port)
{
    printf("Socket: Initializing socket\n");
    server = gethostbyname(host);
    if (server == NULL)
    {
        printf("Socket: Failed getting host name\n");
        return FAILURE_CODE;
    }

    portno = port;
    if (sockfd < 0)
    {
        printf("Socket: Failed getting port\n");
        return FAILURE_CODE;
    }

    printf("Socket: Initialized socket successfully\n");
    return SUCCESS_CODE;
}

int SocketConnect()
{
    int n;
    printf("Socket: Starting SocketConnect\n");

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0)
    {
        printf("Socket: Failed getting port\n");
        return FAILURE_CODE;
    }

    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr,
          (char *)&serv_addr.sin_addr.s_addr,
          server->h_length);
    serv_addr.sin_port = htons(portno);

    n = connect(sockfd,(struct sockaddr *)&serv_addr,sizeof(serv_addr));
    if (n < 0)
    {
        printf("Socket: Failed connecting\n");
        return FAILURE_CODE;
    }

    printf("Socket: Successfully connected\n");
    return n;
}

int SocketWrite(unsigned char *payload, unsigned int len)
{
    int n;

    printf("Socket: Starting SocketWrite\n");

    n = write(sockfd, payload, len);
    if (n < 0)
    {
        printf("Socket: Failed writing to socket\n");
        return FAILURE_CODE;
    }

    printf("Socket: Ending SocketWrite\n");
    return n;
}

int SocketRead(unsigned char *buf, unsigned int max_len, unsigned int timeout_ms)
{
    int n;
    struct timeval timeout;

    printf("Socket: Starting SocketRead\n");

    timeout.tv_sec = timeout_ms / 1000;
    timeout.tv_usec = 0;

    n = setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (char *)&timeout, sizeof(timeout));
    if (n  < 0)
    {
        printf("Socket: Failed setting timeout to socket\n");
        return FAILURE_CODE;
    }

    n = read(sockfd, buf, max_len);
    if (n < 0)
    {
        printf("Socket: Failed reading from socket. errno %d\n", errno);
        if (errno == EAGAIN)
        {
            return 0;
        }
        return FAILURE_CODE;
    }

    printf("Socket: Ending SocketRead\n");
    return n;
}

int SocketClose()
{
    int n;
    printf("Socket: Starting SocketClose\n");

    n = close(sockfd);
    if (n < 0)
    {
        printf("Socket: Failed closing socket\n");
        return FAILURE_CODE;
    }

    printf("Socket: Ending SocketClose\n");
}

void SocketDeInit(void)
{
    sockfd = 0;
    portno = 0;
    server = NULL;
    bzero((char *) &serv_addr, sizeof(serv_addr));
}