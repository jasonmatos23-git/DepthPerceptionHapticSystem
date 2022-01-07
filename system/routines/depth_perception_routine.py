# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		depth_perception_routine.py
# Description:		Process depth map into output

from system.models.routine import Routine
from system.mode import State
from system.API.Output import Output

from numpy import ndarray

class DepthPerceptionRoutine(Routine) :

	# Initialization of vars
	def __init__(self, output_: Output, state: State) -> None:
		self.output_: Output = output_

	# 1:1 map between sections of image to output
	# Currently set to a linear continuous map
	def Execute(self, depth_map: ndarray) -> None:
		depth_map: ndarray = depth_map / 2.55
		i: int
		j: int
		for i in range(0, 2) :
			for j in range(0, 3) :
				self.output_.setDutyCycle(3*i + j, depth_map[(i*8):(i*8 + 8), (j*8):(j*8 + 8)].mean())
		self.output_.printDutyCycles()
