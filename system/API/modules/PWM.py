# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		PWM.py
# Description:		Provides functions for interacting with PCA9685.

from smbus2 import SMBus
from enum import Enum
from typing import Dict, List

# Motor locations
class Motor(Enum) :
	UPPER_LEFT = 0
	UPPER_MIDDLE = 1
	UPPER_RIGHT = 2
	MIDDLE_LEFT = 3
	MIDDLE = 4
	MIDDLE_RIGHT = 5
	LOWER_LEFT = 6
	LOWER_MIDDLE = 7
	LOWER_RIGHT = 8

# All for OFF. ON default of 0 is acceptable
class _Registers(Enum) :
	LED0_L = 0x08
	LED0 = 0x09
	LED1_L = 0x0c
	LED1 = 0x0d
	LED2_L = 0x10
	LED2 = 0x11
	LED3_L = 0x14
	LED3 = 0x15
	LED4_L = 0x18
	LED4 = 0x19
	LED5_L = 0x1c
	LED5 = 0x1d
	LED6_L = 0x20
	LED6 = 0x21
	LED7_L = 0x24
	LED7 = 0x25
	LED8_L = 0x28
	LED8 = 0x29
	MODE1 = 0x00

class PWM :

	# Index 0 maps to OFF_H, index 1 maps to OFF_L
	LocationRegisterMap : Dict[int, List[_Registers]] = \
		{
			Motor.UPPER_LEFT.value : [_Registers.LED0, _Registers.LED0_L],
			Motor.UPPER_MIDDLE.value : [_Registers.LED1, _Registers.LED1_L],
			Motor.UPPER_RIGHT.value : [_Registers.LED2, _Registers.LED2_L],
			Motor.MIDDLE_LEFT.value : [_Registers.LED3, _Registers.LED3_L],
			Motor.MIDDLE.value : [_Registers.LED4, _Registers.LED4_L],
			Motor.MIDDLE_RIGHT.value : [_Registers.LED5, _Registers.LED5_L],
			Motor.LOWER_LEFT.value : [_Registers.LED6, _Registers.LED6_L],
			Motor.LOWER_MIDDLE.value : [_Registers.LED7, _Registers.LED7_L],
			Motor.LOWER_RIGHT.value : [_Registers.LED8, _Registers.LED8_L]
		}

	def setActive(self) -> None:
		# Go through each register and disable OFF mode
		# Also disables all-call address
		for reg in _Registers :
			self._bus.write_byte_data(self._address, reg.value, 0x00)

	def setLowPower(self) -> None:
		# Set all OFF to 0 and re-enable sleep mode
		self.setAllDutyCycle(0)
		self._bus.write_byte_data(self._address, _Registers.MODE1.value, 0x10)

	def close(self) -> None:
		if self._bus is not None :
			self.setLowPower()
			self._bus.close()
			self._bus = None

	def __init__(self, bus_no: int = 1) -> None:
		self._bus: SMBus = SMBus(bus_no)
		self._address: int = 0x40
		self.setActive()

	def __enter__(self) -> None:
		return self

	def __exit__(self, err_type, err, traceback) -> None:
		self.close()

	def __del__(self) -> None:
		self.close()

	def setDutyCycle(self, location, value: int) -> None:
		if isinstance(location, Motor) :
			location = Motor.value
		if value >= 0 and value <= 4095 :
			self._bus.write_byte_data(self._address, PWM.LocationRegisterMap[location][0].value, \
				(value & 0xf00)>>8)	# Write upper 4 bits to OFF_H
			self._bus.write_byte_data(self._address, PWM.LocationRegisterMap[location][1].value, \
				value & 0x0ff)	# Write lower 8 bits to OFF_L

	def setAllDutyCycle(self, value: int) -> None:
		for motor in PWM.LocationRegisterMap.keys() :
			self.setDutyCycle(motor, value)
