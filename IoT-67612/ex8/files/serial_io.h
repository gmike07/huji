/*
 * serial_io_efm32pg12.h
 *
 *  Created on: 20 בדצמ׳ 2021
 *      Author: yuval
 */

#ifndef SERIAL_IO_H_
#define SERIAL_IO_H_


/**
 * @brief Initialises the serial connection.
 * @param port - the port to connected to. e.g: /dev/ttyUSB0, /dev/ttyS1 for Linux and COM8, COM10, COM53 for Windows.
 * @param baud - the baud rate of the communication. For example: 9600, 115200
 * @return 0 if succeeded in opening the port and -1 otherwise.
 */
int SerialInit(char* port, unsigned int baud);

/**
 * @brief Receives data from serial connection.
 * @param buf - the buffer that receives the input.
 * @param max_len - maximum bytes to read into buf (buf must be equal or greater than max_len).
 * @param timeout_ms - read operation timeout milliseconds.
 * @return amount of bytes read into buf, -1 on error.
*/
int SerialRecv(unsigned char *buf, unsigned int max_len, unsigned int timeout_ms);

/**
 * @brief Sends data through the serial connection.
 * @param buf - the buffer that contains the data to send
 * @param size - number of bytes to send
 * @return amount of bytes written into buf, -1 on error
 */
int SerialSend(unsigned char *buf, unsigned int size);

/**
 * @brief Empties the input buffer.
 */
void SerialFlushInputBuff(void);

/**
 * @brief Disable the serial connection.
 * @return 0 if succeeded in closing the port and -1 otherwise.
 */
int SerialDisable(void);

int NumOfBytesToRead();


#endif /* SERIAL_IO_H_ */
