################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../gecko_sdk_3.2.3/platform/emdrv/gpiointerrupt/src/gpiointerrupt.c 

OBJS += \
./gecko_sdk_3.2.3/platform/emdrv/gpiointerrupt/src/gpiointerrupt.o 

C_DEPS += \
./gecko_sdk_3.2.3/platform/emdrv/gpiointerrupt/src/gpiointerrupt.d 


# Each subdirectory must supply rules for building sources it contributes
gecko_sdk_3.2.3/platform/emdrv/gpiointerrupt/src/gpiointerrupt.o: ../gecko_sdk_3.2.3/platform/emdrv/gpiointerrupt/src/gpiointerrupt.c
	@echo 'Building file: $<'
	@echo 'Invoking: GNU ARM C Compiler'
	arm-none-eabi-gcc -g3 -gdwarf-2 -mcpu=cortex-m4 -mthumb -std=c99 '-DDEBUG_EFM=1' '-DEFM32PG12B500F1024GL125=1' '-DSL_COMPONENT_CATALOG_PRESENT=1' '-DRTT_USE_ASM=0' '-DSEGGER_RTT_SECTION="SEGGER_RTT"' '-DRESPONSE_PRINT_USE_LOCAL_CONFIG_HEADER=1' -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\Device\SiliconLabs\EFM32PG12B\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\hardware\board\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\driver\button\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\CMSIS\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\driver\debug\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\service\device_init\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\middleware\glib\dmd" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\middleware\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\emdrv\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\emlib\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\middleware\glib\glib" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\emdrv\gpiointerrupt\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\service\iostream\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\driver\leddrv\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\hardware\driver\memlcd\src\ls013b7dh03" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\hardware\driver\memlcd\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\hardware\driver\memlcd\inc\memlcd_usart" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\service\power_manager\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\util\third_party\printf" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\util\third_party\printf\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\util\third_party\segger\systemview\SEGGER" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\util\silicon_labs\silabs_core\response_print" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\common\toolchain\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\service\system\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\service\sleeptimer\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\gecko_sdk_3.2.3\platform\service\udelay\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\autogen" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\ex7\config" -Os -Wall -Wextra -fno-builtin -ffunction-sections -fdata-sections -imacrossl_gcc_preinclude.h -mfpu=fpv4-sp-d16 -mfloat-abi=softfp -c -fmessage-length=0 -MMD -MP -MF"gecko_sdk_3.2.3/platform/emdrv/gpiointerrupt/src/gpiointerrupt.d" -MT"gecko_sdk_3.2.3/platform/emdrv/gpiointerrupt/src/gpiointerrupt.o" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


