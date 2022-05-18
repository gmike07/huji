cmake_minimum_required(VERSION 3.17.3)
project(IoT3 C)

set(CMAKE_C_STANDARD 99)

add_executable(IoT3 main.c serial_io.c)
