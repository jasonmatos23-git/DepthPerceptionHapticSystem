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
		UPPER_LEFT = 4
		UPPER_MIDDLE = 3
		UPPER_RIGHT = 2
		MIDDLE_LEFT = 18
		MIDDLE = 15
		MIDDLE_RIGHT = 14
		LOWER_LEFT = auto()
		LOWER_MIDDLE = auto()
		LOWER_RIGHT = auto()

	def __init__(self) :
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(Output.MotorLocation.UPPER_LEFT.value, GPIO.OUT)
		GPIO.setup(Output.MotorLocation.UPPER_MIDDLE.value, GPIO.OUT)
		GPIO.setup(Output.MotorLocation.UPPER_RIGHT.value, GPIO.OUT)
		GPIO.setup(Output.MotorLocation.MIDDLE_LEFT.value, GPIO.OUT)
		GPIO.setup(Output.MotorLocation.MIDDLE.value, GPIO.OUT)
		GPIO.setup(Output.MotorLocation.MIDDLE_RIGHT.value, GPIO.OUT)
		self._frequency = 500
		self._nonant = [ \
		GPIO.PWM(Output.MotorLocation.UPPER_LEFT.value, self._frequency), \
		GPIO.PWM(Output.MotorLocation.UPPER_MIDDLE.value, self._frequency), \
		GPIO.PWM(Output.MotorLocation.UPPER_RIGHT.value, self._frequency), \
		GPIO.PWM(Output.MotorLocation.MIDDLE_LEFT.value, self._frequency), \
		GPIO.PWM(Output.MotorLocation.MIDDLE.value, self._frequency), \
		GPIO.PWM(Output.MotorLocation.MIDDLE_RIGHT.value, self._frequency)]	# Connect GPIOx to section of video input
		for pwm in self._nonant :
			pwm.start(0)

	def setDutyCycle(self, index, dc) :
		if dc >= 50 :
			dc = 100
		else
			dc = 0
		self._nonant[index].ChangeDutyCycle(dc)
		# self._nonant[index] = dc

	def printDutyCycles(self) :
		pass
		# print(self._nonant.reshape((4, 4)))
