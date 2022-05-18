#include "sl_iostream_usart_gps_config.h"
#include "sl_iostream_init_usart_instances.h"
#include "sl_iostream.h"
#include "sl_iostream_init_instances.h"
#include "sl_iostream_handles.h"
#include "sl_iostream_usart.h"
#include <stdbool.h>
#include <stdlib.h>
#include "minmea.h"
#define BUFF_SIZE 100

char buff[BUFF_SIZE];
char curr_index = 0;


void initGPS()
{
  sl_iostream_usart_init_gps();
}

void deInitGPS()
{
  sl_iostream_uart_deinit(sl_iostream_uart_gps_handle);
}

void getGPS(struct minmea_sentence_gga* gga, char* gga_msg)
{
  bool found_command = false;
  char c;
  int read;
  memset(buff, 0, BUFF_SIZE);
  while(found_command == false)
  {
      sl_iostream_read(sl_iostream_gps_handle, &c, 1, &read);
      if(read <= 0)
      {
        continue;
      }
      if(c == '$')
      {
          memset(buff, 0, BUFF_SIZE);
          curr_index = 0;
      }
      buff[curr_index] = c;
      curr_index++;
      if(c == '\n')
      {
          if(strstr(buff, "$GPGGA") != NULL)
          {
            found_command = true;
          }
      }
  }
  minmea_parse_gga(gga, buff);
  strcpy(gga_msg, buff);
  gga_msg[strlen(buff)-2] = '\0'; //remove \r\n
}
