# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		linear_distance_routine.py
# Description:		Linear response to LiDAR distance

from system.models.routine import Routine
from system.mode import State
from system.API.Output import Output

from time import sleep

class EmergencyResponse(Routine) :

	def __init__(self, output_: Output = None, state: State = None) -> None:
		self.output_: Output = output_

	def Execute(self) -> None:
		self.output_.setAllDutyCycle(0)
		sleep(0.1)
		self.output_.setAllDutyCycle(4095)
		sleep(0.1)

