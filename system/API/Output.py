# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		Output.py
# Description:		Connects software components to output hardware.

from numpy import zeros, ndarray
from enum import Enum, auto
from system.API.PWM import PWM

class Output :

	def __init__(self) :
		self._pwm = PWM()

	def setDutyCycle(self, location, value) :
		# Can use this function to discretize
		self._pwm.setDutyCycle(location, value)
