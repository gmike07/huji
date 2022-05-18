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

#include "my_printf_lib.h"
#include "sl_sleeptimer.h"
#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include "em_cmu.h"
#include "gps/minmea.h"
#include "em_system.h"
#include <inttypes.h>


/*******************************************************************************
 *******************************   DEFINES   ***********************************
 ******************************************************************************/
#define MILLION 1000000.0
#define CYCLE_TIME_MS 900000
#define MINUTE_IN_MS 60000
#define MINUTE_TO_WAIT 1
/*******************************************************************************
 ***************************  LOCAL VARIABLES   ********************************
 ******************************************************************************/
bool needToCalculateData = true;
uint64_t uniqId;
static sl_sleeptimer_timer_handle_t timer;
struct minmea_sentence_gga gga;
char gga_msg[100];
char* format_mqtt_msg = "{\n"
                        "\"id\":\"%u\",\n"
                        "\"lat\":\"%d\",\n"
                        "\"lat_scale\":\"%d\",\n"
                        "\"long\":\"%d\",\n"
                        "\"long_scale\":\"%d\",\n"
                        "\"distance\":\"%d\",\n"
                        "\"gps_msg\":\"%s\"\n"
                        "}";
char mqtt_msg[1024];
/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/
int minutes_passed = 0;
uint32_t MINUTE_IN_TICKS;

/***************************************************************************//**
 * Initialize application.
 ******************************************************************************/
void app_init(void)
{
  my_printf_init();
  initSonar();
  initGPS();
  uniqId = SYSTEM_GetUnique();
  MINUTE_IN_TICKS = sl_sleeptimer_ms_to_tick(MINUTE_IN_MS);

  needToCalculateData = true;
  my_printf("Say hello to SmarTrash!\n");

}

static void on_timeout(sl_sleeptimer_timer_handle_t *handle,
                       void *data)
{
  (void) handle;
  (void) data;
  minutes_passed++;
  if (minutes_passed >= MINUTE_TO_WAIT){
      needToCalculateData = true;
      minutes_passed = 0;
  }
  sl_sleeptimer_stop_timer(&timer);
}

/***************************************************************************//**
 * App ticking function.
 ******************************************************************************/

void app_process_action(void)
{

  if(needToCalculateData)
  {
      my_printf("Read GPS data.\n");
      getGPS(&gga, gga_msg);
      my_printf("Read sonar distance.\r\n");
      int distance = getSonarDistance();
      my_printf("Generate final message.\r\n");
      sprintf(mqtt_msg, format_mqtt_msg, (unsigned int)uniqId, gga.latitude.value,
          gga.latitude.scale, gga.longitude.value, gga.longitude.scale,
          distance, gga_msg);
      my_printf("%s\n", mqtt_msg);

      sl_sleeptimer_delay_millisecond(2000);
      my_printf("Send final message.\r\n");
      int status = send_mqtt(mqtt_msg);
      needToCalculateData = false;
      my_printf_clear();

      my_printf("Sleeping for %u Minutes.\n", MINUTE_TO_WAIT);
      sl_sleeptimer_start_timer(&timer,
                                MINUTE_IN_TICKS,
                                on_timeout,
                                NULL,
                                0,
                                SL_SLEEPTIMER_NO_HIGH_PRECISION_HF_CLOCKS_REQUIRED_FLAG);

  }
}



