from smbus2 import SMBus
from enum import Enum, auto

class PWM :

	# Motor locations
	class MotorLocation(Enum) :
		UPPER_LEFT = auto()
		UPPER_MIDDLE = auto()
		UPPER_RIGHT = auto()
		MIDDLE_LEFT = auto()
		MIDDLE = auto()
		MIDDLE_RIGHT = auto()
		LOWER_LEFT = auto()
		LOWER_MIDDLE = auto()
		LOWER_RIGHT = auto()

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

	# Index 0 maps to OFF_H, index 1 maps to OFF_L
	LocationRegisterMap: dict = \
		{
			MotorLocation.UPPER_LEFT : [_Registers.LED0, _Registers.LED0_L],
			MotorLocation.UPPER_MIDDLE : [_Registers.LED1, _Registers.LED1_L],
			MotorLocation.UPPER_RIGHT : [_Registers.LED2, _Registers.LED2_L],
			MotorLocation.MIDDLE_LEFT : [_Registers.LED3, _Registers.LED3_L],
			MotorLocation.MIDDLE : [_Registers.LED4, _Registers.LED4_L],
			MotorLocation.MIDDLE_RIGHT : [_Registers.LED5, _Registers.LED5_L],
			MotorLocation.LOWER_LEFT : [_Registers.LED6, _Registers.LED6_L],
			MotorLocation.LOWER_MIDDLE : [_Registers.LED7, _Registers.LED7_L],
			MotorLocation.LOWER_RIGHT : [_Registers.LED8, _Registers.LED8_L]
		}

	def _initializePWM(self) :
		# Go through each register and disable OFF mode
		for reg in PWM._Registers :
			self._bus.write_byte_data(self._address, reg.value, 0x00)

	def __init__(self) :
		self._bus = SMBus(1)
		self._address = 0x40
		self._bus.write_byte_data(self._address, 0x00, 0x00) # Enable normal mode, disable all-call
		self._initializePWM()

	def __del__(self) :
		self._bus.write_byte_data(self._address, 0x00, 0x10) # Re-enable sleep mode
		self._bus.close()

	def setDutyCycle(self, location: MotorLocation, value: int) :
		if value >= 0 and value <= 4095 :
			self._bus.write_byte_data(self._address, PWM.LocationRegisterMap[location][0].value, \
				(value & 0xf00)>>8)	# Write upper 4 bits to OFF_H
			self._bus.write_byte_data(self._address, PWM.LocationRegisterMap[location][1].value, \
				value & 0x0ff)	# Write lower 8 bits to OFF_L
