# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		linear_distance_routine.py
# Description:		Linear response to LiDAR distance

from system.models.routine import Routine
from system.mode import State
from system.API.Output import Output

from numpy import clip

class LinearDistanceRoutine(Routine) :

	# Values below in feet
	minDist: float = 6.0	# Minimum haptic feedback
	maxDist: float = 1.0	# Maximum haptic feedback

	def __init__(self, output_: Output = None, state: State = None) -> None:
		self.output_: Output = output_

	def Execute(self, distance: float) -> None:
		normalized: int = \
			int(4095.0 * ((self.minDist - clip(distance, \
			self.maxDist, self.minDist))/(self.minDist - self.maxDist)))
		self.output_.setAllDutyCycle(normalized)
