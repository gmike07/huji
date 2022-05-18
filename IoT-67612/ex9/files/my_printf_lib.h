
#ifndef MY_PRINTF_H
#define MY_PRINTF_H


/**
 * This function initialize everything to make this lib works.
 */
void my_printf_init();


/**
 * This function is exactly like the original "printf".
 * @param format Format to print, as given in printf.
 */
void my_printf(const char *format, ...);

/**
 * This function clear the screen.
 */
void my_printf_clear();

#endif
