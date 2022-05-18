#include "test_cellular.h"
#include "cellular_common.h"
#include <string.h>

char *test_cops_1 =
        "\r\n+COPS: (3,\"\",\"\",\"42507\",2),(1,\"JAWWAL-PALESTINE\",\"JAWWAL\",\"42505\",0),"
        "(1,\"Orange IL\",\"OrangeIL\",\"42501\",0),(3,\"Wataniya Mobile\",\"WM\",\"42506\",2),"
        "(1,\"Cellcom IL\",\"Cellcom\",\"42502\",0),(1,\"Orange IL\",\"OrangeIL\",\"42501\",2),"
        "(3,\"Wataniya Mobile\",\"WM\",\"42506\",0),(1,\"JAWWAL-PALESTINE\",\"JAWWAL\",\"42505\",2),"
        "(1,\"Cellcom IL\",\"Cellcom\",\"42502\",2),(2,\"IL Pelephone\",\"PCL\",\"42503\",2)\r\n\r\nOK\r\n";

char *test_cops_2 =
        "\r\n+COPS: ,,(0,1,2,3,4),(0,1,2,90,91)\r\n\r\nOK\r\n";

char *test_cops_3 =
        "";

int SendCmdRecvResp_TestCops_1(unsigned char *cmd, unsigned char *resp_buf, unsigned int resp_max_size, unsigned int timeout_ms)
{
    memset(serial_buf, 0, resp_max_size);
    strcpy(serial_buf, test_cops_1);
    return strlen(test_cops_1);
}

int SendCmdRecvResp_TestCops_2(unsigned char *cmd, unsigned char *resp_buf, unsigned int resp_max_size, unsigned int timeout_ms)
{
    memset(serial_buf, 0, resp_max_size);
    strcpy(serial_buf, test_cops_2);
    return strlen(test_cops_2);
}

int SendCmdRecvResp_TestCops_3(unsigned char *cmd, unsigned char *resp_buf, unsigned int resp_max_size, unsigned int timeout_ms)
{
    memset(serial_buf, 0, resp_max_size);
    strcpy(serial_buf, test_cops_3);
    return strlen(test_cops_3);
}