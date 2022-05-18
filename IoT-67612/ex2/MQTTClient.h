//
// Created by Mike on 10/29/2021.
//

#ifndef IOT_MQTTCLIENT_H
#define IOT_MQTTCLIENT_H

#include "socket.h"
#include "wolfmqtt/mqtt_client.h"
#include "examples/mqttexample.h"
#include "wolfmqtt/mqtt_types.h"
/*
* Initializes the Net interface for communication
*/
int MqttClientNet_Init(MqttNet* net, MQTTCtx* mqttCtx);


/*
* De-Initializes all that was allocated by MqttClientNet
*/
int MqttClientNet_DeInit(MqttNet* net);

#endif //IOT_MQTTCLIENT_H
