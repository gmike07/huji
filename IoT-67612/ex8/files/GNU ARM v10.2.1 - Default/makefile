################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include gecko_sdk_4.0.0/platform/service/udelay/src/subdir.mk
-include gecko_sdk_4.0.0/platform/service/system/src/subdir.mk
-include gecko_sdk_4.0.0/platform/service/sleeptimer/src/subdir.mk
-include gecko_sdk_4.0.0/platform/service/power_manager/src/subdir.mk
-include gecko_sdk_4.0.0/platform/service/iostream/src/subdir.mk
-include gecko_sdk_4.0.0/platform/service/device_init/src/subdir.mk
-include gecko_sdk_4.0.0/platform/middleware/glib/glib/subdir.mk
-include gecko_sdk_4.0.0/platform/middleware/glib/dmd/display/subdir.mk
-include gecko_sdk_4.0.0/platform/emlib/src/subdir.mk
-include gecko_sdk_4.0.0/platform/emdrv/gpiointerrupt/src/subdir.mk
-include gecko_sdk_4.0.0/platform/driver/leddrv/src/subdir.mk
-include gecko_sdk_4.0.0/platform/driver/button/src/subdir.mk
-include gecko_sdk_4.0.0/platform/common/toolchain/src/subdir.mk
-include gecko_sdk_4.0.0/platform/common/src/subdir.mk
-include gecko_sdk_4.0.0/platform/Device/SiliconLabs/EFM32PG12B/Source/GCC/subdir.mk
-include gecko_sdk_4.0.0/platform/Device/SiliconLabs/EFM32PG12B/Source/subdir.mk
-include gecko_sdk_4.0.0/hardware/driver/memlcd/src/memlcd_usart/subdir.mk
-include gecko_sdk_4.0.0/hardware/driver/memlcd/src/subdir.mk
-include gecko_sdk_4.0.0/hardware/board/src/subdir.mk
-include autogen/subdir.mk
-include subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 

# All Target
all: ex8.axf

# Tool invocations
ex8.axf: $(OBJS) $(USER_OBJS)
	@echo 'Building target: $@'
	@echo 'Invoking: GNU ARM C Linker'
	arm-none-eabi-gcc -g3 -gdwarf-2 -mcpu=cortex-m4 -mthumb -T "C:\Users\yuval\SimplicityStudio\v5_workspace\ex8/autogen/linkerfile.ld" -Xlinker --gc-sections -Xlinker -Map="ex8.map" -mfpu=fpv4-sp-d16 -mfloat-abi=softfp --specs=nano.specs -o ex8.axf -Wl,--start-group "./app.o" "./main.o" "./my_printf_lib.o" "./serial_io_efm32pg12.o" "./autogen/sl_board_default_init.o" "./autogen/sl_device_init_clocks.o" "./autogen/sl_event_handler.o" "./autogen/sl_iostream_handles.o" "./autogen/sl_iostream_init_usart_instances.o" "./autogen/sl_power_manager_handler.o" "./autogen/sl_simple_button_instances.o" "./autogen/sl_simple_led_instances.o" "./gecko_sdk_4.0.0/hardware/board/src/sl_board_control_gpio.o" "./gecko_sdk_4.0.0/hardware/board/src/sl_board_init.o" "./gecko_sdk_4.0.0/hardware/driver/memlcd/src/memlcd_usart/sl_memlcd_spi.o" "./gecko_sdk_4.0.0/hardware/driver/memlcd/src/sl_memlcd.o" "./gecko_sdk_4.0.0/hardware/driver/memlcd/src/sl_memlcd_display.o" "./gecko_sdk_4.0.0/platform/Device/SiliconLabs/EFM32PG12B/Source/GCC/startup_efm32pg12b.o" "./gecko_sdk_4.0.0/platform/Device/SiliconLabs/EFM32PG12B/Source/system_efm32pg12b.o" "./gecko_sdk_4.0.0/platform/common/src/sl_slist.o" "./gecko_sdk_4.0.0/platform/common/toolchain/src/sl_memory.o" "./gecko_sdk_4.0.0/platform/driver/button/src/sl_button.o" "./gecko_sdk_4.0.0/platform/driver/button/src/sl_simple_button.o" "./gecko_sdk_4.0.0/platform/driver/leddrv/src/sl_led.o" "./gecko_sdk_4.0.0/platform/driver/leddrv/src/sl_simple_led.o" "./gecko_sdk_4.0.0/platform/emdrv/gpiointerrupt/src/gpiointerrupt.o" "./gecko_sdk_4.0.0/platform/emlib/src/em_assert.o" "./gecko_sdk_4.0.0/platform/emlib/src/em_cmu.o" "./gecko_sdk_4.0.0/platform/emlib/src/em_core.o" "./gecko_sdk_4.0.0/platform/emlib/src/em_emu.o" "./gecko_sdk_4.0.0/platform/emlib/src/em_gpio.o" "./gecko_sdk_4.0.0/platform/emlib/src/em_rtcc.o" "./gecko_sdk_4.0.0/platform/emlib/src/em_system.o" "./gecko_sdk_4.0.0/platform/emlib/src/em_usart.o" "./gecko_sdk_4.0.0/platform/middleware/glib/dmd/display/dmd_memlcd.o" "./gecko_sdk_4.0.0/platform/middleware/glib/glib/bmp.o" "./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib.o" "./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_bitmap.o" "./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_circle.o" "./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_narrow_6x8.o" "./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_normal_8x8.o" "./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_font_number_16x20.o" "./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_line.o" "./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_polygon.o" "./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_rectangle.o" "./gecko_sdk_4.0.0/platform/middleware/glib/glib/glib_string.o" "./gecko_sdk_4.0.0/platform/service/device_init/src/sl_device_init_dcdc_s1.o" "./gecko_sdk_4.0.0/platform/service/device_init/src/sl_device_init_emu_s1.o" "./gecko_sdk_4.0.0/platform/service/device_init/src/sl_device_init_hfxo_s1.o" "./gecko_sdk_4.0.0/platform/service/device_init/src/sl_device_init_lfxo_s1.o" "./gecko_sdk_4.0.0/platform/service/device_init/src/sl_device_init_nvic.o" "./gecko_sdk_4.0.0/platform/service/iostream/src/sl_iostream.o" "./gecko_sdk_4.0.0/platform/service/iostream/src/sl_iostream_uart.o" "./gecko_sdk_4.0.0/platform/service/iostream/src/sl_iostream_usart.o" "./gecko_sdk_4.0.0/platform/service/power_manager/src/sl_power_manager.o" "./gecko_sdk_4.0.0/platform/service/power_manager/src/sl_power_manager_debug.o" "./gecko_sdk_4.0.0/platform/service/power_manager/src/sl_power_manager_hal_s0_s1.o" "./gecko_sdk_4.0.0/platform/service/sleeptimer/src/sl_sleeptimer.o" "./gecko_sdk_4.0.0/platform/service/sleeptimer/src/sl_sleeptimer_hal_rtcc.o" "./gecko_sdk_4.0.0/platform/service/system/src/sl_system_init.o" "./gecko_sdk_4.0.0/platform/service/system/src/sl_system_process_action.o" "./gecko_sdk_4.0.0/platform/service/udelay/src/sl_udelay.o" "./gecko_sdk_4.0.0/platform/service/udelay/src/sl_udelay_armv6m_gcc.o" -lgcc -lc -lm -lnosys -Wl,--end-group -Wl,--start-group -lgcc -lc -lnosys -Wl,--end-group
	@echo 'Finished building target: $@'
	@echo ' '

	@echo 'Building hex file: ex8.hex'
	arm-none-eabi-objcopy -O ihex "ex8.axf" "ex8.hex"
	@echo ' '

	@echo 'Building bin file: ex8.bin'
	arm-none-eabi-objcopy -O binary "ex8.axf" "ex8.bin"
	@echo ' '

	@echo 'Building s37 file: ex8.s37'
	arm-none-eabi-objcopy -O srec "ex8.axf" "ex8.s37"
	@echo ' '

	@echo 'Running size tool'
	arm-none-eabi-size "ex8.axf" -A
	@echo ' '

# Other Targets
clean:
	-@$(foreach FILE, $(EXECUTABLES), $(shell $(RM) $(FILE)) )
	-@$(foreach FILE, $(OBJS), $(shell $(RM) $(FILE)) )
	-@$(foreach FILE, $(C_DEPS), $(shell $(RM) $(FILE)) )
	-$(RM) ex8.axf
	-@echo ' '

.PHONY: all clean dependents

-include ../makefile.targets
