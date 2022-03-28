# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		outdoormode.py
# Description:		Wrapper for playing outdoor mode enable/disable sequence.

from system.models.service import Service
from system.models.routine import Routine
from system.API.Input import Input
from system.routine_container import RoutineContainer

class OutdoorMode(Service) :

	def __init__(self, input_: Input, routineContainer: RoutineContainer) -> None:
		self.routine: Routine = routineContainer.GetRoutine("OutdoorMode")

	def Execute(self, enabled: bool) -> None:
		self.routine.Execute(enabled)
