# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		depth_perception_routine.py
# Description:		Process depth map into output

from system.models.routine import Routine
from system.mode import State
from system.API.Output import Output
from system.API.modules.PWM import PWM, Motor	# Used for Motor Enum

from numpy import ndarray

class DepthPerceptionRoutine(Routine) :

	# Initialization of vars
	def __init__(self, output_: Output = None, state: State = None) -> None:
		self.output_: Output = output_

	# 1:1 map between sections of image to output
	# Currently set to a linear continuous map
	def Execute(self, depth_map: ndarray) -> None:
		depth_map = (depth_map * 2048).astype("int")
		self.output_.setDutyCycle(Motor.UPPER_LEFT, depth_map[0,0])
		self.output_.setDutyCycle(Motor.UPPER_MIDDLE, depth_map[0,1])
		self.output_.setDutyCycle(Motor.UPPER_RIGHT, depth_map[0,2])
		self.output_.setDutyCycle(Motor.MIDDLE_LEFT, depth_map[1,0])
		self.output_.setDutyCycle(Motor.MIDDLE, depth_map[1,1])
		self.output_.setDutyCycle(Motor.MIDDLE_RIGHT, depth_map[1,2])
		self.output_.setDutyCycle(Motor.LOWER_LEFT, depth_map[2,0])
		self.output_.setDutyCycle(Motor.LOWER_MIDDLE, depth_map[2,1])
		self.output_.setDutyCycle(Motor.LOWER_RIGHT, depth_map[2,2])
