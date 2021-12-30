# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		templateservice.py
# Description:		Template for services

from system.models.service import Service
from system.models.routine import Routine
from system.API.Input import Input
from system.routine_container import RoutineContainer

class TemplateService(Service) :

	# Save reference to routine(s) that the service may use
	# and whatever other initialization needed
	def __init__(self, input_: Input, routineContainer: RoutineContainer) -> None:
		self.input_: Input = input_
		self.routine: Routine = routineContainer.GetRoutine("TemplateRoutine")

	# Service logic (e.g. CNN for depth perception)
	def Execute(self) -> None:
		self.routine.Execute()	# Execute method may take parameters
