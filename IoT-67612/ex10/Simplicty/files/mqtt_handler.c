#include <stdio.h>
#include <string.h>
#include "MQTTClient.h"
#include "global.h"
#include "cellular.h"
#include "utils.h"
#include "my_printf_lib.h"

static char default_mqtt_host[] = "broker.mqttdashboard.com"; //"3.65.154.195";
static char default_mqtt_client_id[] = "Grades for Ex4 in Huji IoT? Mike \\ Yuval";

static char default_mqtt_topic[] = "huji_iot_class/2021_2022/smarTrash";

static int is_cellular_initialized = FALSE;

static volatile word16 mPacketIdLast;


#define READ_BUFF_SIZE 2048
#define WRITE_BUFF_SIZE 2048
#define MSG_BUFF_SIZE 2048
#define TOPIC_BUFF_SIZE 64
#define ID_BUFF_SIZE 20
#define MSG_ITEM_BUFF_SIZE 512
#define MSG_ARRAY_BUFF_SIZE 2048

#define DEFAULT_MQTT_QOS 1
#define DEFAULT_KEEP_ALIVE_SEC 60
#define DEFAULT_CMD_TIMEOUT_MS  10000
#define DEFAULT_CON_TIMEOUT_MS  5000

#define CELLULAR_PORT "/dev/ttyS0"
#define NUM_OF_OPERATORS 30

static byte read_buffer[READ_BUFF_SIZE], write_buffer[WRITE_BUFF_SIZE];
static char lwt_msg_buf[MSG_BUFF_SIZE];
static char  lwt_topic[TOPIC_BUFF_SIZE];
static char id[ID_BUFF_SIZE];

static OPERATOR_INFO ops[NUM_OF_OPERATORS] = { 0 };
static char msg_item[MSG_ITEM_BUFF_SIZE] = { 0 };
static char msg_array[MSG_ARRAY_BUFF_SIZE] = { 0 };

#undef PRINTF
#define PRINTF(_f_, ...)  my_printf( (_f_ LINE_END), ##__VA_ARGS__)

static word16 mqtt_get_packetid(void)
{
    /* Check rollover */
    if (mPacketIdLast >= MAX_PACKET_ID) {
        mPacketIdLast = 0;
    }

    return ++mPacketIdLast;
}

static void mqtt_init_ctx(MQTTCtx* mqttCtx)
{
    XMEMSET(mqttCtx, 0, sizeof(MQTTCtx));
    mqttCtx->host = default_mqtt_host;
    mqttCtx->qos = DEFAULT_MQTT_QOS;
    mqttCtx->clean_session = 0;
    mqttCtx->keep_alive_sec = DEFAULT_KEEP_ALIVE_SEC;
    mqttCtx->client_id = default_mqtt_client_id;
    mqttCtx->topic_name = default_mqtt_topic;
    mqttCtx->cmd_timeout_ms = DEFAULT_CMD_TIMEOUT_MS;
}

static int mqtt_message_cb(MqttClient *client, MqttMessage *msg,
                           byte msg_new, byte msg_done)
{
    byte buf[MSG_BUFF_SIZE+1];
    word32 len;
    MQTTCtx* mqttCtx = (MQTTCtx*)client->ctx;

    (void)mqttCtx;

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

static void clean_network(MQTTCtx *mqttCtx)
{
    int rc;

    /* Cleanup network */
    rc = MqttClientNet_DeInit(&mqttCtx->net);
    if (rc != MQTT_CODE_SUCCESS) {
        PRINTF("Main: Failed cleaning network resources\n");
        return;
    }

    MqttClient_DeInit(&mqttCtx->client);
}

static int disconnect(MQTTCtx *mqttCtx)
{
    int rc;

    /* Disconnect */
    rc = MqttClient_Disconnect_ex(&mqttCtx->client, &mqttCtx->disconnect);

    PRINTF("MQTT Disconnect: %s (%d)", MqttClient_ReturnCodeToString(rc), rc);
    if (rc != MQTT_CODE_SUCCESS) {
        PRINTF("Main: failed disconnecting from MQTT broker\r");
        return rc;
    }

    rc = MqttClient_NetDisconnect(&mqttCtx->client);

    PRINTF("MQTT Socket Disconnect: %s (%d)", MqttClient_ReturnCodeToString(rc), rc);

    return rc;
}

static int send_msg(MQTTCtx *mqttCtx)
{
    int rc;

    /* Publish Topic */
    XMEMSET(&mqttCtx->publish, 0, sizeof(MqttPublish));
    mqttCtx->publish.retain = 0;
    mqttCtx->publish.qos = mqttCtx->qos;
    mqttCtx->publish.duplicate = 0;
    mqttCtx->publish.topic_name = mqttCtx->topic_name;
    mqttCtx->publish.packet_id = mqtt_get_packetid();

    mqttCtx->publish.buffer = (byte*)mqttCtx->message;
    mqttCtx->publish.total_len = (word16)XSTRLEN(mqttCtx->message);

    /* This loop allows payloads larger than the buffer to be sent by
       repeatedly calling publish.
    */
    do {
        rc = MqttClient_Publish(&mqttCtx->client, &mqttCtx->publish);
    } while(rc == MQTT_CODE_PUB_CONTINUE);


    PRINTF("MQTT Publish: Topic %s, %s (%d)",
           mqttCtx->publish.topic_name,
           MqttClient_ReturnCodeToString(rc), rc);

    if (rc != MQTT_CODE_SUCCESS) {
        PRINTF("Main: Failed publishing message to the broker\r");
        return FAILURE_CODE;
    }

    PRINTF("Main: Successfully published message to the broker\r");
    return rc;
}

static void build_connect_packet(MQTTCtx *mqttCtx)
{
    /* Build connect packet */
    XMEMSET(&mqttCtx->connect, 0, sizeof(MqttConnect));
    mqttCtx->connect.keep_alive_sec = mqttCtx->keep_alive_sec;
    mqttCtx->connect.clean_session = mqttCtx->clean_session;
    mqttCtx->connect.client_id = mqttCtx->client_id;
}

static void set_lwt(MQTTCtx *mqttCtx, int active, char *lwt_msg_buf, char *lwt_topic)
{
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

static int subscribe(MQTTCtx *mqttCtx)
{
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

static int wait_for_message(MQTTCtx *mqttCtx)
{
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
        }
        else if (rc != MQTT_CODE_SUCCESS) {
            /* There was an error */
            PRINTF("MQTT Message Wait: %s (%d)",
                   MqttClient_ReturnCodeToString(rc), rc);
            break;
        }
        else if (rc == MQTT_CODE_SUCCESS) {
            PRINTF("MQTT Message Wait: %s (%d)",
                   MqttClient_ReturnCodeToString(rc), rc);
            break;
        }
    } while (1);

    return rc;
}

int get_identifier(char* id, int maxlen)
{
    if (CellularInit(CELLULAR_PORT) != SUCCESS_CODE)
    {
        CellularDisable();
        return FALSE;
    }

    if (CellularWaitUntilModemResponds() != SUCCESS_CODE)
    {
        CellularDisable();
        return FALSE;
    }

    if (CellularGetIMEI(id, maxlen) != SUCCESS_CODE)
    {
        CellularDisable();
        return FALSE;
    }

    is_cellular_initialized = TRUE;

    return TRUE;
}

int send_mqtt(char* publish_msg)
{
    int rc;
    MQTTCtx mqttCtx;

    PRINTF("Main: Starting program\n");

    memset(id, 0, ID_BUFF_SIZE);
    if (!get_identifier(id, ID_BUFF_SIZE - 1))
    {
        PRINTF("Main: Failed getting id\n");
        return FAILURE_CODE;
    }

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

    build_connect_packet(&mqttCtx);

    set_lwt(&mqttCtx, FALSE, lwt_msg_buf, lwt_topic);

    /* Optional authentication */
    mqttCtx.connect.username = mqttCtx.username;
    mqttCtx.connect.password = mqttCtx.password;

    rc = MqttClient_Connect(&mqttCtx.client, &mqttCtx.connect);

    PRINTF("MQTT Connect: Proto (%s), %s (%d)",
           MqttClient_GetProtocolVersionString(&mqttCtx.client),
           MqttClient_ReturnCodeToString(rc), rc);
    if (rc != MQTT_CODE_SUCCESS) {
        PRINTF("Main: Failed connecting to broker\n");
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

    // msg 1 - general topic
    mqttCtx.topic_name = default_mqtt_topic;
    mqttCtx.message = publish_msg;
    if (send_msg(&mqttCtx) < 0)
    {
        disconnect(&mqttCtx);
        clean_network(&mqttCtx);
        return FAILURE_CODE;
    }

    rc = disconnect(&mqttCtx);

    if (rc != MQTT_CODE_SUCCESS) {
        PRINTF("Main: failed disconnecting from socket\n");
    }

    clean_network(&mqttCtx);

    PRINTF("Main: Ending program\n");

    return rc;
}
