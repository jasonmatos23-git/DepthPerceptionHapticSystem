# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		Output.py
# Description:		Connects software components to output hardware.

# import RPi.GPIO as GPIO

from numpy import zeros, ndarray

class Output :

	def __init__(self) :
		# GPIO.setmode(GPIO.BCM)
		# GPIO.setwarnings(False)
		# GPIO.setup(18, GPIO.OUT)
		# GPIO.setup(12, GPIO.OUT)
		# self._frequency = 500
		# self._nonant = [GPIO.PWM(12, self._frequency), \
		# GPIO.PWM(18, self._frequency)]	# Connect GPIOx to section of video input
		# self._nonant[0].start(0)
		# self._nonant[1].start(0)
		self._nonant: ndarray = zeros(4*4)

	def setDutyCycle(self, index, dc) :
		# self._nonant[index].ChangeDutyCycle(dc)
		self._nonant[index] = dc

	def printDutyCycles(self) :
		print(self._nonant.reshape((4, 4)))
