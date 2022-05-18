#include "sonar_reader.h"
#include <stdbool.h>
#include <em_cmu.h>
#include <stdint.h>
#include "sl_sleeptimer.h"
#include "gpiointerrupt.h"
#include "ustimer.h"
#include "my_printf_lib.h"

#define TRIG_PORT           gpioPortC
#define TRIG_PIN            9
#define ECHO_PORT           gpioPortB
#define ECHO_PIN            6
#define ECHO_PIN_INTERRUPT  7

#define TIMEOUT_US 1000000
#define TIMEOUT_VALUE -1

#define SLEEP_BETWEEN_MEASURES_MS 200
#define NUM_OF_MEASURES 5





void initSonar()
{
  USTIMER_Init();
  CMU_ClockEnable(cmuClock_GPIO, true);
  GPIO_PinModeSet(TRIG_PORT, TRIG_PIN, gpioModePushPull, 0);
  GPIO_PinModeSet(ECHO_PORT, ECHO_PIN, gpioModeInput, 0);

  my_printf("end init Sonar\n");
}

void deInitSonar()
{
  CMU_ClockEnable(cmuClock_GPIO, false);
  USTIMER_DeInit();
}

void pulseTime(bool high, int time)
{
  if(high == true)
  {
      GPIO_PinOutSet(TRIG_PORT, TRIG_PIN);
  }
  else
  {
      GPIO_PinOutClear(TRIG_PORT, TRIG_PIN);
  }
  if(time > 0)
  {
    USTIMER_DelayIntSafe(time);
  }
}


int getSonarDistanaceOnce(){
    unsigned int echo_pulse_time = 0;
    unsigned int echo_wait_time = 0;
    //send LOW
    pulseTime(false, 2);

    //send HIGH
    pulseTime(true, 10);

    //send LOW
    pulseTime(false, -1);
    while(GPIO_PinInGet(ECHO_PORT, ECHO_PIN) == 0)
    {
        ++echo_wait_time;
        if (echo_wait_time > TIMEOUT_US){
                   return TIMEOUT_VALUE; // Error: Timeout
        }
    }

    while(GPIO_PinInGet(ECHO_PORT, ECHO_PIN) == 1)
      {
          USTIMER_DelayIntSafe(10);
          echo_pulse_time += 10;
          if (echo_pulse_time > TIMEOUT_US){
              return TIMEOUT_VALUE; // Error: Timeout
          }
      }

    return echo_pulse_time / 58;
}

void sort(int values[], int length){
  int i, j, min_idx, temp;
  for (i = 0; i < length - 1; i++) {

      // Find the minimum element in unsorted array
      min_idx = i;
      for (j = i + 1; j < length; j++)
          if (values[j] < values[min_idx])
              min_idx = j;

      // Swap the found minimum element
      // with the first element
      temp = values[min_idx];
      values[min_idx] = values[i];
      values[i] = temp;
  }
}

int findMedian(int values[], int length){
  sort(values, length);
  return values[length/2];
}

int getSonarDistance()
{
  int all_measures[NUM_OF_MEASURES];

  for(int i = 0; i < NUM_OF_MEASURES; ++i){
      all_measures[i] = getSonarDistanaceOnce();
      sl_sleeptimer_delay_millisecond(SLEEP_BETWEEN_MEASURES_MS);
  }

  return findMedian(all_measures, NUM_OF_MEASURES);
}

