#include <stdio.h>
#include <string.h>
#include <time.h>
#include <signal.h>
#include <unistd.h>
#include "MQTTClient.h"
#include "cellular.h"
#include "global.h"
#include "socket.h"

static char default_mqtt_host[] = "broker.mqttdashboard.com";
static char default_mqtt_client_id[] = "YuvalError3";

static char default_mqtt_topic[] = "huji_iot_class/2021_2022";
static char mqtt_lwt_topic_suffix[] = "disconnect";


static char subscribe_topic[] = "huji_iot_class/2021_2022/%s/recv/#";

static char default_mqtt_message[] = "{"
                                     "\"Student1ID\":\"206647620\","
                                     "\"Student2ID\":\"211747639\","
                                     "\"Student1Name\":\"Yuval Otmazgin\","
                                     "\"Student2Name\":\"Mike Greenbaum\","
                                     "\"Identifier\":\"%s\""
                                     "}";

static char end_message[] = "{"
                            "\"DisconnectedGracefully\":%s"
                            "}";

static volatile word16 mPacketIdLast = 0;
static int default_port = 1883;


#define READ_BUFF_SIZE 512
#define WRITE_BUFF_SIZE 512
#define MSG_BUFF_SIZE 256
#define TOPIC_BUFF_SIZE 64

#define DEFAULT_MQTT_QOS 1
#define DEFAULT_KEEP_ALIVE_SEC (60)
#define DEFAULT_CMD_TIMEOUT_MS  (30000)
#define DEFAULT_CON_TIMEOUT_MS  (5000)


#define IMEI_LEN 32
#define COPS_MESSAGE_LEN 4096
#define COPS_HELPER_LEN 1024
#define MAX_NETWORKS 15


int create_cops_message(char* buf, int len)
{
    char helper_buf[COPS_HELPER_LEN];
    memset(buf, 0, len);
    strcpy(buf, "{\n"
                "\"AvailableOperators\":[\n");
    int lst_len = get_num_ops();
    OPERATOR_INFO* lst = get_ops();
    const char* format = "{\n"
                         "\"OperatorName\":\"%s\",\n"
                         "\"OperatorCode\":\"%d\",\n"
                         "\"AccessTechnology\":\"%s\"\n"
                         "}";
    int i = 0;
    for(;i < lst_len - 1; i++)
    {
        memset(helper_buf, 0, COPS_HELPER_LEN);
        if(sprintf(helper_buf, format, lst[i].operator_name, lst[i].operator_code, lst[i].access_technology) < 0)
        {
            return FAILURE_CODE;
        }
        strcat(buf, helper_buf);
        strcat(buf, ",\n");
    }
    memset(helper_buf, 0, COPS_HELPER_LEN);
    if(sprintf(helper_buf, format, lst[i].operator_name, lst[i].operator_code, lst[i].access_technology) < 0)
    {
        return FAILURE_CODE;
    }
    strcat(buf, helper_buf);
    strcat(buf, "\n]\n}");
    return SUCCESS_CODE;
}

/*
 * This function called when ^c is pressed.
 */
void sig_handler(int signum) {
    printf("trl+C, why did you press it?!!!\n");
    CellularDisable();
    exit(FAILURE_CODE);
}


static word16 mqtt_get_packetid(void) {
    /* Check rollover */
    if (mPacketIdLast >= MAX_PACKET_ID) {
        mPacketIdLast = 0;
    }

    return ++mPacketIdLast;
}

static void mqtt_init_ctx(MQTTCtx *mqttCtx) {
    XMEMSET(mqttCtx, 0, sizeof(MQTTCtx));
    mqttCtx->host = default_mqtt_host;
    mqttCtx->port = default_port;
    mqttCtx->qos = DEFAULT_MQTT_QOS;
    mqttCtx->clean_session = 0;
    mqttCtx->keep_alive_sec = DEFAULT_KEEP_ALIVE_SEC;
    mqttCtx->client_id = default_mqtt_client_id;
    mqttCtx->topic_name = default_mqtt_topic;
    mqttCtx->cmd_timeout_ms = DEFAULT_CMD_TIMEOUT_MS;
}

static int mqtt_message_cb(MqttClient *client, MqttMessage *msg,
                           byte msg_new, byte msg_done) {
    byte buf[MSG_BUFF_SIZE + 1];
    word32 len;
    MQTTCtx *mqttCtx = (MQTTCtx *) client->ctx;

    (void) mqttCtx;

    if (msg_new) {
        /* Determine min size to dump */
        len = msg->topic_name_len;
        if (len > MSG_BUFF_SIZE) {
            len = MSG_BUFF_SIZE;
        }
        XMEMCPY(buf, msg->topic_name, len);
        buf[len] = '\0'; /* Make sure its null terminated */

        /* Print incoming message */
        PRINTF("MQTT Message: Topic %s, Qos %d, Len %u",
               buf, msg->qos, msg->total_len);
    }

    /* Print message payload */
    len = msg->buffer_len;
    if (len > MSG_BUFF_SIZE) {
        len = MSG_BUFF_SIZE;
    }
    XMEMCPY(buf, msg->buffer, len);
    buf[len] = '\0'; /* Make sure its null terminated */
    PRINTF("Payload (%d - %d): %s",
           msg->buffer_pos, msg->buffer_pos + len, buf);

    if (msg_done) {
        PRINTF("MQTT Message: Done");
    }

    /* Return negative to terminate publish processing */
    return MQTT_CODE_SUCCESS;
}

static void clean_network(MQTTCtx *mqttCtx) {
    int rc;

    /* Cleanup network */
    rc = MqttClientNet_DeInit(&mqttCtx->net);
    if (rc != MQTT_CODE_SUCCESS) {
        printf("Main: Failed cleaning network resources\n");
        return;
    }

    MqttClient_DeInit(&mqttCtx->client);
}

static int disconnect(MQTTCtx *mqttCtx) {
    int rc;

    /* Disconnect */
    rc = MqttClient_Disconnect_ex(&mqttCtx->client, &mqttCtx->disconnect);

    PRINTF("MQTT Disconnect: %s (%d)", MqttClient_ReturnCodeToString(rc), rc);
    if (rc != MQTT_CODE_SUCCESS) {
        printf("Main: failed disconnecting from MQTT broker\r");
        return rc;
    }

    rc = MqttClient_NetDisconnect(&mqttCtx->client);

    PRINTF("MQTT Socket Disconnect: %s (%d)", MqttClient_ReturnCodeToString(rc), rc);

    return rc;
}

static int send_msg(MQTTCtx *mqttCtx) {
    int rc;

    /* Publish Topic */
    XMEMSET(&mqttCtx->publish, 0, sizeof(MqttPublish));
    mqttCtx->publish.retain = 0;
    mqttCtx->publish.qos = mqttCtx->qos;
    mqttCtx->publish.duplicate = 0;
    mqttCtx->publish.topic_name = mqttCtx->topic_name;
    mqttCtx->publish.packet_id = mqtt_get_packetid();

    mqttCtx->publish.buffer = (byte *) mqttCtx->message;
    mqttCtx->publish.total_len = (word16) XSTRLEN(mqttCtx->message);

    /* This loop allows payloads larger than the buffer to be sent by
       repeatedly calling publish.
    */
    do {
        rc = MqttClient_Publish(&mqttCtx->client, &mqttCtx->publish);
    } while (rc == MQTT_CODE_PUB_CONTINUE);

    //TODO: added %s to print message for debugging. need to remove later.
    PRINTF("MQTT Publish: Topic %s, %s, %s (%d)",
           mqttCtx->publish.topic_name,
           mqttCtx->message,
           MqttClient_ReturnCodeToString(rc), rc);

    if (rc != MQTT_CODE_SUCCESS) {
        printf("Main: Failed publishing message to the broker\r");
        return FAILURE_CODE;
    }

    printf("Main: Successfully published message to the broker\r");
    return rc;
}

static void build_connect_packet(MQTTCtx *mqttCtx) {
    /* Build connect packet */
    XMEMSET(&mqttCtx->connect, 0, sizeof(MqttConnect));
    mqttCtx->connect.keep_alive_sec = mqttCtx->keep_alive_sec;
    mqttCtx->connect.clean_session = mqttCtx->clean_session;
    mqttCtx->connect.client_id = mqttCtx->client_id;
}

static void set_lwt(MQTTCtx *mqttCtx, int active, char *lwt_msg_buf, char *lwt_topic) {
    /* Last will and testament sent by broker to subscribers
    of topic when broker connection is lost */
    XMEMSET(&mqttCtx->lwt_msg, 0, sizeof(mqttCtx->lwt_msg));
    mqttCtx->enable_lwt = active;
    mqttCtx->connect.lwt_msg = &mqttCtx->lwt_msg;
    mqttCtx->connect.enable_lwt = mqttCtx->enable_lwt;

    if (mqttCtx->enable_lwt) {
        /* Send client id in LWT payload */
        mqttCtx->lwt_msg.qos = mqttCtx->qos;
        mqttCtx->lwt_msg.retain = FALSE;
        mqttCtx->lwt_msg.topic_name = lwt_topic;
        mqttCtx->lwt_msg.buffer = (byte *) lwt_msg_buf;
        mqttCtx->lwt_msg.total_len = (word16) XSTRLEN(lwt_msg_buf);
    }
}

static int subscribe(MQTTCtx *mqttCtx) {
    int rc, i;

    /* Build list of topics */
    XMEMSET(&mqttCtx->subscribe, 0, sizeof(MqttSubscribe));

    i = 0;
    mqttCtx->topics[i].topic_filter = mqttCtx->topic_name;
    mqttCtx->topics[i].qos = mqttCtx->qos;

    /* Subscribe Topic */
    mqttCtx->subscribe.packet_id = mqtt_get_packetid();
    mqttCtx->subscribe.topic_count =
            sizeof(mqttCtx->topics) / sizeof(MqttTopic);
    mqttCtx->subscribe.topics = mqttCtx->topics;

    rc = MqttClient_Subscribe(&mqttCtx->client, &mqttCtx->subscribe);

    PRINTF("MQTT Subscribe: %s (%d)",
           MqttClient_ReturnCodeToString(rc), rc);
    if (rc != MQTT_CODE_SUCCESS) {
        return rc;
    }

    /* show subscribe results */
    for (i = 0; i < mqttCtx->subscribe.topic_count; i++) {
        MqttTopic *topic = &mqttCtx->subscribe.topics[i];
        PRINTF("  Topic %s, Qos %u, Return Code %u",
               topic->topic_filter,
               topic->qos, topic->return_code);
    }

    return rc;
}

static int wait_for_message(MQTTCtx *mqttCtx) {
    int rc;

    /* Read Loop */
    PRINTF("MQTT Waiting for message...");

    do {
        /* Try and read packet */
        rc = MqttClient_WaitMessage(&mqttCtx->client,
                                    mqttCtx->cmd_timeout_ms);


        /* check return code */
        if (rc == MQTT_CODE_ERROR_TIMEOUT) {
            /* Keep Alive */
            PRINTF("Keep-alive timeout, sending ping");

            rc = MqttClient_Ping_ex(&mqttCtx->client, &mqttCtx->ping);
            if (rc != MQTT_CODE_SUCCESS) {
                PRINTF("MQTT Ping Keep Alive Error: %s (%d)",
                       MqttClient_ReturnCodeToString(rc), rc);
                break;
            }
        } else if (rc != MQTT_CODE_SUCCESS) {
            /* There was an error */
            PRINTF("MQTT Message Wait: %s (%d)",
                   MqttClient_ReturnCodeToString(rc), rc);
            break;
        } else if (rc == MQTT_CODE_SUCCESS) {
            PRINTF("MQTT Message Wait: %s (%d)",
                   MqttClient_ReturnCodeToString(rc), rc);
            break;
        }
    } while (1);

    return rc;
}

int main() {
    byte read_buffer[READ_BUFF_SIZE], write_buffer[WRITE_BUFF_SIZE];
    char msg[MSG_BUFF_SIZE], lwt_msg_buf[MSG_BUFF_SIZE];
    char second_msg_topic[TOPIC_BUFF_SIZE], lwt_topic[TOPIC_BUFF_SIZE], subscribe_id_topic[TOPIC_BUFF_SIZE];
    int rc;
    MQTTCtx mqttCtx;
    struct timespec spec;
    time_t s;  // Seconds

    printf("Main: Starting program\n");

    // Handle ^C
    signal(SIGINT, sig_handler); // Register signal handler

    /* init defaults */
    mqtt_init_ctx(&mqttCtx);
    mqttCtx.app_name = "mqttclient";

    PRINTF("MQTT Client: QoS %d, Use TLS %d", mqttCtx.qos, mqttCtx.use_tls);

    /* Initialize Network */
    rc = MqttClientNet_Init(&(mqttCtx.net), &mqttCtx);
    PRINTF("MQTT Net Init: %s (%d)", MqttClient_ReturnCodeToString(rc), rc);
    if (rc != MQTT_CODE_SUCCESS) {
        clean_network(&mqttCtx);
        return FAILURE_CODE;
    }

    /* setup tx/rx buffers */
    bzero(write_buffer, READ_BUFF_SIZE);
    bzero(read_buffer, WRITE_BUFF_SIZE);

    mqttCtx.tx_buf = write_buffer;
    mqttCtx.rx_buf = read_buffer;

    /* Initialize MqttClient structure */
    rc = MqttClient_Init(&mqttCtx.client, &mqttCtx.net,
                         mqtt_message_cb,
                         mqttCtx.tx_buf, WRITE_BUFF_SIZE,
                         mqttCtx.rx_buf, READ_BUFF_SIZE,
                         mqttCtx.cmd_timeout_ms);

    PRINTF("MQTT Init: %s (%d)", MqttClient_ReturnCodeToString(rc), rc);
    if (rc != MQTT_CODE_SUCCESS) {
        clean_network(&mqttCtx);
        return FAILURE_CODE;
    }

    /* The client.ctx will be stored in the cert callback ctx during
     * MqttSocket_Connect for use by mqtt_tls_verify_cb
     */
    mqttCtx.client.ctx = &mqttCtx;

    /* Connect to broker */
    rc = MqttClient_NetConnect(&mqttCtx.client, mqttCtx.host,
                               mqttCtx.port,
                               DEFAULT_CON_TIMEOUT_MS, mqttCtx.use_tls, NULL);

    PRINTF("MQTT Socket Connect: %s (%d)", MqttClient_ReturnCodeToString(rc), rc);
    if (rc != MQTT_CODE_SUCCESS) {
        clean_network(&mqttCtx);
        return FAILURE_CODE;
    }
    char* imei = get_imei();

    bzero(msg, MSG_BUFF_SIZE);
    if (sprintf(msg, default_mqtt_message, imei) < 0) {
        printf("Main: Failed assembling message\r");
        return FAILURE_CODE;
    }
    printf("message: %s\n", msg);

    build_connect_packet(&mqttCtx);

    /* Last will and testament */
    bzero(lwt_msg_buf, MSG_BUFF_SIZE);
    if (sprintf(lwt_msg_buf, end_message, "false") < 0) {
        printf("Main: Failed assembling message\r");
        return FAILURE_CODE;
    }

    bzero(lwt_topic, TOPIC_BUFF_SIZE);
    strcpy(lwt_topic, default_mqtt_topic);
    strcat(lwt_topic, "/");
    strcat(lwt_topic, imei);
    strcat(lwt_topic, "/");
    strcat(lwt_topic, mqtt_lwt_topic_suffix);

    set_lwt(&mqttCtx, TRUE, lwt_msg_buf, lwt_topic);

    /* Optional authentication */
    mqttCtx.connect.username = mqttCtx.username;
    mqttCtx.connect.password = mqttCtx.password;

    rc = MqttClient_Connect(&mqttCtx.client, &mqttCtx.connect);

    PRINTF("MQTT Connect: Proto (%s), %s (%d)",
           MqttClient_GetProtocolVersionString(&mqttCtx.client),
           MqttClient_ReturnCodeToString(rc), rc);
    if (rc != MQTT_CODE_SUCCESS) {
        printf("Main: Failed connecting to broker\r");
        disconnect(&mqttCtx);
        clean_network(&mqttCtx);
        return FAILURE_CODE;
    }

    /* Validate Connect Ack info */
    PRINTF("MQTT Connect Ack: Return Code %u, Session Present %d",
           mqttCtx.connect.ack.return_code,
           (mqttCtx.connect.ack.flags &
            MQTT_CONNECT_ACK_FLAG_SESSION_PRESENT) ?
           1 : 0
    );

    bzero(subscribe_id_topic, TOPIC_BUFF_SIZE);
    if (sprintf(subscribe_id_topic, subscribe_topic, imei) < 0) {
        printf("Main: Failed assembling topic\r");
        return FAILURE_CODE;
    }

    mqttCtx.topic_name = subscribe_id_topic;
    rc = subscribe(&mqttCtx);
    if (rc != MQTT_CODE_SUCCESS) {
        disconnect(&mqttCtx);
        clean_network(&mqttCtx);
        return FAILURE_CODE;
    }

    // msg 1 - general topic
    mqttCtx.topic_name = default_mqtt_topic;
    mqttCtx.message = msg;
    if (send_msg(&mqttCtx) < 0) {
        disconnect(&mqttCtx);
        clean_network(&mqttCtx);
        return FAILURE_CODE;
    }

    // msg 2 - specific topic
    char second_message[COPS_MESSAGE_LEN];
    if(create_cops_message(second_message, COPS_MESSAGE_LEN) == FAILURE_CODE)
    {
        return FAILURE_CODE;
    }
    bzero(second_msg_topic, TOPIC_BUFF_SIZE);
    strcpy(second_msg_topic, default_mqtt_topic);
    strcat(second_msg_topic, "/");
    strcat(second_msg_topic, imei);

    mqttCtx.message = second_message;
    mqttCtx.topic_name = second_msg_topic;
    if (send_msg(&mqttCtx) < 0) {
        disconnect(&mqttCtx);
        clean_network(&mqttCtx);
        return FAILURE_CODE;
    }

    bzero(msg, MSG_BUFF_SIZE);
    if (sprintf(msg, end_message, "true") < 0) {
        printf("Main: Failed assembling message\r");
        return FAILURE_CODE;
    }

    if (wait_for_message(&mqttCtx) < 0) {
        disconnect(&mqttCtx);
        clean_network(&mqttCtx);
        return FAILURE_CODE;
    }

    // msg 3 - end message
    mqttCtx.message = msg;
    mqttCtx.topic_name = lwt_topic;
    mqttCtx.return_code = send_msg(&mqttCtx);

    rc = disconnect(&mqttCtx);

    if (rc != MQTT_CODE_SUCCESS) {
        printf("Main: failed disconnecting from socket\r");
    }

    clean_network(&mqttCtx);

    printf("Main: Ending program\n");

    return rc;
}