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

	def reset_mode_button(channel) :
		#call function for reset system
		pass

	def pathway_finder_button(channel) :
		#call function for pathway finder
		pass

	def __init__(self, routineContainer: RoutineContainer) :
		self._conf: Configuration = Configuration()
		#reset mode
		GPIO.add_event_detect(self._conf.BUTTON_PIN_55, GPIO.RISING,
					callback=reset_mode_button,
					bouncetime=50)
		#Pathway Finder
		GPIO.add_event_detect(self._conf.BUTTON_PIN_51, GPIO.RISING,
					callback=pathway_finder_button,
					bouncetime=50)
