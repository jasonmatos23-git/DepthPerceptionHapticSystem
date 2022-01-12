# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		Output.py
# Description:		Connects software components to output hardware.

# import RPi.GPIO as GPIO

from numpy import zeros, ndarray
from enum import Enum, auto

class Output :

	# Replace 'auto' with GPIO numbers or internal I2C address
	# (decimal) for PWM driver
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

	def __init__(self) :
		self._nonant: ndarray = zeros(4*4)	# Holds values for duty cycle

	def setDutyCycle(self, index, dc) :
		self._nonant[index] = dc

	def printDutyCycles(self) :
		print(self._nonant.reshape((4, 4)))
