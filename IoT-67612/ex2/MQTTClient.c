//
// Created by Mike on 10/29/2021.
//
#include "global.h"
#include "MQTTClient.h"

/*
* Connects the socket to the broker,
* to the given host and port.
* Returns 0 on success, and a negative number otherwise
* (one of MqttPacketResponseCodes)
* timeout_ms defines the timeout in milliseconds.
*/
static int NetConnect(void *context, const char *host, word16 port,
                      int timeout_ms) {
    if (SocketInit(host, port) != SUCCESS_CODE) {
        return MQTT_CODE_ERROR_NETWORK;
    }
    if (SocketConnect() != SUCCESS_CODE) {
        return MQTT_CODE_ERROR_NETWORK;
    }
    return MQTT_CODE_SUCCESS;
}


/*
* Performs a network (socket) read from the connected broker,
* to the given buffer buf, and reads buf_len bytes.
* Returns number of read bytes on success, and a negative number
* otherwise (one of MqttPacketResponseCodes).
* timeout_ms defines the timeout in milliseconds.
*/
static int NetRead(void *context, byte *buf, int buf_len, int timeout_ms) {
    int n = SocketRead(buf, buf_len, timeout_ms);
    if (n < 0) {
        return MQTT_CODE_ERROR_NETWORK;
    }
    return n;
}


/*
* Performs a network (socket) write to the connected broker,
* from the given buffer buf, with size of buf_len.
* Returns the number of sent bytes on success,
* and a negative number otherwise (one of MqttPacketResponseCodes)
* timeout_ms defines the timeout in milliseconds
*/
static int NetWrite(void *context, const byte *buf, int buf_len,
                    int timeout_ms) {
    int n = SocketWrite(buf, buf_len);
    if (n < 0) {
        return MQTT_CODE_ERROR_NETWORK;
    }
    return n;
}


/*
* Closes the network (socket) connection to the connected broker.
* Returns 0, and a negative number otherwise
* (one of MqttPacketResponseCodes)
*/
static int NetDisconnect(void *context) {
    if (SocketClose() != SUCCESS_CODE) {
        return MQTT_CODE_ERROR_NETWORK;
    }
    SocketDeInit();
    return MQTT_CODE_SUCCESS;
}


/*
* Initializes the Net interface for communication
*/
int MqttClientNet_Init(MqttNet *net, MQTTCtx *mqttCtx) {
    net->connect = NetConnect;
    net->read = NetRead;
    net->write = NetWrite;
    net->disconnect = NetDisconnect;
    net->context = mqttCtx;
    return 0;
}

/*
* De-Initializes all that was allocated by MqttClientNet
*/
int MqttClientNet_DeInit(MqttNet *net) { return 0; }

