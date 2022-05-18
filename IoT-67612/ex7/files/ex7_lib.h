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

#ifndef EX7_LIB_H
#define EX7_LIB_H

/***************************************************************************//**
 * Initialize example
 ******************************************************************************/

/**
 * This function initialize the lib.
 */
void ex7_lib_init(void);

/***************************************************************************//**
 * ticking function
 ******************************************************************************/

/**
 * This is the "main" function, which called every iteration.
 */
void ex7_process_action(void);

#endif  // SIMPLE_BUTTON_BAREMETAL_H
