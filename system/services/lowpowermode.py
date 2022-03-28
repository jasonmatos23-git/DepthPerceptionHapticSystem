# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		lowpowermode.py
# Description:		Wrapper for playing low-power mode enable/disable sequence.

from system.models.service import Service
from system.models.routine import Routine
from system.API.Input import Input
from system.routine_container import RoutineContainer

class LowPowerMode(Service) :

	def __init__(self, input_: Input, routineContainer: RoutineContainer) -> None:
		self.routine: Routine = routineContainer.GetRoutine("LowPowerMode")

	def Execute(self, enabled: bool) -> None:
		# SPECIAL CASE MODE.
		# This script should alter inputs to
		# their low power modes.
		self.routine.Execute(enabled)
