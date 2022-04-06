# Primary Author:	Christa Lawrence (cal47day@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		curb_detection_routine.py
# Description:		Process depth map into output

from system.models.routine import Routine
from system.mode import State
from system.API.Output import Output
from system.API.modules.PWM import PWM, Motor	# Used for Motor Enum
from time import sleep



class CurbDetectionRoutine(Routine) :

	# Initialization of vars
	def __init__(self, output_: Output, state: State) -> None:
		self.output_: Output = output_

	#Step Up
	def UpExecute(self)-> None:
		self.output_.setDutyCycle(Motor.LOWER_LEFT, 2048)
		sleep(0.1)
		self.output_.setDutyCycle(Motor.LOWER_MIDDLE, 2048)
		sleep(0.1)
		self.output_.setDutyCycle(Motor.LOWER_RIGHT, 2048)

	#Step down
	def DownExecute(self)-> None:
		self.output_.setDutyCycle(Motor.LOWER_RIGHT, 2048)
		sleep(0.1)
		self.output_.setDutyCycle(Motor.LOWER_MIDDLE, 2048)
		sleep(0.1)
		self.output_.setDutyCycle(Motor.LOWER_LEFT, 2048)