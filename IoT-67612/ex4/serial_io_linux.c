#include "serial_io.h"

#include <stdio.h>
#include <fcntl.h>      /* File Control Definitions            */
#include <termios.h>    /* POSIX Terminal Control Definitions  */
#include <unistd.h>     /* UNIX Standard Definitions 	       */
#include <stdlib.h>
#include <string.h>     /* string function definitions         */

#define RECV_BUFFER_SIZE 256

int g_fd; // File Descriptor

/**
 * @brief Initialises the serial connection.
 * @param port - the port to connected to. e.g: /dev/ttyUSB0, /dev/ttyS1 for Linux.
 * @param baud - the baud rate of the communication. For example: 9600, 115200
 * @return 0 if succeeded in opening the port and -1 otherwise.
 */
int SerialInit(char *port, unsigned int baud) {
    speed_t structured_baud;
    struct termios SerialPortSettings;

    // Opening a Serial Port

    g_fd = open(port, O_RDWR | O_NOCTTY);   // O_RDWR   - Read/Write access to serial port.
    // O_NOCTTY - No terminal will control the process of opening the serial
    // port. The port is open in blocking mode, read will wait.

    if (g_fd == -1) {
        return -1;
    }

    // Configuring the termios structure

    // configure the mode, baud rate, data format, number of start/stop bits etc.
    // In Linux it is done by a structure called termios.

    /*
     * struct termios
     * {
     *      tcflag_t c_iflag; // input mode flags
     *      tcflag_t c_oflag; // output mode flags
     *      tcflag_t c_cflag; // control mode flags
     *      tcflag_t c_lflag; // local mode flags
     *      cc_t c_line;      // line discipline
     *      cc_t c_cc[NCCS];  // control characters
     * };
     */

    // get the current settings of the serial port
    tcgetattr(g_fd, &SerialPortSettings);

    // Setting the baud rate
    switch (baud) {
        case 9600:
            structured_baud = B9600;
            break;
        case 19200:
            structured_baud = B19200;
            break;
        case 38400:
            structured_baud = B38400;
            break;
        case 57600:
            structured_baud = B57600;
            break;
        case 115200:
            structured_baud = B115200;
            break;
        default:
            close(g_fd); // Close the serial port
            return -1;
    }

    cfsetispeed(&SerialPortSettings, structured_baud); // set the input speed or read speed
    cfsetospeed(&SerialPortSettings, structured_baud); // set the output speed or write speed

    // The control flags (c_cflag) of the termios structure configures the data format (8 or 7 bits for data),
    // parity (Even, Odd, None) and the number of start and stop bits to use while communicating.
    // Configuring these information involves setting and clearing individual bits of the control flags.

    SerialPortSettings.c_iflag &= ~(IGNBRK | BRKINT | PARMRK | ISTRIP
                                    | INLCR | IGNCR | ICRNL | IXON);
    SerialPortSettings.c_oflag &= ~OPOST;
    SerialPortSettings.c_lflag &= ~(ECHO | ECHONL | ICANON | ISIG | IEXTEN);
    SerialPortSettings.c_cflag &= ~(CSIZE | PARENB);
    SerialPortSettings.c_cflag |= CS8;

    // Set the attributes to the termios structure. TCSANOW applies the changes now without waiting
    if ((tcsetattr(g_fd, TCSANOW, &SerialPortSettings)) != 0) {
        close(g_fd); // Close the serial port
        return -1;
    }

    // Pay attention that tcflush may not work right after open. See stackoverflow for more details
    // https://stackoverflow.com/questions/13013387/clearing-the-serial-ports-buffer
    tcflush(g_fd, TCIFLUSH); // Discards old data in the rx buffer

    return 0;
}

/**
 * @brief Receives data from serial connection.
 * @param buf - the buffer that receives the input.
 * @param max_len - maximum bytes to read into buf (buf must be equal or greater than max_len).
 * @param timeout_ms - read operation timeout milliseconds.
 * @return amount of bytes read into buf, -1 on error.
*/
int SerialRecv(unsigned char *buf, unsigned int max_len, unsigned int timeout_ms) {
    int sel_res;
    unsigned char recv_buf[RECV_BUFFER_SIZE];
    unsigned int read_count, bytes_read = 0, read_res = 0;
    fd_set set;
    struct timeval timeout;

    FD_ZERO(&set); // clear the set
    FD_SET(g_fd, &set); // add our file descriptor to the set

    // Set the timeout struct
    // timeout_ms is used for every select. If we want to use something a bit more precise, we should count ticks
    // and before every select call, reduce the time passed from the previous select call to the new call
    timeout.tv_sec = 0;
    timeout.tv_usec = timeout_ms * 1000; // shortcut, use only usec instead of dividing into sec and usec

    // Read RECV_BUFFER_SIZE char at a time until we see a nl (set VEOL in termios if another EOL is needed
    do {
        sel_res = select(g_fd + 1, &set, NULL, NULL, &timeout);

        memset(recv_buf, 0, RECV_BUFFER_SIZE);
        if ((max_len - bytes_read) > RECV_BUFFER_SIZE) {
            read_count = RECV_BUFFER_SIZE;
        } else {
            read_count = max_len - bytes_read;
        }

        if (sel_res > 0) {
            read_res = read(g_fd, &recv_buf, read_count);
            if (read_res > 0) {
                memcpy(buf + bytes_read, recv_buf, read_res);
                bytes_read += read_res;
            }
        }
    } while (sel_res > 0 && read_res > 0 && bytes_read < max_len);

    return bytes_read;
}

/**
 * @brief Sends data through the serial connection.
 * @param buf - the buffer that contains the data to send
 * @param size - number of bytes to send
 * @return amount of bytes written into buf, -1 on error
 */
int SerialSend(unsigned char *buf, unsigned int size) {
    int bytes_written;
    bytes_written = write(g_fd, buf, size);

    return bytes_written;
}

/**
 * @brief Empties the input buffer.
 */
void SerialFlushInputBuff(void) {
    tcflush(g_fd, TCIFLUSH);   // Discards old data in the rx buffer
}

/**
 * @brief Disable the serial connection.
 * @return 0 if succeeded in closing the port and -1 otherwise.
 */
int SerialDisable(void) {
    tcflush(g_fd, TCIFLUSH);   // Discards old data in the rx buffer
    close(g_fd);
    return 0;
}