# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		service_container.py
# Description:		Manages service instantiation.

from system.routine_container import RoutineContainer
from system.models.executable import Executable
from system.models.container import Container
from system.services.servicelist import *
from system.API.Input import Input
from typing import Dict
from smbus2 import SMBus

# Manages instantiation specific to services
class ServiceContainer(Container) :

	classMap: Dict[str, type] = servicelist

	# System instance of RoutineContainer passed to connect
	# services to their routines when running _newExecutable
	def __init__(self, routineContainer: RoutineContainer = None, bus: SMBus = None) :
		self.instanceMap: Dict[str, Executable] = {}
		self.input_: Input = None
		self.routineContainer: RoutineContainer = routineContainer
		if bus is not None :
			self.input_: Input = Input(bus)

	def _newExecutable(self, clss: type) -> Executable:
		return clss(self.input_, self.routineContainer)

	def GetService(self, name: str) -> Executable:
		return self._getExecutable(name)
