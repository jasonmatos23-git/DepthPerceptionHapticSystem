# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		distanceservice.py
# Description:		Check lidar for emergencies

from system.models.service import Service
from system.models.routine import Routine
from system.API.Input import Input
from system.routine_container import RoutineContainer

class DistanceService(Service) :

	# Thresholds below in feet.
	emergencyThreshold: float = 1.5

	def __init__(self, input_: Input = None, routineContainer: RoutineContainer = None) -> None:
		self.input_: Input = input_
		self.emergencyRoutine: Routine = None
		if routineContainer is None :
			return
		self.emergencyRoutine: Routine = routineContainer.GetRoutine("EmergencyResponse")
		self.linDistRoutine: Routine = routineContainer.GetRoutine("LinearDistanceRoutine")

	def Execute(self) -> None:
		distance: float = self.input_.GetForwardLidar()
		if distance <= 3 :	# Ignore abnormal distances
			return
		distance = distance * 0.03281	# Conversion from cm to feet
		# Lock execution if threshold distance reached
		while distance < self.emergencyThreshold :
			self.emergencyRoutine.Execute()
			distance = self.input_.GetForwardLidar() * 0.03281
		self.linDistRoutine.Execute(distance)
