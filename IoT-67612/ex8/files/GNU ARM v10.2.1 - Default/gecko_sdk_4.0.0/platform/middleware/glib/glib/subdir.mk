################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../gecko_sdk_4.0.0/platform/middleware/glib/glib/bmp.c \
../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib.c \
../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_bitmap.c \
../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_circle.c \
../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_narrow_6x8.c \
../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_normal_8x8.c \
../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_number_16x20.c \
../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_line.c \
../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_polygon.c \
../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_rectangle.c \
../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_string.c 

OBJS += \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/bmp.o \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib.o \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_bitmap.o \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_circle.o \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_narrow_6x8.o \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_normal_8x8.o \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_number_16x20.o \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_line.o \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_polygon.o \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_rectangle.o \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_string.o 

C_DEPS += \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/bmp.d \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib.d \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_bitmap.d \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_circle.d \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_narrow_6x8.d \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_normal_8x8.d \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_number_16x20.d \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_line.d \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_polygon.d \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_rectangle.d \
./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_string.d 


# Each subdirectory must supply rules for building sources it contributes
gecko_sdk_4.0.0/platform/middleware/glib/glib/bmp.o: ../gecko_sdk_4.0.0/platform/middleware/glib/glib/bmp.c
	@echo 'Building file: $<'
	@echo 'Invoking: GNU ARM C Compiler'
	arm-none-eabi-gcc -g3 -gdwarf-2 -mcpu=cortex-m4 -mthumb -std=c99 '-DDEBUG_EFM=1' '-DEFM32PG12B500F1024GL125=1' '-DSL_BOARD_NAME="BRD2501A"' '-DSL_BOARD_REV="A02"' '-DSL_COMPONENT_CATALOG_PRESENT=1' -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\Device\SiliconLabs\EFM32PG12B\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\board\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\button\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\CMSIS\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\device_init\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\dmd" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emlib\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\gpiointerrupt\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\iostream\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\leddrv\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\src\ls013b7dh03" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc\memlcd_usart" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\power_manager\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\toolchain\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\system\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\sleeptimer\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\udelay\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\autogen" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\config" -Os -Wall -Wextra -fno-builtin -ffunction-sections -fdata-sections -imacrossl_gcc_preinclude.h -mfpu=fpv4-sp-d16 -mfloat-abi=softfp -c -fmessage-length=0 -MMD -MP -MF"gecko_sdk_4.0.0/platform/middleware/glib/glib/bmp.d" -MT"gecko_sdk_4.0.0/platform/middleware/glib/glib/bmp.o" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

gecko_sdk_4.0.0/platform/middleware/glib/glib/glib.o: ../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib.c
	@echo 'Building file: $<'
	@echo 'Invoking: GNU ARM C Compiler'
	arm-none-eabi-gcc -g3 -gdwarf-2 -mcpu=cortex-m4 -mthumb -std=c99 '-DDEBUG_EFM=1' '-DEFM32PG12B500F1024GL125=1' '-DSL_BOARD_NAME="BRD2501A"' '-DSL_BOARD_REV="A02"' '-DSL_COMPONENT_CATALOG_PRESENT=1' -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\Device\SiliconLabs\EFM32PG12B\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\board\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\button\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\CMSIS\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\device_init\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\dmd" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emlib\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\gpiointerrupt\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\iostream\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\leddrv\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\src\ls013b7dh03" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc\memlcd_usart" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\power_manager\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\toolchain\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\system\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\sleeptimer\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\udelay\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\autogen" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\config" -Os -Wall -Wextra -fno-builtin -ffunction-sections -fdata-sections -imacrossl_gcc_preinclude.h -mfpu=fpv4-sp-d16 -mfloat-abi=softfp -c -fmessage-length=0 -MMD -MP -MF"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib.d" -MT"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib.o" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_bitmap.o: ../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_bitmap.c
	@echo 'Building file: $<'
	@echo 'Invoking: GNU ARM C Compiler'
	arm-none-eabi-gcc -g3 -gdwarf-2 -mcpu=cortex-m4 -mthumb -std=c99 '-DDEBUG_EFM=1' '-DEFM32PG12B500F1024GL125=1' '-DSL_BOARD_NAME="BRD2501A"' '-DSL_BOARD_REV="A02"' '-DSL_COMPONENT_CATALOG_PRESENT=1' -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\Device\SiliconLabs\EFM32PG12B\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\board\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\button\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\CMSIS\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\device_init\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\dmd" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emlib\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\gpiointerrupt\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\iostream\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\leddrv\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\src\ls013b7dh03" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc\memlcd_usart" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\power_manager\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\toolchain\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\system\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\sleeptimer\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\udelay\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\autogen" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\config" -Os -Wall -Wextra -fno-builtin -ffunction-sections -fdata-sections -imacrossl_gcc_preinclude.h -mfpu=fpv4-sp-d16 -mfloat-abi=softfp -c -fmessage-length=0 -MMD -MP -MF"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_bitmap.d" -MT"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_bitmap.o" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_circle.o: ../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_circle.c
	@echo 'Building file: $<'
	@echo 'Invoking: GNU ARM C Compiler'
	arm-none-eabi-gcc -g3 -gdwarf-2 -mcpu=cortex-m4 -mthumb -std=c99 '-DDEBUG_EFM=1' '-DEFM32PG12B500F1024GL125=1' '-DSL_BOARD_NAME="BRD2501A"' '-DSL_BOARD_REV="A02"' '-DSL_COMPONENT_CATALOG_PRESENT=1' -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\Device\SiliconLabs\EFM32PG12B\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\board\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\button\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\CMSIS\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\device_init\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\dmd" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emlib\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\gpiointerrupt\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\iostream\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\leddrv\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\src\ls013b7dh03" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc\memlcd_usart" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\power_manager\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\toolchain\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\system\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\sleeptimer\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\udelay\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\autogen" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\config" -Os -Wall -Wextra -fno-builtin -ffunction-sections -fdata-sections -imacrossl_gcc_preinclude.h -mfpu=fpv4-sp-d16 -mfloat-abi=softfp -c -fmessage-length=0 -MMD -MP -MF"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_circle.d" -MT"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_circle.o" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_narrow_6x8.o: ../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_narrow_6x8.c
	@echo 'Building file: $<'
	@echo 'Invoking: GNU ARM C Compiler'
	arm-none-eabi-gcc -g3 -gdwarf-2 -mcpu=cortex-m4 -mthumb -std=c99 '-DDEBUG_EFM=1' '-DEFM32PG12B500F1024GL125=1' '-DSL_BOARD_NAME="BRD2501A"' '-DSL_BOARD_REV="A02"' '-DSL_COMPONENT_CATALOG_PRESENT=1' -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\Device\SiliconLabs\EFM32PG12B\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\board\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\button\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\CMSIS\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\device_init\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\dmd" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emlib\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\gpiointerrupt\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\iostream\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\leddrv\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\src\ls013b7dh03" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc\memlcd_usart" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\power_manager\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\toolchain\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\system\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\sleeptimer\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\udelay\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\autogen" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\config" -Os -Wall -Wextra -fno-builtin -ffunction-sections -fdata-sections -imacrossl_gcc_preinclude.h -mfpu=fpv4-sp-d16 -mfloat-abi=softfp -c -fmessage-length=0 -MMD -MP -MF"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_narrow_6x8.d" -MT"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_narrow_6x8.o" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_normal_8x8.o: ../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_normal_8x8.c
	@echo 'Building file: $<'
	@echo 'Invoking: GNU ARM C Compiler'
	arm-none-eabi-gcc -g3 -gdwarf-2 -mcpu=cortex-m4 -mthumb -std=c99 '-DDEBUG_EFM=1' '-DEFM32PG12B500F1024GL125=1' '-DSL_BOARD_NAME="BRD2501A"' '-DSL_BOARD_REV="A02"' '-DSL_COMPONENT_CATALOG_PRESENT=1' -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\Device\SiliconLabs\EFM32PG12B\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\board\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\button\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\CMSIS\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\device_init\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\dmd" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emlib\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\gpiointerrupt\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\iostream\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\leddrv\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\src\ls013b7dh03" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc\memlcd_usart" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\power_manager\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\toolchain\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\system\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\sleeptimer\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\udelay\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\autogen" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\config" -Os -Wall -Wextra -fno-builtin -ffunction-sections -fdata-sections -imacrossl_gcc_preinclude.h -mfpu=fpv4-sp-d16 -mfloat-abi=softfp -c -fmessage-length=0 -MMD -MP -MF"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_normal_8x8.d" -MT"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_normal_8x8.o" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_number_16x20.o: ../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_number_16x20.c
	@echo 'Building file: $<'
	@echo 'Invoking: GNU ARM C Compiler'
	arm-none-eabi-gcc -g3 -gdwarf-2 -mcpu=cortex-m4 -mthumb -std=c99 '-DDEBUG_EFM=1' '-DEFM32PG12B500F1024GL125=1' '-DSL_BOARD_NAME="BRD2501A"' '-DSL_BOARD_REV="A02"' '-DSL_COMPONENT_CATALOG_PRESENT=1' -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\Device\SiliconLabs\EFM32PG12B\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\board\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\button\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\CMSIS\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\device_init\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\dmd" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emlib\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\gpiointerrupt\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\iostream\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\leddrv\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\src\ls013b7dh03" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc\memlcd_usart" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\power_manager\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\toolchain\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\system\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\sleeptimer\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\udelay\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\autogen" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\config" -Os -Wall -Wextra -fno-builtin -ffunction-sections -fdata-sections -imacrossl_gcc_preinclude.h -mfpu=fpv4-sp-d16 -mfloat-abi=softfp -c -fmessage-length=0 -MMD -MP -MF"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_number_16x20.d" -MT"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_number_16x20.o" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_line.o: ../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_line.c
	@echo 'Building file: $<'
	@echo 'Invoking: GNU ARM C Compiler'
	arm-none-eabi-gcc -g3 -gdwarf-2 -mcpu=cortex-m4 -mthumb -std=c99 '-DDEBUG_EFM=1' '-DEFM32PG12B500F1024GL125=1' '-DSL_BOARD_NAME="BRD2501A"' '-DSL_BOARD_REV="A02"' '-DSL_COMPONENT_CATALOG_PRESENT=1' -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\Device\SiliconLabs\EFM32PG12B\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\board\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\button\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\CMSIS\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\device_init\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\dmd" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emlib\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\gpiointerrupt\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\iostream\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\leddrv\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\src\ls013b7dh03" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc\memlcd_usart" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\power_manager\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\toolchain\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\system\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\sleeptimer\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\udelay\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\autogen" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\config" -Os -Wall -Wextra -fno-builtin -ffunction-sections -fdata-sections -imacrossl_gcc_preinclude.h -mfpu=fpv4-sp-d16 -mfloat-abi=softfp -c -fmessage-length=0 -MMD -MP -MF"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_line.d" -MT"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_line.o" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_polygon.o: ../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_polygon.c
	@echo 'Building file: $<'
	@echo 'Invoking: GNU ARM C Compiler'
	arm-none-eabi-gcc -g3 -gdwarf-2 -mcpu=cortex-m4 -mthumb -std=c99 '-DDEBUG_EFM=1' '-DEFM32PG12B500F1024GL125=1' '-DSL_BOARD_NAME="BRD2501A"' '-DSL_BOARD_REV="A02"' '-DSL_COMPONENT_CATALOG_PRESENT=1' -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\Device\SiliconLabs\EFM32PG12B\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\board\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\button\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\CMSIS\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\device_init\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\dmd" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emlib\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\gpiointerrupt\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\iostream\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\leddrv\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\src\ls013b7dh03" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc\memlcd_usart" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\power_manager\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\toolchain\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\system\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\sleeptimer\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\udelay\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\autogen" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\config" -Os -Wall -Wextra -fno-builtin -ffunction-sections -fdata-sections -imacrossl_gcc_preinclude.h -mfpu=fpv4-sp-d16 -mfloat-abi=softfp -c -fmessage-length=0 -MMD -MP -MF"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_polygon.d" -MT"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_polygon.o" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_rectangle.o: ../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_rectangle.c
	@echo 'Building file: $<'
	@echo 'Invoking: GNU ARM C Compiler'
	arm-none-eabi-gcc -g3 -gdwarf-2 -mcpu=cortex-m4 -mthumb -std=c99 '-DDEBUG_EFM=1' '-DEFM32PG12B500F1024GL125=1' '-DSL_BOARD_NAME="BRD2501A"' '-DSL_BOARD_REV="A02"' '-DSL_COMPONENT_CATALOG_PRESENT=1' -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\Device\SiliconLabs\EFM32PG12B\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\board\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\button\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\CMSIS\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\device_init\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\dmd" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emlib\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\gpiointerrupt\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\iostream\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\leddrv\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\src\ls013b7dh03" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc\memlcd_usart" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\power_manager\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\toolchain\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\system\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\sleeptimer\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\udelay\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\autogen" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\config" -Os -Wall -Wextra -fno-builtin -ffunction-sections -fdata-sections -imacrossl_gcc_preinclude.h -mfpu=fpv4-sp-d16 -mfloat-abi=softfp -c -fmessage-length=0 -MMD -MP -MF"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_rectangle.d" -MT"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_rectangle.o" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_string.o: ../gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_string.c
	@echo 'Building file: $<'
	@echo 'Invoking: GNU ARM C Compiler'
	arm-none-eabi-gcc -g3 -gdwarf-2 -mcpu=cortex-m4 -mthumb -std=c99 '-DDEBUG_EFM=1' '-DEFM32PG12B500F1024GL125=1' '-DSL_BOARD_NAME="BRD2501A"' '-DSL_BOARD_REV="A02"' '-DSL_COMPONENT_CATALOG_PRESENT=1' -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\Device\SiliconLabs\EFM32PG12B\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\board\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\button\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\CMSIS\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\device_init\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\dmd" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emlib\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\middleware\glib\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\emdrv\gpiointerrupt\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\iostream\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\driver\leddrv\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\src\ls013b7dh03" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\hardware\driver\memlcd\inc\memlcd_usart" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\power_manager\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\common\toolchain\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\system\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\sleeptimer\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\gecko_sdk_4.0.0\platform\service\udelay\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\autogen" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex8\config" -Os -Wall -Wextra -fno-builtin -ffunction-sections -fdata-sections -imacrossl_gcc_preinclude.h -mfpu=fpv4-sp-d16 -mfloat-abi=softfp -c -fmessage-length=0 -MMD -MP -MF"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_string.d" -MT"gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_string.o" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


