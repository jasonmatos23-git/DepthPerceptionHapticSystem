# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		service_container.py
# Description:		Manages service instantiation.

from system.routine_container import RoutineContainer
from system.models.executable import Executable
from system.models.container import Container
from system.API.Input import Input
from typing import Dict

# Manages instantiation specific to services
class ServiceContainer(Container) :

	classMap: Dict[str, type] = {}	# TODO: Better way to list services

	# System instance of RoutineContainer passed to connect
	# services to their routines when running _newExecutable
	def __init__(self, routineContainer: RoutineContainer) :
		self.instanceMap: Dict[str, Executable] = {}
		self.input_: Input = Input()
		self.routineContainer: RoutineContainer = routineContainer

	def _newExecutable(self, clss: type) -> Executable:
		return clss(self.input_, self.routineContainer)

	def GetService(self, name: str) :
		return self._getExecutable(name)
