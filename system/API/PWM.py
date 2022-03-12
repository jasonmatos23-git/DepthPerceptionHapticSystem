# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		PWM.py
# Description:		Provides functions for interacting with PCA9685.

from smbus2 import SMBus
from enum import Enum, auto

# Motor locations
class Motor(Enum) :
	UPPER_LEFT = auto()
	UPPER_MIDDLE = auto()
	UPPER_RIGHT = auto()
	MIDDLE_LEFT = auto()
	MIDDLE = auto()
	MIDDLE_RIGHT = auto()
	LOWER_LEFT = auto()
	LOWER_MIDDLE = auto()
	LOWER_RIGHT = auto()

class PWM :

	# All for OFF. ON default of 0 is acceptable
	class _Registers(Enum) :
		MODE1 = 0x00
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

	# Index 0 maps to OFF_H, index 1 maps to OFF_L
	LocationRegisterMap : dict = \
		{
			Motor.UPPER_LEFT : [_Registers.LED0, _Registers.LED0_L],
			Motor.UPPER_MIDDLE : [_Registers.LED1, _Registers.LED1_L],
			Motor.UPPER_RIGHT : [_Registers.LED2, _Registers.LED2_L],
			Motor.MIDDLE_LEFT : [_Registers.LED3, _Registers.LED3_L],
			Motor.MIDDLE : [_Registers.LED4, _Registers.LED4_L],
			Motor.MIDDLE_RIGHT : [_Registers.LED5, _Registers.LED5_L],
			Motor.LOWER_LEFT : [_Registers.LED6, _Registers.LED6_L],
			Motor.LOWER_MIDDLE : [_Registers.LED7, _Registers.LED7_L],
			Motor.LOWER_RIGHT : [_Registers.LED8, _Registers.LED8_L]
		}

	def _initializePWM(self) :
		# Go through each register and disable OFF mode
		for reg in PWM._Registers :
			self._bus.write_byte_data(self._address, reg.value, 0x00)

	def __init__(self) :
		self._bus = SMBus(1)
		self._address = 0x40
		self._bus.write_byte_data(self._address, _Registers.MODE1, 0x00) # Enable normal mode, disable all-call
		self._initializePWM()

	def __del__(self) :
		self._bus.write_byte_data(self._address, _Registers.MODE1, 0x10) # Re-enable sleep mode
		self._bus.close()

	def setDutyCycle(self, location: Motor, value: int) :
		if value >= 0 and value <= 4095 :
			self._bus.write_byte_data(self._address, PWM.LocationRegisterMap[location][0].value, \
				(value & 0xf00)>>8)	# Write upper 4 bits to OFF_H
			self._bus.write_byte_data(self._address, PWM.LocationRegisterMap[location][1].value, \
				value & 0x0ff)	# Write lower 8 bits to OFF_L
