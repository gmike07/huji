#include "MQTTClient.h"
#include "wolfmqtt/mqtt_types.h"
#include "socket.h"
#include "utils.h"
#include "my_printf_lib.h"


#define PORT_LENGTH 10

typedef struct _SocketContext {
    char *host;
    MQTTCtx* mqttCtx;
} SocketContext;

static SocketContext g_sock;

/*
 * Connects the socket to the broker, to the given host and port
 * Returns 0 on success, and a negative number otherwise (one of MqttPacketResponseCodes)
 * timeout_ms defines the timeout in milliseconds
 */
static int NetConnect(void *context, const char* host, word16 port, int timeout_ms)
{
    my_printf("MQTTClient: Initializing socket\n");

    SocketContext *sock = (SocketContext *)context;
    sock->host = host;

    if (SocketInit(host, port) < 0)
    {
        my_printf("MQTTClient: Failed initializing socket\n");
        return MQTT_CODE_ERROR_SYSTEM;
    }

    my_printf("MQTTClient: Initialized socket successfully\n");

    my_printf("MQTTClient: Connecting to the host\n");

    if (SocketConnect() < 0)
    {
        my_printf("HTTP: Failed connecting to host\n");
        return MQTT_CODE_ERROR_NETWORK;
    }

    my_printf("MQTTClient: Connected to the host successfully\n");

    return MQTT_CODE_SUCCESS;
}

/*
 * Performs a network (socket) read from the connected broker,
 * to the given buffer buf, and reads buf_len bytes.
 * Returns number of read bytes on success, and a negative number otherwise (one of MqttPacketResponseCodes)
 * timeout_ms defines the timeout in milliseconds.
 */
static int NetRead(void *context, byte* buf, int buf_len, int timeout_ms)
{
    int n;
    bzero(buf, buf_len);

    n = SocketRead(buf, buf_len, timeout_ms);

    if (n == 0)
    {
        my_printf("MQTTClient: socket timeout\n");
        return MQTT_CODE_ERROR_TIMEOUT;
    }

    if (n < 0)
    {
        my_printf("MQTTClient: Failed reading from socket\n");
        return MQTT_CODE_ERROR_NETWORK;
    }

    return n;
}

/*
 * Performs a network (socket) write to the connected broker,
 * from the given buffer buf, with size of buf_len.
 * Returns the number of sent bytes on success, and a negative number otherwise (one of MqttPacketResponseCodes)
 * timeout_ms defines the timeout in milliseconds
 */
static int NetWrite(void *context, const byte* buf, int buf_len, int timeout_ms)
{
    if (SocketWrite(buf, buf_len) < buf_len)
    {
        my_printf("MQTTClient: Failed writing to socket\n");
        return MQTT_CODE_ERROR_NETWORK;
    }

    return buf_len;
}

/*
 * Closes the network (socket) connection to the connected broker.
 * Returns 0, and a negative number otherwise (one of MqttPacketResponseCodes)
 */
static int NetDisconnect(void *context)
{
    if (SocketClose() < 0)
    {
        my_printf("MQTTClient: Failed closing socket\n");
        return MQTT_CODE_ERROR_SYSTEM;
    }

    SocketDeInit();

    return MQTT_CODE_SUCCESS;
}

/* public functions */
int MqttClientNet_Init(MqttNet* net, MQTTCtx* mqttCtx)
{
    if (net) {
        XMEMSET(net, 0, sizeof(MqttNet));
        net->connect = NetConnect;
        net->read = NetRead;
        net->write = NetWrite;
        net->disconnect = NetDisconnect;

        memset(&g_sock, 0, sizeof(g_sock));
        net->context = &g_sock;
        g_sock.mqttCtx = mqttCtx;
    }

    return MQTT_CODE_SUCCESS;
}

int MqttClientNet_DeInit(MqttNet* net)
{
    if (net) {
        if (net->context) {
            memset(&g_sock, 0, sizeof(g_sock));
        }
        XMEMSET(net, 0, sizeof(MqttNet));
    }
    return MQTT_CODE_SUCCESS;
}