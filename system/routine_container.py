# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		routine_container.py
# Description:		Manages routine instantiation.

from system.models.executable import Executable
from system.models.container import Container
from system.mode import State
from system.API.Output import Output
from typing import Dict

class RoutineContainer(Container) :

	classMap: Dict[str, type] = {}	# TODO: Better way to list routines

	def __init__(self, state: State) :
		self.instanceMap: Dict[str, Executable] = {}
		self.output_: Output = Output()
		self.state: State = state

	def _newExecutable(self, clss: type) -> Executable:
		return clss(self.output_, self.state)

	def GetRoutine(self, name: str) :
		return self._getExecutable(name)
