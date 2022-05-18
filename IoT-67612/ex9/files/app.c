/***************************************************************************//**
 * @file
 * @brief Top level application functions
 *******************************************************************************
 * # License
 * <b>Copyright 2020 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * The licensor of this software is Silicon Laboratories Inc. Your use of this
 * software is governed by the terms of Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * www.silabs.com/about-us/legal/master-software-license-agreement. This
 * software is distributed to you in Source Code format and is governed by the
 * sections of the MSLA applicable to Source Code.
 *
 ******************************************************************************/

#include "sl_simple_led_instances.h"
#include "sl_simple_button_instances.h"
#include "my_printf_lib.h"
#include "sl_sleeptimer.h"
#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include "serial_io.h"
#include "global.h"
#include "mqtt_handler.h"
#include"cellular_common.h"

#define COM_PORT "/dev/ttyS0"
#define cmd_CFUN "AT+CFUN=1,1\r\n"

static char inner_serial_buf[SHORT_RESPONSE_BUF_SIZE];

/*******************************************************************************
 *******************************   DEFINES   ***********************************
 ******************************************************************************/

/*******************************************************************************
 ***************************  LOCAL VARIABLES   ********************************
 ******************************************************************************/
static int sent_mqtt = FAILURE_CODE;

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

/***************************************************************************//**
 * Initialize application.
 ******************************************************************************/
void app_init(void)
{
  my_printf_init();
}

/***************************************************************************//**
 * App ticking function.
 ******************************************************************************/
static int clear_modem()
{
  if (CellularInit(COM_PORT) < 0)
  {
      return FAILURE_CODE;
  }

  if (CellularWaitUntilModemResponds() < 0)
  {
      return FAILURE_CODE;
  }

  int n = SendCmdRecvResp(cmd_CFUN, inner_serial_buf, SHORT_RESPONSE_BUF_SIZE, SHORT_TIMEOUT);

  if (n <= 0 || !HasOK(inner_serial_buf))
  {
      my_printf("Cellular CFUN: Not OK response received. Received: %s\n", inner_serial_buf);
      return FAILURE_CODE;
  }
  return SUCCESS_CODE;
}


void app_process_action(void)
{
  if(sent_mqtt == FAILURE_CODE)
  {
     sent_mqtt = send_mqtt();
     if(sent_mqtt == FAILURE_CODE)
     {
       clear_modem();
     }

  }
}


/***************************************************************************//**
 * Callback on button change.
 ******************************************************************************/

/***************************************************************************//**
 * Sleeptimer timeout callback.
 ******************************************************************************/




