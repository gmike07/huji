cmake_minimum_required(VERSION 3.20)
project(IoT4 C)

set(CMAKE_C_STANDARD 99)

add_executable(IoT4 main.c cellular.c serial_io_linux.c)
