#include "serial_io.h"
#include <unistd.h>
#include <termios.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/select.h>
#include "global.h"

#define SEC_TO_MS_DIVIDER 1000
#define MS_TO_US_MULTIPLIER 1000

static int serialFd = -1;
static struct termios tty;

/**
 * This function translate each baud rate to it's struct.
 * @param baud Baud rate to translate.
 * @return The corresponding struct.
 */
speed_t baudToSpeedT(unsigned int baud)
{
    if (baud == 9600)
    {
        return B9600;
    }
    else if (baud == 19200)
    {
        return B19200;
    } else if (baud == 38400)
    {
        return B38400;
    } else if (baud == 57600)
    {
        return B57600;
    }
    else if (baud == 115200)
    {
        return B115200;
    }
    return -1;
}

/**
 * @brief Initialises the serial connection.
 * @param port - the port to connected to. e.g: /dev/ttyUSB0, /dev/ttyS1 for Linux and COM8, COM10, COM53 for Windows.
 * @param baud - the baud rate of the communication. For example: 9600, 115200
 * @return 0 if succeeded in opening the port and -1 otherwise.
 */
int SerialInit(char* port, unsigned int baud)
{
    serialFd = open(port, O_RDWR | O_NOCTTY | O_SYNC);
    if(serialFd < 0)
    {
        printf("Serial: Error %i from open: %s\n", errno, strerror(errno));
        return FAILURE_CODE;
    }

    if(tcgetattr(serialFd, &tty) != 0)
    {
        printf("Serial: Error %i from tcgetattr: %s\n", errno, strerror(errno));
        close(serialFd);
        serialFd = -1;
        return FAILURE_CODE;
    }

    tty.c_cflag &= ~(CSIZE | PARENB); // must clear to define bits per byte
    tty.c_cflag |= CS8; //define that we expect 8 bits per byte
    // can use CSTOPB if we want 2 bits to stop instead of 1
    // can use CRTSCTS to enable RTS/CTS hardware flow control (most common)
    tty.c_iflag &= ~(IGNBRK|BRKINT|PARMRK|ISTRIP|INLCR|IGNCR|ICRNL|IXON); // Disable any special handling of received byt
    tty.c_oflag &= ~OPOST; // Prevent special interpretation of output bytes (e.g. newline chars)
    tty.c_lflag &= ~ECHO; // Disable echo
    tty.c_lflag &= ~ECHONL; // Disable new-line echo
    tty.c_lflag &= ~ICANON; //disable canonical input
    tty.c_lflag &= ~ISIG; // Disable interpretation of INTR, QUIT and SUSP
    tty.c_lflag &= ~IEXTEN;

    cfsetispeed(&tty, baudToSpeedT(baud)); //set input speed
    cfsetospeed(&tty, baudToSpeedT(baud)); //set output speed

    if (tcsetattr(serialFd, TCSANOW, &tty) != 0)
    {
        printf("Serial: Error %i from tcsetattr: %s\n", errno, strerror(errno));
        close(serialFd);
        serialFd = -1;
        return FAILURE_CODE;
    }
    return SUCCESS_CODE;
}

/**
* @brief Sends data through the serial connection.
* @param buf - the buffer that contains the data to send
* @param size - number of bytes to send
* @return amount of bytes written into buf, -1 on error
*/
int SerialSend(unsigned char *buf, unsigned int size)
{
    printf("Serial: Starting SerialSend\n");
    int n = write(serialFd, buf, size);
    if (n < 0)
    {
        printf("Serial: Failed writing to serial\n");
        return FAILURE_CODE;
    }
    printf("Serial: Ending SerialSend\n");
    return n;
}

/**
 * @brief Empties the input buffer.
 */
void SerialFlushInputBuff(void)
{
    printf("Serial: Starting SerialFlushInputBuff\n");
    tcflush(serialFd, TCIFLUSH);
    printf("Serial: Ending SerialFlushInputBuff\n");
}

/**
 * @brief Disable the serial connection.
 * @return 0 if succeeded in closing the port and -1 otherwise.
 */
int SerialDisable(void)
{
    printf("Serial: Starting SerialDisable\n");
    SerialFlushInputBuff();
    int n = close(serialFd);
    serialFd = -1;
    if (n < 0)
    {
        printf("Serial: Failed closing serial\n");
        return FAILURE_CODE;
    }
    printf("Serial: Ending SerialDisable\n");
    return SUCCESS_CODE;
}


/**
 * @brief Receives data from serial connection.
 * @param buf - the buffer that receives the input.
 * @param max_len - maximum bytes to read into buf (buf must be equal or greater than max_len).
 * @param timeout_ms - read operation timeout milliseconds.
 * @return amount of bytes read into buf, -1 on error.
*/
int SerialRecv(unsigned char *buf, unsigned int max_len, unsigned int timeout_ms)
{
    printf("Serial: Starting SerialRecv\n");

    fd_set read_fds;
    struct timeval timeout;

    FD_ZERO(&read_fds);
    FD_SET(serialFd, &read_fds);

    timeout.tv_sec = timeout_ms / SEC_TO_MS_DIVIDER;
    timeout.tv_usec = (timeout_ms % SEC_TO_MS_DIVIDER) * MS_TO_US_MULTIPLIER;


    unsigned char* end_pointer = buf + max_len;
    unsigned char* start_pointer = buf;

    while(buf < end_pointer)
    {
        if(select(serialFd + 1, &read_fds, NULL, NULL, &timeout) <= 0)
        {
            printf("Serial: Timeout SerialRecv\n");
            return buf - start_pointer;
        }

        int r = read(serialFd, buf, end_pointer - buf);

        if(r < 0)
        {
            return r;
        }
        if(r == 0)
        {
            break;
        }
        buf += r;
    }

    printf("Serial: Ending SerialRecv\n");

    return buf - start_pointer;
}
