cmake_minimum_required(VERSION 3.17.3)
project(IoT6 C)

set(CMAKE_C_STANDARD 99)


add_executable(IoT6

        main.c

        wolfmqtt/mqtt_client.h
        wolfmqtt/mqtt_client.c
        wolfmqtt/mqtt_packet.h
        wolfmqtt/mqtt_packet.c
        wolfmqtt/mqtt_socket.h
        wolfmqtt/mqtt_socket.c
        wolfmqtt/mqtt_types.h
        wolfmqtt/visibility.h
        wolfmqtt/options.h

        cellular.c
        serial_io_linux.c
        socket_linux_modem.c
        cellular_common.c
        cellular_parse_operators.c
        cellular_parse_physical.c
        utils.c
        global.h
        MQTTClient.c
        MQTTClient.h

        serial_io.h
        socket.h
        test_cellular.c
        test_cellular.h
        cellular_internet.c
        cellular_internet.h
        )
