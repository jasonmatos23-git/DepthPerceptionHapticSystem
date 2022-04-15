# Primary Author:	Chad Pauley (chadpauley65@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		hardware_interrupt.py
# Description:		The purpose of this code is to enable 3 out of the
#					5 pins to work through the use of GPIO pins.
#					All buttons will be connected from the named
#					GPIO pin to a button, then to GND

#Notes
#1 power button // input pin 99 // GLOBAL_EN // low
#2 Reset mode //pin 55 // low
#3 Pathway finder //pin 51 // low
#4 Lower level of vibration // leaving for later due to lack of time/testing
#5 Increase level of vibration // leaving for later due to lack of time/testing

#---------------

from system.routine_container import RoutineContainer
from system.models.routine import Routine
from system.configure import Configuration
import RPi.GPIO as GPIO

#power button does not need programming due to default manufacturer settings
#N/A Code

#event_detect is the detection method for inturrupts
#callback used to call function and loop the code
#bounce time set to 50 but can be changed

class HardwareInterrupt :

	# Set an individual callback event
	def setCallback(self, pin: int, callback) -> None:
		GPIO.add_event_detect(pin, GPIO.RISING, \
			callback = callback, bouncetime = self._bouncetime)

	# Remove an event
	def resetCallback(self, pin: int) -> None:
		GPIO.remove_event_detect(pin)

	# Connect functions to callbacks
	def setAllCallback(self, routine: Routine) -> None:
		self.setCallback(self.conf.BUTTON_PIN_6, routine.Button1Down)
		self.setCallback(self.conf.BUTTON_PIN_14, routine.Button2Down)
		self.setCallback(self.conf.BUTTON_PIN_15, routine.Button3Down)
		self.setCallback(self.conf.BUTTON_PIN_16, routine.Button4Down)
		self.setCallback(self.conf.BUTTON_PIN_7, routine.Button5Down)

	# Remove all callbacks
	def resetAllCallback(self) -> None:
		self.resetCallback(self.conf.BUTTON_PIN_6)
		self.resetCallback(self.conf.BUTTON_PIN_14)
		self.resetCallback(self.conf.BUTTON_PIN_15)
		self.resetCallback(self.conf.BUTTON_PIN_16)
		self.resetCallback(self.conf.BUTTON_PIN_7)

	def close(self) -> None:
		if self.conf is not None :
			self.resetAllCallback()
			self.conf = None

	def __init__(self, routineContainer: RoutineContainer = None, \
			configuration: Configuration = None, response: Routine = None) :
		# Set ALTs, define pins, set GPIO to BCM
		self.conf: Configuration = configuration
		self._bouncetime: int = 400
		# Get response routine (should have ButtonNDown implemented)
		if routineContainer is not None :
			response = routineContainer.GetRoutine("ButtonResponse")
		if response is not None :
			self.setAllCallback(response)

	def __enter__(self) -> None:
		return self

	def __del__(self) -> None:
		self.close()

	def __exit__(self, err_type, err, traceback) -> None:
		self.close()
