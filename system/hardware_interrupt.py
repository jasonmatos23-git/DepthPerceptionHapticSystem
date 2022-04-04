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

	def button1down(self, channel) :
		pass

	def button2down(self, channel) :
		pass

	def button3down(self, channel) :
		pass

	def button4down(self, channel) :
		pass

	def button5down(self, channel) :
		pass

	def __init__(self, routineContainer: RoutineContainer) :
		# Set ALTs, define pins, set GPIO to BCM
		self._conf: Configuration = Configuration()
		self._bouncetime: int = 250
		# Connect functions to callbacks
		GPIO.add_event_detect(self._conf.BUTTON_PIN_6, GPIO.RISING, \
			callback = button1down, bouncetime = self._bouncetime)
		GPIO.add_event_detect(self._conf.BUTTON_PIN_14, GPIO.RISING, \
			callback = button2down, bouncetime = self._bouncetime)
		GPIO.add_event_detect(self._conf.BUTTON_PIN_15, GPIO.RISING, \
			callback = button3down, bouncetime = self._bouncetime)
		GPIO.add_event_detect(self._conf.BUTTON_PIN_16, GPIO.RISING, \
			callback = button4down, bouncetime = self._bouncetime)
		GPIO.add_event_detect(self._conf.BUTTON_PIN_17, GPIO.RISING, \
			callback = button5down, bouncetime = self._bouncetime)

	def __del__(self) :
		# Remove callbacks and configuration
		GPIO.remove_event_detect(self._conf.BUTTON_PIN_6)
		GPIO.remove_event_detect(self._conf.BUTTON_PIN_14)
		GPIO.remove_event_detect(self._conf.BUTTON_PIN_15)
		GPIO.remove_event_detect(self._conf.BUTTON_PIN_16)
		GPIO.remove_event_detect(self._conf.BUTTON_PIN_17)
		del(self._conf)
