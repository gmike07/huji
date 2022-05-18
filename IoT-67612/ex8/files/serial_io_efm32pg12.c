/*
 * serial_io_efm32pg12.c
 *
 *  Created on: 20 בדצמ׳ 2021
 *      Author: yuval
 */

#include "serial_io.h"
#include "sl_sleeptimer.h"
#include "global.h"
#include <stdio.h>
#include <string.h>
#include "em_chip.h"
#include "my_printf_lib.h"
#include <stdbool.h>
#include "sl_iostream_init_usart_instances.h"
#include "sl_iostream.h"
#include "sl_iostream_init_instances.h"
#include "sl_iostream_handles.h"
#include "sl_iostream_usart.h"


#if defined(SL_COMPONENT_CATALOG_PRESENT)
#include "sl_component_catalog.h"
#endif
#if defined(SL_CATALOG_POWER_MANAGER_PRESENT)
#include "sl_power_manager.h"
#endif
#include "em_device.h"
#include "sl_iostream.h"
#include "sl_iostream_uart.h"
#include "sl_iostream_usart.h"
// Include instance config
 #include "sl_iostream_usart_vcom_config.h"

#define BUFF_SIZE 4096
static sl_iostream_usart_context_t context_vcom;

static uint8_t buff[BUFF_SIZE];
/*******************************************************************************
 *******************************   DEFINES   ***********************************
 ******************************************************************************/

/*******************************************************************************
 ***************************   VARIABLES   ********************************
 ******************************************************************************/
static sl_sleeptimer_timer_handle_t timer;
int is_time_out_passed = false;

static void on_timeout(sl_sleeptimer_timer_handle_t *handle, void *data);
static void init_sl(unsigned int baud);
/**
 * @brief Initialises the serial connection.
 * @param port - the port to connected to. e.g: /dev/ttyUSB0, /dev/ttyS1 for Linux and COM8, COM10, COM53 for Windows.
 * @param baud - the baud rate of the communication. For example: 9600, 115200
 * @return 0 if succeeded in opening the port and -1 otherwise.
 */
int SerialInit(char* port, unsigned int baud){
  (void)port;
  init_sl(baud);
  return SUCCESS_CODE;

}

/**
 * @brief Receives data from serial connection.
 * @param buf - the buffer that receives the input.
 * @param max_len - maximum bytes to read into buf (buf must be equal or greater than max_len).
 * @param timeout_ms - read operation timeout milliseconds.
 * @return amount of bytes read into buf, -1 on error.
*/
int SerialRecv(unsigned char *buf, unsigned int max_len, unsigned int timeout_ms){
//  my_printf("Serial: Starting SerialRecv\n");
  is_time_out_passed = false;
  unsigned int num_of_readen_bytes = 0;
  sl_sleeptimer_start_periodic_timer_ms(&timer,
                                        timeout_ms,
                                        on_timeout,
                                          NULL,
                                          0,
                                          SL_SLEEPTIMER_NO_HIGH_PRECISION_HF_CLOCKS_REQUIRED_FLAG);

  unsigned char* end_pointer = buf + max_len;
  unsigned char* start_pointer = buf;

  size_t r;
  while (!is_time_out_passed && num_of_readen_bytes <= max_len){
      sl_iostream_read(sl_iostream_vcom_handle, buf, end_pointer - buf, &r);
      buf += r;
  }
  sl_sleeptimer_stop_timer(&timer);
//  my_printf("Serial: Ending SerialRecv\n");
  return buf - start_pointer;
}

/**
 * @brief Sends data through the serial connection.
 * @param buf - the buffer that contains the data to send
 * @param size - number of bytes to send
 * @return amount of bytes written into buf, -1 on error
 */
int SerialSend(unsigned char *buf, unsigned int size){
//    my_printf("Serial: Starting SerialSend\n");
      sl_iostream_write(sl_iostream_vcom_handle, buf, size);
//     my_printf("Serial: Ending SerialSend\n");
      return size;
}

/**
 * @brief Empties the input buffer.
 */
void SerialFlushInputBuff(void){
  sl_iostream_usart_context_t *context = (sl_iostream_usart_context_t*) sl_iostream_uart_vcom_handle->stream.context;
  context->context.rx_read_index = 0;
  context->context.rx_write_index = 0;
  context->context.rx_count = 0;
}

/**
 * @brief Disable the serial connection.
 * @return 0 if succeeded in closing the port and -1 otherwise.
 */
int SerialDisable(void){
  if(sl_iostream_uart_deinit(sl_iostream_uart_vcom_handle) == SL_STATUS_OK){
      return SUCCESS_CODE;
  }
  else{
      return FAILURE_CODE;
  }
}




/***************************************************************************//**
 * Sleeptimer timeout callback.
 ******************************************************************************/
static void on_timeout(sl_sleeptimer_timer_handle_t *handle,
                       void *data)
{
  (void) handle;
  (void) data;
  is_time_out_passed = true;
}

int NumOfBytesToRead()
{
  sl_iostream_usart_context_t *context = (sl_iostream_usart_context_t*) sl_iostream_uart_vcom_handle->stream.context;
  return context->context.rx_count;
}



/***************************************************************************//**
 * Trash code. dont touch this, better left hidden
 ******************************************************************************/

// MACROs for generating name and IRQ handler function
#define SL_IOSTREAM_USART_CONCAT_PASTER(first, second, third)        first ##  second ## third




#define SL_IOSTREAM_USART_TX_IRQ_NUMBER(periph_nbr)     SL_IOSTREAM_USART_CONCAT_PASTER(USART, periph_nbr, _TX_IRQn)
#define SL_IOSTREAM_USART_RX_IRQ_NUMBER(periph_nbr)     SL_IOSTREAM_USART_CONCAT_PASTER(USART, periph_nbr, _RX_IRQn)
#define SL_IOSTREAM_USART_TX_IRQ_HANDLER(periph_nbr)    SL_IOSTREAM_USART_CONCAT_PASTER(USART, periph_nbr, _TX_IRQHandler)
#define SL_IOSTREAM_USART_RX_IRQ_HANDLER(periph_nbr)    SL_IOSTREAM_USART_CONCAT_PASTER(USART, periph_nbr, _RX_IRQHandler)

#define SL_IOSTREAM_USART_CLOCK_REF(periph_nbr)         SL_IOSTREAM_USART_CONCAT_PASTER(cmuClock_, USART, periph_nbr)




static void init_sl(unsigned int baud)
{
#if defined(SL_CATALOG_POWER_MANAGER_PRESENT) &&  defined(_SILICON_LABS_32B_SERIES_2)
  // Enable power manager notifications
  sl_power_manager_subscribe_em_transition_event(&events_handle, &events_info);
#endif
  sl_status_t status;
  USART_InitAsync_TypeDef init_vcom = USART_INITASYNC_DEFAULT;
  init_vcom.baudrate = baud;
  init_vcom.parity = SL_IOSTREAM_USART_VCOM_PARITY;
  init_vcom.stopbits = SL_IOSTREAM_USART_VCOM_STOP_BITS;
#if (_SILICON_LABS_32B_SERIES > 0)
#if (SL_IOSTREAM_USART_VCOM_FLOW_CONTROL_TYPE != uartFlowControlSoftware)
  init_vcom.hwFlowControl = SL_IOSTREAM_USART_VCOM_FLOW_CONTROL_TYPE;
#else
  init_vcom.hwFlowControl = usartHwFlowControlNone;
#endif
#endif
  sl_iostream_usart_config_t config_vcom = {
    .usart = SL_IOSTREAM_USART_VCOM_PERIPHERAL,
    .clock = SL_IOSTREAM_USART_CLOCK_REF(SL_IOSTREAM_USART_VCOM_PERIPHERAL_NO),
    .tx_port = SL_IOSTREAM_USART_VCOM_TX_PORT,
    .tx_pin = SL_IOSTREAM_USART_VCOM_TX_PIN,
    .rx_port = SL_IOSTREAM_USART_VCOM_RX_PORT,
    .rx_pin = SL_IOSTREAM_USART_VCOM_RX_PIN,
#if (_SILICON_LABS_32B_SERIES > 0)
#if defined(SL_IOSTREAM_USART_VCOM_CTS_PORT)
    .cts_port = SL_IOSTREAM_USART_VCOM_CTS_PORT,
    .cts_pin = SL_IOSTREAM_USART_VCOM_CTS_PIN,
#endif
#if defined(SL_IOSTREAM_USART_VCOM_RTS_PORT)
    .rts_port = SL_IOSTREAM_USART_VCOM_RTS_PORT,
    .rts_pin = SL_IOSTREAM_USART_VCOM_RTS_PIN,
#endif
#endif
#if defined(GPIO_USART_ROUTEEN_TXPEN)
    .usart_index = SL_IOSTREAM_USART_VCOM_PERIPHERAL_NO,
#elif defined(USART_ROUTEPEN_RXPEN)
    .usart_tx_location = SL_IOSTREAM_USART_VCOM_TX_LOC,
    .usart_rx_location = SL_IOSTREAM_USART_VCOM_RX_LOC,
#if defined(SL_IOSTREAM_USART_VCOM_CTS_PORT)
    .usart_cts_location = SL_IOSTREAM_USART_VCOM_CTS_LOC,
#endif
#if defined(SL_IOSTREAM_USART_VCOM_RTS_PORT)
    .usart_rts_location = SL_IOSTREAM_USART_VCOM_RTS_LOC,
#endif
#else
    .usart_location = SL_IOSTREAM_USART_VCOM_ROUTE_LOC,
#endif
  };
  sl_iostream_uart_config_t uart_config_vcom = {
    .tx_irq_number = SL_IOSTREAM_USART_TX_IRQ_NUMBER(SL_IOSTREAM_USART_VCOM_PERIPHERAL_NO),
    .rx_irq_number = SL_IOSTREAM_USART_RX_IRQ_NUMBER(SL_IOSTREAM_USART_VCOM_PERIPHERAL_NO),
    .rx_buffer = buff,
    .rx_buffer_length = BUFF_SIZE,
    .lf_to_crlf = SL_IOSTREAM_USART_VCOM_CONVERT_BY_DEFAULT_LF_TO_CRLF,
    .rx_when_sleeping = SL_IOSTREAM_USART_VCOM_RESTRICT_ENERGY_MODE_TO_ALLOW_RECEPTION,
#if defined(SL_IOSTREAM_USART_VCOM_FLOW_CONTROL_TYPE)
#if (SL_IOSTREAM_USART_VCOM_FLOW_CONTROL_TYPE == uartFlowControlSoftware)
    .sw_flow_control = true,
#else
    .sw_flow_control = false,
#endif
#else
    .sw_flow_control = false,
#endif
  };
  // Instantiate usart instance
  status = sl_iostream_usart_init(sl_iostream_uart_vcom_handle,
                                  &uart_config_vcom,
                                  &init_vcom,
                                  &config_vcom,
                                  &context_vcom);
  EFM_ASSERT(status == SL_STATUS_OK);
}





