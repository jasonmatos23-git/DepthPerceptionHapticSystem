# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		container.py
# Description:		Defines wrapper which contain executables.

from system.models.executable import Executable
from typing import Dict

# Abstract method to manage life of Executable
class Container :

	# Override with list of services/routines
	classMap: Dict[str, type] = {}

	# Override for each subclass
	def __init__(self) :
		self.instanceMap: Dict[str, Executable] = {}
		raise NotImplementedError

	# Override to pass correct parameters to Service/Routine constructor
	def _newExecutable(self, clss: type) -> Executable:
		raise NotImplementedError

	# Creates instance of Executable
	def _initExecutable(self, name: str) -> Executable:
		if name in self.classMap :
			instance: Executable = self._newExecutable(self.classMap[name])
			self.instanceMap[name] = instance
			return instance
		else :
			raise KeyError

	# Ensures exactly one instance of an Executable exists
	def _getExecutable(self, name: str) -> Executable:
		if name in self.instanceMap :
			return self.instanceMap[name]
		else :
			return self._initExecutable(name)
