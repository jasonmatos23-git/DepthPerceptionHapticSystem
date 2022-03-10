# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		depth_perception_routine.py
# Description:		Process depth map into output

from system.models.routine import Routine
from system.mode import State
from system.API.Output import Output
from system.API.PWM import PWM	# Used for MotorLocation Enum

from numpy import ndarray, float32, uint8

class DepthPerceptionRoutine(Routine) :

	# Initialization of vars
	def __init__(self, output_: Output, state: State) -> None:
		self.output_: Output = output_

	# 1:1 map between sections of image to output
	# Currently set to a linear continuous map
	def Execute(self, depth_map: ndarray) -> None:
		dmin = depth_map.min()
		dmax = depth_map.max()
		depth_map = (4095 * (depth_map - dmin) / (dmax - dmin)).astype("uint8")
		Output.setDutyCycle(PWM.MotorLocation.UPPER_LEFT, depth_map[0,0])
		Output.setDutyCycle(PWM.MotorLocation.UPPER_MIDDLE, depth_map[0,1])
		Output.setDutyCycle(PWM.MotorLocation.UPPER_RIGHT, depth_map[0,2])
		Output.setDutyCycle(PWM.MotorLocation.MIDDLE_LEFT, depth_map[1,0])
		Output.setDutyCycle(PWM.MotorLocation.MIDDLE, depth_map[1,1])
		Output.setDutyCycle(PWM.MotorLocation.MIDDLE_RIGHT, depth_map[1,2])
		Output.setDutyCycle(PWM.MotorLocation.LOWER_LEFT, depth_map[2,0])
		Output.setDutyCycle(PWM.MotorLocation.LOWER_MIDDLE, depth_map[2,1])
		Output.setDutyCycle(PWM.MotorLocation.LOWER_RIGHT, depth_map[2,2])
