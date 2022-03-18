# Primary Author:	Christa Lawrence (cal47day@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		curb_detection_routine.py
# Description:		Process depth map into output

from system.models.routine import Routine
from system.mode import State
from system.API.Output import Output
from system.API.modules.PWM import PWM, Motor	# Used for Motor Enum

from numpy import ndarray, float32, uint8

class CurbDetectionRoutine(Routine) :

	# Initialization of vars
	def __init__(self, output_: Output, state: State) -> None:
		self.output_: Output = output_

	# 1:1 map between sections of image to output
	# Currently set to a linear continuous map
	def Execute(self, depth_map: ndarray) -> None:
		dmin = depth_map.min()
		dmax = depth_map.max()
		depth_map = (4095 * (depth_map - dmin) / (dmax - dmin)).astype("uint8")
		self.output_.setDutyCycle(Motor.LOWER_LEFT, depth_map[2,0])
		self.output_.setDutyCycle(Motor.LOWER_MIDDLE, depth_map[2,1])
		self.output_.setDutyCycle(Motor.LOWER_RIGHT, depth_map[2,2])