# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		mode.py
# Description:		Define mode superclass/template.
# Note:				Do not clear or set event flag. Only poll with is_set() or wait().
#					Clearing will be done by the scheduler. Setting by button interrupt.

from threading import Event
from system.service_container import ServiceContainer
from system.models.service import Service

class Mode :

	# Modify init with needed input parameters
	def __init__(self, modeChangedEvent: Event, serviceContainer: ServiceContainer = None) :
		self._modeChangedEvent: Event = modeChangedEvent
		# Request services from ServiceContainer
		# Example: self.depthService: Service = serviceContainer.GetService("DepthPerceptionService")

	def enter(self) -> None:
		pass

	def exit(self) -> None:
		pass

	def Execute(self) -> None:
		while not self._modeChangedEvent.is_set() :
			# Mode execution logic (i.e. running services)
			raise NotImplementedError
		# IMPORTANT NOTE: If only enter() and exit() needed (e.g. for LPM), replace while-loop
		# with the following to wait for mode change:
		# self._modeChangedEvent.wait()
