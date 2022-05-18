#include <stdio.h>

#include "MQTTClient.h"
#include "global.h"
#include <string.h>
#include <time.h>
#include <unistd.h>

#define MAX_BUFFER_SIZE 1024


// Flag that check if we already read message from the broker.
byte is_read_message = 0;


// Connection info.
const char *host = "broker.mqttdashboard.com";
const int port = 1883;

// Buffer for MQTTCtx.
byte buf_r[MAX_BUFFER_SIZE];
byte buf_t[MAX_BUFFER_SIZE];

char subscribe_buffer[MAX_BUFFER_SIZE];
char publish_buffer[MAX_BUFFER_SIZE];
char publish_topic_buffer[MAX_BUFFER_SIZE];

const char* client_id = "WolfMQTTClientYuval1";

const char* identifier = "RickRoll";

const char* lwt_topic = "huji_iot_class/2021_2022/disconnect";
const char* lwt_message = "{\n"
                          "\"DisconnectedGracefully\":false\n"
                          "}";

const char* first_topic = "huji_iot_class/2021_2022";
const char* first_message_format = "{\n"
                                   "\"Student1ID\":\"206647620\",\n"
                                   "\"Student2ID\":\"211747639\",\n"
                                   "\"Student1Name\":\"Yuval\",\n"
                                   "\"Student2Name\":\"Mike\",\n"
                                   "\"Identifier\":\"%s\"\n"
                                   "}";
const char* second_topic_format = "huji_iot_class/2021_2022/%s";
const char* second_message_format = "{\n"
                                    "\"CurrentTimeUTC\":%d\n"
                                    "}";
const char* third_message = "{\n"
                            "\"DisconnectedGracefully\":true\n"
                            "}";
const char* third_topic = "huji_iot_class/2021_2022/disconnect";

const char* subscribe_topic = "huji_iot_class/2021_2022/%s/recv/#";

/**
 * Initializing the MQTTCtx.
 * @param mqttCtx MQTTCtx to initializing.
 */
void init_context(MQTTCtx *mqttCtx) {
    XMEMSET(&(mqttCtx->subscribe), 0, sizeof(mqttCtx->subscribe));
    XMEMSET(&(mqttCtx->publish), 0, sizeof(mqttCtx->publish));
    XMEMSET(&(mqttCtx->connect), 0, sizeof(mqttCtx->connect));
    XMEMSET(&(mqttCtx->lwt_msg), 0, sizeof(mqttCtx->lwt_msg));
    XMEMSET(buf_t, 0, MAX_BUFFER_SIZE);
    XMEMSET(buf_r, 0, MAX_BUFFER_SIZE);


    mqttCtx->host = host;
    mqttCtx->port = port;
    mqttCtx->cmd_timeout_ms = 1000;
    mqttCtx->use_tls = 0;
    mqttCtx->rx_buf = buf_r;
    mqttCtx->tx_buf = buf_t;

    //mqttCtx->connect.username = "";
    //mqttCtx->connect.password = "";
    mqttCtx->connect.keep_alive_sec = 60;
    mqttCtx->connect.clean_session = 0;
    mqttCtx->connect.client_id = client_id;
    mqttCtx->connect.lwt_msg = &mqttCtx->lwt_msg;
    mqttCtx->connect.enable_lwt = 1;

    // LWT
    mqttCtx->lwt_msg.qos = 1;
    mqttCtx->lwt_msg.retain = 0;
    mqttCtx->lwt_msg.topic_name = lwt_topic;
    mqttCtx->lwt_msg.buffer = lwt_message;
    mqttCtx->lwt_msg.total_len = strlen(lwt_message);

    // publish
    mqttCtx->publish.qos = 1;
    mqttCtx->publish.retain = 0;

    //subscribe
    mqttCtx->topics[0].qos = 1;
    XMEMSET(subscribe_buffer, 0, MAX_BUFFER_SIZE);
    sprintf(subscribe_buffer, subscribe_topic, identifier);
    mqttCtx->topics[0].topic_filter = subscribe_buffer;

    /* Subscribe Topic */
    mqttCtx->subscribe.packet_id = mqtt_get_packetid();
    mqttCtx->subscribe.topic_count = sizeof(mqttCtx->topics) / sizeof(MqttTopic);
    mqttCtx->subscribe.topics = mqttCtx->topics;
}


/**
 * Callback function, that called after some message is redden from the broker.
 */
static int mqtt_message_cb(MqttClient *client, MqttMessage *msg,
                           byte msg_new, byte msg_done) {
    byte buf[PRINT_BUFFER_SIZE + 1];
    word32 len;
    MQTTCtx *mqttCtx = (MQTTCtx *) client->ctx;

    (void) mqttCtx;

    if (msg_new) {
        /* Determine min size to dump */
        len = msg->topic_name_len;
        if (len > PRINT_BUFFER_SIZE) {
            len = PRINT_BUFFER_SIZE;
        }
        XMEMCPY(buf, msg->topic_name, len);
        buf[len] = '\0'; /* Make sure its null terminated */

        /* Print incoming message */
        printf("MQTT Message: Topic %s, Qos %d, Len %u\n", buf, msg->qos, msg->total_len);


    }

    /* Print message payload */
    len = msg->buffer_len;
    if (len > PRINT_BUFFER_SIZE) {
        len = PRINT_BUFFER_SIZE;
    }
    XMEMCPY(buf, msg->buffer, len);
    buf[len] = '\0'; /* Make sure its null terminated */
    printf("Payload (%d - %d): %s\n", msg->buffer_pos, msg->buffer_pos + len, buf);

    if (msg_done) {
        is_read_message = 1;
        printf("MQTT Message: Done\n");
    }

    /* Return negative to terminate publish processing */
    return MQTT_CODE_SUCCESS;
}

/**
 * Initializing MqttNet and MQTTCtx.
 * @param net MqttNet object to init.
 * @param mqttCtx MQTTCtx to init.
 * @return FAILURE_CODE on failure, SUCCESS_CODE on success.
 */
int init_objects(MqttNet* net, MQTTCtx* mqttCtx)
{
    printf("Initializing context.\n");
    init_context(mqttCtx);
    printf("Finish initializing context.\n\n");


    /* Initialize MqttClient net */
    printf("Initializing client net.\n");
    if (MqttClientNet_Init(net, mqttCtx) != MQTT_CODE_SUCCESS) {
        printf("error initing.\n");
        return FAILURE_CODE;
    }
    printf("Finish initializing client net.\n\n");


    /* Initialize MqttClient structure */
    printf("Initializing client.\n");
    int rc = MqttClient_Init(&(mqttCtx->client), net,
                             mqtt_message_cb,
                             mqttCtx->tx_buf, MAX_BUFFER_SIZE,
                             mqttCtx->rx_buf, MAX_BUFFER_SIZE,
                             mqttCtx->cmd_timeout_ms);
    if (rc != MQTT_CODE_SUCCESS) {
        printf("Error initing client.\n");
        printf("MQTT Ping Keep Alive Error: %s (%d)\n",
               MqttClient_ReturnCodeToString(rc), rc);
        return FAILURE_CODE;
    }
    return SUCCESS_CODE;
}

/**
 * This function connect to our broker with an initialized MQTTCtx object.
 * @param mqttCtx Initialized MQTTCtx object.
 * @return FAILURE_CODE on failure, SUCCESS_CODE on success.
 */
int connectToBroker(MQTTCtx* mqttCtx)
{
    /* Connect to broker */
    printf("Connect to the broker.\n");
    int rc = MqttClient_NetConnect(&(mqttCtx->client),
                               mqttCtx->host,
                               mqttCtx->port,
                               DEFAULT_CON_TIMEOUT_MS,
                               mqttCtx->use_tls, mqtt_tls_cb);
    if ( rc != MQTT_CODE_SUCCESS) {
        printf("MQTT Ping Keep Alive Error: %s (%d)\n",
               MqttClient_ReturnCodeToString(rc), rc);
        printf("Unable to connect to the broker.\n");
        return FAILURE_CODE;
    }
    printf("Finish connect to the broker successfully.\n\n");


    /* Send Connect and wait for Connect Ack */
    printf("Send connect to the broker.\n");
    rc = MqttClient_Connect(&(mqttCtx->client), &(mqttCtx->connect));
    if ( rc != MQTT_CODE_SUCCESS) {
        printf("MQTT Ping Keep Alive Error: %s (%d)\n",
               MqttClient_ReturnCodeToString(rc), rc);
        printf("Unable to send connect to the broker.\n");
        return FAILURE_CODE;
    }
    printf("Finish Send connect to the broker successfully.\n");
    return SUCCESS_CODE;
}

/**
 * This function subscribe to a given topic.
 * @param mqttCtx Initialized MQTTCtx object.
 * @param topic Name of the topic to subscribe.
 * @return FAILURE_CODE on failure, SUCCESS_CODE on success.
 */
int subscribe_to_topic(MQTTCtx* mqttCtx, const char* topic)
{
    mqttCtx->topics[0].topic_filter = topic;
    printf("Subscribe to the broker on topic \n%s\n\n", topic);
    int rc = MqttClient_Subscribe(&(mqttCtx->client), &(mqttCtx->subscribe));
    if (rc != MQTT_CODE_SUCCESS) {
        printf("MQTT Ping Keep Alive Error: %s (%d)\n",
               MqttClient_ReturnCodeToString(rc), rc);
        printf("Error while Subscribing!");
        return FAILURE_CODE;
    }
    printf("Finish Subscribe to the broker.\n\n");
    return SUCCESS_CODE;
}

/**
 * Show the topics we subscribed to.
 * @param mqttCtx Initialized MQTTCtx object.
 */
void show_subscribe_results(MQTTCtx* mqttCtx)
{
    for (int i = 0; i < mqttCtx->subscribe.topic_count; i++) {
        MqttTopic *topic = &(mqttCtx->subscribe.topics)[i];
        printf("Topic %s, Qos %u, Return Code %u\n", topic->topic_filter, topic->qos,
                topic->return_code);
    }
}

/**
 * This function publish a given message to a given topic.
 * @param mqttCtx Initialized MQTTCtx object.
 * @param topic_name Topic to publish.
 * @param message Message to publish.
 */
void publish(MQTTCtx *mqttCtx, const char *topic_name, const char *message) {
    mqttCtx->publish.topic_name = topic_name;
    mqttCtx->publish.buffer = message;
    mqttCtx->publish.total_len = strlen(message);
    mqttCtx->publish.packet_id = mqtt_get_packetid();
    printf("publishing message on topic %s with message: \n%s\n", topic_name, message);

    int rc;
    /* This loop allows payloads larger than the buffer to be sent by
       repeatedly calling publish.
    */
    do {
        rc = MqttClient_Publish(&mqttCtx->client, &mqttCtx->publish);
    } while (rc == MQTT_CODE_PUB_CONTINUE);
    printf("Finish Publishing to the broker.\n\n");
}

/**
 * This function receive message and print the given message.
 * @param mqttCtx Initialized MQTTCtx object.
 */
void read_message(MQTTCtx *mqttCtx) {
    /* Read Loop */
    printf("MQTT Waiting for message...");
    int rc;
    is_read_message = 0;

    do {

        /* Try and read packet */
        rc = MqttClient_WaitMessage(&mqttCtx->client,
                                    mqttCtx->cmd_timeout_ms);

    } while (is_read_message == 0);


    printf("Receiving the message: %s\n", mqttCtx->rx_buf);

}

/**
 * Disconnect from the broker.
 * @param mqttCtx Initialized MQTTCtx object.
 */
void disconnect(MQTTCtx *mqttCtx) {

    printf("Discontectting from the server\n");

    MqttClient_Disconnect_ex(&mqttCtx->client, &mqttCtx->disconnect);
    MqttClient_NetDisconnect(&mqttCtx->client);

    printf("Disconnected succefully!\n");
}


/**
 * The main function to run the exercise code.
 */
int main()
{
    // Initializing the objects we need.
    MQTTCtx mqttCtx;
    MqttNet net;

    if(init_objects(&net, &mqttCtx) != SUCCESS_CODE)
    {
        return FAILURE_CODE;
    }

    if(connectToBroker(&mqttCtx) != SUCCESS_CODE)
    {
        return FAILURE_CODE;
    }

    // Subscribe to the given topic.
    XMEMSET(subscribe_buffer, 0, MAX_BUFFER_SIZE);
    sprintf(subscribe_buffer, subscribe_topic, identifier);
    if(subscribe_to_topic(&mqttCtx, subscribe_buffer) != SUCCESS_CODE)
    {
        return FAILURE_CODE;
    }

    show_subscribe_results(&mqttCtx);

    //send first message
    XMEMSET(publish_buffer, 0, MAX_BUFFER_SIZE);
    sprintf(publish_buffer, first_message_format, identifier);
    publish(&mqttCtx, first_topic, publish_buffer);

    //send second message
    time_t epoch;
    time(&epoch);
    XMEMSET(publish_buffer, 0, MAX_BUFFER_SIZE);
    sprintf(publish_buffer, second_message_format, epoch);
    XMEMSET(publish_topic_buffer, 0, MAX_BUFFER_SIZE);
    sprintf(publish_topic_buffer, second_topic_format, identifier);
    publish(&mqttCtx, publish_topic_buffer, publish_buffer);

    // Receive message.
    printf("Receive message.\n");
    read_message(&mqttCtx);
    printf("Finish receive message successfully.\n\n");

    //send third message
    publish(&mqttCtx, third_topic, third_message);

    // Disconnecting.
    printf("Disconnecting, bye!\n");
    disconnect(&mqttCtx);
    printf("Disconnecting successfully!\n\n");

    return SUCCESS_CODE;
}