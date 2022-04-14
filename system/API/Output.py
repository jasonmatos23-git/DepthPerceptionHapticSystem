# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		Output.py
# Description:		Connects software components to output hardware.

from numpy import zeros, ndarray
from enum import Enum, auto
from smbus2 import SMBus
from system.API.modules.PWM import PWM, Motor

class Output :

	def __init__(self, bus: SMBus) :
		self._pwm: PWM = PWM(bus)

	def __del__(self) :
		del(self._pwm)

	def setDutyCycle(self, location: Motor, value: int) -> None:
		# Can use this function to discretize
		self._pwm.setDutyCycle(location, value)

	def setAllDutyCycle(self,value: int) -> None:
		self._pwm.setAllDutyCycle(value)

	def setLowPower(self) -> None:
		self._pwm.setLowPower()

	def setNormalPower(self) -> None:
		self._pwm.setNormalPower()
