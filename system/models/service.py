# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		service.py
# Description:		Template and superclass for services

from system.models.executable import Executable
from system.API.Input import Input
from system.routine_container import RoutineContainer

class Service(Executable) :

	def __init__(self, input_: Input, routineContainer: RoutineContainer) -> None:
		self.input_: Input = input_
		raise NotImplementedError
