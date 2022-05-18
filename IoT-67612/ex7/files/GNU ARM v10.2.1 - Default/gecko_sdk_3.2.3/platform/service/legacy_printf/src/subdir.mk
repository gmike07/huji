################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../gecko_sdk_3.2.3/platform/service/legacy_printf/src/sl_legacy_printf.c 

OBJS += \
./gecko_sdk_3.2.3/platform/service/legacy_printf/src/sl_legacy_printf.o 

C_DEPS += \
./gecko_sdk_3.2.3/platform/service/legacy_printf/src/sl_legacy_printf.d 


# Each subdirectory must supply rules for building sources it contributes
gecko_sdk_3.2.3/platform/service/legacy_printf/src/sl_legacy_printf.o: ../gecko_sdk_3.2.3/platform/service/legacy_printf/src/sl_legacy_printf.c
	@echo 'Building file: $<'
	@echo 'Invoking: GNU ARM C Compiler'
	arm-none-eabi-gcc -g3 -gdwarf-2 -mcpu=cortex-m4 -mthumb -std=c99 '-DDEBUG_EFM=1' '-DEFM32PG12B500F1024GL125=1' '-DSL_COMPONENT_CATALOG_PRESENT=1' '-DCORTEXM3=1' '-DCORTEXM3_EFM32_MICRO=1' '-DCORTEXM3_EFR32=1' '-DPLATFORM_HEADER=<platform-header.h>' -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\gecko_sdk_3.2.3\platform\Device\SiliconLabs\EFM32PG12B\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\gecko_sdk_3.2.3\platform\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\gecko_sdk_3.2.3\hardware\board\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\gecko_sdk_3.2.3\platform\driver\button\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\gecko_sdk_3.2.3\platform\CMSIS\Include" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\gecko_sdk_3.2.3\platform\service\device_init\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\gecko_sdk_3.2.3\platform\emdrv\common\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\gecko_sdk_3.2.3\platform\emlib\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\gecko_sdk_3.2.3\platform\emdrv\gpiointerrupt\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\gecko_sdk_3.2.3\platform\driver\leddrv\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\gecko_sdk_3.2.3\platform\service\legacy_printf\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\gecko_sdk_3.2.3\platform\service\power_manager\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\gecko_sdk_3.2.3\platform\common\toolchain\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\gecko_sdk_3.2.3\platform\service\system\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\gecko_sdk_3.2.3\platform\service\sleeptimer\inc" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\autogen" -I"C:\Users\yuval\SimplicityStudio\v5_workspace\simple_button_baremetal\config" -Os -Wall -Wextra -fno-builtin -ffunction-sections -fdata-sections -imacrossl_gcc_preinclude.h -mfpu=fpv4-sp-d16 -mfloat-abi=softfp -c -fmessage-length=0 -MMD -MP -MF"gecko_sdk_3.2.3/platform/service/legacy_printf/src/sl_legacy_printf.d" -MT"gecko_sdk_3.2.3/platform/service/legacy_printf/src/sl_legacy_printf.o" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


