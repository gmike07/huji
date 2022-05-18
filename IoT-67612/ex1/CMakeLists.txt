cmake_minimum_required(VERSION 3.20)
project(ex1 C)

set(CMAKE_C_STANDARD 11)

include_directories(.)

add_executable(ex1
        HTTP_client.c
        HTTP_client.h
        main.c
        socket.c
        socket.h)
