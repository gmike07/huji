/***************************************************************************//**
 * @file
 * @brief Simple button baremetal examples functions
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

#include <ex7_lib.h>
#include "sl_simple_led_instances.h"
#include "sl_simple_button_instances.h"
#include "my_printf_lib.h"
#include "stdbool.h"
#include "sl_simple_led.h"
#include "sl_simple_led_instances.h"
#include "sl_sleeptimer.h"
#include <stdio.h>

/*******************************************************************************
 *******************************   DEFINES   ***********************************
 ******************************************************************************/

#ifndef BUTTON_INSTANCE_0
#define BUTTON_INSTANCE_0   sl_button_btn0
#endif

#ifndef LED_INSTANCE_0
#define LED_INSTANCE_0      sl_led_led0
#endif

#ifndef BUTTON_INSTANCE_1
#define BUTTON_INSTANCE_1   sl_button_btn1
#endif

#ifndef LED_INSTANCE_1
#define LED_INSTANCE_1      sl_led_led1
#endif

#ifndef TOOGLE_DELAY_MS
#define TOOGLE_DELAY_MS         500
#endif


#define DEFAULT_COUNTER 0
#define BTN0_COUNTER 1
#define BTN1_COUNTER 2
#define WAIT_TIME 20

/*******************************************************************************
 ***************************   VARIABLES   ********************************
 ******************************************************************************/
static int btn_0_interuppted = false;
static int btn_1_interuppted = false;
static sl_sleeptimer_timer_handle_t timer;
static bool toggle_timeout = false;
static int counter_btn0 = 0;
static int counter_btn1 = 0;
static int counter_default = 0;
static int timeout_caller = DEFAULT_COUNTER;

static const char *instruction_msg = "Insructions:\n"
    "BTN 0 - leds blinks.\n"
    "BTN 1 - HFXO value.";

static const char *num_of_blinks_msg = "counter leds: %d";

static const char *hfxo_msg = "HFXO: %lu";



/*******************************************************************************
 *********************   LOCAL FUNCTION PROTOTYPES   ***************************
 ******************************************************************************/

static void on_timeout(sl_sleeptimer_timer_handle_t *handle,
                       void *data);
int is_time_pass();
void handle_btn0_interrupt();
void handle_btn1_interrupt();

/**
 * This funcion print the instruction to the screen.
 */
static void print_instrutions()
{
  my_printf_clear();
  my_printf(instruction_msg);
}

/**
 * This functon initialize all variables of this lib.
 * @param caller The caller who call this: DEFAULT_COUNTER, BTN0_COUNTER, BTN1_COUNTER
 */
static inline void init_caller(int caller)
{
  timeout_caller = caller;
  counter_default = 0;
  counter_btn0 = 0;
  counter_btn1 = 0;
}

/**
 * This function check if the desired amount of time is passed. (10 sec in this exercise.)
 * @return
 */
int is_time_pass(){
  return counter_default >= WAIT_TIME || counter_btn0 >= WAIT_TIME || counter_btn1 >= WAIT_TIME;
}

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

/***************************************************************************//**
 * Initialize
 ******************************************************************************/

/**
 * This function initialize the lib.
 */
void ex7_lib_init(void)
{
  my_printf_init();
  init_caller(DEFAULT_COUNTER);
  print_instrutions();
  return;
}

/***************************************************************************//**
 * Ticking function.
 ******************************************************************************/

/**
 * This is the "main" function, which called every iteration.
 */
void ex7_process_action(void)
{
  if(is_time_pass())
  {
      print_instrutions();
      init_caller(DEFAULT_COUNTER);
      sl_sleeptimer_start_periodic_timer_ms(&timer,TOOGLE_DELAY_MS, on_timeout,
                                              NULL, 0,
                                              SL_SLEEPTIMER_NO_HIGH_PRECISION_HF_CLOCKS_REQUIRED_FLAG);
  }
  if (toggle_timeout == true && timeout_caller == BTN1_COUNTER) {
      if(counter_btn1 % 2 == 0)
      {
        sl_led_turn_on(&LED_INSTANCE_0);
        sl_led_turn_off(&LED_INSTANCE_1);
      }
      else
      {
          sl_led_turn_off(&LED_INSTANCE_0);
          sl_led_turn_on(&LED_INSTANCE_1);
      }

      my_printf_clear();
      my_printf(num_of_blinks_msg, counter_btn1);
      toggle_timeout = false;
    }

    handle_btn0_interrupt();
    handle_btn1_interrupt();
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
 * This function called after BTN1 is pressed.
 */
void handle_btn1_interrupt(){
  if (btn_1_interuppted != true){
      return;
  }
  init_caller(BTN1_COUNTER);
  toggle_timeout = true;
  sl_sleeptimer_start_periodic_timer_ms(&timer,TOOGLE_DELAY_MS, on_timeout,
                                        NULL, 0,
                                        SL_SLEEPTIMER_NO_HIGH_PRECISION_HF_CLOCKS_REQUIRED_FLAG);
  my_printf_clear();
  my_printf(num_of_blinks_msg, counter_btn1);
  btn_1_interuppted = false;
}


/**
 * This function called after BTN0 is pressed.
 */
void handle_btn0_interrupt(){
  if (btn_0_interuppted != true){
      return;
  }
  my_printf_clear();
  my_printf(hfxo_msg, SystemHFXOClockGet());
  btn_0_interuppted = false;

  init_caller(BTN0_COUNTER);

  sl_sleeptimer_start_periodic_timer_ms(&timer,TOOGLE_DELAY_MS, on_timeout,
                                        NULL, 0,
                                        SL_SLEEPTIMER_NO_HIGH_PRECISION_HF_CLOCKS_REQUIRED_FLAG);
}

/***************************************************************************//**
 * Sleeptimer timeout callback.
 ******************************************************************************/
static void on_timeout(sl_sleeptimer_timer_handle_t *handle,
                       void *data)
{
  (void)&handle;
  (void)&data;

  if(timeout_caller == DEFAULT_COUNTER)
  {
    counter_default++;
  }
  if(timeout_caller == BTN0_COUNTER)
  {
      counter_btn0++;
  }
  if(timeout_caller == BTN1_COUNTER)
  {
      toggle_timeout = true;
      counter_btn1++;
  }
}
