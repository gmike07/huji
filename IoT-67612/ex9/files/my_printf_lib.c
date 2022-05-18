/*
 * my_printf_lib.c
 *
 *  Created on: 13 בדצמ׳ 2021
 *      Author: yuval
 */
#include "my_printf_lib.h"
#include <stdio.h>
#include <string.h>
#include "sl_board_control.h"
#include "em_assert.h"
#include "glib.h"
#include "dmd.h"
#include <stdarg.h>
#include "stdbool.h"

#define LINE_WIDTH 120
#define LINE_HEIGHT 120
#define BUFF_SIZE 1024

static int x = 0;
static int y = 0;
static int line_height = 0;
static int char_width = 0;
static GLIB_Context_t glibContext;
static char buff[BUFF_SIZE];

void printf_helper(const char* str, bool retry);

/**
 * This function initialize everything to make this lib works.
 */
void my_printf_init(){

  uint32_t status;

    /* Enable the memory lcd */
    status = sl_board_enable_display();
    EFM_ASSERT(status == SL_STATUS_OK);

    /* Initialize the DMD support for memory lcd display */
    status = DMD_init(0);
    EFM_ASSERT(status == DMD_OK);

    /* Initialize the glib context */
    status = GLIB_contextInit(&glibContext);
    EFM_ASSERT(status == GLIB_OK);

    glibContext.backgroundColor = White;
    glibContext.foregroundColor = Black;

    /* Fill lcd with background color */
    GLIB_clear(&glibContext);

    /* Use Narrow font */
    GLIB_setFont(&glibContext, (GLIB_Font_t *) &GLIB_FontNarrow6x8);

    line_height = glibContext.font.fontHeight + glibContext.font.lineSpacing;
    char_width = glibContext.font.fontWidth + glibContext.font.charSpacing;

    my_printf_clear();
}

/**
 * This function clear the screen.
 */
void my_printf_clear()
{
  GLIB_clear(&glibContext);
  x = y = 0;
  DMD_updateDisplay();
}

/**
 * This function is exactly like the original "printf".
 * @param format Format to print, as given in printf.
 */
void my_printf(const char *format, ...)
{
  va_list args;
  va_start(args, format);
  bzero(buff, BUFF_SIZE);
  if(vsprintf(buff, format, args) < 0)
  {
    return;
  }
  printf_helper(buff, true);
}


/**
 * Helper function to my_printf.
 * @param str String to print.
 * @param retry is need to try print again.
 */
void printf_helper(const char* str, bool retry)
{
  for(size_t i = 0; i < strlen(str); i++)
  {
      if(str[i] == '\n')
      {
          y += line_height;
          x = 0;
          continue;
      }
      GLIB_drawChar(&glibContext, str[i], x, y, true);
      x += char_width;
      if(x > LINE_WIDTH)
      {
          y += line_height;
          x = 0;
      }
      if(y > LINE_HEIGHT && retry)
      {
          my_printf_clear();
          printf_helper(str, false);
          return;
      }
  }
  DMD_updateDisplay();
}
