cmake_minimum_required(VERSION 3.15)
project(IoT C)

set(CMAKE_C_STANDARD 99)
include_directories(.)
add_executable(IoT main.c
        socket_linux.c
        MQTTClient.c MQTTClient.h
        src/mqtt_client.c src/mqtt_packet.c src/mqtt_socket.c examples/mqttexample.c wolfmqtt)