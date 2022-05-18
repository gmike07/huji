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


/*******************************************************************************
 *******************************   DEFINES   ***********************************
 ******************************************************************************/
#ifndef BUTTON_INSTANCE_0
#define BUTTON_INSTANCE_0   sl_button_btn0
#endif

#ifndef BUTTON_INSTANCE_1
#define BUTTON_INSTANCE_1   sl_button_btn1
#endif

#define SEND_BUFFER_SIZE 500
#define TEN_SECONDS 10000
#define RECV_BUFF_SIZE 4096
#define MIN(x, y) (((x) < (y)) ? (x) : (y))
#define BAUD_RATE 115200
#define RECEIVE_WAIT_TIME 1
#define MSG_AFTER_10S "BTN0 was clicked %d times in last 10 seconds"
#define BTN1_MSG "number of clicks: %d\n"

/*******************************************************************************
 ***************************  LOCAL VARIABLES   ********************************
 ******************************************************************************/
static sl_sleeptimer_timer_handle_t timer;
static unsigned int num_of_times_clicked_btn0 = 0;

static int btn_0_interuppted = false;
static int btn_1_interuppted = false;
static int is_time_over = false;
static char recv_buff[RECV_BUFF_SIZE];
static char* buff_pointer;

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

static void on_10s_timeout(sl_sleeptimer_timer_handle_t *handle, void *data);
void sl_button_on_change(const sl_button_t *handle);
void handle_btn0_interrupt();
void handle_btn1_interrupt();
void handle_time_over();
void handleRecievedData();

/***************************************************************************//**
 * Initialize application.
 ******************************************************************************/
void app_init(void)
{
  sl_button_init(&sl_button_btn0);
  sl_button_init(&sl_button_btn1);
  SerialInit(NULL, BAUD_RATE);
  my_printf_init();

  memset(recv_buff, 0, RECV_BUFF_SIZE);
  buff_pointer = recv_buff;

    // Start 10 seconds timeout.
    sl_sleeptimer_start_periodic_timer_ms(&timer,
                                          TEN_SECONDS,
                                          on_10s_timeout,
                                              NULL,
                                              0,
                                              SL_SLEEPTIMER_NO_HIGH_PRECISION_HF_CLOCKS_REQUIRED_FLAG);


}

/***************************************************************************//**
 * App ticking function.
 ******************************************************************************/
void app_process_action(void)
{
   handle_btn0_interrupt();
   handle_btn1_interrupt();
   handle_time_over();
   handleRecievedData();
}


/***************************************************************************//**
 * Callback on button change.
 ******************************************************************************/
void sl_button_on_change(const sl_button_t *handle)
{
  if (sl_button_get_state(handle) == SL_SIMPLE_BUTTON_PRESSED) {
    if (&BUTTON_INSTANCE_0 == handle) {
        btn_0_interuppted = true;
    }
    if (&BUTTON_INSTANCE_1 == handle) {
        btn_1_interuppted = true;
    }
  }
}


/**
 * This function called after BTN0 is pressed.
 */
void handle_btn0_interrupt(){
  if (btn_0_interuppted == false){
        return;
  }
  num_of_times_clicked_btn0++;
  btn_0_interuppted = false;
}

/**
 * This function called after BTN1 is pressed.
 */
void handle_btn1_interrupt(){
  if (btn_1_interuppted == false){
      return;
  }
  char *msg_template = BTN1_MSG;
  char send_data[SEND_BUFFER_SIZE];
  sprintf(send_data, msg_template, num_of_times_clicked_btn0);
  SerialSend((unsigned char *)send_data, strlen(send_data) + 1);
  btn_1_interuppted = false;
}

/**
 * This function called after BTN1 is pressed.
 */
void handle_time_over(){
  if (is_time_over == false){
      return;
  }
  my_printf_clear();
  my_printf(MSG_AFTER_10S, num_of_times_clicked_btn0);
  num_of_times_clicked_btn0 = 0;
  is_time_over = false;
}


/**
 * This function handle the data that recived on the Serial, and print when needed.
 */
void handleRecievedData()
{
  int left_buff_size = RECV_BUFF_SIZE - (buff_pointer - recv_buff) - 1;
  int bytes_to_read = MIN(left_buff_size, NumOfBytesToRead());
  if(bytes_to_read <= 0)
  {
    return;
  }
  int bytes_read = SerialRecv((unsigned char *)buff_pointer, bytes_to_read, RECEIVE_WAIT_TIME);
  size_t string_size = strlen(buff_pointer);
  if((int) string_size >= bytes_read)
  {
    buff_pointer += bytes_read;
    return;
  }
  my_printf_clear();
  my_printf(recv_buff);
  int read_after_0 = bytes_read - (string_size + 1);
  buff_pointer += string_size + 1;
  memcpy(recv_buff, buff_pointer, read_after_0);
  memset(buff_pointer, 0, RECV_BUFF_SIZE - (buff_pointer - recv_buff)-1);
  buff_pointer = recv_buff + read_after_0;
}

/***************************************************************************//**
 * Sleeptimer timeout callback.
 ******************************************************************************/
static void on_10s_timeout(sl_sleeptimer_timer_handle_t *handle, void *data)
{
  (void)handle;
  (void)data;
  is_time_over = true;
}





